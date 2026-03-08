# Spring Boot 2 → 3 Migration — Pattern Registry

## Migration Key Constraints
- Spring Boot 3 requires **Java 17+** and Spring Framework 6.
- Ecosystem is **Jakarta**: `javax.*` → `jakarta.*` across APIs and dependencies.
- Spring Security upgrade path: Boot 2.7 → Security 5.8 first → Security 6 → Boot 3.
- Apache HttpClient upgraded: 4.x (`org.apache.http.*`) → 5.x (`org.apache.hc.*`).

## Checks (ordered by ROI)

### 1) Baseline detection
- Detect current Spring Boot version and build tool.
- If version < 2.7.x:
  - Create a finding (Warn/Critical depending on gap) recommending two-step upgrade: 2.7.x → 3.x.

### 2) Build toolchain
- Java toolchain targets:
  - Maven: `maven-compiler-plugin`, toolchains, parent POM `<java.version>`
  - Gradle: toolchains, `sourceCompatibility`, `targetCompatibility`
- If < 17 anywhere: **Critical**.

### 3) Dependency blockers

#### Critical
| Old coordinate | New coordinate | Notes |
|---|---|---|
| `javax.xml.bind:jaxb-api` | `jakarta.xml.bind:jakarta.xml.bind-api` | JAXB |
| `javax.servlet:javax.servlet-api` | `jakarta.servlet:jakarta.servlet-api` | Servlet |
| `javax.validation:validation-api` | `jakarta.validation:jakarta.validation-api` | Bean Validation |
| `javax.annotation:javax.annotation-api` | `jakarta.annotation:jakarta.annotation-api` | Lifecycle |
| `org.apache.httpcomponents:httpclient` | `org.apache.httpcomponents.client5:httpclient5` | HttpClient 4→5 |
| `io.springfox:springfox-*` (any version) | `org.springdoc:springdoc-openapi-*` | Springfox incompatible with MVC 6 |
| `org.hibernate:hibernate-core` | `org.hibernate.orm:hibernate-core` | Old group ID not in Boot 3 BOM |
| `mysql:mysql-connector-java` | `com.mysql:mysql-connector-j` | Old coordinates no longer published |

#### Warn
| Old coordinate | New coordinate | Notes |
|---|---|---|
| `pl.project13.maven:git-commit-id-plugin` | `io.github.git-commit-id:git-commit-id-maven-plugin` | Plugin relocation |

- Also flag transitive conflicts likely to break.

### 4) Code-level break patterns

#### Jakarta namespace (each sub-namespace = separate finding)
| Grep pattern | Severity | What it finds |
|---|---|---|
| `javax\.persistence\.` | Critical | JPA imports |
| `javax\.validation\.` | Critical | Bean Validation imports |
| `javax\.xml\.bind\.` | Critical | JAXB imports |
| `javax\.annotation\.PostConstruct\|javax\.annotation\.PreDestroy` | Critical | Lifecycle annotations |
| `javax\.servlet\.` | Critical | Servlet API imports |

#### Other code-level breaks
| Grep pattern | Severity | What it finds |
|---|---|---|
| `org\.apache\.http\.` | Critical | HttpClient 4.x namespace |
| `setConnectTimeout\|setReadTimeout` (in HttpComponentsClientHttpRequestFactory context) | Critical | Removed timeout setters in HC5 |
| `WebSecurityConfigurerAdapter` | Critical | Removed in Security 6 |
| `antMatchers\(` / `mvcMatchers\(` | Critical | Removed in Security 6, use `requestMatchers()` |
| `@EnableSwagger2\|@EnableOpenApi\|springfox` | Critical | Springfox incompatible with Boot 3 |
| `@EnableBatchProcessing` | Warn | Remove if relying on Boot autoconfiguration |
| `@ConstructorBinding` (at type level, not constructor) | Warn | Move to constructor parameter in Boot 3 |

#### Trailing-slash routes
| Grep pattern | Severity | What it finds |
|---|---|---|
| `Mapping.*/$` in `*.java` | Critical | Route mappings with trailing slash |
| `(antMatchers\|mvcMatchers\|requestMatchers)` piped through `/$` | Critical | Security matchers with trailing slash |

> **Separation rule:** Trailing-slash route findings are ALWAYS a separate finding from `antMatchers`/`mvcMatchers` API removal, even when the same line of code exhibits both issues. They have different root causes (API removal vs URL matching default change) and different fix strategies.

> **Shell safety:** These patterns avoid literal `"` in regex. Do NOT combine with other patterns in a double-quoted shell argument — the `"` quoting will break.

Use your built-in search tool with these patterns against `*.java` files under `src/`.

### 5) Config/property changes

| Old key | New key / action | Severity |
|---|---|---|
| `spring.redis.*` | `spring.data.redis.*` | Warn |
| `spring.data.cassandra.*` | `spring.cassandra.*` | Warn |
| `spring.jpa.hibernate.use-new-id-generator-mappings` | Removed — delete it | Critical |
| `server.max.http.header.size` | `server.max-http-request-header-size` | Warn |
| `management.metrics.export.<product>.*` | `management.<product>.metrics.export.*` | Warn |
| `spring.security.saml2.relyingparty.registration.{id}.identity-provider` | Removed — use `asserting-party` | Critical |

Tip: add `spring-boot-properties-migrator` dependency to auto-detect at runtime.

### 6) Spring Batch
- `@EnableBatchProcessing` present + Boot autoconfiguration desired → remove it (Warn).
- Multiple `Job` beans → only one runs at startup; others need `spring.batch.job.name` or scheduler (Warn).
- `JobBuilderFactory` / `StepBuilderFactory` usage → removed in Spring Batch 5 (Critical).
  Replace with `JobBuilder` / `StepBuilder` obtained via `JobRepository` / injected directly.

### 7) Packaging/runtime
- WAR on external container → requires Jakarta-compatible container (Tomcat 10+, Jetty 12+) (Warn/Critical).

### 8) Cross-reference items (from P0 migration guide)
Items not covered by checks 1–7 that may apply depending on repo:
| Pattern / Config | Notes |
|---|---|
| `spring.factories` | → `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` |
| `javax.inject` | → `jakarta.inject` |
| `ErrorController` interface | API changes in Boot 3 |
| `PathPatternParser` | Now default (was `AntPathMatcher`) |
| Flyway version | Boot 3 uses Flyway 9.0+ |
| Liquibase version | Boot 3 uses Liquibase 4.17+ |
| Micrometer / Metrics API | `WebMvcMetricsFilter` → `ServerHttpObservationFilter` etc. |
| `spring.config.import` | Required for Config Server in Boot 3 |

## Required Commands (tailor by build tool)
Maven:
```
mvn -q -DskipTests=false test
mvn -q dependency:tree
```
Gradle:
```
gradlew test
gradlew dependencies
```
Filter dependency output for `javax.` / `jakarta.` using your built-in search tool.
