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

Follow the scan scope and search execution rules from `code_scanner/SKILL.md`.

#### Output contract

Write `review-scanned-<repo>-<YYYYMMDD>.md` per `ai/templates/review_scanned_template.md`.
The file MUST contain these sections:

| Section | Required | Content |
|---|---|---|
| **Header table** | Always | Date, Total Files, Type Counts |
| **Module Structure** | Always | Table of modules with file counts per type (single-module = one row) |
| **Scope Verification** | Always | Glob patterns used and their result counts |
| **Files** | ≤ 100 files only | Numbered table — every scanned file with path and type |

For repos with > 100 files, the **Files** section is omitted — Module Structure + Scope Verification provide sufficient coverage for operator confirmation.

Scope is defined in `ai/tools/scan_scope.py` (SSOT). Do not duplicate scope rules here.

#### Steps

Run the scope scanner tool to produce the manifest:

```
python ai/tools/scan_scope.py <target_dir> -o review-scanned-<repo>-<YYYYMMDD>.md
```

This handles enumeration, classification, module detection, tiered output (≤100 / >100), and scope verification in one deterministic step. Read the output file and proceed to the validation gate.

#### Validation gate

After writing the file:
1. **Read** `review-scanned-<repo>-<YYYYMMDD>.md`.
2. **Verify** ALL of:
   - `# Scanned Files` header exists
   - `## Module Structure` table has ≥ 1 data row
   - `## Scope Verification` table has ≥ 1 glob pattern
   - Module Structure Total row sum = Header Total Files
3. If any check fails → regenerate. Do NOT proceed with an empty or placeholder file.
4. **STOP and present to operator. Wait for confirmation before Pass 2.**
   - Operator may adjust scope (add/remove files) before confirming.

### Pass 2 — Review

**Gate:** Read `review-scanned-<repo>-<YYYYMMDD>.md`. If it is empty or missing the `## Module Structure` table, STOP — go back and complete Pass 1 first. Never proceed with an empty scanned files log.

1. **Read the scanned manifest** (`review-scanned-<repo>-<YYYYMMDD>.md`) — it contains:
   - **Build Profile:** Spring Boot version, Java version, build tool — use these for §1–§2 checks (no need to re-parse build files).
   - **Technology Signals:** pre-detected migration-relevant dependencies and code patterns — use as a checklist for §3–§4 (every signal listed MUST produce a finding or explicit N/A).
   - **Module Structure / Files:** defines the scope for all searches.
2. **Run migration checks** — for each section in `checks.md` §1–§8:
   a. **§1–§3 (build/deps):** Use Build Profile + Technology Signals from the manifest. Cross-check against `pom.xml` / `build.gradle` only if manifest data is insufficient.
   b. **§4/§5/§6/§8 (scan-tool-covered patterns):** The manifest's **Pattern Scan Results** already contains all hits with file:line. Do NOT re-run these searches. For each pattern with ≥ 1 match: **read 1–2 matched files** to verify context (not a comment, not a false positive), confirm severity, and gather evidence snippets for the finding. List ALL affected files from the manifest in the finding's Where section.
   c. **§7 (packaging):** Check the manifest's Build Profile for WAR packaging; if present, read deployment config to verify container compatibility.
   d. Do NOT skip any section. The agent MAY run additional searches beyond the pattern registry if knowledge sources or context suggest uncovered issues.
3. **Run baseline checks** from `springboot_reviewer/SKILL.md` within the confirmed scope.
4. Run the **Completeness Self-Check** from `code_scanner/SKILL.md`:
   - Apply to `checks.md` §1–§8 as the migration pattern registry.
   - Apply to `springboot_reviewer/SKILL.md` code quality categories (§3: error handling, resource management, config validation, logging, security). For each category, record at least one finding or explicit "N/A — reviewed, no issues found."
   - Complete the **Coverage tracker** (item 6) — all sections must be `[x]` or `[-]`.
5. The report's **Files Scanned** count in the Overview table MUST equal the scanned log's Header **Total Files**. If mismatch, reconcile before finalizing.
6. Write the review report per task card DoD.

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
