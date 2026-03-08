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

## Files

**Only for repos with ≤ 100 files.** For larger repos, omit this section — the Module Structure and Scope Verification tables provide sufficient coverage.

| # | File | Type |
|---|------|------|
| 1 | `<path>` | Java |
| 2 | `<path>` | Config |
| ... | ... | ... |
