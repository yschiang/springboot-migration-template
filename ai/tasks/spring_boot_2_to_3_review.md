# Task: Spring Boot 2 → 3 Code Review

| Field | Value |
|---|---|
| **Role** | `reviewer` |
| **Goal** | Identify all blockers preventing a Spring Boot 2.x app from running on Spring Boot 3.x |
| **Scope** | `src/`, `pom.xml`, `build.gradle`, `application*.yml`, `application*.properties` |
| **Constraints** | Read-only. Do not modify source files. |

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

---

## SkillRefs

SkillRefs: ai/skills/springboot_migration/reviewer.md

---

## DoD

- Write **two** report files using `ai/templates/review_report_template.md` as format:
  - `review-report-<repo>-<YYYYMMDD>.md` — English
  - `review-report-<repo>-<YYYYMMDD>-zh.md` — Traditional Chinese (繁體中文)
- Both reports follow `ai/BOOTSTRAP.md` Standard Output Contract
- Clear GO/GO-with-fixes/NO-GO verdict
