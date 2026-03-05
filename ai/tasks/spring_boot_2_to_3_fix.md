# Task: Spring Boot 2 → 3 Migration Fix

| Field | Value |
|---|---|
| **Role** | `submitter` |
| **Goal** | Apply fixes for all blockers identified in a prior review report to make the app Spring Boot 3.x compatible |
| **Scope** | `src/`, `pom.xml`, `build.gradle`, `application*.yml`, `application*.properties` |
| **Constraints** | Fix only what the review report flagged. One commit per area. Do not refactor unrelated code. |

---

## Checks

### C1 — All Critical findings addressed
- Every CRITICAL from the review report has a corresponding fix
- **CRITICAL** if any are skipped without justification

### C2 — Fix order respected
- Java toolchain → Dependencies → Code → Config → Security → Tests
- **WARN** if fixes applied out of order (causes cascading failures)

### C3 — Build passes after fixes
- `mvn -q -DskipTests=false test` or `./gradlew test`
- `mvn dependency:tree | grep "javax\."` → zero results
- **CRITICAL** if build fails or javax dependencies remain

---

## Evidence

- Each fix: `file:line` + before/after snippet
- Validation: `mvn -q -DskipTests=false test`

---

## SkillRefs

SkillRefs: ai/skills/springboot_migration/SKILL.md

---

## DoD

- All Critical findings from the review report are fixed
- Each fix area committed separately with a descriptive message
- Build passes, dependency tree clean of `javax.*`
