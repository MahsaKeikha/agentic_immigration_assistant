from agents.base import BaseAgent, AgentResult

SYSTEM = """You are a practice workflow assistant, not a lawyer. Never give legal advice, predict case outcomes, or invent law. Organize facts from the file only. Flag gaps for human counsel.
Issue map agent: list discussion categories for counsel. Do not choose a legal strategy.
"""


class IssueMapAgent(BaseAgent):
    name = "issue_map"

    def run(self, matter_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"Matter {matter_id}\n\n## Intake\n{self.memory.read_note(f'{matter_id}_intake')}\n\n"
            f"## File\n{self.memory.read_matter(matter_id)}\n\nIssue categories for counsel discussion."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{matter_id}_issues", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
