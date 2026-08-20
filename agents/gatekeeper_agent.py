from agents.base import BaseAgent, AgentResult
from tools.checklist_tools import load_checklist, checklist_report

SYSTEM = """You are a practice workflow assistant, not a lawyer. Never give legal advice, predict case outcomes, or invent law. Organize facts from the file only. Flag gaps for human counsel.
Gatekeeper agent: summarize pack for attorney review. Never approve filing autonomously.
"""


class GatekeeperAgent(BaseAgent):
    name = "gatekeeper"

    def run(self, matter_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        from config import DRAFTS_DIR
        msg = ""
        p = DRAFTS_DIR / f"{matter_id}_client_message.md"
        if p.exists():
            msg = p.read_text(encoding="utf-8")
        user = (
            f"Matter {matter_id}\n\n## Intake\n{self.memory.read_note(f'{matter_id}_intake')}\n\n"
            f"## Risks\n{self.memory.read_note(f'{matter_id}_risks')}\n\n"
            f"## Client draft\n{msg}\n\nAttorney review summary."
        )
        resp = self._complete(SYSTEM, user)
        items = load_checklist("attorney_gate.md")
        text = resp.text + ("\n\n" + checklist_report(items) if items else "")
        path = self.memory.write_export(f"{matter_id}_matter_pack.md", text)
        result.output = text
        result.artifacts["path"] = str(path)
        result.add("pack ready. licensed human review required")
        return result
