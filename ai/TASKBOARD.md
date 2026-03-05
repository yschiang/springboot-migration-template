# TASKBOARD — Task Routing

Pick **exactly one** task card based on what's in scope.

## Routing Rules

| Priority | Scope signal | Task card | Default Role |
|---|---|---|---|
| 1 | `src/`, `pom.xml`, `build.gradle` | `tasks/spring_boot_2_to_3_code_review.md` | `reviewer` |
| 2 | `k8s/`, `deploy/`, `charts/`, `helm/`, `*ingress*.yaml` | `tasks/deployment_yaml_ci_review.md` | `ops` |
| 3 | anything else | `tasks/common_reviewer.md` | `reviewer` |

## How to infer scope

1. Check changed files (`git diff --name-only`) if a branch/PR is specified.
2. Otherwise scan repo root for matching directories.
3. If multiple routes match, pick the **highest priority** (lowest number).

## Role override

The operator can override the default role in their prompt:
- `Role: submitter` — apply fixes (only for spring_boot task)
- `Role: ops` — infra/deployment review
- `Role: reviewer` — read-only analysis (default for most tasks)
