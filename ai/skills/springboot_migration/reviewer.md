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

## Output Contract
Output MUST follow `ai/BOOTSTRAP.md` Standard Output Contract.
Optional: export to file using `ai/templates/review_report_template.md` when operator requests.

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

## Done Definition
- Exactly one report
- No repeated duplicated findings
- Clear GO/GO-with-fixes/NO-GO decision
