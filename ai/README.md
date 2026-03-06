# AI Pipeline — Maintainer Guide

## Pipeline Diagram

```
            .clinerules/project.md          (auto-loaded by Cline)
                    |
                    v
            routing table (inline)          (scope → task card)
                    |
                    v
           ai/tasks/<card>.md               (WHAT: Role, Goal, Checks, SkillRefs)
                    |
            +-------+-------+
            |               |
            v               v
   ai/skills/...    ai/clinerules/*         (HOW + behavioral rules)
            |
            v
   ai/templates/*                           (output format per task type)
```

## SSOT — What Belongs Where

| Layer | Path | Owns |
|---|---|---|
| Entry router | `.clinerules/project.md` | Load sequence, routing table, SkillRefs mandate, intent detection |
| Task cards | `ai/tasks/*` | WHAT: Role, Goal, Scope, acceptance criteria, DoD (deliverable + template) |
| Skills | `ai/skills/*` | HOW: detailed procedures, merge rules, composition |
| Knowledge | `ai/knowledge/*` | Reference docs (migration guides, rubrics, examples) |
| Behavioral rules | `ai/clinerules/*` | Always-on constraints (evidence, severity, scope, minimal diff) |
| Templates | `ai/templates/*` | Output format per task type (SSOT for report structure) |

**Rule:** Each layer adds only what's unique to it. Don't repeat rules from layers above.

## Usage Examples

### Example 1 — Cline (auto-routing)

Just open the repo in Cline. It auto-loads `.clinerules/project.md`, which:
1. Infers scope and selects the right task card from the inline routing table
2. Loads all SkillRefs declared in the task card
3. Loads `ai/clinerules/*` for behavioral rules
4. Executes — no setup required

### Example 2 — Claude Code / other agents (manual)

```
1. Copy one task card from ai/tasks/
2. Copy all files listed in the task card's SkillRefs: line
3. Copy all files in ai/clinerules/
4. Paste all to your agent
```

## Task Cards

| Task | File | Default Role |
|---|---|---|
| Spring Boot 2->3 review | `tasks/spring_boot_2_to_3_review.md` | `reviewer` |
| Spring Boot 2->3 fix | `tasks/spring_boot_2_to_3_fix.md` | `submitter` |
| Deployment YAML / CI review | `tasks/deployment_yaml_ci_review.md` | `ops` |
| Generic code review | `tasks/common_reviewer.md` | `reviewer` |

Role enums: `reviewer` (read-only) / `submitter` (apply fixes) / `ops` (infra review)

## Adding a New Task Card

1. Copy `tasks/_TEMPLATE.md`
2. Fill in: Role, Goal, Scope, Checks (acceptance criteria), SkillRefs, DoD
3. Add a routing rule to `.clinerules/project.md` routing table
4. Add it to the table above
5. Keep each task card under 80 lines

## Adding a New Skill

1. Create a directory under `ai/skills/` with a `SKILL.md` entry point
2. For composition, reference other skills via their `SKILL.md` path
3. Reference the skill from task card SkillRefs
4. Output format defined by the template referenced in the task card's DoD

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
    └── review_report_template.md
```
