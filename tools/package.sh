#!/usr/bin/env bash
set -euo pipefail

input="${1:?Usage: $0 <skill-directory>}"

# Resolve to absolute path, extract name and parent
dir="$(cd "$input" 2>/dev/null && pwd)" || { echo "Error: '$input' is not a directory" >&2; exit 1; }
name="$(basename "$dir")"
parent="$(dirname "$dir")"

[[ -f "$dir/SKILL.md" ]] || { echo "Error: '$dir/SKILL.md' not found" >&2; exit 1; }

# Extract version from SKILL.md frontmatter (metadata.version)
# metadata is a single-line JSON object; extract it and parse with jq
version="$(grep '^metadata:' "$dir/SKILL.md" | sed 's/^metadata: //' | jq -r '.version' 2>/dev/null)"
[[ -n "$version" ]] || { echo "Error: no metadata.version in '$dir/SKILL.md' or jq not available" >&2; exit 1; }

# Output files in the original working directory
output_zip="$(pwd)/${name}-${version}.zip"
output_skill="$(pwd)/${name}-${version}.skill"
rm -f "$output_zip" "$output_skill"

# cd to parent so git ls-files produces clean <name>/... paths
cd "$parent"

git ls-files "$name" \
  | grep -v -E "^${name}/(\.gitignore|README\.md)$" \
  | zip "$output_zip" -@

cp "$output_zip" "$output_skill"

echo "Created $output_zip"
echo "Created $output_skill"
