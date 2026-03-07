<!-- Template for scanned files log. Referenced by task card DoD. -->

# Scanned Files — <repo>

| Field | Value |
|---|---|
| **Date** | `<YYYY-MM-DD>` |
| **Total Files** | `<N>` |

## Directory Structure

Mark files with findings using: `⚠` (Critical/Warning) or `💡` (Suggestion)

```
<repo>/
├── src/
│   ├── main/java/com/example/
│   │   ├── config/
│   │   │   └── SecurityConfig.java        ⚠ C4, W2
│   │   ├── controller/
│   │   │   └── UserController.java        ⚠ C3, W2
│   │   └── dto/
│   │       └── CreateUserRequest.java     ⚠ C3
│   └── test/java/...
├── pom.xml                                ⚠ C1, C2, C5
├── src/main/resources/
│   └── application.yml                    ⚠ W1
└── ...
```

## Files Read

| # | File | Type | Size |
|---|------|------|------|
| 1 | `<path>` | `<Java>` | `<N lines>` |
| 2 | `<path>` | `<Config>` | `<N lines>` |
| ... | ... | ... | ... |
