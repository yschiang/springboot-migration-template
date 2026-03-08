#!/usr/bin/env python3
"""
Pass 1 — Scope Scanner

Produces the scanned-files manifest for any code review or migration task.
Deterministic output — all agents (Cline, Claude Code, etc.) get identical results.

Sections produced:
  1. Header (date, total files, type counts)
  2. Build Profile (SB version, Java version, build tool)
  3. Technology Signals (dependency-level markers)
  4. Pattern Scan Results (all checks.md §4/§5 patterns with line numbers)
  5. Module Structure
  6. Directory Tree
  7. Scope Verification
  8. Files (only if ≤ 100 files)

Usage:
    python ai/tools/scan_scope.py [target_dir]
    python ai/tools/scan_scope.py [target_dir] -o review-scanned-<repo>-<date>.md
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

# ── Dependency-level signals ────────────────────────────────────────────

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
    "httpclient5": "Apache HttpClient 5",
    "mysql-connector-java": "MySQL (old coordinates)",
    "mysql-connector-j": "MySQL (new coordinates)",
    "hibernate-core": "Hibernate",
    "flyway-core": "Flyway",
    "liquibase-core": "Liquibase",
    "git-commit-id-plugin": "git-commit-id-plugin (old coordinates)",
}

# httpclient without 5 — need special handling to avoid matching httpclient5
def _match_httpclient4(gid: str, aid: str) -> bool:
    return aid == "httpclient" and "httpcomponents" in gid and "client5" not in gid


# ── Pattern scan registry (checks.md §4 + §5 + §6 + §8) ───────────────
# (section, pattern_or_regex, file_glob, severity, label)
# pattern is plain string match; regex prefix "re:" triggers re.search

SCAN_PATTERNS_JAVA = [
    # §4 Jakarta namespace
    ("§4", "javax.persistence.", "Critical", "javax.persistence imports"),
    ("§4", "javax.validation.", "Critical", "javax.validation imports"),
    ("§4", "javax.xml.bind.", "Critical", "javax.xml.bind imports (JAXB)"),
    ("§4", "javax.servlet.", "Critical", "javax.servlet imports"),
    # javax.annotation — only PostConstruct/PreDestroy, not all javax.annotation
    ("§4", "javax.annotation.PostConstruct", "Critical", "javax.annotation lifecycle (PostConstruct)"),
    ("§4", "javax.annotation.PreDestroy", "Critical", "javax.annotation lifecycle (PreDestroy)"),
    # Other code-level breaks
    ("§4", "org.apache.http.", "Critical", "Apache HttpClient 4.x namespace"),
    ("§4", "setConnectTimeout", "Critical", "setConnectTimeout (removed in HC5 RequestFactory)"),
    ("§4", "setReadTimeout", "Critical", "setReadTimeout (removed in HC5 RequestFactory)"),
    # Security 6 removals
    ("§4", "WebSecurityConfigurerAdapter", "Critical", "WebSecurityConfigurerAdapter (removed in Security 6)"),
    ("§4", "antMatchers(", "Critical", "antMatchers (removed in Security 6)"),
    ("§4", "mvcMatchers(", "Critical", "mvcMatchers (removed in Security 6)"),
    ("§4", "authorizeRequests(", "Critical", "authorizeRequests() (removed in Security 6, use authorizeHttpRequests())"),
    # Security 6 DSL migration (method chain → lambda)
    ("§4", ".csrf()", "Warn", "csrf() method chain (migrate to lambda style in Security 6)"),
    ("§4", ".cors()", "Warn", "cors() method chain (migrate to lambda style in Security 6)"),
    # Springfox
    ("§4", "@EnableSwagger2", "Critical", "Springfox @EnableSwagger2"),
    ("§4", "@EnableOpenApi", "Critical", "Springfox @EnableOpenApi"),
    ("§4", "springfox", "Critical", "Springfox usage"),
    # Hibernate 6 — dialect class removals
    ("§4", "MySQL5Dialect", "Critical", "MySQL5Dialect (removed in Hibernate 6)"),
    ("§4", "MySQL5InnoDBDialect", "Critical", "MySQL5InnoDBDialect (removed in Hibernate 6)"),
    ("§4", "MySQL8Dialect", "Critical", "MySQL8Dialect (removed in Hibernate 6)"),
    ("§4", "MariaDB106Dialect", "Critical", "MariaDB106Dialect (removed in Hibernate 6)"),
    ("§4", "PostgreSQL95Dialect", "Critical", "PostgreSQL95Dialect (removed in Hibernate 6)"),
    ("§4", "H2Dialect", "Critical", "H2Dialect (removed in Hibernate 6)"),
    ("§4", "Oracle12cDialect", "Critical", "Oracle12cDialect (removed in Hibernate 6)"),
    ("§4", "SQLServerDialect", "Critical", "SQLServerDialect (removed in Hibernate 6)"),
    # Hibernate 6 — silent behavior change
    ("§4", "GenerationType.AUTO", "Warn", "GenerationType.AUTO (Hibernate 6 changed to SEQUENCE for MySQL — silent break)"),
    # Test package relocations
    ("§4", "org.springframework.boot.web.server.LocalServerPort", "Critical", "@LocalServerPort old package (relocated to boot.test.web.server)"),
    # Other
    ("§4", "@EnableBatchProcessing", "Warn", "@EnableBatchProcessing"),
    ("§4", "@ConstructorBinding", "Warn", "@ConstructorBinding (may need relocation)"),
    # Trailing-slash patterns
    ("§4", 'Mapping.*/"', "Critical", "Route mapping with trailing slash"),
    ("§4", 'antMatchers.*/"', "Critical", "Security matcher with trailing slash"),
    ("§4", 'mvcMatchers.*/"', "Critical", "Security matcher with trailing slash (mvc)"),
    ("§4", 'requestMatchers.*/"', "Critical", "Security matcher with trailing slash (new API)"),
    # §6 Spring Batch
    ("§6", "JobBuilderFactory", "Critical", "JobBuilderFactory (removed in Batch 5)"),
    ("§6", "StepBuilderFactory", "Critical", "StepBuilderFactory (removed in Batch 5)"),
    # §8 Cross-reference
    ("§8", "javax.inject", "Critical", "javax.inject imports"),
    ("§8", "ErrorController", "Warn", "ErrorController interface (API changes in Boot 3)"),
    ("§8", "AntPathMatcher", "Warn", "AntPathMatcher (PathPatternParser is now default)"),
    ("§8", "WebMvcMetricsFilter", "Warn", "Micrometer WebMvcMetricsFilter (renamed in Boot 3)"),
    ("§8", "spring.config.import", "Warn", "spring.config.import (required for Config Server)"),
]

# §5 Config property patterns — scanned in .properties and .yml files
SCAN_PATTERNS_CONFIG = [
    ("§5", "spring.redis.", "Warn", "spring.redis.* (renamed to spring.data.redis.*)"),
    ("§5", "spring.data.cassandra.", "Warn", "spring.data.cassandra.* (renamed to spring.cassandra.*)"),
    ("§5", "use-new-id-generator-mappings", "Critical", "spring.jpa.hibernate.use-new-id-generator-mappings (removed)"),
    ("§5", "server.max.http.header.size", "Warn", "server.max.http.header.size (renamed)"),
    ("§5", "management.metrics.export", "Warn", "management.metrics.export.* (path changed)"),
    ("§5", "identity-provider", "Critical", "SAML2 identity-provider (removed, use asserting-party)"),
    # Hibernate dialect in config (removed in Hibernate 6)
    ("§5", "MySQL5Dialect", "Critical", "Hibernate MySQL5Dialect in config (removed in Hibernate 6)"),
    ("§5", "MySQL5InnoDBDialect", "Critical", "Hibernate MySQL5InnoDBDialect in config (removed)"),
    ("§5", "MySQL8Dialect", "Critical", "Hibernate MySQL8Dialect in config (removed in Hibernate 6)"),
    ("§5", "PostgreSQL95Dialect", "Critical", "Hibernate PostgreSQL95Dialect in config (removed)"),
    ("§5", "H2Dialect", "Critical", "Hibernate H2Dialect in config (removed in Hibernate 6)"),
    ("§5", "Oracle12cDialect", "Critical", "Hibernate Oracle12cDialect in config (removed)"),
    ("§5", "SQLServerDialect", "Critical", "Hibernate SQLServerDialect in config (removed)"),
    # §4 trailing-slash config check
    ("§4", "trailing-slash", "Info", "trailing-slash configuration found"),
    # §8
    ("§8", "spring.factories", "Warn", "spring.factories (legacy auto-config registration)"),
]

# Patterns to detect REST controllers (for trailing-slash Warn)
REST_CONTROLLER_PATTERNS = ["@RestController", "@Controller"]


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
    roots = set()
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if rel.parts[0] in EXCLUDE_DIRS:
            continue
        if p.name in BUILD_FILES:
            roots.add(p.parent)
    return sorted(roots, key=lambda p: (len(p.parts), str(p)))


def nearest_module(filepath: Path, module_roots: list, root: Path) -> str:
    for ancestor in [filepath.parent] + list(filepath.parents):
        if ancestor in module_roots:
            rel = ancestor.relative_to(root)
            return str(rel).replace("\\", "/") if str(rel) != "." else root.name
        if ancestor == root:
            break
    return root.name


# ── Scanning ────────────────────────────────────────────────────────────

def scan(target: Path) -> list:
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


# ── File content cache ──────────────────────────────────────────────────

def read_file_lines(path: Path) -> list:
    """Read file and return list of (line_number, line_text) tuples."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        return list(enumerate(text.splitlines(), 1))
    except Exception:
        return []


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


