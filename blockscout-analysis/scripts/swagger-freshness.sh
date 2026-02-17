#!/usr/bin/env bash
# swagger-freshness.sh — Check if cached Blockscout swagger files are up to date.
#
# Compares the version in cache/.version against the latest stable Blockscout release
# on GitHub. Prints status and exits with:
#   0 — cache is current
#   1 — cache is stale or missing
#
# Usage:
#   bash scripts/swagger-freshness.sh
#
# Run from the skill directory (.claude/skills/blockscout-analysis/).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CACHE_DIR="$SKILL_DIR/cache"
VERSION_FILE="$CACHE_DIR/.version"

# Fetch latest stable release tag from GitHub
fetch_latest_version() {
    local raw tag
    raw=$(curl -sf "https://api.github.com/repos/blockscout/blockscout/releases/latest" \
        | grep -o '"tag_name"[^,]*' \
        | head -1)
    # Extract version: strip key, quotes, and optional 'v' prefix
    tag=$(echo "$raw" | sed 's/.*"tag_name"[^"]*"//; s/".*//; s/^v//')
    echo "$tag"
}

# Read cached version
read_cached_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE" | tr -d '[:space:]'
    else
        echo ""
    fi
}

main() {
    local latest cached

    latest=$(fetch_latest_version)
    if [ -z "$latest" ]; then
        echo "ERROR: Could not fetch latest Blockscout release from GitHub."
        echo "Check network connectivity or GitHub API rate limits."
        exit 1
    fi

    cached=$(read_cached_version)

    if [ -z "$cached" ]; then
        echo "STALE: No cached version found. Latest release: $latest"
        echo "Run swagger caching workflow to fetch and index swagger files."
        exit 1
    fi

    if [ "$cached" = "$latest" ]; then
        echo "CURRENT: Cached version $cached matches latest release."
        exit 0
    else
        echo "STALE: Cached version $cached, latest release $latest"
        echo "Run swagger caching workflow to update swagger files and indexes."
        exit 1
    fi
}

main
