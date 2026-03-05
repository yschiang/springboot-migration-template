# Cline Project Rules

This file is auto-loaded by Cline on every session.

## Step 0 — Route to a task

1. Read `ai/TASKBOARD.md`.
2. Infer scope from changed files (`git diff --name-only`) or repo directory structure.
3. Select **exactly one** task card. Do not ask the user to choose — pick the best match.
4. If unclear, pick the lowest-risk option (prefer `common_reviewer.md`).

## Step 1 — Load the contract

Read `ai/BOOTSTRAP.md`. This defines working rules, severity levels, and output format.

## Step 2 — Execute

1. Read every file listed in the task card's **Scope**.
2. Run **Checks** in order. Cite `file:line` + snippet for every finding.
3. Produce output that follows the **Standard Output Contract** from BOOTSTRAP.md exactly.
4. Do NOT modify files unless Role is `submitter`.
5. If Role is `reviewer` or `ops`: stop after producing the report.

## Constraints

- Never self-identify or announce your role. Just execute.
- Stay within declared Scope. Do not touch files outside it.
- When uncertain between two severity levels, choose the higher one.
- Load optional skills from `ai/skills/` only if referenced by the task card.
