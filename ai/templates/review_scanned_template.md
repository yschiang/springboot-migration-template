<!-- Template for scanned files log. Referenced by task card DoD. -->
<!-- Format is tiered by repo size: ≤100 files = full table, >100 files = summary. -->

# Scanned Files — <repo>

| Field | Value |
|---|---|
| **Date** | `<YYYY-MM-DD>` |
| **Total Files** | `<N>` |
| **Type Counts** | `Java: <X>, Config: <Y>, Build: <Z>` |

## Module Structure

| Module | Java | Config | Build | Total |
|--------|------|--------|-------|-------|
| `<module-a>` | `<X>` | `<Y>` | `<Z>` | `<N>` |
| `<module-b>` | `<X>` | `<Y>` | `<Z>` | `<N>` |
| **Total** | **`<X>`** | **`<Y>`** | **`<Z>`** | **`<N>`** |

For single-module projects, use one row (repo name as module).

## Scope Verification

| Glob Pattern | Count |
|---|---|
| `**/src/**/*.java` | `<N>` |
| `**/src/**/*.properties` | `<N>` |
| `**/src/**/*.yml` | `<N>` |
| `**/src/**/*.xml` | `<N>` |
| `**/pom.xml` | `<N>` |

Informational — shows which glob patterns were used. Primary count verification is Module Structure Total = Header Total Files.

<!-- STOP: Check Header Total Files. If > 100, do NOT include this section. -->

## Files

> **Gate: only include this section if Total Files ≤ 100.**
> If Total Files > 100, DELETE this entire section from your output. The Module Structure and Scope Verification tables above are sufficient.

| # | File | Type |
|---|------|------|
| 1 | `<path>` | Java |
| 2 | `<path>` | Config |
| ... | ... | ... |
