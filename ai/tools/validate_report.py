#!/usr/bin/env python3
"""
Report Validator — checks a review report against the template structure.

Usage:
    python ai/tools/validate_report.py <report.md>
    python ai/tools/validate_report.py <report.md> --scanned <scanned.md>

Exit code 0 = pass, 1 = failures found.
"""

import re
import sys
from pathlib import Path


# ── Required sections ───────────────────────────────────────────────────

REQUIRED_SECTIONS = [
    "Overview",
    "Findings",
    "Strengths",
    "Priority Plan",
    "Verification Checklist",
]

# ── Overview table required fields ──────────────────────────────────────

OVERVIEW_FIELDS = [
    "Repo",
    "Boot Version",
    "Java Target",
    "Files Scanned",
    "Recommendation",
]

# ── Finding header pattern ──────────────────────────────────────────────

# Must match: #### [CRITICAL][MIGRATION] C1 — title
#          or: #### [WARN][BASELINE] W1 — title
FINDING_HEADER_RE = re.compile(
    r"^####\s+\[(CRITICAL|WARN|SUGGESTION)\]"
    r"\[(MIGRATION|BASELINE)\]\s+"
    r"\w+\d+\s*[—–-]\s*.+",
)

# Finding sub-sections
FINDING_SUBSECTIONS = ["Where", "Evidence", "Why it's a problem", "Recommended fix"]

# ── Validation ──────────────────────────────────────────────────────────


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_headings(content: str) -> list:
    """Extract all markdown headings with their level and text."""
    return [
        (len(m.group(1)), m.group(2).strip())
        for m in re.finditer(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE)
    ]


def validate_sections(content: str) -> list:
    """Check required top-level sections exist."""
    errors = []
    headings = [text for level, text in extract_headings(content) if level == 2]
    for section in REQUIRED_SECTIONS:
        if not any(section.lower() in h.lower() for h in headings):
            errors.append(f"MISSING SECTION: ## {section}")
    return errors


def validate_overview(content: str) -> list:
    """Check overview table has required fields."""
    errors = []
    # Find the Overview section
    overview_match = re.search(
        r"## Overview\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if not overview_match:
        return ["MISSING: ## Overview section"]

    overview = overview_match.group(1)
    for field in OVERVIEW_FIELDS:
        if field.lower() not in overview.lower():
            errors.append(f"MISSING OVERVIEW FIELD: {field}")

    # Check Recommendation value
    rec_match = re.search(r"Recommendation.*?`(.*?)`", overview)
    if rec_match:
        rec = rec_match.group(1).strip("*")
        valid_recs = {"GO", "GO-with-fixes", "NO-GO"}
        if rec not in valid_recs:
            errors.append(f"INVALID RECOMMENDATION: '{rec}' (must be one of {valid_recs})")
    else:
        errors.append("MISSING: Recommendation value")

    return errors


def validate_findings(content: str) -> list:
    """Check finding format compliance."""
    errors = []

    # Find all h4 headers that look like findings
    finding_headers = list(re.finditer(r"^####\s+.+$", content, re.MULTILINE))
    if not finding_headers:
        errors.append("NO FINDINGS: report has zero #### finding headers")
        return errors

    for match in finding_headers:
        header = match.group(0).strip()
        # Skip if it's inside a code block
        pos = match.start()
        before = content[:pos]
        if before.count("```") % 2 == 1:
            continue

        if not FINDING_HEADER_RE.match(header):
            errors.append(
                f"BAD FINDING FORMAT: '{header}'\n"
                f"  Expected: #### [SEVERITY][SOURCE] ID — title\n"
                f"  Example:  #### [CRITICAL][MIGRATION] C1 — javax.persistence namespace"
            )
            continue

        # Check sub-sections exist (between this h4 and next h4 or h3/h2)
        start = match.end()
        next_header = re.search(r"^#{2,4}\s+", content[start:], re.MULTILINE)
        end = start + next_header.start() if next_header else len(content)
        finding_body = content[start:end]

        for subsection in FINDING_SUBSECTIONS:
            if f"**{subsection}**" not in finding_body:
                finding_id = re.search(r"\w+\d+", header)
                fid = finding_id.group(0) if finding_id else "?"
                errors.append(f"MISSING SUBSECTION in {fid}: **{subsection}**")

    return errors


def validate_severity_sections(content: str) -> list:
    """Check that Critical/Warning/Suggestion subsections exist under Findings."""
    errors = []
    findings_match = re.search(
        r"## Findings\s*\n(.*?)(?=\n## [^F]|\Z)", content, re.DOTALL
    )
    if not findings_match:
        return ["MISSING: ## Findings section"]

    findings = findings_match.group(1)
    for severity in ["Critical", "Warning", "Suggestion"]:
        if f"### {severity}" not in findings:
            errors.append(f"MISSING SEVERITY SECTION: ### {severity} under ## Findings")
    return errors


def validate_priority_plan(content: str) -> list:
    """Check Priority Plan has P0/P1/P2 subsections."""
    errors = []
    pp_match = re.search(
        r"## Priority Plan\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if not pp_match:
        return ["MISSING: ## Priority Plan section"]

    pp = pp_match.group(1)
    for level in ["P0", "P1", "P2"]:
        if level not in pp:
            errors.append(f"MISSING PRIORITY LEVEL: {level} in Priority Plan")
    return errors


def validate_file_count(report_content: str, scanned_content: str) -> list:
    """Cross-check Files Scanned in report vs Total Files in scanned log."""
    errors = []

    # Extract from report
    report_match = re.search(r"Files Scanned.*?`(\d+)`", report_content)
    if not report_match:
        errors.append("MISSING: Files Scanned count in report Overview")
        return errors
    report_count = int(report_match.group(1))

    # Extract from scanned log
    scanned_match = re.search(r"Total Files.*?`(\d+)`", scanned_content)
    if not scanned_match:
        errors.append("MISSING: Total Files count in scanned log")
        return errors
    scanned_count = int(scanned_match.group(1))

    if report_count != scanned_count:
        errors.append(
            f"FILE COUNT MISMATCH: report says {report_count}, "
            f"scanned log says {scanned_count}"
        )
    return errors


# ── Main ────────────────────────────────────────────────────────────────


def validate(report_path: Path, scanned_path: Path = None) -> list:
    content = read_file(report_path)
    errors = []

    errors.extend(validate_sections(content))
    errors.extend(validate_overview(content))
    errors.extend(validate_severity_sections(content))
    errors.extend(validate_findings(content))
    errors.extend(validate_priority_plan(content))

    if scanned_path and scanned_path.exists():
        scanned = read_file(scanned_path)
        errors.extend(validate_file_count(content, scanned))

    return errors


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Report Validator")
    parser.add_argument("report", help="Path to the review report markdown")
    parser.add_argument("--scanned", help="Path to the scanned files log (for cross-check)")
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Error: {report_path} not found")
        sys.exit(1)

    scanned_path = Path(args.scanned) if args.scanned else None
    errors = validate(report_path, scanned_path)

    if errors:
        print(f"FAIL — {len(errors)} issue(s):\n")
        for i, e in enumerate(errors, 1):
            print(f"  {i}. {e}")
        print(f"\nReport: {report_path}")
        sys.exit(1)
    else:
        print(f"PASS — report structure is valid: {report_path}")
        sys.exit(0)


if __name__ == "__main__":
    main()
