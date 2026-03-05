# Usage in Cline

## Option A — Single skill (SB2→3 migration review)
Use:
- `ai/skills/springboot_migration/reviewer.md`

Also include rules:
- `ai/clinerules/02_evidence_first.md`
- `ai/clinerules/03_severity.md`
- `ai/clinerules/06_spring_migration_focus.md`

## Option B — Generic code review
Use:
- `ai/skills/springboot_reviewer/SKILL.md`

Also include all rules in `ai/clinerules/`.

## Run instructions (generic)
Provide the target repo path and ask for:
- detection + findings + fix plan + commands

You should get exactly one report per run.
