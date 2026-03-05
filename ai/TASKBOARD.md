# TASKBOARD — Task Routing

Pick **exactly one** task card based on what's in scope.

## Routing Rules

| Priority | Scope signal | Task card | Default Role |
|---|---|---|---|
| 1a | `src/`, `pom.xml`, `build.gradle` + operator says "review" or default | `tasks/spring_boot_2_to_3_review.md` | `reviewer` |
| 1b | `src/`, `pom.xml`, `build.gradle` + operator says "fix" or "apply" | `tasks/spring_boot_2_to_3_fix.md` | `submitter` |
| 2 | `k8s/`, `deploy/`, `charts/`, `helm/`, `*ingress*.yaml` | `tasks/deployment_yaml_ci_review.md` | `ops` |
| 3 | anything else | `tasks/common_reviewer.md` | `reviewer` |

## How to infer scope

1. Check changed files (`git diff --name-only`) if a branch/PR is specified.
2. Otherwise scan repo root for matching directories.
3. If multiple routes match, pick the **highest priority** (lowest number).
4. For priority 1: default to **1a** (review) unless the operator explicitly requests fixes.
