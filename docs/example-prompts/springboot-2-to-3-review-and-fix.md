# Example Prompt: Spring Boot 2 → 3 Review and Fix

Copy and paste the prompt below into your AI assistant to run a full Spring Boot 2 → 3
migration review followed by an automated fix pass.

**Before using:** replace the values marked with `← change this` for your project.

---

## Prompt

```
ROLE: Code Reviewer (Step 1) / Engineer (Step 2)

TASK:
Review branch `feature/sb2-to-sb3-broken-migration` ← change this
for Spring Boot 2 → 3 migration issues.
Then, after human confirmation, apply fixes based on the review output.

---

INPUTS:
- Skills/rules/templates repo: current working directory (cline-springboot-migration-demo) ← change this
- Target branch: feature/sb2-to-sb3-broken-migration  ← change this
- Build tool: Maven  ← change this if using Gradle

---

READ FIRST (in order):

| # | File                                                      | Role                     |
|---|-----------------------------------------------------------|--------------------------|
| 1 | ai/skills/springboot_migration/SKILL.md                   | Step 1 entry point       |
| 2 | ai/clinerules/ (all files)                                | Behavioral constraints   |
| 3 | ai/knowledge/spring-boot-3.0-migration-guide.md           | Migration reference [P0] |
| 4 | ai/knowledge/baeldung-spring-boot-3-migration.md          | Migration reference [P1] |
| 5 | ai/knowledge/severity_rubric.md                           | Severity definitions     |
| 6 | ai/templates/review_report_template.md                    | Report output format     |

---

## STEP 1 — Review

Follow `ai/skills/springboot_migration/SKILL.md` exactly.
Do NOT apply any fixes yet.

Stop and wait for confirmation before proceeding to Step 2.

---

## STEP 2 — Fix (only after Step 1 is confirmed)

Follow `ai/skills/springboot_migration/engineer.md` exactly.

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

> Step 1 defers to `springboot_migration/SKILL.md`, which composes `springboot_reviewer/SKILL.md` and
> `springboot_migration/checks.md`. Step 2 defers to `springboot_migration/engineer.md`, which internally composes
> `springboot_engineer/SKILL.md` and loads relevant references from
> `springboot_engineer/references/`. The prompt only adds what the skills don't know: target
> branch, build tool, and the two-step gate.

---

## How it works

| Section | Purpose |
|---|---|
| **ROLE** | Declares dual mode — reviewer for Step 1, engineer for Step 2. |
| **READ FIRST table** | Forces the agent to load the entry skill, composed skills, behavioral rules, and knowledge base before touching any source code. Order matters — entry skill first, constraints before knowledge. |
| **STEP 1 gate** | The agent must stop and surface the report before any file is changed. Prevents silent auto-fix without human review. |
| **STEP 2 fix order** | `Java → deps → code → config → batch → tests → runtime` — one commit per area so each fix is independently reviewable. |
| **Verification commands** | Hard pass/fail criteria. The agent cannot mark the task done until both commands succeed. |

---

## Adapting for Gradle

Replace the Maven verification commands:

```
- `./gradlew test` → all tests pass
- `./gradlew dependencies | rg "javax\."` → zero results
```

And update the build proof content accordingly:

```
- Save passing build output to: docs/evidence/reviewer_build_pass.md
  Content: full output of `./gradlew test`
```
