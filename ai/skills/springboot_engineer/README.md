# springboot_engineer

A senior Spring Boot engineer skill for building and maintaining production-grade Spring Boot 3.x applications.

> Source: [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/spring-boot-engineer) — MIT License

---

## When to Use

Use this skill (or a skill that extends it) when the task involves **writing or modifying code**:
- Building REST APIs or reactive WebFlux endpoints
- Implementing Spring Data JPA repositories and services
- Configuring Spring Security 6
- Writing unit, integration, or slice tests
- Fixing or refactoring existing Spring Boot code

For **read-only analysis** (finding problems without changing code), use the reviewer skills instead:
- `common_reviewer.md`
- `sb3_reviewer.md`

---

## File Structure

```
springboot_engineer/
├── SKILL.md            ← entry point — role definition, constraints, workflow
└── references/         ← loaded on-demand based on what the task touches
    ├── web.md          ← Controllers, REST APIs, validation, exception handling
    ├── data.md         ← Spring Data JPA, repositories, transactions, projections
    ├── security.md     ← Spring Security 6, OAuth2, JWT, method security
    ├── cloud.md        ← Spring Cloud, Config, Discovery, Gateway, resilience
    └── testing.md      ← @SpringBootTest, MockMvc, Testcontainers, test slices
```

The skill loads reference files selectively — only the files relevant to the current task are read, keeping context lean.

---

## Key Constraints (summary)

| Must Do | Must Not Do |
|---|---|
| Constructor injection | Field injection (`@Autowired` on fields) |
| `@Valid` on all API inputs | Skip input validation |
| `@ControllerAdvice` for exceptions | Expose internal exceptions to clients |
| `@ConfigurationProperties` for config | Hardcode URLs, credentials, or config |
| `@Transactional` for multi-step ops | Skip transaction management |
| Write tests with appropriate slices | Use deprecated Spring Boot 2.x patterns |

---

## Extends Into

This skill is the base for task-specific engineer skills:

| Task | Skill |
|---|---|
| Spring Boot 2 to 3 migration fixes | `../sb3_engineer.md` |

---

## Usage in Prompt

```
Read and follow: ai/skills/springboot_engineer/SKILL.md
Load relevant references from: ai/skills/springboot_engineer/references/
```
