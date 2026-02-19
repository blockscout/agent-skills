#!/usr/bin/env python3
"""Swagger YAML Indexer — produces compact, grep-friendly endpoint indices.

Dual-mode: uses PyYAML if available for robust parsing, otherwise falls back
to a stdlib-only line-by-line state machine. Both modes produce identical output.

Usage:
    ./index-swagger.py <swagger.yaml> [--output <path>]
    ./index-swagger.py --batch

Index format:
    METHOD /path | summary_or_operationId | line_start-line_end
"""

import sys
import os
import re
import glob as glob_mod
from datetime import datetime, timezone

HTTP_METHODS = frozenset({"get", "post", "put", "delete", "patch", "head", "options"})


# ── OpenAPI version and info detection ────────────────────────────

def detect_metadata(lines):
    """Scan first 30 lines for OpenAPI version and info.version."""
    openapi_ver = ""
    info_ver = ""
    in_info = False
    for line in lines[:30]:
        stripped = line.strip()
        if stripped.startswith("openapi:"):
            openapi_ver = stripped.split(":", 1)[1].strip().strip("'\"")
        elif stripped.startswith("swagger:"):
            openapi_ver = "swagger " + stripped.split(":", 1)[1].strip().strip("'\"")
        elif stripped == "info:" or stripped.startswith("info:"):
            in_info = True
        elif in_info:
            if stripped.startswith("version:"):
                info_ver = stripped.split(":", 1)[1].strip().strip("'\"")
                in_info = False
            elif not stripped.startswith((" ", "-")) and ":" in stripped:
                in_info = False
    return openapi_ver, info_ver


def strip_yaml_quotes(s):
    """Remove surrounding single or double quotes from a YAML value."""
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


# ── PyYAML-based indexing ─────────────────────────────────────────

def _try_pyyaml(filepath, lines):
    """Attempt indexing with PyYAML. Returns list of entries or None if unavailable."""
    try:
        import yaml
    except ImportError:
        return None

    with open(filepath, "r") as f:
        doc = yaml.safe_load(f)

    if not doc or "paths" not in doc:
        return []

    paths = doc["paths"]
    # We still need line ranges, so cross-reference with line scanning
    line_ranges = _scan_line_ranges(lines)

    entries = []
    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, details in methods.items():
            method_lower = method.lower()
            if method_lower not in HTTP_METHODS:
                continue
            if not isinstance(details, dict):
                continue
            summary = details.get("summary", "")
            if not summary:
                summary = details.get("operationId", "")
            if not summary:
                summary = details.get("description", "")
                if summary:
                    # Truncate to first sentence
                    summary = summary.split(".")[0].split("\n")[0]

            key = (path, method_lower)
            start, end = line_ranges.get(key, (0, 0))
            entries.append((method_lower.upper(), path, summary, start, end))

    entries.sort(key=lambda e: e[3])
    return entries


# ── Line-range scanning (shared by both modes) ───────────────────

