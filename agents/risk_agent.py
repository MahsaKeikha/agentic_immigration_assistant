from agents.base import BaseAgent, AgentResult

SYSTEM = """You are a practice workflow assistant, not a lawyer. Never give legal advice, predict case outcomes, or invent law. Organize facts from the file only. Flag gaps for human counsel.
Risk agent: process and completeness flags only. No outcome predictions.
"""


class RiskAgent(BaseAgent):
    name = "risk"

    def run(self, matter_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"Matter {matter_id}\n\n## Timeline\n{self.memory.read_note(f'{matter_id}_timeline')}\n\n"
            f"## Issues\n{self.memory.read_note(f'{matter_id}_issues')}\n\nProcess risk flags."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{matter_id}_risks", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
