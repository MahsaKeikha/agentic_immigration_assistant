from agents.base import BaseAgent, AgentResult

SYSTEM = """You are a practice workflow assistant, not a lawyer. Never give legal advice, predict case outcomes, or invent law. Organize facts from the file only. Flag gaps for human counsel.
Research log agent: create empty structured slots for counsel research. Do not invent statutes or cases.
"""


class ResearchLogAgent(BaseAgent):
    name = "research_log"

    def run(self, matter_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"Matter {matter_id}\n\n## Issues\n{self.memory.read_note(f'{matter_id}_issues')}\n\n"
            f"Research log template."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{matter_id}_research_log", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
