#!/usr/bin/env python3
"""
Common utilities shared between swagger indexer and API file generation scripts.
"""

import re
import sys
from pathlib import Path
from typing import Optional

import requests
import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "head", "options"}

# ---------------------------------------------------------------------------
# Output paths
# ---------------------------------------------------------------------------

REFERENCES_DIR = Path("blockscout-analysis/references")
API_DIR = REFERENCES_DIR / "blockscout-api"

# ---------------------------------------------------------------------------
# Classification config
# ---------------------------------------------------------------------------

# Fixed topic file ordering and display names.
# Note: withdrawals.md is intentionally absent — those endpoints route to ethereum.md.
TOPIC_FILE_ORDER: list[str] = [
    "blocks.md", "transactions.md", "addresses.md", "tokens.md",
    "smart-contracts.md", "search.md", "stats.md", "config.md",
]

# Topic filename → display name / index heading.
# Note: stats.md maps to "Stats" (index display name); the file H3s are
# "Chain Statistics" and "Stats Service", handled by each consuming script.
TOPIC_HEADINGS: dict[str, str] = {
    "blocks.md":          "Blocks",
    "transactions.md":    "Transactions",
    "addresses.md":       "Addresses",
    "tokens.md":          "Tokens",
    "smart-contracts.md": "Smart Contracts",
    "search.md":          "Search",
    "stats.md":           "Stats",
    "config.md":          "Configuration",
}

# Chain-specific prefix table (Pass 1 in classification pipeline).
# Raw swagger paths (no /api prefix).
CHAIN_PREFIXES: list[tuple[str, str]] = [
    # Cross-cutting batch paths under topic prefixes
    ("/v2/blocks/arbitrum-batch/",       "arbitrum.md"),
    ("/v2/blocks/optimism-batch/",       "optimism.md"),
    ("/v2/blocks/scroll-batch/",         "scroll.md"),
    ("/v2/transactions/arbitrum-batch/", "arbitrum.md"),
    ("/v2/transactions/optimism-batch/", "optimism.md"),
    ("/v2/transactions/scroll-batch/",   "scroll.md"),
    ("/v2/transactions/zkevm-batch/",    "polygon-zkevm.md"),
    ("/v2/transactions/zksync-batch/",   "zksync.md"),
    # Main-page chain references
    ("/v2/main-page/arbitrum/",          "arbitrum.md"),
    ("/v2/main-page/optimism-deposits",  "optimism.md"),
    ("/v2/main-page/zksync/",            "zksync.md"),
    # Validators
    ("/v2/validators/stability",         "stability.md"),
    ("/v2/validators/zilliqa",           "zilliqa.md"),
    # Direct chain paths
    ("/v2/arbitrum/",                    "arbitrum.md"),
    ("/v2/beacon/",                      "ethereum.md"),
    ("/v2/celo/",                        "celo.md"),
    ("/v2/mud/",                         "mud.md"),
    ("/v2/optimism/",                    "optimism.md"),
    ("/v2/scroll/",                      "scroll.md"),
    ("/v2/shibarium/",                   "shibarium.md"),
    ("/v2/zkevm/",                       "polygon-zkevm.md"),
    ("/v2/zksync/",                      "zksync.md"),
    # Withdrawals (Ethereum PoS only)
    ("/v2/withdrawals",                  "ethereum.md"),
]

# Chain keyword rules (Pass 2 in classification pipeline).
# Match when a keyword appears as a path segment (between slashes).
CHAIN_KEYWORD_RULES: list[tuple[str, str]] = [
    ("celo",   "celo.md"),      # e.g. /v2/addresses/{addr}/celo/...
    ("beacon", "ethereum.md"),  # e.g. /v2/{base}/{param}/beacon/...
]

# Topic-file prefix table (Pass 3 in classification pipeline).
# Raw swagger paths (no /api prefix).
TOPIC_PREFIXES: list[tuple[str, str]] = [
    ("/v2/internal-transactions", "transactions.md"),  # top-level; block-scoped stays under /v2/blocks/
    ("/v2/blocks/",               "blocks.md"),
    ("/v2/token-transfers",       "tokens.md"),        # global token transfers belong with tokens
    ("/v2/transactions/",         "transactions.md"),
    ("/v2/addresses/",            "addresses.md"),
    ("/v2/tokens/",               "tokens.md"),
    ("/v2/smart-contracts/",      "smart-contracts.md"),
    ("/v2/search/",               "search.md"),
    ("/v1/search",                "search.md"),
    ("/v2/stats",                 "stats.md"),
    ("/v2/main-page/",            "stats.md"),
    ("/v2/config/",               "config.md"),
]

