# Rule: Built-in Tools First, No Scripts

Use your built-in tools for all file operations. Never generate scripts or compound shell commands.

| Task | Use | NOT |
|------|-----|-----|
| List / enumerate files | `list_files`, Glob | `find`, `ls`, `os.walk` |
| Search file content | `search_files`, Grep | `grep`, `rg`, `Select-String` |
| Read files | `read_file` | `cat`, `head`, `tail` |
| Count lines | Read the file — last line number = line count | `wc -l` |
| Classify files | Read extension from path in your tool output | `case`, `if/else` in scripts |

Simple, single-purpose shell commands are OK when no built-in tool applies (e.g., `mvn test`, `git status`).
Pre-written tools in `ai/tools/` are OK to run — they are tested and deterministic (e.g., `python ai/tools/scan_scope.py`).

**Why:** LLM-generated scripts hang or produce wrong results — wrong `case` pattern order, broken quoting, argument length overflow.
