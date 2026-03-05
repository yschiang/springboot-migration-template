# AI Pipeline — Maintainer Guide

## Pipeline Diagram

```
                .clinerules/project.md          (auto-loaded by Cline)
                        |
                        v
               ai/TASKBOARD.md                  (route: scope -> task card)
                        |
                        v
               ai/tasks/<card>.md               (WHAT: Role, Goal, Checks, SkillRefs)
                        |
            +-----------+-----------+
            |                       |
            v                       v
   ai/skills/<skill>/SKILL.md  ai/BOOTSTRAP.md  (HOW + output contract)
```

## SSOT Responsibility Table

| Layer | Path | Responsibility |
|---|---|---|
| Entry router | `.clinerules/project.md` | Strict load sequence; SkillRefs are mandatory |
| Output contract | `ai/BOOTSTRAP.md` | THE one canonical output format |
| Routing | `ai/TASKBOARD.md` | Scope signal -> exactly one task card |
| Task cards | `ai/tasks/*` | Role, Goal, Scope, Checks, SkillRefs, DoD |
| Skills | `ai/skills/*/SKILL.md` | HOW: detailed checklists, procedures, patterns |
| Knowledge | `ai/knowledge/*` | Reference docs |
| Behavioral rules | `ai/clinerules/*` | Always-on constraints |
| Templates | `ai/templates/*` | Optional export formats (cannot override BOOTSTRAP) |

## Usage Examples

### Example 1 — Cline (auto-routing)

Just open the repo in Cline. It auto-loads `.clinerules/project.md`, which:
1. Reads `ai/TASKBOARD.md` and infers scope from your repo structure
2. Picks the right task card automatically
3. Loads all SkillRefs declared in the task card
4. Loads `ai/BOOTSTRAP.md` for output format
5. Executes — no setup required

### Example 2 — Claude Code / other agents (manual)

```
1. Copy ai/BOOTSTRAP.md
2. Copy one task card from ai/tasks/
3. Copy all files listed in the task card's SkillRefs: line
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
2. Fill in: Role, Goal, Scope, Checks (3-5 items), Evidence, SkillRefs
3. Add a routing rule to `ai/TASKBOARD.md`
4. Add it to the table above
5. Keep each task card under 80 lines

## Adding a New Skill

1. Create a directory under `ai/skills/` with a `SKILL.md` entry point
2. For composition, reference other skills via their `SKILL.md` path
3. Reference the skill from task card SkillRefs
4. Output must follow `ai/BOOTSTRAP.md` Standard Output Contract

## Directory Layout

```
ai/
├── BOOTSTRAP.md              <- THE one output contract (always loaded)
├── TASKBOARD.md              <- routing rules: scope -> task card
├── SSOT.md                   <- what belongs where (quick ref)
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
│   │   ├── SKILL.md          # SB2->3 migration engineer
│   │   ├── reviewer.md       # SB2->3 migration reviewer
│   │   └── checks.md         # 7-step migration checklist
│   ├── api_design/SKILL.md
│   ├── coding-standards/SKILL.md
│   ├── springboot_patterns/SKILL.md
│   ├── springboot_security/SKILL.md
│   ├── springboot_tdd/SKILL.md
│   └── springboot_verification/SKILL.md
├── knowledge/                <- reference docs
├── clinerules/               <- behavioral rules
└── templates/
    └── review_report_template.md
```
