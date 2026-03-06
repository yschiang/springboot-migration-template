# Task: Spring Boot 2 → 3 Migration Fix

| Field | Value |
|---|---|
| **Role** | `submitter` |
| **Goal** | Apply fixes for all blockers identified in a prior review report to make the app Spring Boot 3.x compatible |
| **Constraints** | Fix only what the review report flagged. One commit per area. Do not refactor unrelated code. |

---

## Full Load Order

| # | File | Role |
|---|---|---|
| 1 | `ai/skills/springboot_migration/engineer.md` | Skill entry (loads its own Dependencies) |

---

## DoD

- All Critical findings from the review report are fixed
- Each fix area committed separately with a descriptive message
- Build passes, dependency tree clean of `javax.*`
