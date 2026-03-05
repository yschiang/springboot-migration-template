# Rule: Evidence-First Review

- Never claim an issue without pointing to:
  - file path, and
  - a minimal snippet in a code block.
- If the repo lacks evidence (e.g., dependency tree not available), state it explicitly and provide the next best command to gather evidence.
- Prefer `rg`/`grep`-discoverable patterns for broad scans; then narrow into files for snippets.
