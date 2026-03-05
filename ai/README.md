# AI — How to Use in 30 Seconds

## Cline (auto-routing)

Just open the repo in Cline. It auto-loads `.clinerules/project.md`, which:
1. Reads `ai/TASKBOARD.md` and infers scope from your repo structure
2. Picks the right task card automatically
3. Loads `ai/BOOTSTRAP.md` for output format
4. Executes — no setup required

## Claude Code / other agents (manual)

```
1. Copy ai/BOOTSTRAP.md
2. Copy one task card from ai/tasks/
3. Paste both to your agent
```

---

## Task Cards

| Task | File | Default Role |
|---|---|---|
| Spring Boot 2→3 review or fix | `tasks/spring_boot_2_to_3_code_review.md` | `reviewer` |
| Deployment YAML / CI review | `tasks/deployment_yaml_ci_review.md` | `ops` |
| Generic code review | `tasks/common_reviewer.md` | `reviewer` |

Role enums: `reviewer` (read-only) · `submitter` (apply fixes) · `ops` (infra review)

---

## Example 1 — Review src/ for Spring Boot migration

```
[paste ai/BOOTSTRAP.md]

---

[paste ai/tasks/spring_boot_2_to_3_code_review.md]

---

Target: src/
Build tool: Maven
```

Output: structured report with CRITICAL/WARN/SUGGESTION. Set `Role: submitter` in follow-up to apply fixes.

---

## Example 2 — Ops review for charts/

```
[paste ai/BOOTSTRAP.md]

---

[paste ai/tasks/deployment_yaml_ci_review.md]

---

Target: charts/
Environment: production
```

Output: Ingress pathType, probes, secrets hygiene, resource limits, helm lint results.

---

## Adding a New Task Card

1. Copy `tasks/_TEMPLATE.md`
2. Fill in: Role, Goal, Scope, Checks (≤ 5), Evidence
3. Add a routing rule to `ai/TASKBOARD.md`
4. Add it to the table above

Keep each task card under 80 lines.

---

## Directory Layout

```
ai/
├── BOOTSTRAP.md              ← working contract + output format (always loaded)
├── TASKBOARD.md              ← routing rules: scope → task card
├── README.md                 ← this file
├── tasks/                    ← task cards (one per run)
│   ├── _TEMPLATE.md          #   starting point for new tasks
│   ├── spring_boot_2_to_3_code_review.md
│   ├── deployment_yaml_ci_review.md
│   └── common_reviewer.md
├── skills/                   ← optional deep-dive skills (loaded on demand)
├── knowledge/                ← reference docs (P0/P1 priority)
├── clinerules/               ← behavioral rules
└── templates/
    └── review_report_template.md

.clinerules/
└── project.md                ← Cline entry point (auto-route → BOOTSTRAP → task)
```
