# Task: <name>

| Field | Value |
|---|---|
| **Role** | `reviewer` · `submitter` · `ops` |
| **Goal** | One sentence: what does success look like? |
| **Scope** | Paths to read — e.g. `src/`, `k8s/`, `pom.xml` |
| **Constraints** | Any limits — e.g. read-only, no refactoring, one commit per area |

---

## Checks

### C1 — <title>
- What to look for
- **CRITICAL / WARN / SUGGESTION** criteria

### C2 — <title>
- What to look for
- **CRITICAL / WARN / SUGGESTION** criteria

### C3 — <title>
- What to look for
- **CRITICAL / WARN / SUGGESTION** criteria

---

## Evidence

- Each finding: `file:line` + snippet (≤ 10 lines)
- Validation: one command to verify (e.g. `mvn test`, `helm lint .`)

---

## SkillRefs

SkillRefs: ai/skills/<relevant_skill>/SKILL.md

---

## DoD

- One report following `ai/BOOTSTRAP.md` Standard Output Contract
- Findings are evidence-based and actionable
- Clear GO/GO-with-fixes/NO-GO verdict
