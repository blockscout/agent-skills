#!/usr/bin/env python3
"""
API File Generator for Blockscout endpoint maps.

Reads main-indexer and stats-service endpoint maps, classifies GET endpoints
into thematic Markdown API reference files, and writes a master index.

Usage (from repo root):
    python .memory_bank/specs/blockscout-analysis/tools/api-file-generator.py
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

MAIN_INDEXER_MAP = Path("blockscout-analysis/.build/swaggers/main-indexer/endpoints_map.json")
STATS_SERVICE_MAP = Path("blockscout-analysis/.build/swaggers/stats-service/endpoints_map.json")
MAIN_INDEXER_SWAGGER_DIR = Path("blockscout-analysis/.build/swaggers/main-indexer")
STATS_SERVICE_SWAGGER_DIR = Path("blockscout-analysis/.build/swaggers/stats-service")
REFERENCES_DIR = Path("blockscout-analysis/references")
API_DIR = REFERENCES_DIR / "blockscout-api"

# ---------------------------------------------------------------------------
# Classification config
# ---------------------------------------------------------------------------

# Default variant: prefix → output filename.
# Will be sorted by len(pfx.rstrip('/')) descending at module load time.
DEFAULT_PREFIXES: list[tuple[str, str]] = [
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
    ("/v2/withdrawals",           "ethereum.md"),      # validator withdrawals are PoS-specific
]

_SORTED_PREFIXES: list[tuple[str, str]] = sorted(
    DEFAULT_PREFIXES,
    key=lambda x: len(x[0].rstrip("/")),
    reverse=True,
)

# Fixed topic file ordering and display names.
# Note: withdrawals.md is intentionally absent — those endpoints route to ethereum.md.
TOPIC_FILE_ORDER: list[str] = [
    "blocks.md", "transactions.md", "addresses.md", "tokens.md",
    "smart-contracts.md", "search.md", "stats.md", "config.md",
]

# H3 heading for topic files (also used as index display name, except stats.md).
TOPIC_HEADINGS: dict[str, str] = {
    "blocks.md":          "Blocks",
    "transactions.md":    "Transactions",
    "addresses.md":       "Addresses",
    "tokens.md":          "Tokens",
    "smart-contracts.md": "Smart Contracts",
    "search.md":          "Search",
    "stats.md":           "Stats",        # index display name; file uses two H3s
    "config.md":          "Configuration",
}

# Stats.md section names.
STATS_CHAIN_SECTION = "Chain Statistics"
STATS_SERVICE_SECTION = "Stats Service"

# Chain-specific variant special-case configuration.
VARIANT_SPECIAL_CASES: dict[str, dict] = {
    "ethereum": {
        "filename": "ethereum.md",
        "heading":  "Ethereum PoS Chains",
        "preamble": (
            "These endpoints are only available on chains that use Ethereum "
            "proof-of-stake consensus, such as **Ethereum Mainnet** and **Gnosis Chain**. "
            "They expose beacon chain deposit tracking and EIP-4844 blob transaction data "
            "that do not exist on other EVM networks."
        ),
    },
    "optimism-celo": {
        "split": True,
        "celo_filename":     "celo.md",
        "celo_heading":      "Celo",
        "optimism_filename": "optimism.md",
        "optimism_heading":  "Optimism",
    },
    "polygon_zkevm": {"filename": "polygon-zkevm.md", "heading": "Polygon zkEVM"},
    "zksync":        {"filename": "zksync.md",         "heading": "ZkSync"},
}

# Reverse map: filename → {heading, preamble}
# Used when classify_default_endpoint() returns a chain-specific filename
# (e.g. ethereum.md for /v2/withdrawals endpoints).
_CHAIN_FILE_INFO: dict[str, dict] = {
    sc["filename"]: {"heading": sc["heading"], "preamble": sc.get("preamble")}
    for sc in VARIANT_SPECIAL_CASES.values()
    if not sc.get("split") and "filename" in sc
}

# Path parameter substitution heuristics for curl examples.
# Each entry: ([keyword, ...], replacement_value). First match wins.
PATH_PARAM_SUBSTITUTIONS: list[tuple[list[str], str]] = [
    (["address", "hash"], "0xabc..."),
    (["block", "number"], "1000000"),
    (["token_id"],        "1"),
    (["batch"],           "12345"),
]
PATH_PARAM_DEFAULT = "value"

# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------

def load_endpoint_map(path: Path) -> list[dict]:
    """Load a JSON endpoint map. Exits with code 1 on error."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: endpoint map not found: {path}")
        sys.exit(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"Error: malformed JSON in {path}: {exc}")
        sys.exit(1)


