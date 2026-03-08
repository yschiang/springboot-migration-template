#!/usr/bin/env python3
"""
Pass 1 — Scope Scanner

Produces the scanned-files manifest for any code review or migration task.
Deterministic output — all agents (Cline, Claude Code, etc.) get identical results.

Usage:
    python ai/tools/scan_scope.py [target_dir]
    python ai/tools/scan_scope.py [target_dir] -o review-scanned-<repo>-<date>.md

If -o is omitted, prints to stdout.
"""

import argparse
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────

INCLUDE_EXTENSIONS = {".java", ".properties", ".yml", ".yaml", ".xml", ".gradle", ".kts"}
EXCLUDE_DIRS = {".git", "target", "build", "node_modules", ".vscode", "ai", ".tools", ".claude"}
BUILD_FILES = {"pom.xml", "build.gradle", "build.gradle.kts"}

# Migration-relevant dependency markers
SIGNAL_DEPS = {
    "spring-boot-starter-web": "Web (Servlet)",
    "spring-boot-starter-webflux": "Web (Reactive)",
    "spring-boot-starter-security": "Spring Security",
    "spring-boot-starter-data-jpa": "JPA / Hibernate",
    "spring-boot-starter-batch": "Spring Batch",
    "spring-boot-starter-validation": "Bean Validation",
    "springfox-swagger2": "Springfox Swagger 2",
    "springfox-boot-starter": "Springfox Swagger 3",
    "springdoc-openapi": "SpringDoc OpenAPI",
    "javax.servlet-api": "javax.servlet",
    "javax.annotation-api": "javax.annotation",
    "validation-api": "javax.validation",
    "jaxb-api": "javax.xml.bind (JAXB)",
    "httpclient": "Apache HttpClient 4",
    "httpclient5": "Apache HttpClient 5",
    "mysql-connector-java": "MySQL (old coordinates)",
    "mysql-connector-j": "MySQL (new coordinates)",
    "flyway-core": "Flyway",
    "liquibase-core": "Liquibase",
}

# Quick-scan patterns for Java files (pattern, label)
SIGNAL_PATTERNS = [
    ("WebSecurityConfigurerAdapter", "WebSecurityConfigurerAdapter (removed in Security 6)"),
    ("antMatchers", "antMatchers (removed in Security 6)"),
    ("mvcMatchers", "mvcMatchers (removed in Security 6)"),
    ("javax.persistence", "javax.persistence imports"),
    ("javax.validation", "javax.validation imports"),
    ("javax.servlet", "javax.servlet imports"),
    ("javax.xml.bind", "javax.xml.bind imports (JAXB)"),
    ("javax.annotation.PostConstruct", "javax.annotation lifecycle"),
    ("org.apache.http", "Apache HttpClient 4.x namespace"),
    ("@EnableBatchProcessing", "@EnableBatchProcessing"),
    ("@EnableSwagger2", "Springfox @EnableSwagger2"),
    ("JobBuilderFactory", "JobBuilderFactory (removed in Batch 5)"),
    ("StepBuilderFactory", "StepBuilderFactory (removed in Batch 5)"),
    ("spring.factories", "spring.factories (legacy auto-config)"),
]


# ── Classification ──────────────────────────────────────────────────────

def classify(path: Path) -> str:
    if path.name in BUILD_FILES or path.suffix in (".gradle", ".kts"):
        return "Build"
    if path.suffix == ".java":
        return "Java"
    if path.suffix in (".properties", ".yml", ".yaml", ".xml"):
        return "Config"
    return "Other"


# ── Module detection ────────────────────────────────────────────────────

def find_module_roots(root: Path) -> list:
    """Find directories containing a build file (pom.xml / build.gradle)."""
    roots = set()
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.relative_to(root).parts[0] in EXCLUDE_DIRS:
            continue
        if p.name in BUILD_FILES:
            roots.add(p.parent)
    return sorted(roots, key=lambda p: (len(p.parts), str(p)))


def nearest_module(filepath: Path, module_roots: list, root: Path) -> str:
    """Find the nearest ancestor module root for a file."""
    for ancestor in [filepath.parent] + list(filepath.parents):
        if ancestor in module_roots:
            rel = ancestor.relative_to(root)
            return str(rel).replace("\\", "/") if str(rel) != "." else root.name
        if ancestor == root:
            break
    return root.name


# ── Scanning ────────────────────────────────────────────────────────────

