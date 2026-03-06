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
| 1 | `ai/skills/springboot_reviewer/SKILL.md` | Composed module — generic review baseline |
| 2 | `ai/skills/springboot_migration/checks.md` | Composed module — SB2→3 migration checklist |
| 3 | `ai/knowledge/spring-boot-3.0-migration-guide.md` | Knowledge [P0] — official, authoritative |
| 4 | `ai/knowledge/baeldung-spring-boot-3-migration.md` | Knowledge [P1] — supplementary examples |

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
- No repeated duplicated findings (merge rules applied)
- All other deliverables per task card DoD
