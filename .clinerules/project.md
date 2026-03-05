# Cline Project Rules

This file is auto-loaded by Cline on every session.

## Step 0 — Route to a task

1. Read `ai/TASKBOARD.md`.
2. Infer scope from changed files (`git diff --name-only`) or repo directory structure.
3. Select **exactly one** task card. Do not ask the user to choose — pick the best match.
4. If multiple routes match, pick the **highest priority** (lowest number).
5. If unclear: infer from repo conventions; proceed with lowest-risk option (prefer `tasks/common_reviewer.md`).

## Step 1 — Load SkillRefs

Parse the selected task card's `SkillRefs:` line as a **comma-separated list of file paths**.
SkillRefs are **REQUIRED, not optional**. Read every file listed before executing.

## Step 2 — Load behavioral rules

Read every file in `ai/clinerules/`. These are always-on constraints (evidence, severity, security, etc.).

## Step 3 — Load the contract

Read `ai/BOOTSTRAP.md`. This is the ONLY canonical output contract.

## Step 4 — Execute

1. Read every file listed in the task card's **Scope**.
2. Run **Checks** in order. Cite `file:line` + snippet for every finding.
3. Produce output that follows the **Standard Output Contract** from BOOTSTRAP.md exactly.
4. Do NOT modify files unless Role is `submitter`.
5. If Role is `reviewer` or `ops`: stop after producing the report.

## Constraints

- Never self-identify or announce your role. Just execute.
- Stay within declared Scope. Do not touch files outside it.
- When uncertain between two severity levels, choose the higher one.
- If unsure: infer from repo conventions; proceed with lowest-risk option; ask only if blocked.
