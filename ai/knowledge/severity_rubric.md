# Severity Rubric (shared)

## Critical
A **migration blocker** or **guaranteed runtime/build break**.
Examples:
- Java < 17 when targeting Spring Boot 3
- `javax.*` imports or `javax.*` artifacts on classpath when migrating to Jakarta
- Removed APIs still used (e.g., known Spring Security removals)
- Build fails / tests fail due to version mismatch
- Trailing-slash route matching disabled by default in SB3: routes mapped to `/foo/` return
  HTTP 404 for `/foo`, and security matchers on `/foo/` stop protecting `/foo` requests

## Warn
High probability issue or **behavior change risk** that needs validation and/or targeted refactor.
Examples:
- Property renames / removed keys requiring verification
- Container/runtime compatibility risks (WAR deployment, servlet container version)

> **Note:** Trailing-slash route matching disabled by default in SB3 is **Critical**, not Warn.
> A route mapped to `/foo/` silently returns HTTP 404 for `/foo` requests, and a security
> `requestMatchers("/foo/")` no longer protects `/foo` — both are guaranteed runtime breaks.

## Suggestion
Not required to ship migration, but improves quality/maintainability while touching code.
Examples:
- Enforcer rules, dependency hygiene, checkers
- Minor refactors to reduce future migration friction