def _scan_line_ranges(lines):
    """Scan YAML lines to find (path, method) -> (start_line, end_line) mapping.

    Line numbers are 1-based (matching 'cat -n' / editor convention).
    """
    ranges = {}  # (path, method) -> (start, end)
    pending = []  # stack of (path, method, start)

    state = "SEEKING_PATHS"
    current_path = None
    path_indent = None
    method_indent = None

    for i, raw_line in enumerate(lines):
        lineno = i + 1
        line = raw_line.rstrip("\n\r")

        # Count leading spaces
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)

        if state == "SEEKING_PATHS":
            if stripped.startswith("paths:") and indent == 0:
                state = "IN_PATHS"
            continue

        if state == "IN_PATHS":
            # Detect path indent from first path entry
            if stripped and not stripped.startswith("#"):
                if stripped.endswith(":") or (stripped.count(":") >= 1):
                    if path_indent is None and indent > 0:
                        path_indent = indent
                    if indent == path_indent:
                        # This is a path
                        key = strip_yaml_quotes(stripped.rstrip(":").rstrip())
                        if key.startswith("/"):
                            current_path = key
                            state = "IN_PATH"
                    elif indent == 0:
                        # New top-level key — end of paths section
                        break

        if state == "IN_PATH":
            if stripped and not stripped.startswith("#"):
                if method_indent is None and indent > path_indent:
                    method_indent = indent

                if indent == 0:
                    # New top-level key
                    state = "DONE"
                    break
                elif indent == path_indent:
                    # New path
                    key = strip_yaml_quotes(stripped.rstrip(":").rstrip())
                    if key.startswith("/"):
                        current_path = key
                        # Close previous method if open
                    else:
                        state = "IN_PATHS"
                elif indent == method_indent:
                    method_name = stripped.rstrip(":").strip().lower()
                    if method_name in HTTP_METHODS:
                        # Close previous pending entry
                        if pending:
                            prev_path, prev_method, prev_start = pending.pop()
                            ranges[(prev_path, prev_method)] = (prev_start, lineno - 1)
                        pending.append((current_path, method_name, lineno))

    # Close last pending entry
    if pending:
        prev_path, prev_method, prev_start = pending.pop()
        # End at last non-blank line
        end = len(lines)
        for j in range(len(lines) - 1, prev_start - 1, -1):
            if lines[j].strip():
                end = j + 1
                break
        ranges[(prev_path, prev_method)] = (prev_start, end)

    return ranges


# ── State machine fallback indexing ───────────────────────────────

def _index_state_machine(lines):
    """Index swagger YAML via line-by-line state machine (stdlib only)."""
    line_ranges = _scan_line_ranges(lines)
    entries = []

    state = "SEEKING_PATHS"
    current_path = None
    current_method = None
    current_summary = ""
    current_opid = ""
    current_desc = ""
    path_indent = None
    method_indent = None
    prop_indent = None

    for i, raw_line in enumerate(lines):
        lineno = i + 1
        line = raw_line.rstrip("\n\r")
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)

        if state == "SEEKING_PATHS":
            if stripped.startswith("paths:") and indent == 0:
                state = "IN_PATHS"
            continue

        if state == "IN_PATHS" or state == "IN_PATH" or state == "IN_METHOD":
            if stripped.startswith("#") or not stripped:
                continue

            # Detect indents
            if path_indent is None and indent > 0 and stripped.endswith(":"):
                path_key = strip_yaml_quotes(stripped.rstrip(":"))
                if path_key.startswith("/"):
                    path_indent = indent

            if path_indent and method_indent is None and indent > path_indent:
                mname = stripped.rstrip(":").strip().lower()
                if mname in HTTP_METHODS:
                    method_indent = indent

            if path_indent and method_indent and prop_indent is None and indent > method_indent:
                if ":" in stripped:
                    prop_indent = indent

            # Top-level key — end of paths
            if indent == 0 and ":" in stripped:
                if state == "IN_METHOD" and current_method:
                    _flush_entry(entries, current_path, current_method,
                                 current_summary, current_opid, current_desc,
                                 line_ranges)
                break

            # Path line
            if path_indent and indent == path_indent:
                if state == "IN_METHOD" and current_method:
                    _flush_entry(entries, current_path, current_method,
                                 current_summary, current_opid, current_desc,
                                 line_ranges)
                    current_method = None
                    current_summary = ""
                    current_opid = ""
                    current_desc = ""
                path_key = strip_yaml_quotes(stripped.rstrip(":"))
                if path_key.startswith("/"):
                    current_path = path_key
                    state = "IN_PATH"
                continue

            # Method line
            if method_indent and indent == method_indent:
                if state == "IN_METHOD" and current_method:
                    _flush_entry(entries, current_path, current_method,
                                 current_summary, current_opid, current_desc,
                                 line_ranges)
                mname = stripped.rstrip(":").strip().lower()
                if mname in HTTP_METHODS:
                    current_method = mname
                    current_summary = ""
                    current_opid = ""
                    current_desc = ""
                    state = "IN_METHOD"
                continue

            # Property lines inside a method
            if state == "IN_METHOD" and prop_indent and indent == prop_indent:
                if stripped.startswith("summary:"):
                    current_summary = strip_yaml_quotes(stripped.split(":", 1)[1].strip())
                elif stripped.startswith("operationId:"):
                    current_opid = strip_yaml_quotes(stripped.split(":", 1)[1].strip())
                elif stripped.startswith("description:"):
                    val = stripped.split(":", 1)[1].strip()
                    if val:
                        current_desc = strip_yaml_quotes(val).split(".")[0].split("\n")[0]

    # Flush last method
    if current_method:
        _flush_entry(entries, current_path, current_method,
                     current_summary, current_opid, current_desc,
                     line_ranges)

    entries.sort(key=lambda e: e[3])
    return entries


