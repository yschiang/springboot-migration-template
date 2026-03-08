# Rule: Output Contract is Non-Negotiable

- Always output **ONE** report using `ai/templates/review_report_template.md`.
- Do not invent stack versions; if unknown, write `unknown` and explain how to detect.
- Findings must be categorized as: **Critical / Warn / Suggestion**.
- Each finding must include:
  - Where (file path)
  - Evidence (code/config snippet)
  - Why it’s a problem (impact)
  - Recommended fix (actionable)
  - References (for migration items)

Failure to comply = skill failure.