def load_swagger(path: Path, cache: dict) -> Optional[dict]:
    """Load and cache a swagger YAML. Returns None on any error (prints warning)."""
    key = str(path)
    if key in cache:
        return cache[key]
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Warning: swagger YAML not found: {path}")
        cache[key] = None
        return None
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        print(f"Warning: invalid YAML in {path}: {exc}")
        cache[key] = None
        return None
    if not isinstance(data, dict) or "paths" not in data:
        print(f"Warning: {path} has no 'paths' key or is not a dict, skipping.")
        cache[key] = None
        return None
    cache[key] = data
    return data

# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_default_endpoint(endpoint_path: str) -> Optional[str]:
    """
    Classify a default-variant swagger path using longest-prefix matching.
    Returns output filename, or None if unmatched (prints a warning).
    """
    for pfx, fname in _SORTED_PREFIXES:
        pfx_base = pfx.rstrip("/")
        if endpoint_path == pfx_base or endpoint_path.startswith(pfx_base + "/"):
            return fname
    print(f"Warning: default endpoint matches no prefix, skipping: {endpoint_path}")
    return None


def derive_variant_info(variant: str) -> dict:
    """
    Return {filename, heading, preamble} for a non-default, non-split variant.
    Applies VARIANT_SPECIAL_CASES first; auto-derives for unknown variants.
    """
    sc = VARIANT_SPECIAL_CASES.get(variant)
    if sc and not sc.get("split"):
        return {
            "filename": sc["filename"],
            "heading":  sc["heading"],
            "preamble": sc.get("preamble"),
        }
    # Auto-derive
    filename = variant.replace("_", "-") + ".md"
    heading = variant.replace("_", " ").replace("-", " ").title()
    return {"filename": filename, "heading": heading, "preamble": None}


def classify_records(
    main_records: list[dict],
    stats_records: list[dict],
) -> tuple[dict, dict]:
    """
    Filter to GET-only, transform paths, classify into output files.

    Returns:
        classified:  {filename: [enriched_record_dict, ...]}
        file_meta:   {filename: {display_name, preamble}}
    """
    classified: dict[str, list[dict]] = {}
    file_meta: dict[str, dict] = {}

    # Pre-populate topic file metadata.
    for fname in TOPIC_FILE_ORDER:
        classified[fname] = []
        file_meta[fname] = {
            "display_name": TOPIC_HEADINGS[fname],
            "preamble": None,
        }

    def _add(record: dict, fname: str, transformed: str, section: str) -> None:
        enriched = dict(record)
        enriched["transformed_path"] = transformed
        enriched["section_heading"] = section
        if fname not in classified:
            classified[fname] = []
        classified[fname].append(enriched)

    # Process main-indexer records.
    for rec in main_records:
        if rec.get("method") != "GET":
            continue
        endpoint = rec["endpoint"]
        # Skip CSV export endpoints and the CSV configuration endpoint.
        if endpoint.endswith("/csv") or endpoint == "/v2/config/csv-export":
            continue
        sf = rec["swagger_file"]
        transformed = "/api" + endpoint

        if sf == "default/swagger.yaml":
            fname = classify_default_endpoint(endpoint)
            if fname is None:
                continue
            # Determine section heading; handle chain-specific routing targets.
            if fname == "stats.md":
                section = STATS_CHAIN_SECTION
            elif fname in TOPIC_HEADINGS:
                section = TOPIC_HEADINGS[fname]
            else:
                # Default-variant endpoint routed to a chain-specific file
                # (currently only ethereum.md for /v2/withdrawals).
                info = _CHAIN_FILE_INFO.get(
                    fname,
                    {"heading": fname.replace(".md", "").replace("-", " ").title(), "preamble": None},
                )
                section = info["heading"]
                if fname not in file_meta:
                    file_meta[fname] = {"display_name": info["heading"], "preamble": info["preamble"]}
                if fname not in classified:
                    classified[fname] = []
            _add(rec, fname, transformed, section)

        elif sf.split("/")[0] == "optimism-celo":
            if "/celo" in endpoint:
                fname = "celo.md"
                heading = "Celo"
            else:
                fname = "optimism.md"
                heading = "Optimism"
            if fname not in file_meta:
                file_meta[fname] = {"display_name": heading, "preamble": None}
            _add(rec, fname, transformed, heading)

        else:
            variant = sf.split("/")[0]
            info = derive_variant_info(variant)
            fname = info["filename"]
            if fname not in file_meta:
                file_meta[fname] = {
                    "display_name": info["heading"],
                    "preamble": info["preamble"],
                }
            _add(rec, fname, transformed, info["heading"])

    # Process stats-service records.
    for rec in stats_records:
        if rec.get("method") != "GET":
            continue
        # Skip the /health endpoint — not useful for agent queries.
        if rec["endpoint"] == "/health":
            continue
        transformed = "/stats-service" + rec["endpoint"]
        enriched = dict(rec)
        enriched["transformed_path"] = transformed
        enriched["section_heading"] = STATS_SERVICE_SECTION
        enriched["_source"] = "stats-service"
        classified["stats.md"].append(enriched)

    return classified, file_meta