def _flush_entry(entries, path, method, summary, opid, desc, line_ranges):
    """Create an index entry from accumulated method data."""
    label = summary or opid or desc or ""
    key = (path, method)
    start, end = line_ranges.get(key, (0, 0))
    entries.append((method.upper(), path, label, start, end))


# ── Public API ────────────────────────────────────────────────────

def index_swagger(filepath):
    """Index a swagger file. Returns (metadata, entries).

    metadata: dict with openapi_ver, info_ver
    entries:  list of (METHOD, path, summary, start_line, end_line)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    openapi_ver, info_ver = detect_metadata(lines)

    # Try PyYAML first
    entries = _try_pyyaml(filepath, lines)
    if entries is None:
        # Fallback to state machine
        entries = _index_state_machine(lines)

    metadata = {
        "openapi_ver": openapi_ver,
        "info_ver": info_ver,
    }
    return metadata, entries


def format_index(filepath, metadata, entries, service_name=""):
    """Format index entries as grep-friendly text."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header_parts = []
    if service_name:
        header_parts.append(f"Service: {service_name}")
    if metadata.get("info_ver"):
        header_parts.append(f"Version: {metadata['info_ver']}")
    if metadata.get("openapi_ver"):
        header_parts.append(f"OpenAPI: {metadata['openapi_ver']}")

    lines = []
    lines.append(f"# {' | '.join(header_parts)}")
    lines.append(f"# Source: {filepath}")
    lines.append(f"# Generated: {now} | Endpoints: {len(entries)}")
    lines.append("#")
    lines.append("# FORMAT: METHOD /path | summary_or_operationId | line_start-line_end")

    for method, path, summary, start, end in entries:
        lines.append(f"{method} {path} | {summary} | {start}-{end}")

    return "\n".join(lines) + "\n"


# ── CLI ───────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    batch = "--batch" in args
    output = None

    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        else:
            print("ERROR: --output requires a value", file=sys.stderr)
            sys.exit(1)

    if batch:
        # Find skill directory (parent of scripts/)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)
        cache_dir = os.path.join(skill_dir, "cache", "swagger")

        pattern = os.path.join(cache_dir, "*", "swagger.yaml")
        files = glob_mod.glob(pattern)

        if not files:
            print(f"No swagger files found matching {pattern}", file=sys.stderr)
            sys.exit(1)

        for filepath in sorted(files):
            service = os.path.basename(os.path.dirname(filepath))
            print(f"Indexing {service}...", end=" ")
            try:
                metadata, entries = index_swagger(filepath)
                rel_path = os.path.relpath(filepath, skill_dir)
                text = format_index(rel_path, metadata, entries, service_name=service)
                out_path = os.path.join(os.path.dirname(filepath), "swagger.index")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"{len(entries)} endpoints -> {out_path}")
            except Exception as e:
                print(f"ERROR: {e}", file=sys.stderr)
        return

    # Single file mode
    non_flag_args = [a for a in args if a != "--batch"]
    if not non_flag_args:
        print("Usage: index-swagger.py <swagger.yaml> [--output <path>]", file=sys.stderr)
        print("       index-swagger.py --batch", file=sys.stderr)
        sys.exit(1)

    filepath = non_flag_args[0]
    if not os.path.isfile(filepath):
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    metadata, entries = index_swagger(filepath)
    service = os.path.basename(os.path.dirname(os.path.abspath(filepath)))
    text = format_index(filepath, metadata, entries, service_name=service)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote {len(entries)} endpoints to {output}")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