# Chain file heading/preamble overrides keyed by output filename.
# When no override exists, heading is auto-derived from the filename.
CHAIN_FILE_CONFIG: dict[str, dict] = {
    "ethereum.md": {
        "heading": "Ethereum PoS Chains",
        "preamble": (
            "These endpoints are only available on chains that use Ethereum "
            "proof-of-stake consensus, such as **Ethereum Mainnet** and **Gnosis Chain**. "
            "They expose beacon chain deposit tracking and EIP-4844 blob transaction data "
            "that do not exist on other EVM networks."
        ),
    },
    "polygon-zkevm.md": {"heading": "Polygon zkEVM"},
    "zksync.md":         {"heading": "ZkSync"},
}

# ---------------------------------------------------------------------------
# Classification functions
# ---------------------------------------------------------------------------

def sort_prefixes(table: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Sort a prefix table by descending stripped length (longest match first)."""
    return sorted(table, key=lambda x: len(x[0].rstrip("/")), reverse=True)


# Pre-sorted tables (used internally by classify_endpoint).
_SORTED_CHAIN_PREFIXES = sort_prefixes(CHAIN_PREFIXES)
_SORTED_TOPIC_PREFIXES = sort_prefixes(TOPIC_PREFIXES)


def classify_endpoint(endpoint: str) -> Optional[str]:
    """
    Unified path-based classification pipeline on a raw swagger path.

    Pass 1 — Chain-specific prefix (longest match first).
    Pass 2 — Chain keyword in path segments, plus /blobs suffix rule.
    Pass 3 — Topic prefix (longest match first).

    Returns output filename, or None if no rule matched.
    """
    # Pass 1: Chain-specific prefix
    for pfx, fname in _SORTED_CHAIN_PREFIXES:
        pfx_base = pfx.rstrip("/")
        if endpoint == pfx_base or endpoint.startswith(pfx_base + "/"):
            return fname

    # Pass 2: Chain keyword in path segments
    segments = endpoint.split("/")
    for keyword, fname in CHAIN_KEYWORD_RULES:
        if keyword in segments:
            return fname
    if endpoint.endswith("/blobs"):
        return "ethereum.md"

    # Pass 3: Topic prefix
    for pfx, fname in _SORTED_TOPIC_PREFIXES:
        pfx_base = pfx.rstrip("/")
        if endpoint == pfx_base or endpoint.startswith(pfx_base + "/"):
            return fname

    return None


def chain_file_info(filename: str) -> dict:
    """
    Return {heading, preamble} for a chain-specific output file.
    Uses CHAIN_FILE_CONFIG overrides; auto-derives heading from filename otherwise.
    """
    cfg = CHAIN_FILE_CONFIG.get(filename, {})
    heading = cfg.get("heading") or filename.replace(".md", "").replace("-", " ").title()
    preamble = cfg.get("preamble")
    return {"heading": heading, "preamble": preamble}


def heading_for(filename: str) -> str:
    """
    Return the primary H3 section heading for any output file.

    For topic files: returns the canonical H3 heading.
    For chain files: uses CHAIN_FILE_CONFIG overrides or auto-derives from filename.

    Note: stats.md returns "Chain Statistics" (the primary H3 section).
    The "Stats Service" section is handled by each consuming script individually.
    """
    # Check CHAIN_FILE_CONFIG first (handles ethereum.md, polygon-zkevm.md, zksync.md)
    cfg = CHAIN_FILE_CONFIG.get(filename, {})
    if "heading" in cfg:
        return cfg["heading"]
    # Topic files
    if filename in TOPIC_HEADINGS:
        if filename == "stats.md":
            return "Chain Statistics"
        return TOPIC_HEADINGS[filename]
    # Auto-derive for unknown chain files
    return filename.replace(".md", "").replace("-", " ").title()


def format_index_line(path: str, desc: str) -> str:
    """
    Format a single index line item.
    Omits colon and description when desc is empty (no trailing whitespace).
    """
    if desc:
        return f"- `{path}`: {desc}"
    return f"- `{path}`"


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
