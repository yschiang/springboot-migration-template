# cline-springboot-migration-demo

[繁體中文](README.zh-TW.md)

A Cline skills + rules kit for **Spring Boot 2 to 3 migration code review**.

Load this repo as context in Cline, point it at a target repo, and get a structured review report with Critical/Warn/Suggestion findings, a prioritized fix plan, and verification commands — in two controlled steps.

---

## Quick Start

A ready-to-use copy-paste prompt is in:

```
docs/example-prompts/springboot-2-to-3-review-and-fix.md
```

Replace the `<- change this` placeholders (branch name, build tool) and paste into Cline.

The prompt runs in two gated steps:
1. **Review** — AI reads the target repo, produces a report, then stops
2. **Fix** — after you confirm the report, AI applies fixes and commits by area

---

## Repo Structure

```
cline-springboot-migration-demo/
├── ai/
│   ├── clinerules/          # Behavioral rules — always applied
│   │   ├── 01_output_contract.md
│   │   ├── 02_evidence_first.md
│   │   ├── 03_severity.md
│   │   ├── 04_no_fluff.md
│   │   ├── 05_verification_commands.md
│   │   └── 06_spring_migration_focus.md
│   │
│   ├── knowledge/           # Reference material the AI reads during review
│   │   ├── spring-boot-3.0-migration-guide.md   [P0 — authoritative]
│   │   ├── baeldung-spring-boot-3-migration.md  [P1 — supplementary]
│   │   ├── severity_rubric.md                   [severity definitions]
│   │   └── examples.md                          [good vs bad code patterns, optional]
│   │
│   ├── skills/
│   │   ├── springboot_reviewer/     # Generic baseline code review
│   │   │   └── SKILL.md             #   entry point — correctness, security, reliability
│   │   │
│   │   ├── springboot_engineer/     # Generic Spring Boot engineer
│   │   │   ├── SKILL.md             #   entry point — role, constraints, workflow
│   │   │   ├── README.md            #   skill documentation
│   │   │   └── references/          #   loaded on-demand
│   │   │       ├── web.md
│   │   │       ├── data.md
│   │   │       ├── security.md
│   │   │       ├── cloud.md
│   │   │       └── testing.md
│   │   │
│   │   └── springboot_migration/           # SB2→3 migration (reviewer + engineer + checks)
│   │       ├── SKILL.md             #   engineer entry — fix patterns, fix order
│   │       ├── reviewer.md          #   reviewer entry — merges generic + migration checks
│   │       └── checks.md            #   migration-specific 7-step checklist
│   │
│   └── templates/
│       └── review_report_template.md            # output format (all skills use this)
│
├── docs/
│   ├── USAGE_IN_CLINE.md    # Cline-specific setup options
│   └── example-prompts/
│       └── springboot-2-to-3-review-and-fix.md  # copy-paste prompt for Cline
├── examples/
│   └── example_review_report.md   # sample output for reference
└── README.md
```

---

## Skills

Skills are split into two chains — **Reviewer** (Step 1, read-only) and **Engineer** (Step 2, applies fixes):

```
REVIEWER chain                                   ENGINEER chain
─────────────────────────────────────            ──────────────────────────────────────────
springboot_reviewer/SKILL.md (generic base)      springboot_engineer/SKILL.md (generic base)
        ↑                                                    ↑
springboot_migration/checks.md (migration checklist)    springboot_migration/SKILL.md (SB2→3 specific)
        ↑
springboot_migration/reviewer.md (SB2→3 entry)
```

### Which skill to use

| Step | Goal | Entry point (SKILL.md) |
|---|---|---|
| Review | General code quality (any project) | `springboot_reviewer/SKILL.md` |
| Review | SB2→3 migration — recommended | `springboot_migration/reviewer.md` |
| Fix | SB2 to SB3 migration fixes | `springboot_migration/SKILL.md` |
| Fix | General Spring Boot engineering | `springboot_engineer/SKILL.md` |

### Reviewer skill composition

`springboot_reviewer/SKILL.md` is the generic baseline covering correctness, security, observability, and build reliability.

For SB2→3 migration, `springboot_migration/reviewer.md` composes the generic reviewer with `springboot_migration/checks.md` (Java 17, Jakarta, Security 6, HttpClient 5, Batch, config keys). Findings from both are merged: duplicate issues collapsed, stronger severity wins.

### Engineer skill composition

