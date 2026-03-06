# Skill: Spring Boot 2 to 3 Migration Engineer

## Mission

Apply fixes to a Spring Boot 2.x codebase to make it compatible with Spring Boot 3.x.
Work from the findings in a review report produced by `ai/skills/springboot_migration/SKILL.md`.
Do not invent new findings — fix only what the report identified.

## Dependencies

Load these files IN ORDER before executing:

| # | File | Role |
|---|---|---|
| 1 | `ai/skills/springboot_engineer/SKILL.md` | Composed module — base engineer role, constraints |
| 2 | `ai/knowledge/spring-boot-3.0-migration-guide.md` | Knowledge [P0] — official, authoritative |
| 3 | `ai/knowledge/baeldung-spring-boot-3-migration.md` | Knowledge [P1] — supplementary examples |

Additionally, load references from `ai/skills/springboot_engineer/references/` based on what you touch:
- Fixing security config → load `references/security.md`
- Fixing data/JPA → load `references/data.md`
- Fixing controllers/web → load `references/web.md`
- Writing/fixing tests → load `references/testing.md`

P0 precedes P1 in all reasoning.

## Fix Constraints

- Fix **only** what was identified in the review report. Do not refactor unrelated code.
- Prefer the minimal change that restores compatibility.
- Each fix area gets its own commit — do not bundle unrelated changes.
- Add tests only if needed to verify that a specific fix works correctly.

## Fix Order

Apply fixes strictly in this order to avoid cascading failures:

| Order | Area | Why first |
|---|---|---|
| 1 | Java toolchain | Everything else depends on the right JDK |
| 2 | Dependencies | Classpath must be correct before code compiles |
| 3 | Code (javax → jakarta, API changes) | Compile-time fixes |
| 4 | Config / application properties | Runtime correctness |
| 5 | Spring Batch | Autoconfiguration behavior |
| 6 | Tests | Verify each prior fix |
| 7 | Runtime / packaging | Final deployment validation |

## Fix Patterns

### Java toolchain
```xml
<!-- pom.xml -->
<java.version>17</java.version>
```

### javax to jakarta (imports)
- Replace all `import javax.` with `import jakarta.`
- Common: `javax.servlet.*` → `jakarta.servlet.*`, `javax.persistence.*` → `jakarta.persistence.*`, `javax.validation.*` → `jakarta.validation.*`

### javax to jakarta (dependencies)
```xml
<!-- Remove -->
<groupId>javax.servlet</groupId><artifactId>javax.servlet-api</artifactId>

<!-- Add -->
<groupId>jakarta.servlet</groupId><artifactId>jakarta.servlet-api</artifactId><version>6.0.0</version>
```

### Spring Security — replace WebSecurityConfigurerAdapter
```java
// Remove this pattern
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception { ... }
}

// Replace with SecurityFilterChain bean
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated())
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

### antMatchers / mvcMatchers → requestMatchers
```java
// Before
.antMatchers("/admin/**").hasRole("ADMIN")

// After
.requestMatchers("/admin/**").hasRole("ADMIN")
```

### Apache HttpClient 4.x → 5.x
```xml
<!-- Remove -->
<groupId>org.apache.httpcomponents</groupId><artifactId>httpclient</artifactId>

<!-- Add -->
<groupId>org.apache.httpcomponents.client5</groupId><artifactId>httpclient5</artifactId>
```
```java
// Before (4.x)
CloseableHttpClient client = HttpClients.custom().build();
factory.setConnectTimeout(30000);

// After (5.x)
RequestConfig config = RequestConfig.custom()
    .setConnectTimeout(Timeout.ofSeconds(30))
    .setResponseTimeout(Timeout.ofSeconds(30))
    .build();
CloseableHttpClient client = HttpClients.custom()
    .setDefaultRequestConfig(config)
    .build();
```

### Renamed config properties
| Old key | New key |
|---|---|
| `spring.redis.*` | `spring.data.redis.*` |
| `spring.data.cassandra.*` | `spring.cassandra.*` |
| `server.max.http.header.size` | `server.max-http-request-header-size` |
| `spring.jpa.hibernate.use-new-id-generator-mappings` | removed — delete it |

### Spring Batch — remove @EnableBatchProcessing
```java
// Remove this annotation to restore Boot autoconfiguration
@EnableBatchProcessing  // ← delete
@Configuration
public class BatchConfig { ... }
```

## Verification (must pass before done)

Maven:
- `mvn -q -DskipTests=false test` → all tests pass
- `mvn -q dependency:tree | rg "javax\."` → zero results (document any safe exceptions)

Gradle:
- `./gradlew test` → all tests pass
- `./gradlew dependencies | rg "javax\."` → zero results

