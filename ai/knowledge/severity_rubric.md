# Severity Rubric (shared)

## Design intent
This rubric is designed for **code review and CI gating**. The goal is zero missed blockers with minimal false alarms.

## Binding rules

### Rule 1 — Explicit listing is binding
If the rubric below **explicitly lists** an item with a severity, the reviewer **MUST NOT override it** — even if the reviewer believes the runtime impact is lower (e.g., "relocation still resolves", "works at runtime today"). The rubric is the source of truth.

### Rule 2 — Unlisted items: judge by impact
If an issue is NOT explicitly listed below, determine severity by asking:
- **Will it cause a compile or build failure?** → Critical
- **Will it cause a guaranteed runtime error (ClassNotFoundException, NoSuchMethodError, startup crash)?** → Critical
- **Will it cause a silent behavior change (wrong results, security gap, data loss)?** → Critical
- **Will it cause a deprecation warning, suboptimal behavior, or need validation?** → Warn
- **Is it purely style, best practice, or future-proofing?** → Suggestion

Note: Scanning discipline rules (exhaustive file listing, severity enforcement, etc.) are defined in `ai/skills/code_scanner/SKILL.md`.

## Critical
A **migration blocker** or **guaranteed runtime/build break**.
Examples:
- Java < 17 when targeting Spring Boot 3
- `javax.*` imports or `javax.*` artifacts on classpath when migrating to Jakarta
  - Each `javax.*` sub-namespace (`persistence`, `validation`, `xml.bind`, `annotation`, `servlet`) is a **separate** Critical finding
- Removed APIs still used (e.g., `WebSecurityConfigurerAdapter`, `antMatchers()`, `mvcMatchers()`, `authorizeRequests()`)
- Build fails / tests fail due to version mismatch
- **Dependency coordinate changes that break resolution in Boot 3 BOM**:
  - `mysql:mysql-connector-java` → `com.mysql:mysql-connector-j`
  - `org.hibernate:hibernate-core` → `org.hibernate.orm:hibernate-core`
  - Springfox (any version) — incompatible with Spring MVC 6
- Removed property keys: `spring.jpa.hibernate.use-new-id-generator-mappings`
- Hibernate 6 removed dialect classes (`MySQL5Dialect`, `MySQL5InnoDBDialect`, `H2Dialect`, etc.)
- `@LocalServerPort` package relocation (`boot.web.server` → `boot.test.web.server`)
- Trailing-slash route matching disabled by default in SB3: routes mapped to `/foo/` return
  HTTP 404 for `/foo`, and security matchers on `/foo/` stop protecting `/foo` requests

## Warn
High probability issue or **behavior change risk** that needs validation and/or targeted refactor.
Examples:
- Property renames requiring update: `spring.redis.*` → `spring.data.redis.*`, `server.max.http.header.size` → `server.max-http-request-header-size`
- Metrics export property path changes: `management.metrics.export.*` → `management.<product>.metrics.export.*`
- Plugin coordinate changes that don't break build but need updating: `pl.project13.maven:git-commit-id-plugin`
- Container/runtime compatibility risks (WAR deployment, servlet container version)
- `@ConstructorBinding` at type level (move to constructor)
- `@EnableBatchProcessing` when Boot autoconfiguration is desired

## Suggestion
Not required to ship migration, but improves quality/maintainability while touching code.
Examples:
- Enforcer rules, dependency hygiene, checkers
- Minor refactors to reduce future migration friction
