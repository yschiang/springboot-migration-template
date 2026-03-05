# cline-springboot-migration-demo

A **demo repository** to bootstrap Cline skills + rules for:
1) **Spring Boot 2 → 3 Migration (repo review + fix plan)**
2) **Spring Boot 2 → 3 Reviewer (extends a common code reviewer)**
3) **Common Reviewer (repo code review baseline)**

## Repo layout

- `ai/skills/`
  - Skills (what to do + output contract)
- `ai/clinerules/`
  - Rules (how to behave; consistent formatting; evidence requirements)
- `ai/templates/`
  - Reusable report templates + checklists
- `examples/`
  - Example output reports and “toy” repo snippets for dry-run

## How to use in Cline (suggested)
- Load the repo as your “knowledge base”.
- Pick a skill file from `ai/skills/` as the system/task prompt.
- Apply rules from `ai/clinerules/` in addition (or paste them into Cline rules).
- Run on a target repo path.

### Typical run
1. Use `ai/skills/common_reviewer.md` to generate a baseline review.
2. Use `ai/skills/springboot_2_to_3_migration.md` for migration blockers + plan.
3. Use `ai/skills/springboot_2_to_3_reviewer_extends_common.md` to merge both into a single consistent report.

## Output contract
All skills use the same report structure:
- Header (repo meta + detected stack + summary counts)
- Findings (Critical/Warn/Suggestion) with:
  - Where, Evidence snippet, Why, Recommended fix, References
- Fast Fix Plan (ordered)
- Verification Checklist (commands)
- Assumptions / Open Questions (minimal)

## Notes
- This repo does **not** include any proprietary code.
- You can fork it and tune rules/skills for your organization.

