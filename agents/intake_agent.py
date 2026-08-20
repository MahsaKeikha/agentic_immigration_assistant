from agents.base import BaseAgent, AgentResult

SYSTEM = """You are a practice workflow assistant, not a lawyer. Never give legal advice, predict case outcomes, or invent law. Organize facts from the file only. Flag gaps for human counsel.
Intake agent: summarize facts present in the matter file and list missing information as questions.
"""


class IntakeAgent(BaseAgent):
    name = "intake"

    def run(self, matter_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        raw = self.memory.read_matter(matter_id)
        if not raw:
            result.ok = False
            result.output = f"Matter {matter_id} not found"
            return result
        resp = self._complete(SYSTEM, f"Matter {matter_id}:\n\n{raw}\n\nIntake summary.")
        path = self.memory.write_note(f"{matter_id}_intake", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
