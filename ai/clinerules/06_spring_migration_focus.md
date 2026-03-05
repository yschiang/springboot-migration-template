# Rule: Spring Boot 2 → 3 Focus Areas

When using Spring migration skills, always check and report:
1) Java toolchain 17+
2) Jakarta migration (`javax.*` in code and deps)
3) Spring Security breaking config (if security present)
4) Hibernate / JPA major upgrade implications (if JPA present)
5) application property changes (if config present)
6) Packaging/runtime container compatibility (WAR/JAR)

If any are not applicable, explicitly mark as N/A with rationale.
