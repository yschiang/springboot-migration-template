# Cline Project Rules

This file is auto-loaded by Cline on every session.

## Step 0 — Route to a task

Select **exactly one** task card. Do not ask the user to choose — pick the best match.

| Priority | Signal | Task card | Role |
|---|---|---|---|
| 0 | Operator names a task directly (e.g. "run spring_boot_2_to_3_review") | named task | as declared |
| 1a | Operator mentions migration/upgrade/2→3/sb3/Boot 3 keywords + review (or default) | `tasks/spring_boot_2_to_3_review.md` | `reviewer` |
| 1b | Same keywords + fix/apply/implement | `tasks/spring_boot_2_to_3_fix.md` | `submitter` |
| 2 | `k8s/`, `deploy/`, `charts/`, `helm/`, `*ingress*.yaml` exist in repo | `tasks/deployment_yaml_ci_review.md` | `ops` |
| 3 | default | `tasks/common_reviewer.md` | `reviewer` |

- Priority 0 wins unconditionally. Otherwise pick highest priority (lowest number).
- If unclear: default to `tasks/common_reviewer.md`.

## Step 1 — Load

1. Read every file in the task card's `## Full Load Order` table, in order.
2. For each skill entry, also read every file in its `## Dependencies` table.
3. Read every file in `ai/clinerules/` (behavioral rules — always loaded).

## Step 2 — Execute

1. Scan the target repo as directed by the skill procedure. Default target: repo root (`.`). Operator may narrow scope in their prompt.
2. Produce output per the task card's **DoD**.
3. Do NOT modify files unless Role is `submitter`.
4. If Role is `reviewer` or `ops`: stop after producing the report.

## Constraints

- Never self-identify or announce your role. Just execute.
- If unsure: infer from repo conventions; proceed with lowest-risk option; ask only if blocked.
