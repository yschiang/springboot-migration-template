# Task: Deployment YAML / CI Review

| Field | Value |
|---|---|
| **Role** | `ops` |
| **Goal** | Identify misconfigurations in k8s manifests, Helm charts, or Kustomize overlays that would cause failed deployments, probe failures, or routing bugs |
| **Scope** | `k8s/`, `deploy/`, `charts/`, `helm/`, `.github/`, `*deployment*.yaml`, `*ingress*.yaml`, `*values*.yaml` |
| **Constraints** | Read-only. Flag issues; do not apply changes unless explicitly asked. |

---

## Checks

### C1 — Ingress `pathType` and `//` URL normalization
- Every Ingress rule must have `pathType: Prefix` or `pathType: Exact` — never omitted
- nginx ingress does **not** normalize `//` → upstream receives `//path` literally
- **CRITICAL** if `pathType` missing; **WARN** if `//` in path rules

### C2 — Liveness and Readiness probes
- Every Deployment/StatefulSet container must define both probes
- `initialDelaySeconds` ≥ app startup time; `failureThreshold` ≥ 3
- Spring Boot: prefer `/actuator/health/liveness` and `/actuator/health/readiness`
- **WARN** for missing probes; **CRITICAL** if probe path returns non-2xx on healthy pod

### C3 — Resource limits and requests
- Every container must declare `resources.requests` and `resources.limits` for CPU and memory
- **WARN** if missing; **SUGGESTION** if limits are unreasonably high

### C4 — Env / ConfigMap / Secret hygiene
- `grep -r "value:.*password\|value:.*secret\|value:.*token" k8s/ charts/ helm/ deploy/`
- Hardcoded secrets: **CRITICAL** — must use `secretKeyRef`
- Missing ConfigMap/Secret cross-references: **WARN**

### C5 — Helm template / Kustomize build validation
- `helm template . --values values.yaml` must produce valid YAML
- `helm lint .` must pass; `kustomize build overlays/<env>` must succeed
- Image tags = `latest` in production: **WARN**; template render errors: **CRITICAL**

---

## Evidence

- Each finding: manifest file path + offending YAML block (≤ 15 lines)
- Validation: run **one** of `helm template .`, `kustomize build overlays/prod`, or `kubectl apply --dry-run=client -f k8s/`

---

## SkillRefs

<!-- TODO: add a dedicated k8s/helm/kustomize review skill when one exists -->
SkillRefs: ai/skills/springboot_verification/SKILL.md