# ---------------------------------------------------------------------------
# Description resolution
# ---------------------------------------------------------------------------

def resolve_description(record: dict, swagger_path: Path, cache: dict) -> str:
    """Return description from record, falling back to swagger summary if empty."""
    desc = record.get("description", "")
    if desc:
        return desc
    swagger = load_swagger(swagger_path, cache)
    if swagger is None:
        return ""
    method_lower = record["method"].lower()
    method_obj = swagger.get("paths", {}).get(record["endpoint"], {}).get(method_lower, {})
    return method_obj.get("summary", "") or ""

# ---------------------------------------------------------------------------
# Parameter extraction
# ---------------------------------------------------------------------------

def _get_param_type(param: dict) -> str:
    """Resolve parameter type, supporting both OpenAPI 3.0 and Swagger 2.0."""
    schema = param.get("schema")
    if isinstance(schema, dict):
        t = schema.get("type")
        if t:
            return t
    return param.get("type") or "string"


def extract_parameters(
    record: dict,
    swagger_path: Path,
    cache: dict,
) -> Optional[list[dict]]:
    """
    Extract path and query parameters from swagger for this endpoint.
    Returns None on load failure or missing path/method (prints warning).
    Returns [] for endpoints with no path/query params.
    """
    swagger = load_swagger(swagger_path, cache)
    if swagger is None:
        return None

    endpoint = record["endpoint"]
    method_lower = record["method"].lower()
    paths = swagger.get("paths", {})

    path_obj = paths.get(endpoint)
    if path_obj is None:
        print(f"Warning: endpoint path not in swagger ({swagger_path}): {endpoint}")
        return None

    method_obj = path_obj.get(method_lower)
    if method_obj is None:
        print(f"Warning: method {record['method']} not in swagger for: {endpoint}")
        return None

    result = []
    for p in method_obj.get("parameters", []):
        param_in = p.get("in", "")
        if param_in not in ("path", "query"):
            continue
        name = p.get("name", "")
        type_str = _get_param_type(p)
        required = True if param_in == "path" else bool(p.get("required", False))
        description = p.get("description", "") or ""
        result.append({
            "name":        name,
            "param_in":    param_in,
            "required":    required,
            "type_str":    type_str,
            "description": description,
        })
    return result

# ---------------------------------------------------------------------------
# Example request generation
# ---------------------------------------------------------------------------

def _substitute_path_param(name: str) -> str:
    """Return a realistic placeholder for a path parameter."""
    name_lower = name.lower()
    for keywords, value in PATH_PARAM_SUBSTITUTIONS:
        if any(kw in name_lower for kw in keywords):
            return value
    return PATH_PARAM_DEFAULT


def _needs_example(params: Optional[list[dict]]) -> bool:
    """True if any parameter has type 'object' or 'array'."""
    if not params:
        return False
    return any(p["type_str"] in ("object", "array") for p in params)


