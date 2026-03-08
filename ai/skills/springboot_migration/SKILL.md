# Skill: Spring Boot 2 → 3 Reviewer (Extends Common Reviewer)

## Mission
Produce **one merged review report** that:
- Runs the **Common Reviewer** baseline
- Adds **Spring Boot 2 → 3 migration** specific checks
- Outputs **one unified report** (no duplicate sections)

## Dependencies

Load these files IN ORDER before executing:

| # | File | Role |
|---|---|---|
| 1 | `ai/skills/code_scanner/SKILL.md` | Composed module — generic scanning discipline & methodology |
| 2 | `ai/skills/springboot_reviewer/SKILL.md` | Composed module — generic review baseline |
| 3 | `ai/skills/springboot_migration/checks.md` | Composed module — SB2→3 migration pattern registry |
| 4 | `ai/knowledge/spring-boot-3.0-migration-guide.md` | Knowledge [P0] — official, authoritative |
| 5 | `ai/knowledge/baeldung-spring-boot-3-migration.md` | Knowledge [P1] — supplementary examples |
| 6 | `ai/knowledge/severity_rubric.md` | Knowledge — severity definitions (Critical/Warn/Suggestion) |

P0 precedes P1 in all reasoning and conflict resolution.

### Known Conflicts Between Knowledge Sources
When the two sources disagree, apply these rules:
1. **Property name — prefer official**
   - Official: `spring.jpa.hibernate.use-new-id-generator-mappings` (correct, includes `-mappings`)
   - Baeldung: `spring.jpa.hibernate.use-new-id-generator` (incorrect, missing `-mappings`)
2. **Trailing slash matching — prefer official framing**
   - Official: the default value changed to `false` (still configurable)
   - Baeldung: describes the option as "deprecated" (imprecise)
   - The configuration option is NOT deprecated; only the default changed.

## Procedure (2-pass)

### Pass 1 — Discovery

Follow the scan scope rules from `code_scanner/SKILL.md`.

#### Output contract

Write `review-scanned-<repo>-<YYYYMMDD>.md` per `ai/templates/review_scanned_template.md`.
The file MUST contain these three sections:

| Section | Required content |
|---|---|
| **Header table** | Date, Total Files, Type Counts (`Java`, `Config`, `Build`, …) |
| **Directory Structure** | Indented list of all scanned files inside a fenced code block |
| **Files Read** | Numbered table — every scanned file with path, type, and line count |

Scope:
- **Include:** `src/` and build files (`pom.xml`, `build.gradle`, `*.kts`)
- **Exclude:** `.git`, `target`, `build`, `node_modules`, `.vscode`, `ai`, `.tools`, `.claude`
- **Extensions:** `.java`, `.xml`, `.yml`, `.yaml`, `.properties`, `.gradle`, `.kts`

#### Steps

> **Do NOT generate scripts** (Python, bash, PowerShell, etc.) to create this file.
> Use your built-in file tools directly. See `code_scanner/SKILL.md` Rule 2 for rationale.

1. **Enumerate** — use your file listing tool (e.g., `list_files`, Glob) to collect all matching files under `src/` and build files at repo root.
2. **Count** — tally files by type (`Java`, `Config`, `Build`) for the header table.
3. **Write** — directly write the markdown file with the header table, an indented file list, and the files-read table. Use 2-space indentation per directory level. Do NOT use `├──`/`└──` connectors.

Indentation example:
```
repo-name/
  src/
    main/java/com/example/
      config/
        SecurityConfig.java
      model/
        User.java
    main/resources/
      application.properties
  pom.xml
```

#### Validation gate

After writing the file:
1. **Read** `review-scanned-<repo>-<YYYYMMDD>.md`.
2. **Verify** ALL of:
   - `# Scanned Files` header exists
   - `## Directory Structure` contains a non-empty tree
   - `## Files Read` table has ≥ 1 data row
3. If any check fails → regenerate. Do NOT proceed with an empty or placeholder file.
4. **STOP and present to operator. Wait for confirmation before Pass 2.**
   - Operator may adjust scope (add/remove files) before confirming.

### Pass 2 — Review

**Gate:** Read `review-scanned-<repo>-<YYYYMMDD>.md`. If it is empty or missing the `## Files Read` table, STOP — go back and complete Pass 1 first. Never proceed with an empty scanned files log.

1. Read the confirmed scanned files log as the manifest.
2. Execute the pattern registry from `checks.md` (migration) and the review procedure from `springboot_reviewer/SKILL.md` (baseline) on the listed files only.
3. Run the **Completeness Self-Check** from `code_scanner/SKILL.md`:
   - Apply to `checks.md` §1–§8 as the migration pattern registry.
   - Apply to `springboot_reviewer/SKILL.md` code quality categories (§3: error handling, resource management, config validation, logging, security). For each category, record at least one finding or explicit "N/A — reviewed, no issues found."
4. The report's **Files Scanned** count in the Overview table MUST equal the number of rows in the scanned log's **Files Read** table. If mismatch, reconcile before finalizing.
5. Write the review report per task card DoD.
6. **Update** `review-scanned-<repo>-<YYYYMMDD>.md`: annotate the directory tree with finding IDs (`⚠ C1, W2` etc.).

## Merge Rules
- **Every finding MUST include a source tag** — no finding may omit it:
  - `[MIGRATION]` — finding from SB2→3 migration checks (`checks.md`)
  - `[BASELINE]` — finding from generic reviewer checks (`springboot_reviewer/SKILL.md`)
- Header format: `#### [SEVERITY][SOURCE] ID — title`
  - Example: `#### [CRITICAL][MIGRATION] C1 — title` or `#### [WARN][BASELINE] W1 — title`
- **When to merge:** Only merge when BOTH skills flag the **exact same issue** (same root cause, same fix).
  - Example: both flag "Java 11" → merge into one Critical finding.
- **When NOT to merge:** Different `javax.*` sub-namespaces are **separate findings** because they have different fix strategies:
  - `javax.persistence.*` → `jakarta.persistence.*` (JPA / Hibernate)
  - `javax.validation.*` → `jakarta.validation.*` (Bean Validation)
  - `javax.xml.bind.*` → `jakarta.xml.bind.*` (JAXB) — also needs new dependency
  - `javax.annotation.*` → `jakarta.annotation.*` (PostConstruct, PreDestroy)
  - `javax.servlet.*` → `jakarta.servlet.*` (Servlet API)
  - Each sub-namespace = **one finding**, listing ALL affected files in the **Where** section.
  - Code imports AND their corresponding dependency coordinate change for the same library belong in the **same** finding (e.g., `javax.xml.bind.*` imports + `javax.xml.bind:jaxb-api` dependency = one JAXB finding, not two).
- When merging is valid, apply:
  - Stronger severity (Critical > Warn > Suggestion)
  - Tag from the more specific source (`[MIGRATION]` wins over `[BASELINE]`)
  - One evidence snippet (or two snippets if needed)
  - One recommended fix (may include staged steps)

## Prioritization
Order findings:
1) Critical migration blockers (Java/Jakarta/deps)
2) Security/runtime correctness
3) Config/deployment risks
4) Suggestions

## Done Definition
- All scanning discipline rules from `code_scanner/SKILL.md` satisfied
- No repeated duplicated findings (merge rules applied)
- All other deliverables per task card DoD
