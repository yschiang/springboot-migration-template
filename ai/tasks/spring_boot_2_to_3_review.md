# Task: Spring Boot 2 → 3 Code Review

| Field | Value |
|---|---|
| **Role** | `reviewer` |
| **Goal** | Identify all blockers preventing a Spring Boot 2.x app from running on Spring Boot 3.x |
| **Constraints** | Read-only. Do not modify source files. |

---

## Full Load Order

| # | File | Role |
|---|---|---|
| 1 | `ai/skills/springboot_migration/SKILL.md` | Skill entry (loads its own Dependencies) |
| 2 | `ai/templates/review_report_template.md` | Output format |

---

## DoD

- **Pass 1**: Write `review-scanned-<repo>-<YYYYMMDD>.md` with directory tree and file list → STOP and wait for operator confirmation
- **Pass 2**: Write `review-report-<repo>-<YYYYMMDD>-zh.md` (Traditional Chinese) using `ai/templates/review_report_template.md` → update scanned files log with finding annotations
- Clear GO/GO-with-fixes/NO-GO verdict