from agents.base import BaseAgent, AgentResult

SYSTEM = """You are a practice workflow assistant, not a lawyer. Never give legal advice, predict case outcomes, or invent law. Organize facts from the file only. Flag gaps for human counsel.
Client communications agent: draft administrative messages only. Explicitly state this is not legal advice.
"""


class ClientCommsAgent(BaseAgent):
    name = "client_comms"

    def run(self, matter_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        from config import DOCS_DIR
        docs = ""
        p = DOCS_DIR / f"{matter_id}_documents.md"
        if p.exists():
            docs = p.read_text(encoding="utf-8")
        user = (
            f"Matter {matter_id}\n\n## Documents checklist\n{docs}\n\n"
            f"Draft administrative client message (not legal advice)."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_draft(f"{matter_id}_client_message", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
