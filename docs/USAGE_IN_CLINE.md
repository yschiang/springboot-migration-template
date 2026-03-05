# Usage in Cline

## Option A — Single skill
Use:
- `ai/skills/sb3_migration_reviewer.md`

Also include rules:
- `ai/clinerules/01_output_contract.md`
- `ai/clinerules/02_evidence_first.md`
- `ai/clinerules/03_severity.md`
- `ai/clinerules/05_verification_commands.md`
- `ai/clinerules/06_spring_migration_focus.md`

## Option B — Merged reviewer
Use:
- `ai/skills/sb3_reviewer.md`

Also include all rules in `ai/clinerules/`.

## Run instructions (generic)
Provide the target repo path and ask for:
- detection + findings + fix plan + commands

You should get exactly one report per run.
