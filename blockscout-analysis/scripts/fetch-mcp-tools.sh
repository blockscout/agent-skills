#!/usr/bin/env bash
set -euo pipefail

# fetch-mcp-tools.sh — Download and cache MCP tools list with version-based freshness check.
#
# Usage:
#   ./fetch-mcp-tools.sh [--force]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CACHE_DIR="$SKILL_DIR/cache/mcp-tools"
VERSION_FILE="$CACHE_DIR/version.json"
TOOLS_FILE="$CACHE_DIR/tools.json"

MCP_BASE="https://mcp.blockscout.com/v1"

# ── Dependency checks ─────────────────────────────────────────────

check_deps() {
    if ! command -v curl &>/dev/null; then
        echo "ERROR: curl is required but not installed." >&2
        echo "  Install: brew install curl (macOS) or apt-get install curl (Debian/Ubuntu)" >&2
        exit 1
    fi
    if ! command -v python3 &>/dev/null; then
        echo "ERROR: python3 is required but not installed." >&2
        echo "  Install: brew install python3 (macOS) or apt-get install python3 (Debian/Ubuntu)" >&2
        exit 1
    fi
}

# ── Version helpers ───────────────────────────────────────────────

get_server_version() {
    local response
    response=$(curl -sf "$MCP_BASE/unlock_blockchain_analysis" 2>/dev/null) || {
        echo "WARNING: Failed to reach unlock_blockchain_analysis endpoint." >&2
        echo ""
        return 0
    }
    python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
print(data.get('data', {}).get('version', ''))
" <<< "$response" 2>/dev/null
}

read_cached_version() {
    if [ -f "$VERSION_FILE" ]; then
        python3 -c "
import json
with open('$VERSION_FILE') as f:
    d = json.load(f)
print(d.get('mcp_server_version', ''))
" 2>/dev/null
    fi
}

# ── Download ──────────────────────────────────────────────────────

download_tools() {
    echo "  Downloading MCP tools list..."
    local raw
    raw=$(curl -sf "$MCP_BASE/tools" 2>/dev/null) || {
        echo "ERROR: Failed to download tools from $MCP_BASE/tools" >&2
        echo "  Check network connectivity." >&2
        return 1
    }

    mkdir -p "$CACHE_DIR"

    # Pretty-print for line-range indexing
    echo "$raw" | python3 -m json.tool > "$TOOLS_FILE"

    local count
    count=$(python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
print(len(data) if isinstance(data, list) else 0)
" <<< "$raw" 2>/dev/null)

    echo "  Saved $count tools to $TOOLS_FILE"
    echo "$count"
}

update_version_json() {
    local version="$1" count="$2"
    local fetched_at
    fetched_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    python3 -c "
import json
data = {
    'mcp_server_version': '$version',
    'tools_count': int('$count') if '$count' else 0,
    'fetched_at': '$fetched_at'
}
with open('$VERSION_FILE', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
"
}

# ── Main ──────────────────────────────────────────────────────────

main() {
    check_deps

    local force="false"
    for arg in "$@"; do
        case "$arg" in
            --force) force="true" ;;
            -h|--help)
                echo "Usage: $0 [--force]"
                echo ""
                echo "Downloads the MCP tools list and caches it for offline use."
                echo "Freshness is checked against the MCP server version."
                echo ""
                echo "Options:"
                echo "  --force  Skip freshness check and re-download"
                exit 0
                ;;
            *)
                echo "ERROR: Unknown argument: $arg" >&2
                exit 1
                ;;
        esac
    done

    echo "[mcp-tools]"

    # Get current server version
    local server_version
    server_version=$(get_server_version)

    if [ -z "$server_version" ]; then
        echo "  WARNING: Could not determine MCP server version."
        echo "  Will download tools list regardless."
        force="true"
    fi

    # Check freshness
    if [ "$force" != "true" ]; then
        local cached_version
        cached_version=$(read_cached_version)
        if [ -n "$cached_version" ] && [ "$cached_version" = "$server_version" ] && [ -f "$TOOLS_FILE" ]; then
            echo "  CURRENT (server v$cached_version)"
            return 0
        fi
        if [ -n "$cached_version" ]; then
            echo "  UPDATING (server v$cached_version -> v$server_version)"
        else
            echo "  FETCHING (server v$server_version, no cached version)"
        fi
    else
        if [ -n "$server_version" ]; then
            echo "  FORCE fetching (server v$server_version)"
        else
            echo "  FORCE fetching (server version unknown)"
        fi
    fi

    # Download
    local count
    count=$(download_tools) || exit 1

    # Extract just the numeric count (last line of download_tools output)
    count=$(echo "$count" | tail -n 1)

    # Update version metadata
    update_version_json "${server_version:-unknown}" "$count"
    echo "  OK"
}

main "$@"
