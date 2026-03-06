# Task: <name>

| Field | Value |
|---|---|
| **Role** | `reviewer` · `submitter` · `ops` |
| **Goal** | One sentence: what does success look like? |
| **Constraints** | Any limits — e.g. read-only, no refactoring, one commit per area |

---

## Full Load Order

| # | File | Role |
|---|---|---|
| 1 | `ai/skills/<relevant_skill>/SKILL.md` | Skill entry (loads its own Dependencies) |
| 2 | `ai/templates/<template>.md` | Output format |

---

## DoD

- Write report to `<filename>` using `ai/templates/<template>.md` as format
- Clear GO/GO-with-fixes/NO-GO verdict