`springboot_migration/SKILL.md` composes:
- `springboot_engineer/SKILL.md` — base engineer role, constraints, output quality bar
- Loads `springboot_engineer/references/` selectively (security.md, data.md, web.md, testing.md) based on what the fix touches
- Works from findings produced by `springboot_migration/reviewer.md`
- Migration knowledge base P0/P1 for fix patterns

See `ai/skills/springboot_engineer/README.md` for the base engineer skill documentation.

---

## Code Review Procedure

The migration skill inspects the target repo in this order (highest ROI first):

| Step | What is checked | Default severity |
|---|---|---|
| 1 | Spring Boot version — if < 2.7.x, flag two-step upgrade needed | Warn / Critical |
| 2 | Java toolchain — `maven-compiler-plugin`, parent POM, Gradle `sourceCompatibility` | Critical if < 17 |
| 3 | Dependency blockers — `javax.*` artifacts, `httpclient` 4.x, Security < 5.8, Hibernate group ID | Critical |
| 4 | Code patterns — `javax.`, `org.apache.http.`, `WebSecurityConfigurerAdapter`, `antMatchers`, `@EnableBatchProcessing` | Critical / Warn |
| 5 | Config property renames — `spring.redis`, `spring.data.cassandra`, removed JPA/SAML2 keys | Warn / Critical |
| 6 | Spring Batch — `@EnableBatchProcessing` usage, multiple Job beans | Warn |
| 7 | Packaging / runtime — WAR on external container, actuator, security implications | Warn / Critical |

---

## Rules

All rules in `ai/clinerules/` are always applied:

| File | Enforces |
|---|---|
| `01_output_contract` | One report per run, exact template format, no invented versions |
| `02_evidence_first` | Every finding must cite file path + code snippet |
| `03_severity` | Critical = guaranteed break · Warn = likely break · Suggestion = quality |
| `04_no_fluff` | Actionable, repo-specific recommendations only — no generic advice |
| `05_verification_commands` | Report must end with build, test, and dependency-inspection commands |
| `06_spring_migration_focus` | Always check all 6 Spring-specific areas; mark N/A with rationale if not applicable |

---

## Knowledge Base

| File | Priority | Purpose |
|---|---|---|
| `spring-boot-3.0-migration-guide.md` | **P0 — authoritative** | Official Spring guide; wins all conflicts |
| `baeldung-spring-boot-3-migration.md` | P1 — supplementary | Practical examples, HttpClient 5.x migration detail |
| `severity_rubric.md` | Reference | Detailed severity definitions |
| `examples.md` | Optional | Good vs bad code patterns; consulted when writing fix snippets |

### Known conflicts between P0 and P1

| Topic | P0 (correct) | P1 (imprecise) |
|---|---|---|
| JPA property name | `spring.jpa.hibernate.use-new-id-generator-mappings` | `spring.jpa.hibernate.use-new-id-generator` (missing `-mappings`) |
| Trailing slash | Default changed to `false` — still configurable | Described as "deprecated" |

---

## Report Format

Every review produces one Markdown file following `ai/templates/review_report_template.md`:

```
# Review Report — <repo>

## Overview          <- repo meta table + GO / GO-with-fixes / NO-GO
## Summary           <- counts table: Critical | Warning | Suggestion
## Findings
   ### Critical      <- [CRITICAL] ID — Title
   ### Warning       <- [WARN] ID — Title        each with:
   ### Suggestion    <- [SUGGESTION] ID — Title    Where · Evidence · Why · Fix · Action items
## Strengths         <- what is done well
## Priority Plan     <- P0 / P1 / P2 tables with file + estimated effort
## Verification Checklist  <- build · test · smoke commands
## Assumptions / Open Questions
```

Output filename: `review-report-<repo-name>-<YYYYMMDD>.md` saved to the project root.

See `examples/example_review_report.md` for a complete sample output.

---

## Severity Reference

| Level | Meaning | Action |
|---|---|---|
| **Critical** | Guaranteed build or runtime break | Must fix before merge |
| **Warn** | Likely break or behavior change requiring verification | Fix soon |
| **Suggestion** | Code quality improvement | Backlog / nice to have |

When uncertain between two levels, choose the higher one and explain why.

---

## Customization

This repo has no proprietary code. Fork it and:
- Add rules to `ai/clinerules/` for your org's conventions
- Add knowledge files to `ai/knowledge/` and register them in the skill's Knowledge Base section
- Adjust severity thresholds in `ai/knowledge/severity_rubric.md`
- Extend the report template in `ai/templates/review_report_template.md`