# ── Build profile ──────────────────────────────────────────────────────

def parse_pom(pom_path: Path) -> dict:
    info = {}
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        ns = ""
        m = re.match(r"\{(.+)\}", root.tag)
        if m:
            ns = m.group(1)

        def _find(parent, tag):
            return parent.find(f"{{{ns}}}{tag}") if ns else parent.find(tag)

        def _findall(tag):
            return root.findall(f".//{{{ns}}}{tag}") if ns else root.findall(f".//{tag}")

        # Properties (read first for placeholder resolution)
        props = {}
        props_elem = _find(root, "properties")
        if props_elem is not None:
            for prop in props_elem:
                tag = prop.tag.replace(f"{{{ns}}}", "") if ns else prop.tag
                if prop.text:
                    props[tag] = prop.text

        def _resolve(val):
            """Resolve ${property} placeholders."""
            if not val or "${" not in val:
                return val
            for k, v in props.items():
                val = val.replace(f"${{{k}}}", v)
            return val

        # Parent
        parent = _find(root, "parent")
        if parent is not None:
            g = _find(parent, "groupId")
            a = _find(parent, "artifactId")
            v = _find(parent, "version")
            if a is not None:
                ver = _resolve(v.text) if v is not None else "?"
                info["parent"] = f"{g.text if g is not None else '?'}:{a.text}:{ver}"
                if "spring-boot" in a.text.lower():
                    info["spring_boot_version"] = ver

        # Java version from properties
        for key in ("java.version", "maven.compiler.source", "maven.compiler.target"):
            if key in props:
                info["java_version"] = _resolve(props[key])
                break

        # Spring Boot version from properties (if not from parent)
        for key, val in props.items():
            if "spring-boot" in key.lower() and "version" in key.lower():
                info.setdefault("spring_boot_version", _resolve(val))

        # Dependencies
        deps = []
        for dep in _findall("dependency"):
            a = _find(dep, "artifactId")
            g = _find(dep, "groupId")
            v = _find(dep, "version")
            if a is not None:
                aid = a.text
                gid = g.text if g is not None else ""
                ver = _resolve(v.text) if v is not None else None
                deps.append((gid, aid, ver))
        info["dependencies"] = deps

        # Packaging
        pkg = _find(root, "packaging")
        if pkg is not None and pkg.text:
            info["packaging"] = pkg.text

    except Exception:
        pass
    return info


