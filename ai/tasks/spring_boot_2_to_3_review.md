# Task: Spring Boot 2 → 3 Code Review

| Field | Value |
|---|---|
| **Role** | `reviewer` |
| **Goal** | Identify all blockers preventing a Spring Boot 2.x app from running on Spring Boot 3.x |
| **Scope** | `src/`, `pom.xml`, `build.gradle`, `application*.yml`, `application*.properties` |
| **Constraints** | Read-only. Do not modify source files. |

---

## Checks

Acceptance criteria — detailed procedure is in SkillRefs.

- C1: Java toolchain ≥ 17
- C2: javax → jakarta namespace (imports + dependencies)
- C3: Spring Security API changes (antMatchers, WebSecurityConfigurerAdapter)
- C4: Path matching behavior changes (trailing slash, URL normalization)
- C5: Dependency alignment (HttpClient, actuator, config properties)

---

## SkillRefs

SkillRefs: ai/skills/springboot_migration/reviewer.md

---

## DoD

- Write report to `review-report-<repo>-<YYYYMMDD>.md` using `ai/templates/review_report_template.md` as format
- Clear GO/GO-with-fixes/NO-GO verdict
- Optional: if operator requests zh, also write `review-report-<repo>-<YYYYMMDD>-zh.md` (Traditional Chinese)
