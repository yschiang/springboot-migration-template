# Skill: Spring Boot 2 → 3 Migration Review (Repo-based)

## Mission
Review a given repository for a Spring Boot 2 → 3 migration and produce:
- Blockers and upgrade path
- Concrete fix recommendations
- Verification checklist

## Knowledge Base (must use)
Read in priority order. P0 precedes P1 in all reasoning and conflict resolution.

- **[P0] Spring Boot 3.0 Migration Guide (official — authoritative):**
  ai/knowledge/spring-boot-3.0-migration-guide.md
- **[P1] Baeldung migration guide (supplementary — practical examples):**
  ai/knowledge/baeldung-spring-boot-3-migration.md

## Known Conflicts Between Knowledge Sources
When the two sources disagree, apply these rules:

1. **Property name — prefer official**
   - Official: `spring.jpa.hibernate.use-new-id-generator-mappings` (correct, includes `-mappings`)
   - Baeldung: `spring.jpa.hibernate.use-new-id-generator` (incorrect, missing `-mappings`)
   - Use the official name when checking or reporting this property.

2. **Trailing slash matching — prefer official framing**
   - Official: the default value changed to `false` (still configurable)
   - Baeldung: describes the option as "deprecated" (imprecise)
   - The configuration option is NOT deprecated; only the default changed.

## Output Contract
Output MUST follow `ai/BOOTSTRAP.md` Standard Output Contract.
Optional: export to file using `ai/templates/review_report_template.md` when operator requests.

## Migration Key Constraints (anchor)
- Spring Boot 3 requires **Java 17+** and Spring Framework 6.
- Ecosystem is **Jakarta**: `javax.*` → `jakarta.*` across APIs and dependencies.
- Spring Security upgrade path: Boot 2.7 → Security 5.8 first → Security 6 → Boot 3.
- Apache HttpClient upgraded: 4.x (`org.apache.http.*`) → 5.x (`org.apache.hc.*`).

## Procedure (ordered by ROI)
### 1) Baseline detection
- Detect current Spring Boot version and build tool.
- If version < 2.7.x:
  - Create a finding (Warn/Critical depending on gap) recommending two-step upgrade: 2.7.x → 3.x.

### 2) Build toolchain (Critical)
- Check Java toolchain targets:
  - Maven: `maven-compiler-plugin`, toolchains, parent POM
  - Gradle: toolchains, `sourceCompatibility`, `targetCompatibility`
- If < 17 anywhere: Critical.

### 3) Dependency blockers (Critical first)
- Scan dependencies and dependency tree:
  - Direct `javax.*` artifacts (Critical)
  - `org.apache.httpcomponents:httpclient` (4.x) — must migrate to `org.apache.httpcomponents.client5:httpclient5` (Critical if RestTemplate is customized)
  - Swagger/Springfox legacy issues (Warn/Critical depending on compile break)
  - Spring Security < 5.8 — must upgrade to 5.8 before Boot 3 (Critical)
  - Hibernate — must use `org.hibernate.orm` group ID (Critical)
- Flag transitive conflicts likely to break.

### 4) Code-level breaks (targeted grep)
Search patterns:
- `javax\.` (Critical)
- `org\.apache\.http\.` (Critical — old HttpClient 4.x namespace, must migrate to `org.apache.hc.*`)
- `HttpComponentsClientHttpRequestFactory` with `setConnectTimeout\|setReadTimeout` (Critical — removed in HttpClient 5.x)
- `WebSecurityConfigurerAdapter` (Critical if present)
- `antMatchers\(` / `mvcMatchers\(` (Warn/Critical depending on usage)
- `@EnableBatchProcessing` (Warn — remove if relying on Boot autoconfiguration)
- `@ConstructorBinding` at type level (Warn — move to constructor level)

### 5) Config/property changes
- Scan `application*.yml/properties` for deprecated/removed keys:
  - `spring.redis.*` → `spring.data.redis.*` (Warn)
  - `spring.data.cassandra.*` → `spring.cassandra.*` (Warn)
  - `spring.jpa.hibernate.use-new-id-generator` → removed (Critical if present)
  - `server.max.http.header.size` → `server.max-http-request-header-size` (Warn)
  - `spring.security.saml2.relyingparty.registration.{id}.identity-provider` → removed (Critical if present)
- Tip: add `spring-boot-properties-migrator` dependency to auto-detect at runtime.

### 6) Spring Batch
- If `@EnableBatchProcessing` is present and Boot autoconfiguration is desired: remove it (Warn).
- If multiple `Job` beans exist: flag that only one job runs at startup; others need `spring.batch.job.name` or a scheduler (Warn).

### 7) Packaging/runtime
- WAR vs JAR:
  - WAR on external container requires Jakarta-compatible container (Warn/Critical).
- Ensure actuator, security, tracing implications are called out if present.

## Required Commands Section (tailor by build tool)
Maven:
- `mvn -q -DskipTests=false test`
- `mvn -q dependency:tree | rg "javax\.|jakarta\."`
Gradle:
- `./gradlew test`
- `./gradlew dependencies | rg "javax\.|jakarta\."`

## Done Definition
- A single report with Critical/Warn/Suggestion
- Priority Plan ordered: Java → deps → code → config → batch → tests → runtime
