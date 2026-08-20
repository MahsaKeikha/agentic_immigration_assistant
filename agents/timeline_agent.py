from agents.base import BaseAgent, AgentResult

SYSTEM = """You are a practice workflow assistant, not a lawyer. Never give legal advice, predict case outcomes, or invent law. Organize facts from the file only. Flag gaps for human counsel.
Timeline agent: extract dates only as written in the file. Mark uncertain items [CONFIRM].
"""


class TimelineAgent(BaseAgent):
    name = "timeline"

    def run(self, matter_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = f"Matter {matter_id}\n\n## File\n{self.memory.read_matter(matter_id)}\n\nTimeline notes."
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{matter_id}_timeline", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