def parse_gradle(gradle_path: Path) -> dict:
    info = {}
    try:
        content = gradle_path.read_text(encoding="utf-8")

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

        m = re.search(r"org\.springframework\.boot['\"]?\s*version\s*['\"]?([0-9.]+)", content)
        if m:
            info["spring_boot_version"] = m.group(1)

        deps = []
        for m in re.finditer(r"['\"]([^'\"]+):([^'\"]+)(?::([^'\"]+))?['\"]", content):
            gid, aid = m.group(1), m.group(2)
            ver = m.group(3)
            deps.append((gid, aid, ver))
        info["dependencies"] = deps

    except Exception:
        pass
    return info


def collect_build_info(module_roots: list) -> tuple:
    """Parse all build files and aggregate. Returns (build_tool, build_info)."""
    build_info = {}
    build_tool = "Unknown"
    all_deps = []

    for mod_root in module_roots:
        pom = mod_root / "pom.xml"
        if pom.exists():
            build_tool = "Maven"
            parsed = parse_pom(pom)
            # First module with version info wins for top-level fields
            for k, v in parsed.items():
                if k == "dependencies":
                    all_deps.extend(v)
                elif k not in build_info:
                    build_info[k] = v
            continue

        for gf_name in ("build.gradle", "build.gradle.kts"):
            gf = mod_root / gf_name
            if gf.exists():
                build_tool = "Gradle"
                parsed = parse_gradle(gf)
                for k, v in parsed.items():
                    if k == "dependencies":
                        all_deps.extend(v)
                    elif k not in build_info:
                        build_info[k] = v
                break

    # Deduplicate dependencies
    seen = set()
    unique_deps = []
    for dep in all_deps:
        key = (dep[0], dep[1])
        if key not in seen:
            seen.add(key)
            unique_deps.append(dep)
    build_info["dependencies"] = unique_deps

    return build_tool, build_info


