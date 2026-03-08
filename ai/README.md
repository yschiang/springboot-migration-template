# AI Pipeline — Maintainer Guide

## Pipeline Diagram

```
            .clinerules/project.md          (auto-loaded by Cline)
                    |
                    v
            routing table (inline)          (intent → task card)
                    |
                    v
           ai/tasks/<card>.md               (WHAT: Role, Goal, Full Load Order, DoD)
                    |
            +-------+-------+
            |               |
            v               v
   ai/skills/...    ai/clinerules/*         (HOW + behavioral rules)
       |        \
       v         v
 ai/knowledge/*  ai/templates/*            (reference docs + output format)
```

## SSOT — What Belongs Where

| Layer | Path | Owns |
|---|---|---|
| Entry router | `.clinerules/project.md` | Routing table, intent detection, load sequence (Full Load Order) |
| Task cards | `ai/tasks/*` | WHAT: Role, Goal, Constraints, Full Load Order, DoD |
| Skills | `ai/skills/*` | HOW: detailed procedures, merge rules, composition |
| Knowledge | `ai/knowledge/*` | Reference docs (migration guides, rubrics, examples) |
| Behavioral rules | `ai/clinerules/*` | Always-on constraints (evidence, severity, scope, minimal diff) |
| Templates | `ai/templates/*` | Output format per task type (SSOT for report structure) |

**Rule:** Each layer adds only what's unique to it. Don't repeat rules from layers above.

## Usage Examples

### Example 1 — Cline (auto-routing)

Just open the repo in Cline. It auto-loads `.clinerules/project.md`, which:
1. Infers intent and selects the right task card from the routing table
2. Loads all files in the task card's Full Load Order + their Dependencies
3. Loads `ai/clinerules/*` (behavioral rules)
4. Scans repo root and executes

### Example 2 — Claude Code / other agents (manual)

Each task card has a `## Full Load Order` table listing the skill entries and templates needed:

```
1. Read .clinerules/project.md and follow its instructions
2. Or: open a task card from ai/tasks/ directly
3. Load all files in its "Full Load Order" table
4. For each skill entry, also load its "Dependencies" table
5. Load all files in ai/clinerules/
```

Or use the ready-made prompt in `docs/example-prompts/springboot-2-to-3-review-and-fix.md`.

### How to invoke a task

**Direct invocation** — name the task explicitly:

```
Run spring_boot_2_to_3_review
Run spring_boot_2_to_3_fix
Run common_reviewer
```

**Intent-based routing** — the agent picks the task from keywords:

```
# Keywords: migration, upgrade, 2→3, sb3, Boot 3 → routes to SB2→3 review
Review this repo for Spring Boot 2→3 migration issues.

# Same keywords + fix/apply/implement → routes to SB2→3 fix
Fix the Spring Boot 2→3 migration issues.

# No migration keywords → routes to common reviewer
Review this repo.
```

### Specifying scan scope

By default the agent scans the entire repo root. Add a target to narrow scope:

```
# Full repo (default)
Run spring_boot_2_to_3_review

# Specific path
Run spring_boot_2_to_3_review. Target: src/main/

# Intent-based + narrowed scope
Review modules/user-service/ for Spring Boot 2→3 migration issues.
```

## Task Cards

| Task | File | Default Role |
|---|---|---|
| Spring Boot 2->3 review | `tasks/spring_boot_2_to_3_review.md` | `reviewer` |
| Spring Boot 2->3 fix | `tasks/spring_boot_2_to_3_fix.md` | `submitter` |
| Deployment YAML / CI review | `tasks/deployment_yaml_ci_review.md` | `ops` |
| Generic code review | `tasks/common_reviewer.md` | `reviewer` |

Role enums: `reviewer` (read-only) / `submitter` (apply fixes) / `ops` (infra review)

## Migration Reviewer — Tool Spec

### What it does
Automated code review tool that identifies all blockers preventing a Spring Boot 2.x app from running on Spring Boot 3.x. Produces a structured, actionable report in one pass (scan + review).

### Architecture
```
Task Card (spring_boot_2_to_3_review.md)
  └─ Skill: springboot_migration/SKILL.md (2-pass reviewer)
       ├─ Composed: code_scanner/SKILL.md      (scan discipline + methodology)
       ├─ Composed: springboot_reviewer/SKILL.md (baseline code quality)
       ├─ Composed: springboot_migration/checks.md (8-section pattern registry)
       ├─ Knowledge: spring-boot-3.0-migration-guide.md [P0]
       ├─ Knowledge: baeldung-spring-boot-3-migration.md [P1]
       └─ Knowledge: severity_rubric.md
```

