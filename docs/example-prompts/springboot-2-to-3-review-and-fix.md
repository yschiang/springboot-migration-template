# Example Prompt: Spring Boot 2 → 3 Review and Fix

Copy and paste the prompt below into your AI assistant to run a full Spring Boot 2 → 3
migration review followed by an automated fix pass.

**Before using:** replace the values marked with `<- change this` for your project.

---

## Prompt

```
TASK: Spring Boot 2 → 3 migration review, then fix.

INPUTS:
- Target repo: /path/to/your/repo               <- change this
- Target branch: feature/sb2-to-sb3-migration    <- change this
- Build tool: Maven                              <- change this if Gradle

---

STEP 1 — Review

Read and execute: ai/tasks/spring_boot_2_to_3_review.md

Load all files listed in the task card's "Full Load Order" table.
Follow the skill procedure. Do NOT apply any fixes yet.

Stop and wait for confirmation before proceeding to Step 2.

---

STEP 2 — Fix (only after Step 1 is confirmed)

Read and execute: ai/tasks/spring_boot_2_to_3_fix.md

Load all files listed in the task card's "Full Load Order" table.
Follow the skill procedure.

Output:
- Branch: fix/sb3-migration                      <- change this if desired
- Commit each fix area separately with a descriptive message.

Verification (must pass before done):
- `mvn -q -DskipTests=false test` → all tests pass
- `mvn -q dependency:tree | rg "javax\."` → zero results

---

DELIVERABLES:
- Step 1: review report (filename per task card DoD)
- Step 2: fix branch with passing build
```

---

## How it works

| Section | Purpose |
|---|---|
| **STEP 1** | References the review task card directly. The task card's `Full Load Order` table lists every file the agent needs — no guessing. |
| **STEP 2** | References the fix task card. Same principle — `Full Load Order` is the complete manifest. |
| **Gate** | The agent must stop after Step 1 and surface the report before any file is changed. |
| **Verification** | Hard pass/fail criteria. The agent cannot mark the task done until both commands succeed. |

> The prompt itself contains NO procedure, severity rules, or output format.
> All of that lives in the task cards and their Full Load Order (single source of truth).

---

## Adapting for Gradle

Replace the Maven verification commands:

```
- `./gradlew test` → all tests pass
- `./gradlew dependencies | rg "javax\."` → zero results
```
