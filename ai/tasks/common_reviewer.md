# Task: Common Code Review

| Field | Value |
|---|---|
| **Role** | `reviewer` |
| **Goal** | Identify correctness, reliability, security, and maintainability issues in any codebase |
| **Scope** | Specify in prompt — e.g. `src/`, `lib/`, a specific module or PR diff |
| **Constraints** | Read-only. Adapt checks to the language and framework in scope. |

---

## Checks

### C1 — Correctness
- Error handling: no silent swallows; all errors caught, logged, propagated
- Edge cases: null/empty inputs, boundary values, concurrent access
- **CRITICAL** for unhandled exceptions that crash; **WARN** for silent swallows

### C2 — Reliability
- Timeouts: all outbound calls (HTTP, DB, queue) must have explicit timeouts
- Resource cleanup: connections, file handles, threads — closed in `finally` / `try-with-resources`
- **WARN** for missing timeouts; **CRITICAL** for resource leaks

### C3 — Security hygiene
- Input validation: SQL, shell, path traversal
- No hardcoded credentials, tokens, or keys in code or config
- AuthZ: caller is authorized, not just authenticated
- **CRITICAL** for injection risks or hardcoded secrets; **WARN** for missing validation

### C4 — Maintainability
- Functions > 50 lines or nesting > 3 levels → flag for extraction
- Same logic copied ≥ 3 times → flag for shared util
- Dead code: unreachable branches, unused imports
- **SUGGESTION** for all; **WARN** if complexity masks a correctness risk

### C5 — Build and test reliability
- At least one test exercises the main path end-to-end
- Tests are deterministic (no random data, no sleep-based timing)
- **WARN** for untested critical paths; **SUGGESTION** for low edge-case coverage

---

## Evidence

- Each finding: `file:line` + snippet (≤ 10 lines)
- Validation: run the project's test command (`mvn test`, `npm test`, `pytest -q`, etc.)

---

## SkillRefs

SkillRefs: ai/skills/springboot_reviewer/SKILL.md, ai/skills/coding-standards/SKILL.md

---

## DoD

- One report following `ai/BOOTSTRAP.md` Standard Output Contract
- Findings are evidence-based and actionable
- Clear GO/GO-with-fixes/NO-GO verdict
