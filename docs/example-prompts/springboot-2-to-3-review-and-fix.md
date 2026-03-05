# Example Prompt: Spring Boot 2 → 3 Review and Fix

Copy and paste the prompt below into your AI assistant to run a full Spring Boot 2 → 3
migration review followed by an automated fix pass.

**Before using:** replace the values marked with `← change this` for your project.

---

## Prompt

```
ROLE: Code Reviewer

TASK:
Review branch `feature/sb2-to-sb3-broken-migration` ← change this
for Spring Boot 2 → 3 migration issues,
then in a second step apply fixes based on the review output.

---

INPUTS:
- Skills/rules/templates repo: current working directory (cline-springboot-migration-demo) ← change this
- Target branch: feature/sb2-to-sb3-broken-migration  ← change this
- Build tool: Maven  ← change this if using Gradle

---

READ FIRST (in order):

| # | File                                                     | Role                    |
|---|----------------------------------------------------------|-------------------------|
| 1 | ai/skills/sb3_reviewer.md  | Entry point skill       |
| 2 | ai/skills/common_reviewer.md                             | Compose baseline skill  |
| 3 | ai/skills/sb3_migration_reviewer.md                 | Composed migration skill|
| 4 | ai/clinerules/ (all 6 files)                             | Behavioral constraints  |
| 5 | ai/knowledge/spring-boot-3.0-migration-guide.md          | Migration reference [P0]|
| 6 | ai/knowledge/baeldung-spring-boot-3-migration.md         | Migration reference [P1]|
| 7 | ai/knowledge/severity_rubric.md                          | Severity definitions    |
| 8 | ai/templates/review_report_template.md                   | Report output format    |

---

## STEP 1 — Review

Follow `ai/skills/sb3_reviewer.md` exactly.
Do NOT apply any fixes yet.

Stop and wait for confirmation before proceeding to Step 2.

---

## STEP 2 — Fix (only after Step 1 is confirmed)

Follow `ai/skills/sb3_engineer.md` exactly.

Additional files to load for Step 2:

| # | File                                                              | Role                         |
|---|-------------------------------------------------------------------|------------------------------|
| 1 | ai/skills/sb3_engineer.md                | Entry point fix skill        |
| 2 | ai/skills/springboot_engineer/SKILL.md                      | Base engineer role           |
| 3 | ai/skills/springboot_engineer/references/ (load as needed)  | Web / Data / Security / Test |
| 4 | ai/knowledge/spring-boot-3.0-migration-guide.md                  | Fix reference [P0]           |
| 5 | ai/knowledge/baeldung-spring-boot-3-migration.md                 | Fix reference [P1]           |

Output:
- Branch: fix/sb3-migration  ← change this if desired
- Commit each fix area separately with a descriptive message.
- Save passing build output to: docs/evidence/reviewer_build_pass.md
  Content: full output of `mvn -q -DskipTests=false test`

Verification (must pass before done):
- `mvn -q -DskipTests=false test` → all tests pass
- `mvn -q dependency:tree | rg "javax\."` → zero results
  (if any remain, document why they are safe)

---

DELIVERABLES:
- Step 1: review report (as defined by the skill)
- Step 2: docs/evidence/reviewer_build_pass.md + branch fix/sb3-migration
```

> The prompt deliberately keeps Step 1 minimal — the skill owns the output path, filename format,
> and template reference. The prompt only adds what the skill doesn't know: the target branch,
> build tool, and the two-step gate.

---

## How it works

| Section | Purpose |
|---------|---------|
| **ROLE** | Sets the agent's mode to code reviewer, not developer. |
| **READ FIRST table** | Forces the agent to load skills, rules, knowledge base, and report template before touching any source code. Order matters — entry skill first, constraints before knowledge. |
| **STEP 1 gate** | The agent must stop and surface the report before any file is changed. Prevents silent auto-fix without human review. |
| **STEP 2 fix order** | `Java → deps → code → config → tests` maps to commit granularity — one commit per area so each fix is independently reviewable. |
| **Verification commands** | Hard pass/fail criteria. The agent cannot mark the task done until both commands succeed. |

## Adapting for Gradle

Replace the Maven verification commands:

```
- `./gradlew test` → all tests pass
- `./gradlew dependencies | rg "javax\."` → zero results
```

And update the build output path accordingly:

```
- Save passing build output to: docs/evidence/reviewer_build_pass.md
  Content: full output of `./gradlew test`
```
