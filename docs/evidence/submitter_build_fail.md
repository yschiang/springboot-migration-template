# Build Failure Evidence

**Branch:** `feature/sb2-to-sb3-broken-migration`
**Date:** 2026-03-05
**Command:** `mvn -DskipTests=false test`
**Result:** BUILD FAILURE

---

## Raw Build Output

```
[INFO] Scanning for projects...
[INFO]
[INFO] --------------------------< com.example:demo >--------------------------
[INFO] Building demo 0.0.1-SNAPSHOT
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]--------------------------------
[INFO]
[INFO] --- resources:3.3.1:resources (default-resources) @ demo ---
[INFO] Copying 1 resource from src/main/resources to target/classes
[INFO] Copying 0 resource from src/main/resources to target/classes
[INFO]
[INFO] --- compiler:3.11.0:compile (default-compile) @ demo ---
[INFO] Changes detected - recompiling the module! :source
[INFO] Compiling 4 source files with javac [debug release 11] to target/classes
[INFO] -------------------------------------------------------------
[ERROR] COMPILATION ERROR :
[INFO] -------------------------------------------------------------
[ERROR] /…/src/main/java/com/example/demo/controller/UserController.java:[7,24] package javax.annotation does not exist
[ERROR] /…/src/main/java/com/example/demo/controller/UserController.java:[18,6] cannot find symbol
  symbol:   class PostConstruct
  location: class com.example.demo.controller.UserController
[ERROR] /…/src/main/java/com/example/demo/config/SecurityConfig.java:[21,17] cannot find symbol
  symbol:   method antMatchers(java.lang.String)
  location: variable auth of type org.springframework.security.config.annotation.web.configurers.AuthorizeHttpRequestsConfigurer<org.springframework.security.config.annotation.web.builders.HttpSecurity>.AuthorizationManagerRequestMatcherRegistry
[INFO] 3 errors
[INFO] -------------------------------------------------------------
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  3.775 s
[INFO] Finished at: 2026-03-05T21:46:20+08:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.11.0:compile (default-compile) on project demo: Compilation failure: Compilation failure:
[ERROR] /…/src/main/java/com/example/demo/controller/UserController.java:[7,24] package javax.annotation does not exist
[ERROR] /…/src/main/java/com/example/demo/controller/UserController.java:[18,6] cannot find symbol
[ERROR]   symbol:   class PostConstruct
[ERROR]   location: class com.example.demo.controller.UserController
[ERROR] /…/src/main/java/com/example/demo/config/SecurityConfig.java:[21,17] cannot find symbol
[ERROR]   symbol:   method antMatchers(java.lang.String)
[ERROR]   location: variable auth of type org.springframework.security.config.annotation.web.configurers.AuthorizeHttpRequestsConfigurer<…>.AuthorizationManagerRequestMatcherRegistry
[ERROR] -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
```

---

## Observed Failures Summary

| # | Error | File | Line | Root Cause |
|---|-------|------|------|-----------|
| 1 | `package javax.annotation does not exist` | UserController.java | 7 | `javax.annotation.PostConstruct` not migrated to `jakarta.annotation.PostConstruct` |
| 2 | `cannot find symbol: class PostConstruct` | UserController.java | 18 | Consequence of error #1 |
| 3 | `cannot find symbol: method antMatchers(String)` | SecurityConfig.java | 21 | `antMatchers()` removed in Spring Security 6; must use `requestMatchers()` |

---

## Additional Issues (not yet reached due to compile failure)

The following issues would surface once compilation is fixed:

| Scenario | Symptom | Source |
|----------|---------|--------|
| Java toolchain mismatch | `javac [debug release 11]` shown in build output — SB3 requires Java 17 minimum | `pom.xml` line 22 |
| javax.validation.constraints not migrated | `CreateUserRequest.java` still uses `javax.validation.*` (currently masked by explicit `javax.validation:validation-api:2.0.1.Final` dep in pom.xml) | `CreateUserRequest.java` |
| Springfox 2.9.2 incompatible with SB3 | Context load failure: `WebMvcRequestHandlerProvider` / `springfox.documentation.spring.web` expects Spring MVC 5; SB3 ships MVC 6 | `pom.xml` + `DemoApplication.java` |
| Removed properties at startup | `spring.mvc.pathmatch.use-suffix-pattern` / `use-registered-suffix-pattern` removed in SB3 | `application.yml` |
| Renamed properties | `spring.redis.*` → `spring.data.redis.*`; `management.metrics.export.prometheus.*` → `management.prometheus.metrics.export.*` | `application.yml` |
| javax.servlet import not migrated | `SecurityConfig.java` imports `javax.servlet.http.HttpServletRequest` (provided by conflicting `javax.servlet-api:4.0.1`) | `SecurityConfig.java` line 10 |
| Trailing-slash path matching | `GET /api/users/` mapped in controller; `antMatchers("/api/users/")` in security rule — SB3 PathPatternParser does not redirect trailing slashes by default | `SecurityConfig.java`, `UserController.java` |
