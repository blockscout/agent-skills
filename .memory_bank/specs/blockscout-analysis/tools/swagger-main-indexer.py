#!/usr/bin/env python3
"""
Swagger Main Indexer for Blockscout API.

Discovers the latest Blockscout release, downloads all swagger variants from
the blockscout/swaggers repo, and builds a JSON endpoint index across all variants.

Usage:
    python swagger-main-indexer.py

Output:
    blockscout-analysis/.build/swaggers/main-indexer/endpoints_map.json
"""

import json
import sys
from pathlib import Path
from typing import Optional

import requests

from common import HTTP_METHODS, _get, find_line_ranges, index_swagger_file

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RELEASES_URL = "https://api.github.com/repos/blockscout/blockscout/releases"
SWAGGERS_CONTENTS_URL = "https://api.github.com/repos/blockscout/swaggers/contents/blockscout/{version}"
SWAGGER_RAW_URL = "https://raw.githubusercontent.com/blockscout/swaggers/master/blockscout/{version}/{variant}/swagger.yaml"

OUTPUT_DIR = Path("blockscout-analysis/.build/swaggers/main-indexer")
ENDPOINTS_MAP_PATH = OUTPUT_DIR / "endpoints_map.json"


# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------


def discover_latest_version() -> str:
    """Return the latest stable Blockscout release version string (e.g. '9.3.5')."""
    response = _get(RELEASES_URL, params={"per_page": 10})
    if response.status_code == 403:
        reset = response.headers.get("X-RateLimit-Reset", "unknown")
        print(f"Error: GitHub API rate limit exceeded. Resets at: {reset}")
        sys.exit(1)
    response.raise_for_status()

    for release in response.json():
        if not release.get("draft") and not release.get("prerelease"):
            tag = release["tag_name"]
            version = tag.lstrip("v")
            print(f"Discovered latest Blockscout release: {version}")
            return version

    print("Error: no stable Blockscout release found.")
    sys.exit(1)


def discover_variants(version: str) -> list[str]:
    """Return ordered list of swagger variant names, with 'default' first."""
    url = SWAGGERS_CONTENTS_URL.format(version=version)
    response = _get(url)
    if response.status_code == 404:
        print(f"Error: swagger folder for version {version} not found in blockscout/swaggers.")
        sys.exit(1)
    response.raise_for_status()

    entries = response.json()
    dirs = [e["name"] for e in entries if e.get("type") == "dir"]

    # Put 'default' first
    if "default" in dirs:
        dirs.remove("default")
        dirs.insert(0, "default")

    names_display = ", ".join(dirs)
    print(f"Found {len(dirs)} swagger variants: {names_display}")
    return dirs


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def download_swagger(version: str, variant: str, index: int, total: int) -> Optional[Path]:
    """Download swagger.yaml for a variant. Returns the saved path, or None on failure."""
    url = SWAGGER_RAW_URL.format(version=version, variant=variant)
    response = _get(url)
    if response.status_code == 404:
        print(f"[{index}/{total}] Warning: no swagger.yaml found for variant '{variant}', skipping.")
        return None
    if not response.ok:
        print(f"[{index}/{total}] Warning: HTTP {response.status_code} fetching {url}, skipping.")
        return None

    dest = OUTPUT_DIR / variant / "swagger.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(response.content)
    print(f"[{index}/{total}] Downloading {variant}/swagger.yaml ... done")
    return dest


def save_map(endpoint_map: list[dict]) -> None:
    ENDPOINTS_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENDPOINTS_MAP_PATH.write_text(
        json.dumps(endpoint_map, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print()

    # Step 1: Discover release
    version = discover_latest_version()

    # Step 2: Discover variants
    variants = discover_variants(version)
    total = len(variants)
    print()

    endpoint_map: list[dict] = []
    # Set of (endpoint, method) already in the map — for dedup
    seen: set[tuple[str, str]] = set()

    for idx, variant in enumerate(variants, start=1):
        # Step 3: Download
        swagger_path = download_swagger(version, variant, idx, total)
        if swagger_path is None:
            continue

        # Steps 4 & 5: Index
        records = index_swagger_file(swagger_path, f"{variant}/swagger.yaml")
        new_count = 0
        for rec in records:
            key = (rec["endpoint"], rec["method"])
            if key not in seen:
                seen.add(key)
                endpoint_map.append(rec)
                new_count += 1

        save_map(endpoint_map)

        if variant == "default":
            print(f"[{idx}/{total}] Indexing {variant}: {new_count} endpoints added ({len(endpoint_map)} total)")
        else:
            print(f"[{idx}/{total}] Indexing {variant}: {new_count} new endpoints ({len(endpoint_map)} total)")
        print(f"        Saved endpoints_map.json")
        print()

    print(f"Complete. {len(endpoint_map)} total endpoints indexed across {total} variants.")


if __name__ == "__main__":
    main()
