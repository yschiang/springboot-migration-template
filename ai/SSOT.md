# SSOT — What Belongs Where

| Layer | Path | Owns |
|---|---|---|
| Entry router | `.clinerules/project.md` | Load sequence, SkillRefs mandate |
| Output contract | `ai/BOOTSTRAP.md` | THE one output format (Summary/Findings/Evidence) |
| Routing | `ai/TASKBOARD.md` | Scope signal -> task card mapping |
| Task cards | `ai/tasks/*` | WHAT: Role, Goal, Scope, Checks, SkillRefs, DoD |
| Skills | `ai/skills/*/SKILL.md` | HOW: detailed checklists, procedures, patterns |
| Knowledge | `ai/knowledge/*` | Reference docs (migration guides, rubrics, examples) |
| Behavioral rules | `ai/clinerules/*` | Always-on constraints (evidence, severity, security) |
| Templates | `ai/templates/*` | Optional export formats (mirror BOOTSTRAP, never override) |

**Rule:** If two files disagree on output format, `ai/BOOTSTRAP.md` wins.
