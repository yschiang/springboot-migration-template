# Task: Spring Boot 2 → 3 Code Review / Fix

| Field | Value |
|---|---|
| **Role** | `reviewer` (default) · `submitter` to apply fixes |
| **Goal** | Identify — or fix — all blockers preventing a Spring Boot 2.x app from running on Spring Boot 3.x |
| **Scope** | `src/`, `pom.xml`, `build.gradle`, `application*.yml`, `application*.properties` |
| **Constraints** | Reviewer: read-only. Submitter: fix only what Checks flag, one commit per area. |

---

## Role Switch

**reviewer (default):** produce a report. Stop before changing any file.

**submitter:** apply fixes in this order:
1. Java toolchain → 2. Dependencies → 3. Code (javax→jakarta) → 4. Config → 5. Security → 6. Tests

---

## Checks

### C1 — Java 17 toolchain
- `pom.xml`: `<java.version>`, `maven-compiler-plugin` source/target, `<parent>` Spring Boot version
- `build.gradle`: `sourceCompatibility`, `targetCompatibility`, `toolchain`
- **CRITICAL** if Java < 17 anywhere

### C2 — javax → jakarta namespace
- `grep -r "import javax\." src/`
- `mvn dependency:tree | grep "javax\."` or `./gradlew dependencies | grep "javax\."`
- **CRITICAL** for every `javax.*` import or direct dependency

### C3 — Spring Security
- `grep -r "WebSecurityConfigurerAdapter\|antMatchers\|mvcMatchers" src/`
- Must use `SecurityFilterChain` bean + `requestMatchers`
- **CRITICAL** if found

### C4 — Path matching & URL `//` normalization
- `grep -r "setUseTrailingSlashMatch\|configurePathMatch" src/`
- Spring Boot 3: trailing slash matching **off**; `//` not normalized
- **WARN** if patterns found; **CRITICAL** if Ingress forwards `//` to the app

### C5 — Actuator & dependency alignment
- `httpclient` 4.x → must migrate to `httpclient5` (**CRITICAL**)
- Missing `management.endpoint.health.probes.enabled=true` (**WARN**)
- Spring Security version < 6.0 (**CRITICAL**)

---

## Evidence

- Each finding: `file:line` + snippet (≤ 10 lines)
- Validation: `mvn -q -DskipTests=false test`
- Submitter: save build proof to `docs/evidence/build_pass.md`

---

## SkillRefs

SkillRefs: ai/skills/springboot_reviewer/sb3_reviewer.md, ai/skills/springboot_engineer/sb3_engineer.md, ai/knowledge/spring-boot-3.0-migration-guide.md
