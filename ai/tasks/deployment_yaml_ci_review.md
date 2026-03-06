# Task: Deployment YAML / CI Review

| Field | Value |
|---|---|
| **Role** | `ops` |
| **Goal** | Identify misconfigurations in k8s manifests, Helm charts, or Kustomize overlays that would cause failed deployments, probe failures, or routing bugs |
| **Constraints** | Read-only. Flag issues; do not apply changes unless explicitly asked. |

---

## Full Load Order

| # | File | Role |
|---|---|---|
| 1 | `ai/skills/springboot_verification/SKILL.md` | Skill entry (loads its own Dependencies) |
| 2 | `ai/templates/review_report_template.md` | Output format |

---

## DoD

- Write report using `ai/templates/review_report_template.md` as format
- Every finding includes the manifest path and offending YAML block
- Clear GO/GO-with-fixes/NO-GO verdict
