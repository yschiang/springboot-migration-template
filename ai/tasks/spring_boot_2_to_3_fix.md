# Task: Spring Boot 2 → 3 Migration Fix

| Field | Value |
|---|---|
| **Role** | `submitter` |
| **Goal** | Apply fixes for all blockers identified in a prior review report to make the app Spring Boot 3.x compatible |
| **Scope** | `src/`, `pom.xml`, `build.gradle`, `application*.yml`, `application*.properties` |
| **Constraints** | Fix only what the review report flagged. One commit per area. Do not refactor unrelated code. |

---

## Checks

Acceptance criteria — detailed procedure is in SkillRefs.

- C1: All Critical findings from the review report addressed
- C2: Fix order respected (Java → deps → code → config → security → tests)
- C3: Build passes after fixes, dependency tree clean of `javax.*`

---

## SkillRefs

SkillRefs: ai/skills/springboot_migration/engineer.md

---

## DoD

- All Critical findings from the review report are fixed
- Each fix area committed separately with a descriptive message
- Build passes, dependency tree clean of `javax.*`
