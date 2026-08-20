from __future__ import annotations
from pathlib import Path
from config import MATTERS_DIR, NOTES_DIR, DRAFTS_DIR, EXPORTS_DIR, DOCS_DIR


class MatterMemory:
    def read_matter(self, matter_id: str) -> str:
        path = MATTERS_DIR / f"{matter_id}.md"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def write_note(self, name: str, content: str) -> Path:
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        path = NOTES_DIR / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path

    def read_note(self, name: str) -> str:
        path = NOTES_DIR / (name if name.endswith(".md") else f"{name}.md")
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def write_docs_list(self, name: str, content: str) -> Path:
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        path = DOCS_DIR / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path

    def write_draft(self, name: str, content: str) -> Path:
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
        path = DRAFTS_DIR / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path

    def write_export(self, name: str, content: str) -> Path:
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        path = EXPORTS_DIR / name
        path.write_text(content, encoding="utf-8")
        return path