def scan(target: Path) -> list:
    """Collect all in-scope files under target."""
    results = []
    for p in sorted(target.rglob("*")):
        if not p.is_file():
            continue
        rel_parts = p.relative_to(target).parts
        if rel_parts[0] in EXCLUDE_DIRS:
            continue
        if p.suffix not in INCLUDE_EXTENSIONS:
            continue
        rel_str = str(p.relative_to(target)).replace("\\", "/")
        is_src = "/src/" in f"/{rel_str}/" or rel_str.startswith("src/")
        is_build = p.name in BUILD_FILES
        if not (is_src or is_build):
            continue
        results.append(p)
    return results


# ── Glob-pattern counts ────────────────────────────────────────────────

GLOB_PATTERNS = [
    ("**/src/**/*.java", lambda r: r.endswith(".java") and "/src/" in f"/{r}/"),
    ("**/src/**/*.properties", lambda r: r.endswith(".properties") and "/src/" in f"/{r}/"),
    ("**/src/**/*.yml", lambda r: r.endswith(".yml") and "/src/" in f"/{r}/"),
    ("**/src/**/*.yaml", lambda r: r.endswith(".yaml") and "/src/" in f"/{r}/"),
    ("**/src/**/*.xml", lambda r: r.endswith(".xml") and "/src/" in f"/{r}/"),
    ("**/pom.xml", lambda r: r.endswith("pom.xml")),
    ("**/*.gradle", lambda r: r.endswith(".gradle")),
    ("**/*.kts", lambda r: r.endswith(".kts")),
]


# ── Build profile (Maven) ──────────────────────────────────────────────

def parse_pom(pom_path: Path) -> dict:
    """Extract key info from pom.xml."""
    info = {}
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        ns = ""
        # Detect namespace
        m = re.match(r"\{(.+)\}", root.tag)
        if m:
            ns = m.group(1)
            nsmap = {"m": ns}
            find = lambda tag: root.find(f".//m:{tag}", nsmap)
            findall = lambda tag: root.findall(f".//m:{tag}", nsmap)
        else:
            find = lambda tag: root.find(f".//{tag}")
            findall = lambda tag: root.findall(f".//{tag}")

        # Parent
        parent = root.find(f"{{{ns}}}parent") if ns else root.find("parent")
        if parent is not None:
            g = parent.find(f"{{{ns}}}groupId") if ns else parent.find("groupId")
            a = parent.find(f"{{{ns}}}artifactId") if ns else parent.find("artifactId")
            v = parent.find(f"{{{ns}}}version") if ns else parent.find("version")
            if a is not None:
                info["parent"] = f"{g.text if g is not None else '?'}:{a.text}:{v.text if v is not None else '?'}"
                if "spring-boot" in a.text.lower():
                    info["spring_boot_version"] = v.text if v is not None else "?"

        # Properties
        props_elem = root.find(f"{{{ns}}}properties") if ns else root.find("properties")
        if props_elem is not None:
            for prop in props_elem:
                tag = prop.tag.replace(f"{{{ns}}}", "") if ns else prop.tag
                if tag == "java.version":
                    info["java_version"] = prop.text
                elif tag == "maven.compiler.source":
                    info["java_version"] = info.get("java_version", prop.text)
                elif "spring-boot" in tag.lower() and "version" in tag.lower():
                    info["spring_boot_version"] = info.get("spring_boot_version", prop.text)

        # Dependencies — collect artifact IDs
        deps = []
        for dep in findall("dependency"):
            a = dep.find(f"{{{ns}}}artifactId") if ns else dep.find("artifactId")
            g = dep.find(f"{{{ns}}}groupId") if ns else dep.find("groupId")
            if a is not None:
                aid = a.text
                gid = g.text if g is not None else ""
                deps.append((gid, aid))
        info["dependencies"] = deps

    except Exception:
        pass
    return info


