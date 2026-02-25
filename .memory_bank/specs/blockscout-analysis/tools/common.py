#!/usr/bin/env python3
"""
Common utilities shared between swagger indexer scripts.
"""

import re
import sys
from pathlib import Path

import requests
import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "head", "options"}


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _get(url: str, params: dict = None) -> requests.Response:
    """GET a URL, raising on network errors."""
    try:
        response = requests.get(url, params=params, timeout=30)
    except requests.RequestException as exc:
        print(f"Error: network error fetching {url}: {exc}")
        sys.exit(1)
    return response


# ---------------------------------------------------------------------------
# Line number calculation
# ---------------------------------------------------------------------------

def find_line_ranges(lines: list[str]) -> dict[tuple[str, str], tuple[int, int]]:
    """
    Scan raw YAML lines and return line ranges for each path+method block.
    Returns: {(path, method): (start_line, end_line)} — 1-based line numbers.
    """
    ranges: dict[tuple[str, str], int] = {}

    # Find the "paths:" top-level key
    paths_line_idx = None
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if re.match(r'^paths:\s*$', stripped):
            paths_line_idx = i
            break

    if paths_line_idx is None:
        return {}

    # Detect path indent (first /...: line after "paths:")
    path_indent = None
    for i in range(paths_line_idx + 1, len(lines)):
        m = re.match(r'^(\s+)(/.*):\s*$', lines[i])
        if m:
            path_indent = len(m.group(1))
            break
        if lines[i].strip() and not lines[i].startswith(" ") and not lines[i].startswith("\t"):
            break

    if path_indent is None:
        return {}

    method_indent = None
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

        if not rstripped or rstripped.lstrip().startswith("#"):
            continue

        # End of paths section (top-level key with no indentation)
        if not line[0].isspace() and rstripped and not rstripped.startswith("#"):
            flush()
            break

        indent_len = len(line) - len(line.lstrip())

        # Path line
        m = re.match(r'^(\s+)(/.*):\s*$', rstripped)
        if m and indent_len == path_indent:
            flush()
            current_path = m.group(2).rstrip()
            current_method = None
            continue

        # Method line
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
                        current_method_start = i + 1  # 1-based

    flush()

    # Compute end lines from sorted start lines
    sorted_entries = sorted(ranges.items(), key=lambda x: x[1])
    result: dict[tuple[str, str], tuple[int, int]] = {}
    for idx, ((path, method), start) in enumerate(sorted_entries):
        if idx + 1 < len(sorted_entries):
            end = sorted_entries[idx + 1][1] - 1
        else:
            end = len(lines)
            for j in range(start, len(lines)):
                rline = lines[j].rstrip()
                if rline and not lines[j][0].isspace() and not rline.startswith("#"):
                    end = j
                    break
        result[(path, method)] = (start, end)

    return result


# ---------------------------------------------------------------------------
# Endpoint indexing
# ---------------------------------------------------------------------------

def index_swagger_file(
    swagger_path: Path,
    swagger_file_rel: str,
    fatal_on_error: bool = False,
) -> list[dict]:
    """
    Parse a swagger YAML file and return a list of endpoint records.

    Args:
        swagger_path:     Path to the swagger.yaml file.
        swagger_file_rel: Value for the 'swagger_file' field in each record
                          (e.g. 'default/swagger.yaml' or 'swagger.yaml').
        fatal_on_error:   If True, call sys.exit(1) on parse/read errors
                          instead of returning an empty list.

    Returns empty list on parse errors when fatal_on_error is False.
    """
    try:
        content = swagger_path.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        print(f"Error: {swagger_path} is not valid YAML ({exc}).")
        if fatal_on_error:
            sys.exit(1)
        return []
    except OSError as exc:
        print(f"Error: could not read {swagger_path}: {exc}.")
        if fatal_on_error:
            sys.exit(1)
        return []

    if not data or not isinstance(data, dict):
        print(f"Warning: {swagger_path} parsed to empty/non-dict, skipping.")
        if fatal_on_error:
            sys.exit(1)
        return []

    if "paths" not in data:
        print(f"Warning: {swagger_path} has no 'paths' key, treating as 0 endpoints.")
        return []

    line_ranges = find_line_ranges(lines)
    records = []

    for path, path_data in data["paths"].items():
        if not isinstance(path_data, dict):
            continue
        for method in HTTP_METHODS:
            if method not in path_data:
                continue
            method_data = path_data[method]
            description = ""
            if isinstance(method_data, dict):
                description = method_data.get("description", "") or ""

            key = (path, method)
            start_line, end_line = line_ranges.get(key, (0, 0))

            records.append({
                "swagger_file": swagger_file_rel,
                "endpoint": path,
                "method": method.upper(),
                "description": description,
                "start_line": start_line,
                "end_line": end_line,
            })

    return records
