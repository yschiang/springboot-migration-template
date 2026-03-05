# Severity Rubric (shared)

## Critical
A **migration blocker** or **guaranteed runtime/build break**.
Examples:
- Java < 17 when targeting Spring Boot 3
- `javax.*` imports or `javax.*` artifacts on classpath when migrating to Jakarta
- Removed APIs still used (e.g., known Spring Security removals)
- Build fails / tests fail due to version mismatch

## Warn
High probability issue or **behavior change risk** that needs validation and/or targeted refactor.
Examples:
- Property renames / removed keys requiring verification
- Framework major-version behavior changes (matching semantics, serialization, etc.)
- Container/runtime compatibility risks (WAR deployment, servlet container version)

## Suggestion
Not required to ship migration, but improves quality/maintainability while touching code.
Examples:
- Enforcer rules, dependency hygiene, checkers
- Minor refactors to reduce future migration friction
