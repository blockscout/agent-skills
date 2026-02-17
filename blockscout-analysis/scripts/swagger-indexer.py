#!/usr/bin/env python3
"""
Swagger YAML Indexer for Blockscout API Discovery.

Parses a Swagger/OpenAPI YAML file and produces a compact index mapping
each endpoint to its HTTP method, summary, and line range in the source file.

Usage:
    python3 swagger-indexer.py <swagger.yaml> [> output.idx]

Output format:
    # Index: <filename>
    # Generated: <ISO timestamp>
    # Endpoints: <count>
    #
    # FORMAT: METHOD /path | summary | line_start-line_end
    GET /api/v2/addresses/{address_hash} | Get address info | 245-312
    ...

Supports both OpenAPI 3.0 and Swagger 2.0 formats.
Requires PyYAML for structured parsing; falls back to regex-only mode if unavailable.
"""

import sys
import os
import re
from datetime import datetime, timezone

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "head", "options"}
METHOD_ORDER = {"get": 0, "post": 1, "put": 2, "delete": 3, "patch": 4, "head": 5, "options": 6}


def truncate(text, max_len=80):
    """Truncate text to max_len characters, adding ... if truncated."""
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def extract_summary(method_data):
    """Extract a human-readable summary from a method's parsed YAML data."""
    if isinstance(method_data, dict):
        if method_data.get("summary"):
            return truncate(method_data["summary"])
        if method_data.get("operationId"):
            return method_data["operationId"]
        if method_data.get("description"):
            return truncate(method_data["description"])
    return "(no description)"


def find_line_ranges(lines):
    """
    Scan raw lines to find the line ranges for each path+method block.

    Returns dict: {(path, method): (start_line, end_line)} where lines are 1-indexed.
    """
    ranges = {}

    # Detect the indent level of paths entries by finding the "paths:" key
    paths_line_idx = None
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if stripped == "paths:" or stripped == "paths: ":
            paths_line_idx = i
            break
        if re.match(r'^paths:\s*$', stripped):
            paths_line_idx = i
            break

    if paths_line_idx is None:
        return ranges

    # Detect path indent (first non-empty line after "paths:" that starts with spaces + /)
    path_indent = None
    for i in range(paths_line_idx + 1, len(lines)):
        m = re.match(r'^(\s+)(/.*):\s*$', lines[i])
        if m:
            path_indent = len(m.group(1))
            break
        # Stop if we hit a top-level key (no indent)
        if lines[i].strip() and not lines[i].startswith(" ") and not lines[i].startswith("\t"):
            break

    if path_indent is None:
        return ranges

    method_indent = None  # Will detect from first method under a path

    current_path = None
    current_method = None
    current_method_start = None

    def flush():
        nonlocal current_method, current_method_start
        if current_path and current_method and current_method_start is not None:
            ranges[(current_path, current_method)] = current_method_start
        current_method = None
        current_method_start = None

    for i in range(paths_line_idx + 1, len(lines)):
        line = lines[i]
        rstripped = line.rstrip()

        # Skip empty lines and comments
        if not rstripped or rstripped.lstrip().startswith("#"):
            continue

        # Check if this is a top-level key (end of paths section)
        if not line[0].isspace() and rstripped and not rstripped.startswith("#"):
            flush()
            break

        # Check if this is a path line
        indent_len = len(line) - len(line.lstrip())
        m = re.match(r'^(\s+)(/.*):\s*$', rstripped)
        if m and indent_len == path_indent:
            flush()
            current_path = m.group(2).rstrip()
            current_method = None
            continue

        # Check if this is a method line
        if current_path and indent_len > path_indent:
            m2 = re.match(r'^(\s+)(\w+):\s*$', rstripped)
            if m2:
                candidate = m2.group(2).lower()
                candidate_indent = len(m2.group(1))
                if candidate in HTTP_METHODS:
                    if method_indent is None:
                        method_indent = candidate_indent
                    if candidate_indent == method_indent:
                        flush()
                        current_method = candidate
                        current_method_start = i + 1  # 1-indexed

    flush()

    # Now compute end lines: for each entry, end is the line before the next sibling
    # Sort entries by start line
    sorted_entries = sorted(ranges.items(), key=lambda x: x[1])
    result = {}
    for idx, ((path, method), start) in enumerate(sorted_entries):
        if idx + 1 < len(sorted_entries):
            next_start = sorted_entries[idx + 1][1]
            end = next_start - 1
        else:
            # Last entry: scan forward to find end of paths section or EOF
            end = len(lines)
            for j in range(start, len(lines)):
                rline = lines[j].rstrip()
                if rline and not lines[j][0].isspace() and not rline.startswith("#"):
                    end = j  # line before the next top-level key
                    break
        result[(path, method)] = (start, end)

    return result


def index_with_yaml(filepath, lines):
    """Parse swagger with PyYAML and combine with line range detection."""
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    if not data or "paths" not in data:
        return []

    paths = data["paths"]
    line_ranges = find_line_ranges(lines)
    entries = []

    for path, path_data in paths.items():
        if not isinstance(path_data, dict):
            continue
        for method in HTTP_METHODS:
            if method not in path_data:
                continue
            method_data = path_data[method]
            summary = extract_summary(method_data)
            key = (path, method)
            if key in line_ranges:
                start, end = line_ranges[key]
            else:
                start, end = 0, 0
            entries.append((path, method, summary, start, end))

    return entries


def index_with_regex(lines):
    """Regex-only fallback when PyYAML is not available."""
    line_ranges = find_line_ranges(lines)
    entries = []

    for (path, method), (start, end) in line_ranges.items():
        # Try to extract summary from lines following the method
        summary = "(no description)"
        for j in range(start, min(start + 15, len(lines))):
            line = lines[j].strip()
            m = re.match(r'^summary:\s*["\']?(.+?)["\']?\s*$', line)
            if m:
                summary = truncate(m.group(1))
                break
            m2 = re.match(r'^operationId:\s*["\']?(.+?)["\']?\s*$', line)
            if m2 and summary == "(no description)":
                summary = m2.group(1)
            m3 = re.match(r'^description:\s*["\']?(.+?)["\']?\s*$', line)
            if m3 and summary == "(no description)":
                summary = truncate(m3.group(1))

        entries.append((path, method, summary, start, end))

    return entries


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 swagger-indexer.py <swagger.yaml>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r") as f:
        lines = f.readlines()

    filename = os.path.basename(filepath)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if HAS_YAML:
        entries = index_with_yaml(filepath, lines)
    else:
        entries = index_with_regex(lines)

    # Sort by path, then method order
    entries.sort(key=lambda e: (e[0], METHOD_ORDER.get(e[1], 99)))

    # Output
    print(f"# Index: {filename}")
    print(f"# Generated: {timestamp}")
    print(f"# Endpoints: {len(entries)}")
    if not HAS_YAML:
        print("# Mode: regex-only (PyYAML not available)")
    print("#")
    print("# FORMAT: METHOD /path | summary | line_start-line_end")

    for path, method, summary, start, end in entries:
        method_upper = method.upper()
        line_range = f"{start}-{end}" if start > 0 else "?-?"
        # Escape pipe in summary
        summary_clean = summary.replace("|", "/")
        print(f"{method_upper} {path} | {summary_clean} | {line_range}")


if __name__ == "__main__":
    main()
