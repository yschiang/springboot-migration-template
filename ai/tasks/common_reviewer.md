# Task: Common Code Review

| Field | Value |
|---|---|
| **Role** | `reviewer` |
| **Goal** | Identify correctness, reliability, security, and maintainability issues in any codebase |
| **Scope** | Specify in your prompt — e.g. `src/`, `lib/`, a specific module or PR diff |
| **Constraints** | Read-only. Generic checks — adapt to the language and framework in scope. |

---

## Checks (run in order)

### C1 — Correctness
- Error handling: are all errors caught, logged, and propagated correctly? No silent swallows.
- Edge cases: null/empty inputs, boundary values, concurrent access
- Data flow: does output match what callers expect? Check return types and side effects.
- **Flag CRITICAL** for unhandled exceptions that crash the process; **WARN** for silent error swallows

### C2 — Reliability
- Timeouts: are all outbound calls (HTTP, DB, queue) given explicit timeouts?
- Retries: are transient failures retried with backoff? Are retries idempotent?
- Resource cleanup: connections, file handles, threads — closed in `finally` / `try-with-resources`?
- **Flag WARN** for missing timeouts on external calls; **CRITICAL** for connection/resource leaks

### C3 — Security hygiene
- Input validation: are all external inputs validated before use (SQL, shell, path traversal)?
- Secrets: no hardcoded credentials, tokens, or keys anywhere in code or config examples
- AuthZ boundaries: does the code verify the caller is authorized, not just authenticated?
- Dependency versions: are known-vulnerable versions in use? (`mvn dependency:tree`, `npm audit`)
- **Flag CRITICAL** for injection risks or hardcoded secrets; **WARN** for missing input validation

### C4 — Maintainability
- Naming: are variables, functions, and classes named for intent, not implementation?
- Complexity: functions > 50 lines or nesting > 3 levels — flag for extraction
- Duplication: same logic copied ≥ 3 times — flag for extraction to a shared util
- Dead code: unreachable branches, unused imports, commented-out blocks
- **Flag SUGGESTION** for all; escalate to **WARN** if complexity masks a correctness risk

### C5 — Build and test reliability
- Does a passing build exist? Is CI configured?
- Is there at least one test that exercises the main path end-to-end?
- Are tests deterministic? (no random data, no sleep-based timing)
- Test coverage signal — not a hard number, but: are critical paths covered?
- **Flag WARN** for untested critical paths; **SUGGESTION** for low coverage on edge cases

---

## Evidence Requirements

**Output must include:**
- For each finding: `file:line` + the offending snippet (≤ 10 lines)
- Build and test output if runnable:
  ```shell
  # Java/Maven
  mvn -q -DskipTests=false test

  # Node
  npm test

  # Python
  pytest -q
  ```
- Dependency vulnerability scan if applicable:
  ```shell
  mvn dependency:check    # OWASP
  npm audit
  pip-audit
  ```

---

## Optional Skills

If available, load for additional guidance:
- `ai/skills/coding-standards/SKILL.md` — naming and structure conventions
- `ai/skills/api_design/SKILL.md` — REST API contract checks
