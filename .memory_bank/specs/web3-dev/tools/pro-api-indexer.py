#!/usr/bin/env python3
"""Generate a markdown index of every HTTP endpoint in the Blockscout PRO API."""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parents[3]
OUTPUT_PATH = PROJECT_ROOT / "web3-dev" / "references" / "pro-api-index.md"

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}


def resolve_label(operation: dict) -> str:
    summary = operation.get("summary", "")
    if isinstance(summary, str) and summary.strip():
        return summary.strip()

    description = operation.get("description", "")
    if isinstance(description, str) and description.strip():
        lines = description.splitlines()
        cleaned = " ".join(line.strip() for line in lines if line.strip())
        if cleaned:
            return cleaned

    return "NO DESCRIPTION"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index PRO API endpoints into a markdown file."
    )
    parser.add_argument(
        "input",
        help="Path to the OpenAPI v3 JSON spec",
    )
    args = parser.parse_args()

    input_path = Path(args.input)

    try:
        text = input_path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError) as exc:
        print(f"Error: cannot read input file '{input_path}': {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        spec = json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"Error: input file is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)

    if "paths" not in spec:
        print("Error: parsed JSON does not contain a 'paths' key.", file=sys.stderr)
        sys.exit(3)

    # Collect endpoints grouped by tag
    groups: dict[str, list[tuple[str, str, str]]] = defaultdict(list)

    for path, path_item in spec["paths"].items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS:
                continue
            if not isinstance(operation, dict):
                continue

            tags = operation.get("tags") or []
            tag = tags[0].strip() if tags and isinstance(tags[0], str) else "untagged"
            label = resolve_label(operation)
            groups[tag].append((path, method.upper(), label))

    # Sort entries within each group: by path then method
    for entries in groups.values():
        entries.sort(key=lambda e: (e[0], e[1]))

    # Build output
    lines = ["# PRO API Endpoint Index"]
    for tag in sorted(groups.keys(), key=str.casefold):
        lines.append("")
        lines.append(f"## {tag}")
        lines.append("")
        for path, method, label in groups[tag]:
            lines.append(f"{method} {path}: {label}")

    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Written: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
