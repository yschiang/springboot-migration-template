# Skill: Spring Boot 2 → 3 Reviewer (Extends Common Reviewer)

## Mission
Produce **one merged review report** that:
- Runs the **Common Reviewer** baseline
- Adds **Spring Boot 2 → 3 migration** specific checks
- Outputs **one unified report** (no duplicate sections)

## Composition
You MUST incorporate:
- `ai/skills/common_reviewer.md`
- `ai/skills/springboot_2_to_3_migration.md`

## Required Output Contract
Use **exactly** the format in `ai/templates/review_report_template.md`.

## Merge Rules
- If both skills produce similar findings, **merge into one** with:
  - Stronger severity (Critical > Warn > Suggestion)
  - One evidence snippet (or two snippets if needed)
  - One recommended fix (may include staged steps)

## Prioritization
Order findings:
1) Critical migration blockers (Java/Jakarta/deps)
2) Security/runtime correctness
3) Config/deployment risks
4) Suggestions

## Output
After completing the review, write the report to a Markdown file:
- Filename format: `review-report-<repo-name>-<YYYYMMDD>.md`
- Location: project root directory
- Format: follow `ai/templates/review_report_template.md`

## Done Definition
- Exactly one report
- No repeated duplicated findings
- Clear GO/GO-with-fixes/NO-GO decision
- Report written to a Markdown file as specified above
