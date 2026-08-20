# Agentic Immigration Practice Assistant

Multi agent **workflow helper** for immigration case organization: matter intake, issue spotting checklist, document request list, timeline notes, client message draft, research log placeholders, and a human gate before anything is sent or filed.

## Critical limits

- This is **not a lawyer** and does **not** give legal advice.
- It does **not** replace a licensed attorney in the relevant jurisdiction.
- It must **not** be used to prepare false statements, evade immigration law, or coach dishonesty.
- Outputs are organizational drafts. A qualified human professional must review every item.
- Immigration law changes by country and over time. Verify against current official sources.

## Quick start

```bash
cd agentic_immigration_assistant
python3 run_matter.py --matter MAT-3001 --offline
```

## Agents

| Agent | Role |
|-------|------|
| Intake | Normalize facts the client already provided |
| Issue map | Possible issue categories to discuss with counsel |
| Documents | Document request checklist |
| Timeline | Key dates from the file (as recorded) |
| Research log | Placeholder log for counsel research notes |
| Client comms | Draft administrative client message |
| Risk flags | Process risks (missing docs, deadlines noted in file) |
| Gatekeeper | Human review pack before send or file |

## Human gate

Nothing is approved to send to a client or file with an authority unless you pass `--ship` after professional review.
