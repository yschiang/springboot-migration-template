# Cline Project Rules

This file is auto-loaded by Cline on every session.

## Step 0 — Route to a task

Infer scope from changed files (`git diff --name-only`) or repo directory structure.
Determine **intent**: default is `review`. Switch to `fix` only when the operator explicitly uses words like "fix", "apply", "implement", or "migrate".

Select **exactly one** task card using the routing table below. Do not ask the user to choose — pick the best match.

| Priority | Scope signal | Task card | Default Role |
|---|---|---|---|
| 1a | `src/`, `pom.xml`, `build.gradle` + review (or default) | `tasks/spring_boot_2_to_3_review.md` | `reviewer` |
| 1b | `src/`, `pom.xml`, `build.gradle` + fix/apply | `tasks/spring_boot_2_to_3_fix.md` | `submitter` |
| 2 | `k8s/`, `deploy/`, `charts/`, `helm/`, `*ingress*.yaml` | `tasks/deployment_yaml_ci_review.md` | `ops` |
| 3 | anything else | `tasks/common_reviewer.md` | `reviewer` |

- If multiple routes match, pick the **highest priority** (lowest number).
- If unclear: infer from repo conventions; proceed with lowest-risk option (prefer `tasks/common_reviewer.md`).

## Step 1 — Load SkillRefs

Parse the selected task card's `SkillRefs:` line as a **comma-separated list of file paths**.
SkillRefs are **REQUIRED, not optional**. Read every file listed before executing.

## Step 2 — Load behavioral rules

Read every file in `ai/clinerules/`. These are always-on constraints.

## Step 3 — Execute

1. Read every file listed in the task card's **Scope**.
2. Run **Checks** using the procedure defined in SkillRefs.
3. Produce output per the template referenced in the task card's **DoD**.
4. Do NOT modify files unless Role is `submitter`.
5. If Role is `reviewer` or `ops`: stop after producing the report.

## Constraints

- Never self-identify or announce your role. Just execute.
- If unsure: infer from repo conventions; proceed with lowest-risk option; ask only if blocked.
