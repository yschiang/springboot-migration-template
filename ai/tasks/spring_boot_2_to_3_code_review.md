# Task: Spring Boot 2 → 3 Code Review / Fix

| Field | Value |
|---|---|
| **Role** | `reviewer` (default) · switch to `submitter` to apply fixes |
| **Goal** | Identify — or fix — all blockers preventing a Spring Boot 2.x app from running on Spring Boot 3.x |
| **Scope** | `src/`, `pom.xml`, `build.gradle`, `application*.yml`, `application*.properties` |
| **Constraints** | Reviewer: read-only, no file changes. Submitter: fix only what Checks flag, one commit per area. |

---

## Role Switch

**Default (reviewer):** produce a report. Stop before changing any file.

**Submitter mode:** set `Role: submitter` in your prompt. Apply fixes in this order to avoid cascading failures:
1. Java toolchain → 2. Dependencies → 3. Code (javax→jakarta) → 4. Config → 5. Security → 6. Tests

---

## Checks (run in order)

### C1 — Java 17 toolchain
- `pom.xml`: `<java.version>`, `maven-compiler-plugin` source/target, `<parent>` Spring Boot version
- `build.gradle`: `sourceCompatibility`, `targetCompatibility`, `toolchain`
- **Flag CRITICAL** if Java < 17 anywhere

### C2 — javax → jakarta namespace
- Grep imports: `grep -r "import javax\." src/`
- Grep deps: `mvn dependency:tree | grep "javax\."` or `./gradlew dependencies | grep "javax\."`
- **Flag CRITICAL** for every `javax.*` import or direct `javax.*` dependency

### C3 — Spring Security
- Grep: `grep -r "WebSecurityConfigurerAdapter\|antMatchers\|mvcMatchers" src/`
- `WebSecurityConfigurerAdapter` removed in Security 6 → must use `SecurityFilterChain` bean
- `antMatchers`/`mvcMatchers` removed → must use `requestMatchers`
- **Flag CRITICAL** if found

### C4 — Path matching & URL `//` normalization
- Grep: `grep -r "setUseTrailingSlashMatch\|PathMatchConfigurer\|configurePathMatch" src/`
- Spring Boot 3 default: trailing slash matching **off**; `//` is no longer normalized to `/`
- Check if any `@RequestMapping`/`@GetMapping` paths rely on trailing slash or double-slash passthrough
- **Flag WARN** if patterns found; **CRITICAL** if Ingress or gateway forwards `//` to the app

### C5 — Actuator & dependency alignment
- Check `spring-boot-starter-actuator` version aligns with Boot 3 parent
- Verify `/actuator/health` liveness/readiness split: `management.endpoint.health.probes.enabled=true`
- Check `org.apache.httpcomponents:httpclient` (4.x) — must migrate to `httpclient5`
- Check `org.springframework.security` version ≥ 6.0
- **Flag CRITICAL** for httpclient 4.x; **WARN** for missing probe config

---

## Evidence Requirements

**Reviewer output must include:**
- For each finding: `file:line` + the offending snippet (≤ 10 lines)
- Build output if runnable: `mvn -q -DskipTests=false test` or `./gradlew test`
- Dependency scan: `mvn dependency:tree | grep "javax\."` → expect zero after fixes

**Submitter output must include:**
- Diff or patch per commit area
- Final build proof: full output of `mvn -q -DskipTests=false test` (all tests pass)
- Saved to: `docs/evidence/build_pass.md`

---

## Optional Skills

If available, load for richer guidance:
- `ai/skills/springboot_reviewer/sb3_reviewer.md` — detailed migration checklist
- `ai/skills/springboot_engineer/sb3_engineer.md` — fix patterns and code templates
- `ai/knowledge/spring-boot-3.0-migration-guide.md` — authoritative reference [P0]
