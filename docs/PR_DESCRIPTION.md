# PR: Migrate demo app from Spring Boot 2.7 to Spring Boot 3.2

**Branch:** `feature/sb2-to-sb3-broken-migration`
**Base:** `master`

---

## What was attempted

This PR migrates the demo application from Spring Boot 2.7.18 to Spring Boot 3.2.5.
The following changes were made:

### C2 — Bump Spring Boot parent version
- Updated `spring-boot-starter-parent` from `2.7.18` to `3.2.5` in `pom.xml`.
- Java version property left at `11` for now (updating the JDK setup is a separate ticket).

### C3 — Partial javax → jakarta namespace migration
- Updated `UserController.java` to use `jakarta.validation.Valid` instead of `javax.validation.Valid`.
- Other javax imports in the codebase have not been touched yet — plan to address in a follow-up.

### C4 — Add legacy compatibility dependencies
- Added `javax.servlet:javax.servlet-api:4.0.1` (provided) to keep the old servlet imports compiling.
- Added `javax.validation:validation-api:2.0.1.Final` to keep DTO validation imports working.
- Added `springfox-swagger2:2.9.2` and `springfox-swagger-ui:2.9.2` for API documentation (same as before).
- Added `@EnableSwagger2` to `DemoApplication.java`.

### C5 — Spring Security config refactor
- Removed `extends WebSecurityConfigurerAdapter` (class no longer exists in Security 6).
- Replaced `configure(HttpSecurity)` override with a `@Bean SecurityFilterChain` method.
- Kept the same path rules: `/api/public/**` and `/actuator/health` are public; everything else requires authentication.

### C6 — application.yml property updates
- Added `spring.mvc.pathmatch` settings to control suffix-pattern matching.
- Added Redis connection config (`spring.redis.*`).
- Enabled Prometheus metrics export under `management.metrics.export.prometheus`.

---

## Known issues / open items

- The build is currently **failing** (see `docs/evidence/submitter_build_fail.md` for full log).
- Some `javax.*` imports were not fully migrated — needs follow-up.
- Not sure if springfox is compatible with Spring Boot 3; may need to switch to springdoc-openapi.
- Haven't verified if the security rules behave the same under Spring Security 6.
- Java version has not been updated to 17 yet.
- Not all changed properties in `application.yml` have been verified against the SB3 migration guide.

---

## Verification

```bash
# Build (currently fails):
mvn -DskipTests=false test

# Dependency tree inspection:
mvn dependency:tree | grep -E "javax\.|jakarta\."
```

See `docs/evidence/submitter_build_fail.md` for captured build output.
