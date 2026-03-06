# Skill: Spring Boot 2 → 3 Reviewer (Extends Common Reviewer)

## Mission
Produce **one merged review report** that:
- Runs the **Common Reviewer** baseline
- Adds **Spring Boot 2 → 3 migration** specific checks
- Outputs **one unified report** (no duplicate sections)

## Composition
You MUST incorporate:
- `ai/skills/springboot_reviewer/SKILL.md`
- `ai/skills/springboot_migration/checks.md`

## Knowledge Base (must use)
Read in priority order. P0 precedes P1 in all reasoning and conflict resolution.
- **[P0]** `ai/knowledge/spring-boot-3.0-migration-guide.md` — official, authoritative
- **[P1]** `ai/knowledge/baeldung-spring-boot-3-migration.md` — supplementary, practical examples

### Known Conflicts Between Knowledge Sources
When the two sources disagree, apply these rules:
1. **Property name — prefer official**
   - Official: `spring.jpa.hibernate.use-new-id-generator-mappings` (correct, includes `-mappings`)
   - Baeldung: `spring.jpa.hibernate.use-new-id-generator` (incorrect, missing `-mappings`)
2. **Trailing slash matching — prefer official framing**
   - Official: the default value changed to `false` (still configurable)
   - Baeldung: describes the option as "deprecated" (imprecise)
   - The configuration option is NOT deprecated; only the default changed.

## Output Contract
Output MUST follow `ai/BOOTSTRAP.md` Standard Output Contract.
Optional: export to file using `ai/templates/review_report_template.md` when operator requests.

## Merge Rules
- **Every finding MUST include a source tag** — no finding may omit it:
  - `[MIGRATION]` — finding from SB2→3 migration checks (`checks.md`)
  - `[BASELINE]` — finding from generic reviewer checks (`springboot_reviewer/SKILL.md`)
- Header format: `#### [SEVERITY][SOURCE] ID — title`
  - Example: `#### [CRITICAL][MIGRATION] C1 — title` or `#### [WARN][BASELINE] W1 — title`
- If both skills produce similar findings, **merge into one** with:
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
- Exactly one report (English); optional zh translation per task card DoD
- No repeated duplicated findings
- Clear GO/GO-with-fixes/NO-GO decision
