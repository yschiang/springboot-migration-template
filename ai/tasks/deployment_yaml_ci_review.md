# Task: Deployment YAML / CI Review

| Field | Value |
|---|---|
| **Role** | `reviewer` |
| **Goal** | Identify misconfigurations in k8s manifests, Helm charts, or Kustomize overlays that would cause failed deployments, probe failures, or routing bugs |
| **Scope** | `k8s/`, `deploy/`, `charts/`, `helm/`, `.github/`, any `*deployment*.yaml`, `*ingress*.yaml`, `*values*.yaml` found in repo root |
| **Constraints** | Read-only. Flag issues; do not apply changes unless explicitly asked. |

---

## Checks (run in order)

### C1 — Ingress `pathType` and `//` URL normalization
- Every Ingress rule must have `pathType: Prefix` or `pathType: Exact` — never omitted or `ImplementationSpecific`
- Check if any path ends with `/` or uses `//`: nginx ingress does **not** normalize `//` → upstream app receives `//path` literally
- Grep: `grep -r "pathType\|path:" k8s/ charts/ helm/ deploy/`
- **Flag CRITICAL** if `pathType` missing; **WARN** if trailing slash or `//` in path rules

### C2 — Liveness and Readiness probes
- Every `Deployment`/`StatefulSet` container must define both `livenessProbe` and `readinessProbe`
- Check `initialDelaySeconds` is adequate (≥ app startup time); `failureThreshold` ≥ 3
- Spring Boot apps: prefer `/actuator/health/liveness` and `/actuator/health/readiness` (requires `management.endpoint.health.probes.enabled=true`)
- **Flag WARN** for missing probes; **CRITICAL** if liveness probe path returns non-2xx on healthy pod

### C3 — Resource limits and requests
- Every container must declare `resources.requests` and `resources.limits` for CPU and memory
- Limits without requests = Burstable class (can be evicted under pressure)
- `memory.limits` should be ≥ `memory.requests`; avoid `cpu.limits` unless latency-sensitive
- **Flag WARN** if requests/limits missing; **SUGGESTION** if limits are unreasonably high

### C4 — Env / ConfigMap / Secret hygiene
- Grep: `grep -r "value:.*password\|value:.*secret\|value:.*token\|value:.*key" k8s/ charts/ helm/ deploy/`
- Hardcoded secrets in `env.value` fields are **CRITICAL** — must use `secretKeyRef`
- ConfigMap keys referenced via `configMapKeyRef` — verify the ConfigMap name matches what is deployed
- Check for `$(VAR)` substitution chains that may silently fail
- **Flag CRITICAL** for hardcoded secrets; **WARN** for missing ConfigMap/Secret cross-references

### C5 — Helm template / Kustomize build validation
- If Helm: run `helm template . --values values.yaml` — must produce valid YAML with no template errors
- If Kustomize: run `kustomize build overlays/<env>` — must produce valid YAML
- Check `helm lint .` passes with zero errors
- Verify image tags are not `latest` in production values
- **Flag CRITICAL** for template render errors; **WARN** for `latest` image tags

---

## Evidence Requirements

**Output must include:**
- For each finding: the manifest file path + the offending YAML block (≤ 15 lines)
- Validation commands run and their output:
  ```shell
  helm template . --values values.yaml 2>&1 | head -50
  helm lint .
  kustomize build overlays/prod 2>&1 | head -50
  kubectl apply --dry-run=client -f k8s/ 2>&1
  ```
- Grep results for secrets scan

---

## Optional Skills

If available, load for additional context:
- `ai/skills/springboot_verification/SKILL.md` — verification loop for build + security scans