def _build_curl(transformed_path: str) -> str:
    """Build a curl example with {base_url} placeholder, substituting path params."""
    def replace_param(m: re.Match) -> str:
        return _substitute_path_param(m.group(1))

    path = re.sub(r"\{([^}]+)\}", replace_param, transformed_path)
    return f'curl "{{base_url}}{path}"'

# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def _render_param_table(params: Optional[list[dict]]) -> str:
    """
    Render parameter table (indented two spaces) or '*None*'.
    """
    if not params:
        return "  *None*"
    lines = [
        "  | Name | Type | Required | Description |",
        "  | ---- | ---- | -------- | ----------- |",
    ]
    for p in params:
        req = "Yes" if p["required"] else "No"
        lines.append(
            f"  | `{p['name']}` | `{p['type_str']}` | {req} | {p['description']} |"
        )
    return "\n".join(lines)


def _render_endpoint_entry(record: dict, params: Optional[list[dict]]) -> str:
    """Render a full H4 endpoint block."""
    method = record["method"]
    path = record["transformed_path"]
    desc = record.get("_description", "")
    table = _render_param_table(params)

    lines = [f"#### {method} {path}", ""]
    if desc:
        lines += [desc, ""]
    lines += [
        "- **Parameters**",
        "",
        table,
    ]

    if _needs_example(params):
        curl = _build_curl(path)
        lines += [
            "",
            "- **Example Request**",
            "",
            "  ```bash",
            f"  {curl}",
            "  ```",
        ]

    lines.append("")
    return "\n".join(lines)


def _render_api_file(
    sections: dict,   # OrderedDict-like: {section_heading: [records]}
    preamble: Optional[str],
) -> str:
    """Render the full content of one API output file."""
    parts = ["## API Endpoints\n"]

    if preamble:
        parts.append(f"\n{preamble}\n")

    for section_heading, records in sections.items():
        parts.append(f"\n### {section_heading}\n")
        for rec in records:
            params = rec.get("_params")
            parts.append("\n" + _render_endpoint_entry(rec, params))

    return "".join(parts)


def _render_index_file(
    classified: dict,
    file_meta: dict,
    chain_files_sorted: list[str],
) -> str:
    """Render the master index Markdown file."""
    lines = [
        "# Blockscout API Endpoints Index",
        "",
        "Use this index to find available endpoints for the `direct_api_call` MCP tool."
        " Each section links to a dedicated API file with full parameter details.",
    ]

    def _add_section(fname: str) -> None:
        meta = file_meta.get(fname, {})
        display = meta.get("display_name", fname)
        preamble = meta.get("preamble")
        lines.append("")
        lines.append(f"## [{display}](blockscout-api/{fname})")
        lines.append("")
        if preamble:
            lines.append(preamble)
            lines.append("")
        records = _get_index_records(fname, classified)
        for rec in records:
            desc = rec.get("_description", "")
            path = rec["transformed_path"]
            lines.append(f"- `{path}`: {desc}")

    def _get_index_records(fname: str, classified: dict) -> list[dict]:
        """Return records for the index in file order (Chain Stats first for stats.md)."""
        all_recs = classified.get(fname, [])
        if fname == "stats.md":
            chain = [r for r in all_recs if r["section_heading"] == STATS_CHAIN_SECTION]
            service = [r for r in all_recs if r["section_heading"] == STATS_SERVICE_SECTION]
            return chain + service
        return all_recs

    # Topic files (always present).
    for fname in TOPIC_FILE_ORDER:
        _add_section(fname)

    # Chain-specific files (non-empty, alphabetical by filename).
    for fname in chain_files_sorted:
        _add_section(fname)

    lines.append("")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Swagger path resolution
# ---------------------------------------------------------------------------

def _resolve_swagger_path(record: dict) -> Path:
    """Return the Path to the swagger YAML for this record."""
    if record.get("_source") == "stats-service":
        return STATS_SERVICE_SWAGGER_DIR / "swagger.yaml"
    return MAIN_INDEXER_SWAGGER_DIR / record["swagger_file"]

# ---------------------------------------------------------------------------
# File writing
# ---------------------------------------------------------------------------

