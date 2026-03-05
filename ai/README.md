# AI — How to Use in 30 Seconds

Two files. Paste to agent. Done.

```
1. Copy ai/BOOTSTRAP.md
2. Copy one task card from ai/tasks/
3. Paste both to your agent (Claude Code, Cline, etc.)
```

The task card tells the agent **what** to do. `BOOTSTRAP.md` tells it **how** to behave and **what format** to output. No other setup required.

---

## Task Cards

| Task | File | Use when |
|---|---|---|
| Spring Boot 2→3 review or fix | `tasks/spring_boot_2_to_3_code_review.md` | Migrating a Java app to SB3 |
| Deployment YAML / CI review | `tasks/deployment_yaml_ci_review.md` | Reviewing k8s/Helm/Kustomize configs |
| Generic code review | `tasks/common_reviewer.md` | Any codebase, any language |

---

## Example 1 — Spring Boot 2→3 Reviewer

Copy and paste this to your agent:

```
[paste full content of ai/BOOTSTRAP.md here]

---

[paste full content of ai/tasks/spring_boot_2_to_3_code_review.md here]

---

Target repo: <path or branch>
Build tool: Maven
```

The agent will produce a structured report with CRITICAL/WARN/SUGGESTION findings, then stop.
Confirm before asking it to apply fixes (set `Role: submitter` in a follow-up).

---

## Example 2 — Deployment YAML / CI Reviewer

Copy and paste this to your agent:

```
[paste full content of ai/BOOTSTRAP.md here]

---

[paste full content of ai/tasks/deployment_yaml_ci_review.md here]

---

Target: <path to k8s/ or charts/ directory>
Environment: production
```

The agent will check Ingress pathType, probes, secrets hygiene, resource limits, and run `helm lint` / `kustomize build` validation.

---

## Directory Layout

```
ai/
├── BOOTSTRAP.md              ← universal working contract (always include)
├── README.md                 ← this file
├── tasks/                    ← task cards (pick one per run)
│   ├── spring_boot_2_to_3_code_review.md
│   ├── deployment_yaml_ci_review.md
│   └── common_reviewer.md
├── skills/                   ← optional deep-dive skills (loaded on demand)
│   ├── springboot_reviewer/
│   ├── springboot_engineer/
│   ├── springboot_patterns/
│   ├── springboot_security/
│   ├── springboot_tdd/
│   ├── springboot_verification/
│   ├── api_design/
│   └── coding-standards/
├── knowledge/                ← reference docs (P0/P1 priority)
│   ├── spring-boot-3.0-migration-guide.md  [P0]
│   ├── baeldung-spring-boot-3-migration.md [P1]
│   └── severity_rubric.md
├── clinerules/               ← Cline-specific behavioral rules
└── templates/
    └── review_report_template.md
```

Skills and knowledge are **optional** — the two mandatory files (`BOOTSTRAP.md` + task card) are self-contained.

---

## Adding a New Task Card

1. Copy `tasks/common_reviewer.md` as a starting point
2. Fill in the 6 fields: Role, Goal, Scope, Checks (≤ 5), Evidence, Constraints
3. Add it to the table above

Keep each task card under 100 lines. If it grows larger, extract reusable logic into a skill under `ai/skills/`.
