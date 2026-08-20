from agents.base import BaseAgent, AgentResult

SYSTEM = """You are a practice workflow assistant, not a lawyer. Never give legal advice, predict case outcomes, or invent law. Organize facts from the file only. Flag gaps for human counsel.
Documents agent: propose a document request checklist based on the file. Counsel must approve before sending.
"""


class DocumentsAgent(BaseAgent):
    name = "documents"

    def run(self, matter_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"Matter {matter_id}\n\n## Issues\n{self.memory.read_note(f'{matter_id}_issues')}\n\n"
            f"## File\n{self.memory.read_matter(matter_id)}\n\nDocument checklist."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_docs_list(f"{matter_id}_documents", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
