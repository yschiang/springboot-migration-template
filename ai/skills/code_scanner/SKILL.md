# Skill: Code Scanner (Generic Scanning Discipline)

## Mission
Provide reusable scanning methodology and discipline rules for any code review or migration task.
This skill is **composed into** other review skills — it does NOT run standalone.

## Scan Discipline Rules

### D1 — Every pattern match produces a finding
If a grep/search pattern matches at least one file, a finding **MUST** exist in the report.
No silent skips. If a pattern produces zero matches, record "N/A — not found in repo".

### D2 — Exhaustive file listing
Every finding MUST list **ALL** matching files and line numbers in the **Where** section.
No sampling, no "e.g.", no "such as", no representative subset.
If a grep returns 12 files, all 12 appear.
If a file has multiple matching lines (e.g., lines 3,4,5), list the first line per file — but if matches span distinct code locations (e.g., import block vs method body), list each location.

### D3 — Severity is determined by the rubric, not by reviewer judgment
If the severity rubric explicitly lists an item with a severity, the reviewer **MUST** use that severity.
The reviewer may NOT override it based on their own reasoning (e.g., "relocation still resolves", "works at runtime today").
For items NOT explicitly listed in the rubric, apply the rubric's decision framework (e.g., impact-based questions).

### D4 — One finding per distinct root cause
Group by root cause / fix strategy, not by file. Multiple files sharing the same issue = one finding listing all files.
Do NOT collapse issues with different fix strategies into a single finding.
Example: `antMatchers("/owners/")` exhibits two issues — (1) `antMatchers` removed in Security 6, (2) trailing-slash matching disabled by default. These MUST be two findings.

## Scan Methodology

### Search execution rules

1. **Use built-in tools for all actions** — file enumeration, searching, reading, writing, and counting. Built-in tools are cross-platform by design. Do NOT shell out for any of these. Use forward slashes (`/`) for all file paths in output, regardless of OS.
2. **Do NOT generate scripts or shell commands** — never generate shell one-liners, compound commands, piped pipelines, or scripts (bash, Python, PowerShell) for file enumeration, counting, or classification. LLM-generated scripts are prone to token corruption (e.g., `case` pattern ordering bugs, shell quoting issues that cause hangs). Call your built-in tools one at a time. For line counts, use the last line number from your file read tool — do NOT shell out to `wc -l`.
3. **One pattern per search.** Never combine multiple check patterns into a single command. A quoting or regex error in one pattern will hang the entire block.
4. **Escape regex metacharacters** — e.g., `antMatchers\(` not `antMatchers(`.

### Search by file type

| Target | File filter | Example scope |
|---|---|---|
| Java code | `*.java` | `src/` |
| Config | `*.properties`, `*.yml`, `*.yaml` | `src/main/resources/` |
| Maven build | `pom.xml` | repo root |
| Gradle build | `*.gradle`, `*.kts` | repo root |

### Scan scope
- Default: `src/` and build files (`pom.xml`, `build.gradle`, `*.kts`)
- Exclude: `target/`, `build/`, `node_modules/`, `.git/`
- If `examples/` or other subdirectories exist, confirm with operator in Pass 1 whether to include

## Completeness Self-Check

**MANDATORY before writing the final report.** Walk through this checklist:

1. **Check coverage:** For every numbered check in the pattern registry (e.g., checks.md §1–§8), verify at least one finding or explicit "N/A" is recorded.
2. **File coverage:** For each finding, re-run the relevant grep and confirm the **Where** section lists every matching file. Add any missing files.
3. **Severity verification:** For each finding, look up the item in the severity rubric. If the rubric explicitly lists it, verify the finding uses the rubric's severity.
4. **No orphan matches:** Review all grep results. If any matched file is not referenced in any finding, either add it to the correct finding or explain why it's excluded.

## Knowledge Cross-Reference Pattern

After running all specific checks from the pattern registry:
1. Scan the authoritative knowledge source(s) for any additional breaking changes relevant to the dependencies and patterns found in this repo.
2. If a knowledge source item matches something in the repo (a dependency, a pattern, a config key), it MUST produce a finding — even if the pattern registry didn't explicitly list it.
3. Record which knowledge source items were checked and their match status (hit / N/A).
