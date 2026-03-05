# Submitter Summary: Broken SB2 → SB3 Migration Demo

**Branch:** `feature/sb2-to-sb3-broken-migration` (7 commits off `master`)

---

## Commit History

| Commit | Change |
|--------|--------|
| C1 | Baseline Spring Boot 2.7.18 app (web, validation, security, test) |
| C2 | Bump parent to SB3 3.2.5 — `java.version` intentionally left at 11 |
| C3 | Partial javax→jakarta: only `@Valid` migrated; `@PostConstruct`, `HttpServletRequest`, `javax.validation.constraints.*` left as-is |
| C4 | Old deps: `javax.servlet-api:4.0.1`, `javax.validation:validation-api:2.0.1.Final`, `springfox-swagger2:2.9.2`, `@EnableSwagger2` |
| C5 | Security "fix": removed `WebSecurityConfigurerAdapter`, but still calls `antMatchers()` (removed in Security 6) |
| C6 | `application.yml` with removed/renamed SB3 properties (`use-suffix-pattern`, `spring.redis.*`, Prometheus metrics) |
| C7 | `docs/evidence/submitter_build_fail.md` + `docs/PR_DESCRIPTION.md` |

---

## Build Failure (verified)

```
[ERROR] COMPILATION ERROR :
[ERROR] UserController.java:[7,24] package javax.annotation does not exist
[ERROR] UserController.java:[18,6] cannot find symbol: class PostConstruct
[ERROR] SecurityConfig.java:[21,17] cannot find symbol: method antMatchers(String)
[INFO] BUILD FAILURE
```

Full output: [`docs/evidence/submitter_build_fail.md`](evidence/submitter_build_fail.md)

---

## 8 Intentional Pitfalls

| # | Scenario | Location |
|---|----------|----------|
| 1 | **Java toolchain mismatch** — `java.version=11` with SB3 (requires Java 17+) | `pom.xml` |
| 2 | **Incomplete javax→jakarta** — `@PostConstruct`, `HttpServletRequest`, all DTO constraints still `javax.*` | `UserController.java`, `CreateUserRequest.java` |
| 3 | **Spring Security API removal** — `antMatchers()` removed in Security 6; must use `requestMatchers()` | `SecurityConfig.java` |
| 4 | **Dependency conflicts** — `springfox-swagger2:2.9.2` and old `javax.*` APIs on SB3 classpath | `pom.xml` |
| 5 | **Removed properties** — `spring.mvc.pathmatch.use-suffix-pattern` deleted in SB3 | `application.yml` |
| 6 | **Renamed properties** — `spring.redis.*` → `spring.data.redis.*`; Micrometer Prometheus namespace changed | `application.yml` |
| 7 | **Springfox legacy** — `@EnableSwagger2` / `springfox-swagger2:2.9.2` incompatible with Spring MVC 6 | `DemoApplication.java`, `pom.xml` |
| 8 | **Trailing-slash path matching** — `GET /api/users/` + security rule `/api/users/` silently break under SB3 `PathPatternParser` | `SecurityConfig.java`, `UserController.java` |

---

## Related Docs

- [`docs/PR_DESCRIPTION.md`](PR_DESCRIPTION.md) — PR description (no solutions)
- [`docs/evidence/submitter_build_fail.md`](evidence/submitter_build_fail.md) — captured build log
