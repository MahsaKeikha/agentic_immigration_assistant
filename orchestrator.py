from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from config import AgentConfig
from memory import MatterMemory
from llm_client import LLMClient
from agents.intake_agent import IntakeAgent
from agents.issue_agent import IssueMapAgent
from agents.documents_agent import DocumentsAgent
from agents.timeline_agent import TimelineAgent
from agents.research_agent import ResearchLogAgent
from agents.comms_agent import ClientCommsAgent
from agents.risk_agent import RiskAgent
from agents.gatekeeper_agent import GatekeeperAgent


@dataclass
class MatterRunReport:
    matter_id: str
    steps: List[str] = field(default_factory=list)
    ok: bool = True

    def log(self, msg: str) -> None:
        self.steps.append(msg)
        print(f"[immigration-assist] {msg}")


class MatterOrchestrator:
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.config.ensure_dirs()
        self.memory = MatterMemory()
        self.llm = LLMClient(self.config)
        self.intake = IntakeAgent(self.config, self.memory, self.llm)
        self.issues = IssueMapAgent(self.config, self.memory, self.llm)
        self.documents = DocumentsAgent(self.config, self.memory, self.llm)
        self.timeline = TimelineAgent(self.config, self.memory, self.llm)
        self.research = ResearchLogAgent(self.config, self.memory, self.llm)
        self.comms = ClientCommsAgent(self.config, self.memory, self.llm)
        self.risk = RiskAgent(self.config, self.memory, self.llm)
        self.gatekeeper = GatekeeperAgent(self.config, self.memory, self.llm)

    def run(self, matter_id: str, *, ship: bool = False) -> MatterRunReport:
        report = MatterRunReport(matter_id=matter_id)
        pipeline = [
            ("intake", lambda: self.intake.run(matter_id)),
            ("issue_map", lambda: self.issues.run(matter_id)),
            ("documents", lambda: self.documents.run(matter_id)),
            ("timeline", lambda: self.timeline.run(matter_id)),
            ("research_log", lambda: self.research.run(matter_id)),
            ("client_comms", lambda: self.comms.run(matter_id)),
            ("risk", lambda: self.risk.run(matter_id)),
            ("gatekeeper", lambda: self.gatekeeper.run(matter_id)),
        ]
        for name, fn in pipeline:
            r = fn()
            report.log(f"{name}: {'ok' if r.ok else 'FAIL'}")
            if not r.ok:
                report.ok = False
                return report
        if ship:
            self.memory.write_export(
                f"{matter_id}_ATTORNEY_APPROVED.txt",
                (
                    f"Human attorney approved next administrative step for {matter_id}.\n"
                    f"Still not an autonomous filing system. Follow professional and ethical rules.\n"
                ),
            )
            report.log("ATTORNEY APPROVED flag written")
        else:
            report.log("HUMAN ATTORNEY GATE: review matter_pack.md then --ship only after counsel approval")
        return report
