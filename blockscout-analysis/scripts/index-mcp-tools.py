#!/usr/bin/env python3
"""MCP Tools Indexer — maps tool names to line ranges in pretty-printed JSON.

Usage:
    ./index-mcp-tools.py [<tools.json>]

Defaults to cache/mcp-tools/tools.json relative to skill directory.
Output: cache/mcp-tools/tools.index

Index format:
    tool_name | description | line_start-line_end
"""

import sys
import os
import json
import re
from datetime import datetime, timezone

def clean_description(desc):
    """Clean description text for single-line index output."""
    if not desc:
        return ""
    # Collapse all whitespace runs into single spaces, strip edges
    cleaned = re.sub(r"\s+", " ", desc).strip()
    # Escape pipe characters to protect the delimiter format
    cleaned = cleaned.replace("|", "\\|")
    return cleaned


def find_tool_boundaries(lines):
    """Find line ranges for each tool in pretty-printed JSON array.

    Returns list of (start_line, end_line, name, description) tuples.
    Line numbers are 1-based.
    """
    tools = []
    depth = 0
    in_array = False
    tool_start = None
    current_name = ""
    current_desc = ""

    for i, raw_line in enumerate(lines):
        lineno = i + 1
        stripped = raw_line.strip()

        # Detect array start
        if not in_array and stripped == "[":
            in_array = True
            continue

        if not in_array:
            continue

        # Detect tool object start (4-space indent opening brace)
        if stripped == "{" and raw_line.startswith("    ") and depth == 0:
            tool_start = lineno
            current_name = ""
            current_desc = ""
            depth = 1
            continue

        if depth > 0:
            # Track nested depth
            open_braces = stripped.count("{") + stripped.count("[")
            close_braces = stripped.count("}") + stripped.count("]")

            # Extract name at depth 1 (top-level property of tool object)
            if depth == 1 and '"name"' in stripped:
                match = re.search(r'"name"\s*:\s*"([^"]+)"', stripped)
                if match:
                    current_name = match.group(1)

            # Extract description at depth 1
            if depth == 1 and '"description"' in stripped:
                match = re.search(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"', stripped)
                if match:
                    current_desc = match.group(1)
                    # Unescape JSON string
                    current_desc = current_desc.replace("\\n", " ").replace("\\t", " ").replace('\\"', '"')

            depth += open_braces - close_braces

            # Detect tool object end
            if depth == 0 and tool_start is not None:
                tools.append((tool_start, lineno, current_name, current_desc))
                tool_start = None

    return tools


def index_mcp_tools(filepath):
    """Index a pretty-printed MCP tools JSON file.

    Returns (tool_count, entries) where entries is list of
    (name, description, start_line, end_line).
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Validate JSON
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print("ERROR: Expected JSON array in tools file.", file=sys.stderr)
        sys.exit(1)

    boundaries = find_tool_boundaries(lines)

    entries = []
    for start, end, name, desc in boundaries:
        entries.append((name, clean_description(desc), start, end))

    return len(data), entries


def format_index(filepath, tool_count, entries):
    """Format index as grep-friendly text."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = []
    lines.append(f"# MCP Tools Index")
    lines.append(f"# Source: {filepath}")
    lines.append(f"# Generated: {now} | Tools: {tool_count}")
    lines.append("#")
    lines.append("# FORMAT: tool_name | description | line_start-line_end")

    for name, desc, start, end in entries:
        lines.append(f"{name} | {desc} | {start}-{end}")

    return "\n".join(lines) + "\n"


def main():
    # Determine input file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    default_path = os.path.join(skill_dir, "cache", "mcp-tools", "tools.json")

    filepath = default_path
    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            print("Usage: index-mcp-tools.py [<tools.json>]")
            print(f"  Default: {default_path}")
            print(f"  Output:  cache/mcp-tools/tools.index")
            sys.exit(0)
        else:
            filepath = arg

    if not os.path.isfile(filepath):
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        print("  Run fetch-mcp-tools.sh first to download the tools list.", file=sys.stderr)
        sys.exit(1)

    tool_count, entries = index_mcp_tools(filepath)

    rel_path = os.path.relpath(filepath, skill_dir)
    text = format_index(rel_path, tool_count, entries)

    out_path = os.path.join(os.path.dirname(filepath), "tools.index")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Indexed {len(entries)} tools -> {out_path}")


if __name__ == "__main__":
    main()
