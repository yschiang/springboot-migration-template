# Review Report — <repo>

- Repo: `<path>`
- Commit/Branch: `<...>`
- Detected stack:
  - Build: <Maven|Gradle>
  - Boot: <detected version or unknown>
  - Java target: <detected>
  - Web: <Servlet|Reactive|None>
- Summary counts: Critical <X> | Warn <Y> | Suggestion <Z>
- Recommendation: **<GO | GO-with-fixes | NO-GO>**

---

## Findings

### [<SEVERITY>] <ID> - <Title>
**Where**
- File: `<path>`
- Symbol/Section: `<class/method/property>` (if applicable)

**Evidence**
```<lang>
<minimal snippet showing the issue>
```

**Why it’s a problem**
- <short explanation tied to runtime/build/behavior impact>

**Recommended fix**
- <actionable steps>
```<lang>
<example patch or replacement snippet>
```

**References**
- <links>

---

## Fast Fix Plan
1. <...>
2. <...>

## Verification Checklist
- Build:
  - <command>
- Unit tests:
  - <command>
- Smoke run:
  - <command>

## Assumptions / Open Questions
- <only if unavoidable>