# ── Technology signals (dependency level) ───────────────────────────────

def detect_dep_signals(build_info: dict) -> list:
    signals = []
    deps = build_info.get("dependencies", [])
    matched = set()

    for gid, aid, ver in deps:
        # Special case: httpclient4 vs httpclient5
        if _match_httpclient4(gid, aid):
            ver_str = f" ({ver})" if ver else ""
            signals.append(("dep", "Apache HttpClient 4", f"{gid}:{aid}{ver_str}"))
            matched.add(aid)
            continue

        for key, label in SIGNAL_DEPS.items():
            if key in aid and aid not in matched:
                ver_str = f" ({ver})" if ver else ""
                signals.append(("dep", label, f"{gid}:{aid}{ver_str}"))
                matched.add(aid)
                break

    return signals


# ── Pattern scan (checks.md §4/§5/§6/§8) ───────────────────────────────

def run_pattern_scan(files: list, target: Path) -> tuple:
    """
    Run all registered patterns against source files.
    Returns (results, has_rest_controllers, has_trailing_slash_config).
    """
    # Separate files by type
    java_files = [f for f in files if f.suffix == ".java"]
    config_files = [f for f in files if f.suffix in (".properties", ".yml", ".yaml")]

    # Read all files into cache: {rel_path: [(line_no, line_text), ...]}
    java_cache = {}
    for jf in java_files:
        rel = str(jf.relative_to(target)).replace("\\", "/")
        java_cache[rel] = read_file_lines(jf)

    config_cache = {}
    for cf in config_files:
        rel = str(cf.relative_to(target)).replace("\\", "/")
        config_cache[rel] = read_file_lines(cf)

    # Also check META-INF files for spring.factories
    for f in files:
        if f.name == "spring.factories":
            rel = str(f.relative_to(target)).replace("\\", "/")
            config_cache[rel] = read_file_lines(f)

    # Run Java patterns
    # result: {label: [(rel_path, line_no, line_text), ...]}
    results = defaultdict(lambda: {"section": "", "severity": "", "hits": []})

    for section, pattern, severity, label in SCAN_PATTERNS_JAVA:
        for rel, lines in java_cache.items():
            for line_no, line_text in lines:
                if pattern in line_text:
                    results[label]["section"] = section
                    results[label]["severity"] = severity
                    results[label]["hits"].append((rel, line_no, line_text.strip()))

    # Run config patterns
    for section, pattern, severity, label in SCAN_PATTERNS_CONFIG:
        for rel, lines in config_cache.items():
            for line_no, line_text in lines:
                if pattern in line_text:
                    results[label]["section"] = section
                    results[label]["severity"] = severity
                    results[label]["hits"].append((rel, line_no, line_text.strip()))

    # Detect REST controllers
    has_rest_controllers = False
    for rel, lines in java_cache.items():
        for _, line_text in lines:
            for pat in REST_CONTROLLER_PATTERNS:
                if pat in line_text:
                    has_rest_controllers = True
                    break
            if has_rest_controllers:
                break
        if has_rest_controllers:
            break

    # Check if trailing-slash config exists
    trailing_slash_label = "trailing-slash configuration found"
    has_trailing_slash_config = trailing_slash_label in results and len(results[trailing_slash_label]["hits"]) > 0

    return results, has_rest_controllers, has_trailing_slash_config


# ── Directory tree ──────────────────────────────────────────────────────

