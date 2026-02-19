#!/usr/bin/env bash
set -euo pipefail

# fetch-swagger.sh — Download and cache Blockscout swagger files with freshness checking.
#
# Usage:
#   ./fetch-swagger.sh <service|--all> [--variant <name>] [--force]
#
# Services: blockscout, bens, metadata, stats, multichain-aggregator
# --variant  Only for blockscout service (default: "default")
# --force    Skip freshness check and re-download

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CACHE_DIR="$SKILL_DIR/cache/swagger"
VERSION_FILE="$CACHE_DIR/version.json"

SERVICES="blockscout bens metadata stats multichain-aggregator"
SWAGGERS_BASE="https://raw.githubusercontent.com/blockscout/swaggers/master"
GITHUB_API="https://api.github.com"

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

# ── JSON helpers ──────────────────────────────────────────────────

json_get() {
    local file="$1" key="$2"
    python3 -c "
import json, sys
try:
    with open('$file') as f:
        d = json.load(f)
    v = d
    for k in '$key'.split('.'):
        v = v[k]
    print(v)
except Exception:
    pass
" 2>/dev/null
}

json_get_str() {
    local json_str="$1" key="$2"
    python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    v = d
    for k in '$key'.split('.'):
        if isinstance(v, list):
            v = v[int(k)]
        else:
            v = v[k]
    print(v)
except Exception:
    pass
" <<< "$json_str" 2>/dev/null
}

# ── Version detection ─────────────────────────────────────────────

detect_latest_version() {
    local service="$1"
    case "$service" in
        blockscout)
            # Latest release from blockscout/blockscout
            local response
            response=$(curl -sf "$GITHUB_API/repos/blockscout/blockscout/releases/latest" 2>/dev/null) || {
                echo "ERROR: Failed to fetch latest blockscout release from GitHub." >&2
                return 1
            }
            local tag
            tag=$(json_get_str "$response" "tag_name")
            # Strip leading 'v' prefix
            echo "${tag#v}"
            ;;
        bens|stats|multichain-aggregator)
            # Latest release from blockscout/blockscout-rs with service prefix
            local response
            response=$(curl -sf "$GITHUB_API/repos/blockscout/blockscout-rs/releases?per_page=50" 2>/dev/null) || {
                echo "ERROR: Failed to fetch blockscout-rs releases from GitHub." >&2
                return 1
            }
            local version
            version=$(python3 -c "
import json, sys
releases = json.loads(sys.stdin.read())
prefix = '${service}/v'
for r in releases:
    tag = r.get('tag_name', '')
    if tag.startswith(prefix) and '-rc' not in tag and '-alpha' not in tag:
        print(tag[len(prefix):])
        break
" <<< "$response" 2>/dev/null)
            if [ -z "$version" ]; then
                echo "ERROR: No release found for $service in blockscout-rs." >&2
                return 1
            fi
            echo "$version"
            ;;
        metadata)
            # Special case: no release tag — use hosted_versions.txt from swaggers repo
            local versions_url="$SWAGGERS_BASE/services/metadata/hosted_versions.txt"
            local versions
            versions=$(curl -sf "$versions_url" 2>/dev/null) || {
                # Fallback: GitHub Contents API
                local contents
                contents=$(curl -sf "$GITHUB_API/repos/blockscout/swaggers/contents/services/metadata" 2>/dev/null) || {
                    echo "ERROR: Failed to detect metadata version from swaggers repo." >&2
                    return 1
                }
                versions=$(python3 -c "
import json, sys, re
items = json.loads(sys.stdin.read())
versions = []
for item in items:
    name = item.get('name', '')
    if re.match(r'^\d+\.\d+\.\d+$', name):
        versions.append(name)
versions.sort(key=lambda v: list(map(int, v.split('.'))))
if versions:
    print(versions[-1])
" <<< "$contents" 2>/dev/null)
            }
            if [ -z "$versions" ]; then
                echo "ERROR: Failed to detect metadata version." >&2
                return 1
            fi
            # Take the last (highest) version line
            local version
            version=$(echo "$versions" | tail -n 1 | tr -d '[:space:]')
            # Strip leading 'v' if present
            echo "${version#v}"
            ;;
        *)
            echo "ERROR: Unknown service: $service" >&2
            return 1
            ;;
    esac
}

read_cached_version() {
    local service="$1"
    if [ -f "$VERSION_FILE" ]; then
        json_get "$VERSION_FILE" "$service.version"
    fi
}

# ── Download ──────────────────────────────────────────────────────

build_swagger_url() {
    local service="$1" version="$2" variant="${3:-}"
    case "$service" in
        blockscout)
            local v="${variant:-default}"
            echo "$SWAGGERS_BASE/blockscout/$version/$v/swagger.yaml"
            ;;
        bens|metadata|stats|multichain-aggregator)
            echo "$SWAGGERS_BASE/services/$service/$version/swagger.yaml"
            ;;
    esac
}