### 2-Pass Process
| Pass | Action | Output |
|------|--------|--------|
| **Pass 1 — Discovery** | Enumerate files, build manifest | `review-scanned-<repo>-<YYYYMMDD>.md` |
| *(operator gate)* | Operator confirms/adjusts scope | — |
| **Pass 2 — Review** | Run pattern registry + baseline checks against manifest | `review-report-<repo>-<YYYYMMDD>-zh.md` |

### Key Constraints
- **Read-only** — does not modify source files
- **Built-in tools only** — all actions (search, read, write, count) use the AI tool's built-in capabilities; no shell scripts, no `wc -l`, no `grep` piping
- **Cross-platform** — forward slashes for all paths in output, no OS-specific commands in scanning logic
- **Pattern-driven** — every check comes from `checks.md` §1–§8 or knowledge source cross-reference; no ad-hoc checks without traceability

### Discipline Rules (from code_scanner)
| Rule | Summary |
|------|---------|
| D1 | Every pattern match → a finding (no silent skips) |
| D2 | Exhaustive file listing in every finding's Where section |
| D3 | Severity from rubric, not reviewer judgment |
| D4 | One finding per distinct root cause |

### Severity Levels
| Level | Meaning | Gate |
|-------|---------|------|
| Critical | Migration blocker or guaranteed runtime/build break | NO-GO |
| Warn | Behavior change risk needing validation | GO-with-fixes |
| Suggestion | Quality improvement while touching code | GO |

### Output Artifacts
| File | Content |
|------|---------|
| `review-scanned-*.md` | Module structure + scope verification (+ full file table if ≤ 100 files) |
| `review-report-*-zh.md` | Full review report: findings, priority plan, verification checklist |

## Adding a New Task Card

1. Copy `tasks/_TEMPLATE.md`
2. Fill in: Role, Goal, Constraints, DoD
3. Build the `Full Load Order` table: skill entry + its `## Dependencies` + `ai/clinerules/*` + template
4. Add a routing rule to `.clinerules/project.md` routing table
5. Add it to the table above

## Adding a New Skill

1. Create a directory under `ai/skills/` with a `SKILL.md` entry point
2. Add a `## Dependencies` table listing all composed modules and knowledge files
3. For composition, reference other skills via their `SKILL.md` path
4. Reference the skill from the task card's Full Load Order
5. Update the task card's `Full Load Order` table to include the new dependencies
6. Output format defined by the template referenced in the task card's DoD

## Upgrade Path

This MVP (task cards + skills + clinerules) scales to ~10 task cards without changes.

Introduce the next layer **only when you hit these triggers**:

| Trigger | Addition |
|---|---|
| Reviewer spawns a fixer agent automatically | Add a `roles/` directory with agent-specific constraints |
| State must persist across multiple agent runs | Add a `session/` scratch directory for handoff notes |
| Org-wide consistency needed across many repos | Promote clinerules to a shared package (npm, pip, or git submodule) |

Until then: resist the urge.

## Directory Layout

```
ai/
├── README.md                 <- this file
├── tasks/                    <- task cards (one per run)
│   ├── _TEMPLATE.md
│   ├── spring_boot_2_to_3_review.md
│   ├── spring_boot_2_to_3_fix.md
│   ├── common_reviewer.md
│   └── deployment_yaml_ci_review.md
├── skills/                   <- detailed checklists and procedures
│   ├── code_scanner/
│   │   └── SKILL.md          # generic scan discipline & methodology (composed)
│   ├── springboot_reviewer/
│   │   └── SKILL.md          # baseline code review
│   ├── springboot_engineer/
│   │   ├── SKILL.md          # Spring Boot 3.x engineer
│   │   └── references/       # on-demand: web, data, security, cloud, testing
│   ├── springboot_migration/
│   │   ├── SKILL.md          # SB2->3 migration reviewer (entry)
│   │   ├── engineer.md       # SB2->3 migration engineer (fix entry)
│   │   └── checks.md         # 7-step migration checklist
│   ├── api_design/SKILL.md
│   ├── coding-standards/SKILL.md
│   ├── springboot_patterns/SKILL.md
│   ├── springboot_security/SKILL.md
│   ├── springboot_tdd/SKILL.md
│   └── springboot_verification/SKILL.md
├── knowledge/                <- reference docs
├── clinerules/               <- behavioral rules (always loaded)
│   ├── 01_read_before_write.md
│   ├── 02_evidence_first.md
│   ├── 03_severity.md
│   ├── 04_no_fluff.md
│   ├── 05_minimal_diff.md
│   ├── 06_spring_migration_focus.md
│   ├── 07_one_output.md
│   ├── coding-style.md
│   └── security.md
└── templates/
    ├── review_report_template.md
    └── review_scanned_template.md
```
