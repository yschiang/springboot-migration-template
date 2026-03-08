# Example Prompt: Spring Boot 2 → 3 Review and Fix

## Quick Start

With routing enabled (Cline auto-loads `.clinerules/project.md`), just say:

```
Review this repo for Spring Boot 2→3 migration issues.
```

Or be explicit:

```
Run spring_boot_2_to_3_review
```

After the review report is confirmed, start fixes:

```
Fix the Spring Boot 2→3 migration issues.
```

Or:

```
Run spring_boot_2_to_3_fix
```

## How it works

The routing table in `.clinerules/project.md` detects intent from keywords (`migration`, `upgrade`, `2→3`, `Boot 3`) and loads the correct task card + full dependency chain automatically. No need to manually specify file paths or load orders.

| Step | Trigger | Task Card |
|------|---------|-----------|
| Review | keywords: migration/upgrade/review | `ai/tasks/spring_boot_2_to_3_review.md` |
| Fix | keywords: migration/upgrade + fix/apply | `ai/tasks/spring_boot_2_to_3_fix.md` |

## Gate

The reviewer stops after Pass 1 (scanned files log) and waits for operator confirmation before proceeding to Pass 2 (review report). No source files are modified during review.
