# Review Report — example-spring-app

- Repo: `examples/toy-spring-app`
- Commit/Branch: `main`
- Detected stack:
  - Build: Maven
  - Boot: 2.6.3
  - Java target: 11
  - Web: Servlet
- Summary counts: Critical 2 | Warn 2 | Suggestion 1
- Recommendation: **NO-GO**

---

## Findings

### [Critical] SB3-001 - Java toolchain < 17 blocks Spring Boot 3
**Where**
- File: `pom.xml`
- Symbol/Section: `maven-compiler-plugin`

**Evidence**
```xml
<properties>
  <java.version>11</java.version>
</properties>
```

**Why it’s a problem**
- Spring Boot 3 requires Java 17+. Keeping Java 11 will fail compilation and/or runtime when upgrading to Spring Framework 6.

**Recommended fix**
- Upgrade build + runtime JDK to 17.
- Ensure CI agents and container base image also use 17.
```xml
<properties>
  <java.version>17</java.version>
</properties>
```

**References**
- https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide

---

### [Critical] SB3-002 - `javax.*` import must migrate to `jakarta.*`
**Where**
- File: `src/main/java/com/acme/DemoController.java`
- Symbol/Section: `@PostConstruct`

**Evidence**
```java
import javax.annotation.PostConstruct;
```

**Why it’s a problem**
- Spring Boot 3 ecosystem moved to Jakarta namespaces; `javax.*` APIs are no longer the baseline and will break compilation without the right migration.

**Recommended fix**
```java
import jakarta.annotation.PostConstruct;
```

**References**
- https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide

---

## Fast Fix Plan
1. Upgrade toolchain to Java 17 in build + CI + runtime images.
2. Upgrade Spring Boot to 2.7.x first (if starting below 2.7), run tests, then move to 3.x.
3. Migrate `javax.*` → `jakarta.*` in code and dependencies.
4. Validate security config and endpoint behavior changes with targeted tests.

## Verification Checklist
- Build:
  - `mvn -q -DskipTests=false test`
- Dependency check:
  - `mvn -q dependency:tree | rg "javax\.|jakarta\."`
- Smoke run:
  - `mvn -q spring-boot:run`

## Assumptions / Open Questions
- N/A
