# Skill: Common Reviewer (Repo Code Review Baseline)

## Mission
Given a repository, produce a structured review report with:
- Correctness
- Maintainability
- Security hygiene
- Observability basics
- Build/test reliability
- Deployment/config risks

## Inputs
- Repo path (local workspace)
- Optional: focus areas (security/perf/reliability)
- Optional: target branch/commit

## Optional Reference
- `ai/knowledge/examples.md` — good vs bad code examples; consult when pattern-matching findings or writing fix snippets.

## Review Procedure
1) Repo understanding
- Identify build tool, modules, runtime type, entrypoints.
- Capture key stack versions (language, framework, major libs).

2) Build & tests
- Identify how to build and run tests.
- If CI config exists, compare local commands vs CI pipeline.

3) Code quality scan (lightweight, evidence-based)
- Locate common risk hot-spots:
  - Error handling / retries / timeouts
  - Resource handling (threads, pools, connections)
  - Configuration validation (fail-fast)
  - Logging (structured fields, correlation IDs)
  - Security (authn/authz boundaries, secrets handling)

4) Produce findings
- Recommend fixes that are immediately actionable.

## Standard Checks (non-exhaustive)
- Dependency hygiene:
  - Pin versions via BOM
  - Avoid unmanaged transitive surprises
- Secrets:
  - No hard-coded credentials
  - No tokens in config examples
- Config:
  - `application.yml` sanity
  - Environment variable usage
- Testing:
  - Minimal smoke test path exists
  - One “context loads” test for Spring apps (if applicable)