fetch_swagger() {
    local service="$1" version="$2" variant="${3:-}"
    local url
    url=$(build_swagger_url "$service" "$version" "$variant")
    local target_dir="$CACHE_DIR/$service"
    local target_file="$target_dir/swagger.yaml"

    mkdir -p "$target_dir"

    echo "  Downloading $url"
    local http_code
    http_code=$(curl -sf -w "%{http_code}" -o "$target_file" "$url" 2>/dev/null) || {
        echo "ERROR: Failed to download swagger for $service v$version." >&2
        echo "  URL: $url" >&2
        echo "  Check if this version exists in the swaggers repository." >&2
        rm -f "$target_file"
        return 1
    }

    if [ "$http_code" -ge 400 ] 2>/dev/null; then
        echo "ERROR: HTTP $http_code when downloading swagger for $service v$version." >&2
        echo "  URL: $url" >&2
        rm -f "$target_file"
        return 1
    fi

    echo "  Saved to $target_file"
}

update_version_json() {
    local service="$1" version="$2" variant="${3:-}"
    local fetched_at
    fetched_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    mkdir -p "$CACHE_DIR"

    # Read existing version.json or start fresh
    local existing="{}"
    if [ -f "$VERSION_FILE" ]; then
        existing=$(cat "$VERSION_FILE")
    fi

    python3 -c "
import json, sys
data = json.loads('''$existing''')
entry = {'version': '$version', 'fetched_at': '$fetched_at'}
variant = '$variant'
if variant and variant != 'default':
    entry['variant'] = variant
data['$service'] = entry
with open('$VERSION_FILE', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
"
}

# ── Main logic ────────────────────────────────────────────────────

process_service() {
    local service="$1" variant="$2" force="$3"

    echo "[$service]"

    # Detect latest version
    local latest
    latest=$(detect_latest_version "$service") || return 1

    if [ -z "$latest" ]; then
        echo "  ERROR: Could not determine latest version for $service." >&2
        return 1
    fi

    # Check freshness
    if [ "$force" != "true" ]; then
        local cached
        cached=$(read_cached_version "$service")
        if [ -n "$cached" ] && [ "$cached" = "$latest" ] && [ -f "$CACHE_DIR/$service/swagger.yaml" ]; then
            echo "  CURRENT (v$cached)"
            return 0
        fi
        if [ -n "$cached" ]; then
            echo "  UPDATING from v$cached to v$latest"
        else
            echo "  FETCHING v$latest (no cached version)"
        fi
    else
        echo "  FORCE fetching v$latest"
    fi

    # Download
    local effective_variant=""
    if [ "$service" = "blockscout" ]; then
        effective_variant="${variant:-default}"
    fi

    fetch_swagger "$service" "$latest" "$effective_variant" || return 1
    update_version_json "$service" "$latest" "$effective_variant"

    # Re-index after download
    local index_script="$SCRIPT_DIR/index-swagger.py"
    if [ -f "$index_script" ]; then
        echo "  Re-indexing..."
        python3 "$index_script" "$CACHE_DIR/$service/swagger.yaml" \
            --output "$CACHE_DIR/$service/swagger.index"
    fi

    echo "  OK (v$latest)"
}

usage() {
    echo "Usage: $0 <service|--all> [--variant <name>] [--force]"
    echo ""
    echo "Services: $SERVICES"
    echo ""
    echo "Options:"
    echo "  --all             Fetch all services"
    echo "  --variant <name>  Swagger variant for blockscout (default: \"default\")"
    echo "  --force           Skip freshness check and re-download"
    exit 1
}

main() {
    check_deps

    local target=""
    local variant=""
    local force="false"

    while [ $# -gt 0 ]; do
        case "$1" in
            --all)
                target="--all"
                shift
                ;;
            --variant)
                shift
                variant="${1:-}"
                if [ -z "$variant" ]; then
                    echo "ERROR: --variant requires a value" >&2
                    usage
                fi
                shift
                ;;
            --force)
                force="true"
                shift
                ;;
            -h|--help)
                usage
                ;;
            *)
                target="$1"
                shift
                ;;
        esac
    done

    if [ -z "$target" ]; then
        usage
    fi

    if [ "$target" = "--all" ]; then
        local failed=0
        for svc in $SERVICES; do
            process_service "$svc" "$variant" "$force" || failed=$((failed + 1))
            echo ""
        done
        if [ "$failed" -gt 0 ]; then
            echo "WARNING: $failed service(s) failed." >&2
            exit 1
        fi
    else
        # Validate service name
        local valid=false
        for svc in $SERVICES; do
            if [ "$svc" = "$target" ]; then
                valid=true
                break
            fi
        done
        if [ "$valid" != "true" ]; then
            echo "ERROR: Unknown service '$target'." >&2
            echo "Valid services: $SERVICES" >&2
            exit 1
        fi
        process_service "$target" "$variant" "$force"
    fi
}

main "$@"
