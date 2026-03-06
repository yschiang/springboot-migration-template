# Task: Common Code Review

| Field | Value |
|---|---|
| **Role** | `reviewer` |
| **Goal** | Identify correctness, reliability, security, and maintainability issues in any codebase |
| **Constraints** | Read-only. Adapt checks to the language and framework in scope. |

---

## Full Load Order

| # | File | Role |
|---|---|---|
| 1 | `ai/skills/springboot_reviewer/SKILL.md` | Skill entry (loads its own Dependencies) |
| 2 | `ai/skills/coding-standards/SKILL.md` | Skill entry |
| 3 | `ai/templates/review_report_template.md` | Output format |

---

## DoD

- Write report using `ai/templates/review_report_template.md` as format
- Findings are evidence-based and actionable
- Clear GO/GO-with-fixes/NO-GO verdict
