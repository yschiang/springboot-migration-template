<!-- This template is the SSOT for review report output format. -->
<!-- Task cards reference this template in their DoD. Behavioral rules are in ai/clinerules/. -->

# Review Report — <repo>

## Table of Contents
- [Overview](#overview)
- [Findings](#findings)
  - [Critical](#critical)
  - [Warning](#warning)
  - [Suggestion](#suggestion)
- [Strengths](#strengths)
- [Priority Plan](#priority-plan)
- [Verification Checklist](#verification-checklist)
- [Assumptions / Open Questions](#assumptions--open-questions)

---

## Overview

| Field              | Value                            |
|--------------------|----------------------------------|
| **Repo**           | `<path>`                         |
| **Commit / Branch**| `<...>`                          |
| **Build**          | `<Maven \| Gradle>`              |
| **Boot Version**   | `<detected version or unknown>`  |
| **Java Target**    | `<detected>`                     |
| **Web**            | `<Servlet \| Reactive \| None>`  |
| **Reviewed**       | `<YYYY-MM-DD HH:MM>` → `<HH:MM>` (`<N>` min) |
| **Files Scanned**  | `<N>` (`<X>` Java, `<Y>` config, `<Z>` build) |
| **Recommendation** | **`<GO \| GO-with-fixes \| NO-GO>`** |

### Summary

| Severity   | Count  | Description              |
|------------|--------|--------------------------|
| Critical   | `<X>`  | Must fix before merge    |
| Warning    | `<Y>`  | Fix soon                 |
| Suggestion | `<Z>`  | Nice to have             |
| **Total**  | **`<N>`** | —                     |

---

## Findings

### Critical

#### [CRITICAL] <ID> — <Title>

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
<patch or replacement snippet>
```

**Action items**
- [ ] <specific task>

**References**
- <links>

---

### Warning

#### [WARN] <ID> — <Title>

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
<patch or replacement snippet>
```

**Action items**
- [ ] <specific task>

**References**
- <links>

---

### Suggestion

#### [SUGGESTION] <ID> — <Title>

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

**Action items**
- [ ] <specific task>

---

## Strengths

> Highlight what is done well — worth preserving.

- <strength 1>
- <strength 2>

---

## Priority Plan

### P0 — Must Fix (Critical)
> Impact: system stability / correctness

| # | Issue | File | Est. Effort |
|---|-------|------|-------------|
| 1 | `<issue title>` | `<file>` | `<Xh>` |

### P1 — Fix Soon (Warning)
> Impact: code quality / maintainability

| # | Issue | File | Est. Effort |
|---|-------|------|-------------|
| 1 | `<issue title>` | `<file>` | `<Xh>` |

### P2 — Backlog (Suggestion)
> Impact: readability / best practices

| # | Issue | Est. Effort |
|---|-------|-------------|
| 1 | `<issue title>` | `<Xh>` |

---

## Verification Checklist

- Build:
  - `<command>`
- Unit tests:
  - `<command>`
- Smoke run:
  - `<command>`

---

## Assumptions / Open Questions

- <only if unavoidable>
