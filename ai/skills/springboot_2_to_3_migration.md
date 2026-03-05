# Skill: Spring Boot 2 → 3 Migration Review (Repo-based)

## Mission
Review a given repository for a Spring Boot 2 → 3 migration and produce:
- Blockers and upgrade path
- Concrete fix recommendations
- Verification checklist

## Knowledge Base (must use)
- Spring Boot 3.0 Migration Guide (official):
  https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide
- Baeldung migration guide:
  https://www.baeldung.com/spring-boot-3-migration

## Required Output Contract
Use **exactly** the format in `ai/templates/review_report_template.md`.

## Migration Key Constraints (anchor)
- Spring Boot 3 requires **Java 17+** and Spring Framework 6.
- Ecosystem is **Jakarta**: `javax.*` → `jakarta.*` across APIs and dependencies.

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
  - Swagger/Springfox legacy issues (Warn/Critical depending on compile break)
  - Spring Security / Hibernate major upgrades (Warn/Critical depending on usage)
- Flag transitive conflicts likely to break.

### 4) Code-level breaks (targeted grep)
Search patterns:
- `javax\.` (Critical)
- `WebSecurityConfigurerAdapter` (Critical if present)
- `antMatchers\(` / `mvcMatchers\(` (Warn/Critical depending on usage)
- `@ConstructorBinding` / configuration binding pitfalls (Warn)

### 5) Config/property changes
- Scan `application*.yml/properties` for deprecated/removed keys (Warn or Critical if obvious).

### 6) Packaging/runtime
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
- A “Fast Fix Plan” ordered: Java → deps → code → config → tests → runtime
