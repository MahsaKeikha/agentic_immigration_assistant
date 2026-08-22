# F17 | Agentic Immigration Practice Assistant

A reference implementation of a governed multi-agent system for immigration-matter organization and attorney-support workflows. The repository demonstrates how specialized agents can collaborate across matter intake, issue spotting, document checklists, timeline construction, research logging, client communications, process-risk review, and a final professional gate before anything is sent or filed.

This repository is part of the Agentic AI Library and is intended for education, workflow engineering, architecture study, legal-operations prototyping, and adaptation into attorney-supervised systems.

## Scope and critical limits

This repository supports organization and drafting. It is not a lawyer and does not provide binding legal advice. Immigration law varies by jurisdiction and changes over time, so current official sources and qualified counsel remain authoritative.

The system must not be used to prepare false statements, coach dishonesty, evade legal requirements, or file material without appropriate professional review.

## What this system does

The workflow begins with a matter file and transforms it into a structured review package. A typical run can normalize client-provided facts, identify categories of issues to discuss with counsel, create a document request checklist, organize dates, maintain a research-log placeholder, draft an administrative client message, identify process risks, and consolidate the matter for professional review.

## Multi-agent architecture

| Agent | Responsibility | Typical output |
|---|---|---|
| Intake Agent | Normalize facts already provided in the matter file | intake note |
| Issue Agent | Identify issue categories requiring legal review | issue map |
| Documents Agent | Build a document-request and completeness checklist | document checklist |
| Timeline Agent | Organize key dates and recorded deadlines | timeline note |
| Research Agent | Maintain a structured placeholder for counsel research | research log |
| Comms Agent | Draft administrative client communication | client-message draft |
| Risk Agent | Surface process risks such as missing documents or deadlines | risk note |
| Gatekeeper Agent | Consolidate the matter package and enforce professional review | matter pack |

## Workflow

A typical matter progresses through intake, issue mapping, document review, timeline organization, research logging, client-communication drafting, process-risk review, and gatekeeping. The workflow stops before client send or government filing unless a qualified human explicitly approves the package.

## Repository structure

```text
agentic_immigration_assistant/
  README.md
  config.py
  memory.py
  llm_client.py
  orchestrator.py
  run_matter.py
  agents/
    intake_agent.py
    issue_agent.py
    documents_agent.py
    timeline_agent.py
    research_agent.py
    comms_agent.py
    risk_agent.py
    gatekeeper_agent.py
  tools/
  checklists/attorney_gate.md
  examples/sample_matter/
    matters/
    notes/
    checklists_docs/
    drafts/
    exports/
```

## Quick start

```bash
python3 run_matter.py --matter MAT-3001 --offline
```

Live execution, where configured:

```bash
export ANTHROPIC_API_KEY=your_key_here
python3 run_matter.py --matter MAT-3001 --live
```

Offline mode is useful for studying orchestration and artifact flow without an external model API.

## Inputs and outputs

Typical inputs include the matter summary, client-provided facts, immigration history, status documents, known dates, correspondence, document inventory, jurisdiction, and questions for counsel.

The sample workflow produces artifacts such as:

```text
notes/MAT-3001_intake.md
notes/MAT-3001_issues.md
checklists_docs/MAT-3001_documents.md
notes/MAT-3001_timeline.md
notes/MAT-3001_research_log.md
notes/MAT-3001_risks.md
drafts/MAT-3001_client_message.md
exports/MAT-3001_matter_pack.md
```

These are organizational artifacts. The system does not independently file forms, sign representations, make eligibility determinations, or communicate as legal counsel.

## Attorney gate

The repository includes `checklists/attorney_gate.md` as the boundary between matter preparation and consequential legal communication. A qualified professional should verify factual accuracy, current law, jurisdiction, deadlines, document sufficiency, client instructions, and the wording of any external communication or filing.

Passing `--ship` records a human review decision within the reference workflow. It is not a substitute for attorney responsibility or filing authorization.

## Governance boundaries

A production adaptation should not autonomously give legal advice, determine immigration eligibility, select a legal strategy, make representations to government authorities, sign or submit forms, alter client records, or send legal communications without professional authorization.

## How to use this repository as a reference

Reusable patterns include matter-centered memory, separate issue and document agents, explicit timeline tracking, legal-research placeholders rather than fabricated authority, process-risk review, and an attorney gate before external action.

## Extension points

Common extensions include secure case-management connectors, document OCR and classification, official-source retrieval, citation provenance, jurisdiction-aware deadline calculators, form-data validation, attorney task queues, client portals, audit trails, document versioning, and filing connectors that remain behind professional authorization.

## Evaluation strategy

Useful evaluation dimensions include factual extraction accuracy, issue-category recall, document-checklist completeness, date accuracy, source provenance, process-risk detection, client-message quality, hallucinated-law rate, and correct enforcement of the attorney gate.

## Appropriate use

Good uses include legal-operations education, matter-organization prototyping, attorney-support workflow research, and governed multi-agent system design.

## Design principle

Immigration practice combines factual organization, issue spotting, documents, timelines, research, communication, and legal judgment. The first six can be structured as reviewable agent workflows, while binding legal judgment and filing authority remain explicitly human.