def build_tree(files: list, target: Path) -> str:
    tree = {}
    for f in files:
        rel = str(f.relative_to(target)).replace("\\", "/")
        parts = rel.split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = None

    lines = []

    def render(node: dict, prefix: str = ""):
        items = sorted(node.items(), key=lambda x: (x[1] is None, x[0]))
        for i, (name, children) in enumerate(items):
            is_last = i == len(items) - 1
            connector = "\u2514\u2500\u2500 " if is_last else "\u251c\u2500\u2500 "
            if children is None:
                lines.append(f"{prefix}{connector}{name}")
            else:
                collapsed = name
                inner = children
                while isinstance(inner, dict) and len(inner) == 1:
                    child_name, child_val = next(iter(inner.items()))
                    if child_val is None:
                        break
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

    classified = [(f, classify(f)) for f in files]

    type_counts = defaultdict(int)
    for _, t in classified:
        type_counts[t] += 1

    module_roots = find_module_roots(target)
    if not module_roots:
        module_roots = [target]

    module_data = defaultdict(lambda: defaultdict(int))
    for f, t in classified:
        mod = nearest_module(f, module_roots, target)
        module_data[mod][t] += 1
        module_data[mod]["Total"] += 1

    glob_counts = {}
    for pattern, matcher in GLOB_PATTERNS:
        count = sum(1 for f, _ in classified if matcher(str(f.relative_to(target)).replace("\\", "/")))
        if count > 0:
            glob_counts[pattern] = count

    build_tool, build_info = collect_build_info(module_roots)
    dep_signals = detect_dep_signals(build_info)
    scan_results, has_rest_controllers, has_trailing_slash_config = run_pattern_scan(files, target)

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

    # ── Build Profile ──
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
    if "packaging" in build_info:
        lines.append(f"| **Packaging** | `{build_info['packaging']}` |")
    lines.append("")

    # ── Technology Signals (dependency level) ──
    if dep_signals:
        lines.append("## Technology Signals")
        lines.append("")
        lines.append("Migration-relevant dependencies detected:")
        lines.append("")
        lines.append("| Signal | Dependency |")
        lines.append("|--------|-----------|")
        for _, label, detail in dep_signals:
            lines.append(f"| {label} | `{detail}` |")
        lines.append("")

    # ── Pattern Scan Results ──
    lines.append("## Pattern Scan Results")
    lines.append("")
    lines.append("All checks.md patterns executed. Pass 2 agent: create a finding for every row with matches, or record N/A.")
    lines.append("")

    # Group by section
    sections_order = ["§4", "§5", "§6", "§8"]
    section_names = {"§4": "Code-level breaks", "§5": "Config/property changes", "§6": "Spring Batch", "§8": "Cross-reference"}

    for section in sections_order:
        section_results = {k: v for k, v in scan_results.items() if v["section"] == section}
        if not section_results and section not in ("§4", "§5"):
            continue

        lines.append(f"### {section} — {section_names.get(section, section)}")
        lines.append("")
        lines.append("| Severity | Pattern | Matches | Files |")
        lines.append("|----------|---------|---------|-------|")

        # Also show patterns with 0 matches from the registry
        all_patterns_for_section = []
        for sec, pat, sev, label in SCAN_PATTERNS_JAVA + SCAN_PATTERNS_CONFIG:
            if sec == section:
                all_patterns_for_section.append(label)

        shown = set()
        # Patterns with hits
        for label, data in sorted(section_results.items(), key=lambda x: (0 if x[1]["severity"] == "Critical" else 1, x[0])):
            hits = data["hits"]
            severity = data["severity"]
            if not hits:
                continue
            shown.add(label)

            # Deduplicate by file (show first line per file, then count)
            by_file = defaultdict(list)
            for rel, line_no, _ in hits:
                by_file[rel].append(line_no)

            file_refs = []
            for rel, line_nos in sorted(by_file.items()):
                lines_str = ",".join(str(n) for n in line_nos[:5])
                if len(line_nos) > 5:
                    lines_str += f"... (+{len(line_nos) - 5})"
                file_refs.append(f"`{rel}:{lines_str}`")

            match_count = len(hits)
            file_count = len(by_file)
            files_cell = file_refs[0] if file_count == 1 else f"{file_refs[0]} (+{file_count - 1} files)"
            lines.append(f"| {severity} | {label} | {match_count} | {files_cell} |")

        # Patterns with 0 matches (N/A)
        for label in all_patterns_for_section:
            if label not in shown and label not in scan_results:
                lines.append(f"| — | {label} | 0 | N/A |")

        lines.append("")

    # Trailing-slash Warn (missing config + has REST controllers)
    if has_rest_controllers and not has_trailing_slash_config:
        lines.append("> **⚠ Trailing-slash default change:** REST controllers detected but no `trailing-slash` configuration found.")
        lines.append("> Recommend: set `spring.mvc.pathmatch.trailing-slash=true` or audit all endpoint URLs.")
        lines.append("")

    # ── Coverage Tracker ──
    lines.append("## Coverage Tracker")
    lines.append("")
    lines.append("Pre-filled by scan tool. Pass 2 agent: verify and update.")
    lines.append("")

    # §1 Baseline
    sb_status = "detected" if sb_ver != "?" else "not detected"
    lines.append(f"- [{'x' if sb_ver != '?' else ' '}] §1 Baseline — Spring Boot `{sb_ver}` {sb_status}")

    # §2 Build toolchain
    java_status = f"Java `{java_ver}`"
    java_ok = java_ver != "?" and java_ver.isdigit() and int(java_ver) >= 17
    if java_ver != "?" and java_ver.isdigit() and int(java_ver) < 17:
        java_status += " (**< 17, Critical**)"
    lines.append(f"- [{'x' if java_ver != '?' else ' '}] §2 Build toolchain — {java_status}")

    # §3 Dependencies
    dep_blockers = [s for s in dep_signals if any(kw in s[1].lower() for kw in ("old coordinates", "javax", "httpcomponent", "springfox", "hibernate"))]
    if dep_blockers:
        lines.append(f"- [x] §3 Dependencies — {len(dep_blockers)} blocker(s) detected")
    else:
        lines.append("- [x] §3 Dependencies — no blockers detected")

    # §4 Code-level
    s4_hits = sum(1 for v in scan_results.values() if v["section"] == "§4" and v["hits"])
    lines.append(f"- [x] §4 Code-level — {s4_hits} pattern(s) matched")

    # §5 Config
    s5_hits = sum(1 for v in scan_results.values() if v["section"] == "§5" and v["hits"])
    lines.append(f"- [x] §5 Config — {s5_hits} deprecated key(s) found")

    # §6 Batch
    s6_hits = sum(1 for v in scan_results.values() if v["section"] == "§6" and v["hits"])
    has_batch = any("batch" in s[1].lower() for s in dep_signals)
    if has_batch:
        lines.append(f"- [x] §6 Batch — {s6_hits} pattern(s) matched")
    else:
        lines.append("- [-] §6 Batch — no Spring Batch dependency")

    # §7 Packaging (needs agent review)
    packaging = build_info.get("packaging", "jar")
    if packaging == "war":
        lines.append("- [ ] §7 Packaging — WAR detected, agent must verify container compatibility")
    else:
        lines.append(f"- [-] §7 Packaging — `{packaging}` (no WAR concerns)")

    # §8 Cross-reference
    s8_hits = sum(1 for v in scan_results.values() if v["section"] == "§8" and v["hits"])
    lines.append(f"- [{'x' if s8_hits else '-'}] §8 Cross-reference — {s8_hits} pattern(s) matched")
    lines.append("")

    # ── Module Structure ──
    lines.append("## Module Structure")
    lines.append("")
    lines.append("| Module | Java | Config | Build | Total |")
    lines.append("|--------|------|--------|-------|-------|")
    sum_j = sum_c = sum_b = sum_t = 0
    for mod in sorted(module_data.keys()):
        d = module_data[mod]
        j, c, b, t = d.get("Java", 0), d.get("Config", 0), d.get("Build", 0), d["Total"]
        sum_j += j; sum_c += c; sum_b += b; sum_t += t
        lines.append(f"| `{mod}` | `{j}` | `{c}` | `{b}` | `{t}` |")
    lines.append(f"| **Total** | **`{sum_j}`** | **`{sum_c}`** | **`{sum_b}`** | **`{sum_t}`** |")
    lines.append("")

    # ── Directory Tree ──
    lines.append("## Directory Tree")
    lines.append("")
    lines.append("```")
    lines.append(f"{repo_name}/")
    lines.append(build_tree(files, target))
    lines.append("```")
    lines.append("")

    # ── Scope Verification ──
    lines.append("## Scope Verification")
    lines.append("")
    lines.append("| Glob Pattern | Count |")
    lines.append("|---|---|")
    for pattern, count in glob_counts.items():
        lines.append(f"| `{pattern}` | `{count}` |")
    lines.append("")

    # ── Files (only if <= 100) ──
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