def parse_gradle(gradle_path: Path) -> dict:
    """Extract key info from build.gradle (basic text parsing)."""
    info = {}
    try:
        content = gradle_path.read_text(encoding="utf-8")

        # Java version
        for pattern in [
            r"sourceCompatibility\s*=\s*['\"]?(\d+)",
            r"targetCompatibility\s*=\s*['\"]?(\d+)",
            r"JavaVersion\.VERSION_(\d+)",
            r"jvmToolchain\((\d+)\)",
        ]:
            m = re.search(pattern, content)
            if m:
                info["java_version"] = m.group(1)
                break

        # Spring Boot version (from plugins)
        m = re.search(r"org\.springframework\.boot['\"]?\s*version\s*['\"]?([0-9.]+)", content)
        if m:
            info["spring_boot_version"] = m.group(1)

        # Dependencies — collect artifact names
        deps = []
        for m in re.finditer(r"['\"]([^'\"]+):([^'\"]+)(?::([^'\"]+))?['\"]", content):
            gid, aid = m.group(1), m.group(2)
            deps.append((gid, aid))
        info["dependencies"] = deps

    except Exception:
        pass
    return info


# ── Technology signals ──────────────────────────────────────────────────

def detect_signals(files: list, target: Path, build_info: dict) -> list:
    """Quick-scan files for migration-relevant patterns."""
    signals = []

    # From dependencies
    deps = build_info.get("dependencies", [])
    for gid, aid in deps:
        for key, label in SIGNAL_DEPS.items():
            if key in aid:
                signals.append(("dep", label, f"{gid}:{aid}"))
                break

    # From Java source (quick scan — read first 50 lines of each file)
    pattern_hits = defaultdict(list)  # pattern_label -> [file_paths]
    java_files = [f for f in files if f.suffix == ".java"]
    for jf in java_files:
        try:
            head = jf.read_text(encoding="utf-8", errors="ignore")[:3000]  # ~50 lines
            rel = str(jf.relative_to(target)).replace("\\", "/")
            for pattern, label in SIGNAL_PATTERNS:
                if pattern in head:
                    pattern_hits[label].append(rel)
        except Exception:
            continue

    for label, hit_files in sorted(pattern_hits.items()):
        count = len(hit_files)
        example = hit_files[0] if count == 1 else f"{hit_files[0]} (+{count - 1} more)"
        signals.append(("code", label, example))

    # Check for spring.factories
    for f in files:
        rel = str(f.relative_to(target)).replace("\\", "/")
        if "spring.factories" in f.name:
            signals.append(("config", "spring.factories (legacy auto-config)", rel))

    return signals


# ── Directory tree ──────────────────────────────────────────────────────

def build_tree(files: list, target: Path) -> str:
    """Build an annotated directory tree of scanned files."""
    # Build tree structure
    tree = {}
    for f in files:
        rel = str(f.relative_to(target)).replace("\\", "/")
        parts = rel.split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = None  # leaf

    lines = []

    def render(node: dict, prefix: str = "", is_last_parent: bool = True):
        items = sorted(node.items(), key=lambda x: (x[1] is None, x[0]))  # dirs first
        for i, (name, children) in enumerate(items):
            is_last = i == len(items) - 1
            connector = "\u2514\u2500\u2500 " if is_last else "\u251c\u2500\u2500 "
            if children is None:
                # Leaf file
                lines.append(f"{prefix}{connector}{name}")
            else:
                # Directory — check if we can collapse single-child chains
                collapsed = name
                inner = children
                while isinstance(inner, dict) and len(inner) == 1:
                    child_name, child_val = next(iter(inner.items()))
                    if child_val is None:
                        break  # don't collapse into a file
                    collapsed = f"{collapsed}/{child_name}"
                    inner = child_val

                lines.append(f"{prefix}{connector}{collapsed}/")
                extension = "    " if is_last else "\u2502   "
                render(inner, prefix + extension)

    render(tree)
    return "\n".join(lines)


# ── Markdown generation ────────────────────────────────────────────────

