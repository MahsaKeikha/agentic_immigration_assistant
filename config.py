from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

ROOT = Path(__file__).resolve().parent / "examples" / "sample_matter"
MATTERS_DIR = ROOT / "matters"
NOTES_DIR = ROOT / "notes"
DRAFTS_DIR = ROOT / "drafts"
EXPORTS_DIR = ROOT / "exports"
DOCS_DIR = ROOT / "checklists_docs"
CHECKLISTS_DIR = Path(__file__).resolve().parent / "checklists"

DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096
TEMPERATURE = 0.2


@dataclass
class AgentConfig:
    root: Path = field(default_factory=lambda: ROOT)
    model: str = DEFAULT_MODEL
    max_tokens: int = MAX_TOKENS
    temperature: float = TEMPERATURE
    offline: bool = True
    api_key: Optional[str] = None

    def ensure_dirs(self) -> None:
        for d in (MATTERS_DIR, NOTES_DIR, DRAFTS_DIR, EXPORTS_DIR, DOCS_DIR):
            d.mkdir(parents=True, exist_ok=True)
