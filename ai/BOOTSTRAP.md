# BOOTSTRAP.md — Agent Working Contract

Paste this file + one task card from `ai/tasks/` to run any task.
The task card defines WHAT. This file defines HOW.

---

## Working Rules

These rules apply to every run, regardless of task.

| # | Rule | Detail |
|---|---|---|
| 1 | **Read before write** | Read every file in `Scope` before proposing any change. |
| 2 | **Evidence first** | Every finding must cite `file:line` + a code/config snippet. No assertion without evidence. |
| 3 | **Minimal diff** | Only change what the task explicitly requires. Do not refactor surrounding code. |
| 4 | **Scope boundary** | Do not read or modify files outside the declared `Scope`. If unsure, ask. |
| 5 | **One output** | Produce exactly one report or diff per run. No partial outputs, no second passes unless asked. |
| 6 | **Severity discipline** | CRITICAL = guaranteed break · WARN = likely break or behavior change · SUGGESTION = quality improvement. When uncertain, choose the higher level and explain why. |

---

## Standard Output Contract

Every run produces output in this exact format.

```
## Summary

| Severity   | Count |
|------------|-------|
| CRITICAL   | N     |
| WARN       | N     |
| SUGGESTION | N     |

**Verdict:** [GO | GO-with-fixes | NO-GO] — one sentence reason.

---

## Findings

### [CRITICAL] C1 — <title>

- **Symptom:** what is observed (be specific)
- **Why:** why this breaks or risks the system
- **Fix:** exactly what to change
- **Patch:**
  ```language
  // before
  // after
  ```
- **Evidence:** `path/to/file:line` — snippet

### [WARN] W1 — <title>
(same structure)

### [SUGGESTION] S1 — <title>
(same structure; Patch is optional)

---

## Evidence Log

Commands run and their output (truncated if long):

```shell
$ <command>
<output>
```
```

---

## Operator Instructions

**To run a task:**

1. Copy the full content of this file (`ai/BOOTSTRAP.md`)
2. Copy the full content of one task card from `ai/tasks/`
3. Paste both into your agent (Claude Code, Cline, etc.) as the system/context prompt
4. The agent will execute the task and produce output in the format above

**That's it. No other files are required.**

Optional: if the task card references skills under `ai/skills/`, load them too for richer guidance.

---

## Upgrade Path

This MVP (BOOTSTRAP + task card) scales to ~10 task cards without changes.

Introduce the next layer **only when you hit these triggers**:

| Trigger | Addition |
|---|---|
| 5+ task cards, hard to find the right one | Add a `ROUTER.md` — a decision table mapping problem type → task card |
| Reviewer spawns a fixer agent automatically | Add a `roles/` directory with agent-specific constraints |
| State must persist across multiple agent runs | Add a `session/` scratch directory for handoff notes |
| Org-wide consistency needed across many repos | Promote `BOOTSTRAP.md` to a shared package (npm, pip, or git submodule) |

Until then: resist the urge. Two files is enough.