def _write_api_file(
    filename: str,
    classified: dict,
    file_meta: dict,
) -> None:
    """Build sections, render, and write one API file."""
    records = classified.get(filename, [])
    preamble = file_meta.get(filename, {}).get("preamble")

    if filename == "stats.md":
        sections = {
            STATS_CHAIN_SECTION: [r for r in records if r["section_heading"] == STATS_CHAIN_SECTION],
            STATS_SERVICE_SECTION: [r for r in records if r["section_heading"] == STATS_SERVICE_SECTION],
        }
    else:
        heading = file_meta.get(filename, {}).get("display_name") or TOPIC_HEADINGS.get(filename, filename)
        sections = {heading: records}

    content = _render_api_file(sections, preamble)
    (API_DIR / filename).write_text(content, encoding="utf-8")
    print(f"  Written: {filename}")

# ---------------------------------------------------------------------------
# Console output helpers
# ---------------------------------------------------------------------------

def _print_classification_summary(
    classified: dict,
    chain_files_sorted: list[str],
) -> None:
    """Print aligned classification counts."""
    all_files = list(TOPIC_FILE_ORDER) + chain_files_sorted
    max_len = max(len(f) for f in all_files) + 1  # +1 for the colon

    for fname in TOPIC_FILE_ORDER:
        records = classified.get(fname, [])
        count = len(records)
        label = fname + ":"
        if fname == "stats.md":
            chain_count = sum(1 for r in records if r["section_heading"] == STATS_CHAIN_SECTION)
            svc_count = sum(1 for r in records if r["section_heading"] == STATS_SERVICE_SECTION)
            endpoint_word = "endpoint" if count == 1 else "endpoints"
            print(f"  {label:<{max_len}} {count} {endpoint_word} ({chain_count} chain stats + {svc_count} stats service)")
        else:
            endpoint_word = "endpoint" if count == 1 else "endpoints"
            print(f"  {label:<{max_len}} {count} {endpoint_word}")

    for fname in chain_files_sorted:
        records = classified.get(fname, [])
        count = len(records)
        label = fname + ":"
        endpoint_word = "endpoint" if count == 1 else "endpoints"
        print(f"  {label:<{max_len}} {count} {endpoint_word}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # 1. Load endpoint maps.
    main_records = load_endpoint_map(MAIN_INDEXER_MAP)
    print(f"Reading main-indexer endpoint map: {len(main_records)} endpoints loaded")
    stats_records = load_endpoint_map(STATS_SERVICE_MAP)
    print(f"Reading stats-service endpoint map: {len(stats_records)} endpoints loaded")
    print()

    # 2. Classify (filter GET, transform paths, assign files).
    classified, file_meta = classify_records(main_records, stats_records)

    # Determine chain-specific files (non-topic, non-empty, sorted by filename).
    topic_set = set(TOPIC_FILE_ORDER)
    chain_files_sorted = sorted(
        fn for fn in classified if fn not in topic_set and classified[fn]
    )

    print("Classifying endpoints...")
    _print_classification_summary(classified, chain_files_sorted)

    # 3. Create output directories.
    API_DIR.mkdir(parents=True, exist_ok=True)

    # 4. Enrich records: resolve descriptions and extract parameters.
    swagger_cache: dict = {}
    all_filenames = list(TOPIC_FILE_ORDER) + chain_files_sorted
    for fname in all_filenames:
        for rec in classified.get(fname, []):
            swagger_path = _resolve_swagger_path(rec)
            rec["_description"] = resolve_description(rec, swagger_path, swagger_cache)
            rec["_params"] = extract_parameters(rec, swagger_path, swagger_cache)

    # 5. Sort records within each file.
    for fname in all_filenames:
        classified[fname].sort(key=lambda r: (r["transformed_path"].lower(), r["method"]))

    # 6. Write API files.
    print("\nWriting API files...")
    for fname in TOPIC_FILE_ORDER:
        _write_api_file(fname, classified, file_meta)
    for fname in chain_files_sorted:
        _write_api_file(fname, classified, file_meta)

    # 7. Write index file.
    total = sum(len(classified.get(fn, [])) for fn in all_filenames)
    print(f"\nWriting blockscout-api-index.md: {total} total endpoints")
    index_content = _render_index_file(classified, file_meta, chain_files_sorted)
    (REFERENCES_DIR / "blockscout-api-index.md").write_text(index_content, encoding="utf-8")

    print("\nDone.")


if __name__ == "__main__":
    main()
