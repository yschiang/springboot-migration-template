# Skills Index

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        GENERIC SKILLS                           │
│  (any Spring Boot project, not tied to a specific task)         │
│                                                                 │
│  springboot_reviewer/SKILL.md    springboot_engineer/SKILL.md   │
│  ┌─────────────────────────┐     ┌──────────────────────────┐   │
│  │ Code Review Baseline    │     │ Spring Boot 3.x Engineer │   │
│  │ ─────────────────────── │     │ ──────────────────────── │   │
│  │ • Correctness           │     │ • REST API development   │   │
│  │ • Security hygiene      │     │ • Spring Data JPA        │   │
│  │ • Observability         │     │ • Spring Security 6      │   │
│  │ • Build/test reliability│     │ • Testing best practices │   │
│  │ • Deployment risks      │     │ • references/ (on-demand)│   │
│  │                         │     │                          │   │
│  │ Role: reviewer          │     │ Role: submitter          │   │
│  │ Output: review report   │     │ Output: code changes     │   │
│  └────────┬────────────────┘     └──────────┬───────────────┘   │
│           │ extends                          │ extends           │
└───────────┼──────────────────────────────────┼──────────────────┘
            │                                  │
┌───────────┼──────────────────────────────────┼──────────────────┐
│           ▼       springboot_migration/       ▼                  │
│  TASK-SPECIFIC SKILL (Spring Boot 2 → 3 Migration)             │
│                                                                 │
│  ┌─────────────────────────┐     ┌──────────────────────────┐   │
│  │ reviewer.md             │     │ SKILL.md (engineer)      │   │
│  │ ─────────────────────── │     │ ──────────────────────── │   │
│  │ Composes:               │     │ Composes:                │   │
│  │  • springboot_reviewer/ │     │  • springboot_engineer/  │   │
│  │    SKILL.md (generic)   │     │    SKILL.md (generic)    │   │
│  │  • checks.md (SB3      │     │  • Fix patterns          │   │
│  │    migration checklist) │     │  • Fix order (7 steps)   │   │
│  │                         │     │  • Knowledge base P0/P1  │   │
│  │ Role: reviewer          │     │ Role: submitter          │   │
│  │ Output: migration report│     │ Output: migration fixes  │   │
│  └─────────────────────────┘     └──────────────────────────┘   │
│                                                                 │
│  checks.md ← 7-step migration checklist (module, not standalone)│
│    Java toolchain → deps → code → config → batch → pkg → cmds  │
└─────────────────────────────────────────────────────────────────┘
```

## How Composition Works

**Reviewer chain** (for identifying problems):
```
springboot_migration/reviewer.md
    ├── reads → springboot_reviewer/SKILL.md   (generic review procedure)
    └── reads → springboot_migration/checks.md        (SB3-specific 7-step checklist)
    → merges findings into ONE report, deduplicates, stronger severity wins
```

**Engineer chain** (for applying fixes):
```
springboot_migration/SKILL.md
    ├── reads → springboot_engineer/SKILL.md   (generic engineer constraints)
    ├── reads → springboot_engineer/references/ (on-demand: web, data, security, testing)
    └── reads → springboot_migration/reviewer.md      (the report it needs to fix)
    → fixes ONLY what the reviewer found, one commit per area
```

## Skill Directory

### Core Skills (generic, reusable)

| Skill | Entry Point | Role | Purpose |
|---|---|---|---|
| **springboot_reviewer** | `SKILL.md` | reviewer | Baseline code review for any repo: correctness, security, reliability, maintainability |
| **springboot_engineer** | `SKILL.md` | submitter | Spring Boot 3.x development: REST, JPA, Security 6, testing. Loads `references/` on demand |

### Task-Specific Skills

| Skill | Entry Point | Role | Purpose |
|---|---|---|---|
| **springboot_migration** (reviewer) | `reviewer.md` | reviewer | SB2→3 migration review. Extends `springboot_reviewer` + adds migration checks |
| **springboot_migration** (engineer) | `SKILL.md` | submitter | SB2→3 migration fixes. Extends `springboot_engineer` + adds fix patterns |
| **springboot_migration** (checks) | `checks.md` | — | Module: 7-step migration checklist (not standalone, used by reviewer.md) |

### Supplementary Skills (standalone, no composition)

| Skill | Entry Point | Purpose |
|---|---|---|
| **api_design** | `SKILL.md` | REST API design patterns and conventions |
| **coding-standards** | `SKILL.md` | Universal coding standards (naming, structure, error handling) |
| **springboot_patterns** | `SKILL.md` | Spring Boot architecture patterns (layering, DI, config) |
| **springboot_security** | `SKILL.md` | Spring Security best practices (OWASP, OAuth2, CORS) |
| **springboot_tdd** | `SKILL.md` | TDD workflow for Spring Boot (red-green-refactor, test slices) |
| **springboot_verification** | `SKILL.md` | Post-implementation verification loop (build, test, lint) |

## Naming Convention

- **`SKILL.md`** — every skill directory has exactly ONE entry point named `SKILL.md`
- Exception: `springboot_migration/` has two entry points (`SKILL.md` for engineer, `reviewer.md` for reviewer) because it serves both roles
- Files that are NOT `SKILL.md` are **modules** — they are composed by an entry point, never used standalone

## Which Skill Do I Use?

| I want to… | Use this |
|---|---|
| Review any codebase for general issues | `springboot_reviewer/SKILL.md` |
| Review for Spring Boot 2→3 migration blockers | `springboot_migration/reviewer.md` |
| Apply SB2→3 migration fixes from a review report | `springboot_migration/SKILL.md` |
| Build or modify Spring Boot 3.x code (general) | `springboot_engineer/SKILL.md` |
