from __future__ import annotations
import os
import re
from dataclasses import dataclass
from typing import Dict, Optional
from config import AgentConfig, DEFAULT_MODEL, MAX_TOKENS


@dataclass
class LLMResponse:
    text: str
    model: str
    offline: bool
    usage: Dict[str, int]


class LLMClient:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.offline = config.offline or not (config.api_key or os.getenv("ANTHROPIC_API_KEY"))
        self._client = None
        if not self.offline:
            try:
                import anthropic
                self._client = anthropic.Anthropic(
                    api_key=config.api_key or os.getenv("ANTHROPIC_API_KEY")
                )
            except Exception:
                self.offline = True

    def complete(self, system: str, user: str, **kwargs) -> LLMResponse:
        if self.offline:
            return self._offline(system, user)
        model = kwargs.get("model") or self.config.model or DEFAULT_MODEL
        msg = self._client.messages.create(
            model=model,
            max_tokens=kwargs.get("max_tokens") or self.config.max_tokens or MAX_TOKENS,
            temperature=self.config.temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(b.text for b in msg.content if hasattr(b, "text"))
        return LLMResponse(
            text=text, model=model, offline=False,
            usage={
                "input_tokens": getattr(msg.usage, "input_tokens", 0),
                "output_tokens": getattr(msg.usage, "output_tokens", 0),
            },
        )

    def _offline(self, system: str, user: str) -> LLMResponse:
        role = "general"
        s = system.lower()
        for key in ("intake", "issue", "document", "timeline", "research", "client", "risk", "gate"):
            if key in s:
                role = {
                    "issue": "issue_map",
                    "document": "documents",
                    "research": "research_log",
                    "client": "client_comms",
                    "gate": "gatekeeper",
                }.get(key, key)
                break
        m = re.search(r"(MAT-\d+)", user)
        mid = m.group(1) if m else "MAT-XXXX"
        templates = {
            "intake": (
                f"## Intake summary ({mid})\n"
                f"- Facts limited to those in the matter file\n"
                f"- Missing items should be listed as questions for counsel\n"
                f"- Not a legal conclusion\n"
            ),
            "issue_map": (
                f"## Issue categories to discuss with counsel ({mid})\n"
                f"- Status history completeness\n"
                f"- Document gaps\n"
                f"- Deadline tracking from file notes\n"
                f"Counsel decides strategy. This is a discussion list only.\n"
            ),
            "documents": (
                f"## Document request checklist ({mid})\n"
                f"- Identity documents as listed by counsel process\n"
                f"- Prior filings mentioned in the matter file\n"
                f"- Proof items the client said they can obtain\n"
                f"Confirm list with supervising attorney before sending.\n"
            ),
            "timeline": (
                f"## Timeline notes ({mid})\n"
                f"- Record only dates present in the matter file\n"
                f"- Flag unclear dates as [CONFIRM]\n"
            ),
            "research_log": (
                f"## Research log template ({mid})\n"
                f"- Question for counsel research\n"
                f"- Official source to check\n"
                f"- Date checked and by whom\n"
                f"Do not invent case law or regulation text offline.\n"
            ),
            "client_comms": (
                f"## Draft client message ({mid})\n\n"
                f"This is an administrative draft only. It is not legal advice. "
                f"Please send the documents your attorney requested and reply with any "
                f"date corrections. Your attorney will advise on legal options.\n"
            ),
            "risk": (
                f"## Process risk flags ({mid})\n"
                f"- Incomplete document set\n"
                f"- Unconfirmed deadlines in file\n"
                f"- Need attorney review before any filing language\n"
            ),
            "gatekeeper": (
                f"## Gatekeeper ({mid})\n"
                f"- Pack is for human attorney review\n"
                f"- Not approved for filing or legal advice delivery\n"
            ),
            "general": f"[offline immigration assistant] {user[:200]}\n",
        }
        text = templates.get(role, templates["general"])
        return LLMResponse(
            text=text, model="offline-standin", offline=True,
            usage={"input_tokens": 0, "output_tokens": len(text.split())},
        )