def generate_manifest(target: Path) -> str:
    target = target.resolve()
    repo_name = target.name
    today = date.today().strftime("%Y-%m-%d")

    files = scan(target)
    total = len(files)

    # Classify
    classified = [(f, classify(f)) for f in files]

    # Type counts
    type_counts = defaultdict(int)
    for _, t in classified:
        type_counts[t] += 1

    # Module detection
    module_roots = find_module_roots(target)
    if not module_roots:
        module_roots = [target]

    # Module structure
    module_data = defaultdict(lambda: defaultdict(int))
    for f, t in classified:
        mod = nearest_module(f, module_roots, target)
        module_data[mod][t] += 1
        module_data[mod]["Total"] += 1

    # Scope verification
    glob_counts = {}
    for pattern, matcher in GLOB_PATTERNS:
        count = sum(1 for f, _ in classified if matcher(str(f.relative_to(target)).replace("\\", "/")))
        if count > 0:
            glob_counts[pattern] = count

    # Build profile
    build_info = {}
    build_tool = "Unknown"
    for mod_root in module_roots:
        pom = mod_root / "pom.xml"
        if pom.exists():
            build_tool = "Maven"
            parsed = parse_pom(pom)
            # Merge — first module with info wins for top-level fields
            for k, v in parsed.items():
                if k not in build_info:
                    build_info[k] = v
                elif k == "dependencies":
                    build_info[k] = build_info[k] + v
            break  # Use root/first pom for version info
        gradle = mod_root / "build.gradle"
        gradle_kts = mod_root / "build.gradle.kts"
        gf = gradle if gradle.exists() else (gradle_kts if gradle_kts.exists() else None)
        if gf:
            build_tool = "Gradle"
            parsed = parse_gradle(gf)
            for k, v in parsed.items():
                if k not in build_info:
                    build_info[k] = v
            break

    # Technology signals
    signals = detect_signals(files, target, build_info)

    # ── Build markdown ──

    lines = []
    lines.append(f"# Scanned Files — {repo_name}")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| **Date** | `{today}` |")
    lines.append(f"| **Total Files** | `{total}` |")
    tc = ", ".join(f"{k}: {v}" for k, v in sorted(type_counts.items()))
    lines.append(f"| **Type Counts** | `{tc}` |")
    lines.append("")

    # Build Profile
    lines.append("## Build Profile")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| **Build Tool** | `{build_tool}` |")
    sb_ver = build_info.get("spring_boot_version", "?")
    lines.append(f"| **Spring Boot** | `{sb_ver}` |")
    java_ver = build_info.get("java_version", "?")
    lines.append(f"| **Java Version** | `{java_ver}` |")
    if "parent" in build_info:
        lines.append(f"| **Parent POM** | `{build_info['parent']}` |")
    lines.append("")

    # Technology Signals
    if signals:
        lines.append("## Technology Signals")
        lines.append("")
        lines.append("Migration-relevant frameworks and patterns detected:")
        lines.append("")
        lines.append("| Source | Signal | Detail |")
        lines.append("|--------|--------|--------|")
        for src, label, detail in signals:
            lines.append(f"| {src} | {label} | `{detail}` |")
        lines.append("")

    # Module Structure
    lines.append("## Module Structure")
    lines.append("")
    lines.append("| Module | Java | Config | Build | Total |")
    lines.append("|--------|------|--------|-------|-------|")
    sum_j = sum_c = sum_b = sum_t = 0
    for mod in sorted(module_data.keys()):
        d = module_data[mod]
        j, c, b, t = d.get("Java", 0), d.get("Config", 0), d.get("Build", 0), d["Total"]
        sum_j += j
        sum_c += c
        sum_b += b
        sum_t += t
        lines.append(f"| `{mod}` | `{j}` | `{c}` | `{b}` | `{t}` |")
    lines.append(f"| **Total** | **`{sum_j}`** | **`{sum_c}`** | **`{sum_b}`** | **`{sum_t}`** |")
    lines.append("")

    # Directory Tree
    lines.append("## Directory Tree")
    lines.append("")
    lines.append("```")
    lines.append(f"{repo_name}/")
    lines.append(build_tree(files, target))
    lines.append("```")
    lines.append("")

    # Scope Verification
    lines.append("## Scope Verification")
    lines.append("")
    lines.append("| Glob Pattern | Count |")
    lines.append("|---|---|")
    for pattern, count in glob_counts.items():
        lines.append(f"| `{pattern}` | `{count}` |")
    lines.append("")

    # Files (only if <= 100)
    if total <= 100:
        lines.append("## Files")
        lines.append("")
        lines.append("| # | File | Type |")
        lines.append("|---|------|------|")
        for i, (f, t) in enumerate(classified, 1):
            rel = str(f.relative_to(target)).replace("\\", "/")
            lines.append(f"| {i} | `{rel}` | {t} |")
        lines.append("")

    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Pass 1 — Scope Scanner")
    parser.add_argument("target", nargs="?", default=".", help="Target directory to scan (default: .)")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_dir():
        print(f"Error: {target} is not a directory")
        raise SystemExit(1)

    content = generate_manifest(target)

    if args.output:
        out = Path(args.output)
        out.write_text(content + "\n", encoding="utf-8")
        print(f"Written: {out} ({content.count(chr(10))} lines)")
    else:
        print(content)


if __name__ == "__main__":
    main()
