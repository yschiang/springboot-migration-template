# Review Report — demo

## Table of Contents
- [Overview](#overview)
- [Findings](#findings)
  - [Critical](#critical)
  - [Warning](#warning)
  - [Suggestion](#suggestion)
- [Strengths](#strengths)
- [Priority Plan](#priority-plan)
- [Verification Checklist](#verification-checklist)
- [Assumptions / Open Questions](#assumptions--open-questions)

---

## Overview

| Field              | Value                            |
|--------------------|----------------------------------|
| **Repo**           | `cline-springboot-migration-demo` |
| **Commit / Branch**| `refactor/ai-pipeline-ssot-architecture` |
| **Build**          | Maven                            |
| **Boot Version**   | `3.2.5`                          |
| **Java Target**    | `11` (CRITICAL — requires 17)    |
| **Web**            | Servlet                          |
| **Reviewed with**  | `springboot_migration/SKILL.md` → composes `springboot_reviewer/SKILL.md` + `springboot_migration/checks.md` |
| **Recommendation** | **`NO-GO`** — 5 critical blockers prevent compilation and runtime |

### Summary

| Severity   | Count  | Description              |
|------------|--------|--------------------------|
| Critical   | `5`    | Must fix before merge    |
| Warning    | `3`    | Fix soon                 |
| Suggestion | `1`    | Nice to have             |
| **Total**  | **`9`** | —                       |

---

## Findings

### Critical

#### [CRITICAL][MIGRATION] C1 — Java toolchain set to 11, requires 17+

**Where**
- File: `pom.xml`
- Symbol/Section: `<java.version>` property

**Evidence**
```xml
<!-- pom.xml:22 -->
<java.version>11</java.version>
```

**Why it's a problem**
- Spring Boot 3.x requires Java 17 minimum (P0 migration guide: "Spring Boot 3.0 requires Java 17 or later"). Code won't compile with bytecode target 11.

**Recommended fix**
- Change `<java.version>` to `17`
```xml
<java.version>17</java.version>
```

**Action items**
- [ ] Update `pom.xml:22` — `<java.version>17</java.version>`

**References**
- P0: Spring Boot 3.0 Migration Guide § "Review System Requirements"

---

#### [CRITICAL][MIGRATION] C2 — Legacy javax.* direct dependencies on classpath

**Where**
- File: `pom.xml`
- Symbol/Section: `javax.servlet:javax.servlet-api`, `javax.validation:validation-api`

**Evidence**
```xml
<!-- pom.xml:55-60 -->
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>4.0.1</version>
    <scope>provided</scope>
</dependency>

<!-- pom.xml:63-67 -->
<dependency>
    <groupId>javax.validation</groupId>
    <artifactId>validation-api</artifactId>
    <version>2.0.1.Final</version>
</dependency>
```

**Why it's a problem**
- Spring Boot 3 / Tomcat 10 ships Jakarta EE 9+ (`jakarta.servlet-api`, `jakarta.validation-api`). These javax dependencies create duplicate APIs under conflicting namespaces, causing `ClassNotFoundException` or `NoSuchMethodError` at runtime.

**Recommended fix**
- Remove both dependencies entirely. Spring Boot 3 starters provide the Jakarta equivalents transitively.
```xml
<!-- DELETE both dependency blocks (pom.xml:54-67) -->
```

**Action items**
- [ ] Remove `javax.servlet:javax.servlet-api` dependency
- [ ] Remove `javax.validation:validation-api` dependency

**References**
- P0: Spring Boot 3.0 Migration Guide § "Jakarta EE"

---

#### [CRITICAL][MIGRATION] C3 — javax.* imports in Java source (6 occurrences, 3 files)

**Where**
- File: `src/main/java/com/example/demo/config/SecurityConfig.java`
- File: `src/main/java/com/example/demo/controller/UserController.java`
- File: `src/main/java/com/example/demo/dto/CreateUserRequest.java`

**Evidence**
```java
// SecurityConfig.java:10
import javax.servlet.http.HttpServletRequest;

// UserController.java:7-8
import javax.annotation.PostConstruct;
import javax.servlet.http.HttpServletRequest;

// CreateUserRequest.java:3-5
import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
```

**Why it's a problem**
- The `javax.*` packages no longer exist on the Spring Boot 3 classpath. All imports must use `jakarta.*`. Compilation fails with `package javax.servlet does not exist`.

**Recommended fix**
- Replace `javax.` → `jakarta.` for all affected imports:
```java
// SecurityConfig.java:10
import jakarta.servlet.http.HttpServletRequest;

// UserController.java:7-8
import jakarta.annotation.PostConstruct;
import jakarta.servlet.http.HttpServletRequest;

// CreateUserRequest.java:3-5
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
```

Note: `UserController.java:9` already has `jakarta.validation.Valid` — partial migration was started but not completed.

**Action items**
- [ ] Replace 6 `javax.*` imports across 3 files

**References**
- P0: Spring Boot 3.0 Migration Guide § "Jakarta EE"

---

#### [CRITICAL][MIGRATION] C4 — antMatchers() removed in Spring Security 6

**Where**
- File: `src/main/java/com/example/demo/config/SecurityConfig.java`
- Symbol/Section: `SecurityConfig.filterChain()`

**Evidence**
```java
// SecurityConfig.java:21-23
.antMatchers("/api/public/**").permitAll()
.antMatchers("/api/users/").permitAll()
.antMatchers("/actuator/health").permitAll()
```

**Why it's a problem**
- `antMatchers()` was removed in Spring Security 6.0 (shipped with Boot 3). Code won't compile: `cannot find symbol: method antMatchers(String)`.

**Recommended fix**
- Replace with `requestMatchers()`:
```java
.requestMatchers("/api/public/**").permitAll()
.requestMatchers("/api/users/").permitAll()
.requestMatchers("/actuator/health").permitAll()
```

**Action items**
- [ ] Replace 3 `antMatchers()` calls with `requestMatchers()` in `SecurityConfig.java:21-23`

**References**
- P0: Spring Boot 3.0 Migration Guide § "Spring Security Changes"

---

#### [CRITICAL][MIGRATION] C5 — Springfox Swagger 2 incompatible with Spring Boot 3

**Where**
- File: `pom.xml` (dependencies)
- File: `src/main/java/com/example/demo/DemoApplication.java` (annotation)

**Evidence**
```xml
<!-- pom.xml:70-79 -->
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.9.2</version>
</dependency>
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.9.2</version>
</dependency>
```
```java
// DemoApplication.java:5,8
import springfox.documentation.swagger2.annotations.EnableSwagger2;
@EnableSwagger2
```

**Why it's a problem**
- Springfox is abandoned and hardwired to `javax.*` + Spring MVC 5 internals. It fails at startup with `NoSuchBeanDefinitionException` and classpath errors on Boot 3.

**Recommended fix**
- Remove Springfox dependencies and `@EnableSwagger2` annotation
- Optionally replace with `springdoc-openapi-starter-webmvc-ui:2.x`
```xml
<!-- REMOVE from pom.xml:69-79 -->

<!-- OPTIONAL replacement -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.5.0</version>
</dependency>
```
```java
// DemoApplication.java — REMOVE lines 5 and 8
```

**Action items**
- [ ] Remove `springfox-swagger2` and `springfox-swagger-ui` from `pom.xml`
- [ ] Remove `@EnableSwagger2` and its import from `DemoApplication.java`
- [ ] (Optional) Add springdoc-openapi if Swagger UI is needed

**References**
- checks.md §3: Dependency blockers — Springfox

---

### Warning

#### [WARN][MIGRATION] W1 — Removed/renamed configuration properties in application.yml

**Where**
- File: `src/main/resources/application.yml`

**Evidence**
```yaml
# application.yml:12-13 — REMOVED in Boot 3
spring.mvc.pathmatch.use-suffix-pattern: true
spring.mvc.pathmatch.use-registered-suffix-pattern: true

# application.yml:16-19 — RENAMED
spring.redis.host: localhost

# application.yml:29-31 — RENAMED
management.metrics.export.prometheus.enabled: true
```

**Why it's a problem**
- `spring.mvc.pathmatch.use-suffix-pattern` and `use-registered-suffix-pattern`: removed in Boot 3, no replacement — causes startup warning or `UnknownPropertyException`
- `spring.redis.*`: renamed to `spring.data.redis.*` (P0 guide § "Redis Properties")
- `management.metrics.export.prometheus.*`: renamed to `management.prometheus.metrics.export.*` (P0 guide § "Actuator Metrics Export Properties")

**Recommended fix**
```yaml
spring:
  # REMOVE the pathmatch block entirely (lines 8-13)

  # RENAME redis → data.redis
  data:
    redis:
      host: localhost
      port: 6379
      timeout: 2000ms

management:
  # RENAME metrics export path
  prometheus:
    metrics:
      export:
        enabled: true
        step: 1m
```

**Action items**
- [ ] Remove `spring.mvc.pathmatch.use-suffix-pattern` and `use-registered-suffix-pattern`
- [ ] Rename `spring.redis.*` → `spring.data.redis.*`
- [ ] Rename `management.metrics.export.prometheus.*` → `management.prometheus.metrics.export.*`

**References**
- P0: Spring Boot 3.0 Migration Guide § "Redis Properties", "Actuator Metrics Export Properties"
- checks.md §5: Config/property changes

---

#### [WARN][MIGRATION] W2 — Trailing slash path matching default changed

**Where**
- File: `src/main/java/com/example/demo/controller/UserController.java:40`
- File: `src/main/java/com/example/demo/config/SecurityConfig.java:22`

**Evidence**
```java
// UserController.java:40
@GetMapping("/users/")

// SecurityConfig.java:22
.antMatchers("/api/users/").permitAll()
```

**Why it's a problem**
- Spring Boot 3 defaults `setUseTrailingSlashMatch` to `false` (P0 guide § "Spring MVC and WebFlux URL Matching"). `/api/users/` and `/api/users` are now different paths. Requests to `/api/users` will return 404. Note: the trailing slash option is NOT deprecated (P0 wins over P1 on this), only the default changed.

**Recommended fix**
- Option A: Remove trailing slashes from mappings (preferred)
- Option B: Add a `WebMvcConfigurer` to re-enable:
```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {
    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        configurer.setUseTrailingSlashMatch(true);
    }
}
```

**Action items**
- [ ] Decide trailing-slash strategy and apply consistently

**References**
- P0: Spring Boot 3.0 Migration Guide § "Spring MVC and WebFlux URL Matching"

---

#### [WARN][BASELINE] W3 — Missing Kubernetes health probe enablement

**Where**
- File: `src/main/resources/application.yml`

**Evidence**
```yaml
# Property absent from application.yml
# management.endpoint.health.probes.enabled is not set
```

**Why it's a problem**
- Actuator health is exposed, but `/actuator/health/liveness` and `/actuator/health/readiness` probes require explicit enablement in Boot 3 for Kubernetes deployments.

**Recommended fix**
```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
```

**Action items**
- [ ] Add probe enablement if deploying to Kubernetes

**References**
- checks.md §7: Packaging/runtime — actuator implications

---

### Suggestion

#### [SUGGESTION][MIGRATION] S1 — Add spring-boot-properties-migrator during migration

**Where**
- File: `pom.xml`

**Evidence**
```xml
<!-- Not present in pom.xml -->
```

**Why it's a problem**
- The `spring-boot-properties-migrator` module can automatically detect renamed/removed properties at runtime and log warnings with correct replacements. Useful during the migration phase.

**Recommended fix**
- Add temporarily, remove after migration:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-properties-migrator</artifactId>
    <scope>runtime</scope>
</dependency>
```

**Action items**
- [ ] Add during migration, remove after all properties are fixed

**References**
- P0: Spring Boot 3.0 Migration Guide § "Configuration Properties Migration"

---

## Strengths

- SecurityConfig already uses the modern `SecurityFilterChain` bean pattern (not `WebSecurityConfigurerAdapter`)
- Test suite exists with `@SpringBootTest` + `MockMvc` covering public endpoint, create user, and validation
- Boot parent version is already 3.2.5 — no two-step upgrade needed (skips 2.7 → 3.x path)
- Clean layered structure: controller → dto, config separated

---

## Priority Plan

### P0 — Must Fix (Critical)
> Impact: compilation and runtime failure

| # | Issue | File | Est. Effort |
|---|-------|------|-------------|
| 1 | C1 — Java 11 → 17 | `pom.xml` | 5m |
| 2 | C2 — Remove javax dependencies | `pom.xml` | 5m |
| 3 | C5 — Remove Springfox | `pom.xml`, `DemoApplication.java` | 10m |
| 4 | C3 — javax → jakarta imports | 3 Java files | 10m |
| 5 | C4 — antMatchers → requestMatchers | `SecurityConfig.java` | 5m |

### P1 — Fix Soon (Warning)
> Impact: runtime behavior change or silent failure

| # | Issue | File | Est. Effort |
|---|-------|------|-------------|
| 1 | W1 — Renamed/removed config properties | `application.yml` | 10m |
| 2 | W2 — Trailing slash matching | `UserController.java`, `SecurityConfig.java` | 10m |
| 3 | W3 — Health probes | `application.yml` | 5m |

### P2 — Backlog (Suggestion)
> Impact: developer experience

| # | Issue | Est. Effort |
|---|-------|-------------|
| 1 | S1 — Add properties-migrator temporarily | 2m |

---

## Verification Checklist

- Build:
  - `mvn clean compile`
- Unit tests:
  - `mvn -q -DskipTests=false test`
- Dependency audit:
  - `mvn -q dependency:tree | rg "javax\."` → expect zero results
- Smoke run:
  - `mvn spring-boot:run` → verify startup without errors
  - `curl http://localhost:8080/api/public/hello` → 200 OK

---

## Assumptions / Open Questions

- Springfox removal: confirm whether Swagger UI is required. If yes, add `springdoc-openapi-starter-webmvc-ui:2.x` as replacement.
- Trailing slash: confirm whether clients depend on `/api/users/` (with trailing slash). If so, add `WebMvcConfigurer` to preserve backward compatibility.
- Redis config: confirm whether Redis is actually used at runtime. If not, the `spring.redis.*` block can be removed entirely rather than renamed.

---

## Migration Checks N/A

The following checks from `springboot_migration/checks.md` were run and found not applicable:

| Check | Result |
|---|---|
| §1 Baseline detection — version < 2.7.x | N/A — already on 3.2.5 |
| §3 HttpClient 4.x | N/A — no `org.apache.httpcomponents:httpclient` dependency |
| §3 Hibernate group ID | N/A — no Hibernate/JPA dependency |
| §4 `WebSecurityConfigurerAdapter` | N/A — already using `SecurityFilterChain` |
| §4 `HttpComponentsClientHttpRequestFactory` | N/A — not present |
| §4 `@EnableBatchProcessing` | N/A — no Spring Batch usage |
| §4 `@ConstructorBinding` at type level | N/A — not present |
| §5 `spring.data.cassandra.*` | N/A — not used |
| §5 `spring.jpa.hibernate.use-new-id-generator-mappings` | N/A — not present |
| §5 SAML2 properties | N/A — not used |
| §6 Spring Batch | N/A — no Batch dependency |
| §7 WAR packaging | N/A — JAR (default) |
