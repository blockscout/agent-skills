#!/usr/bin/env python3
"""
Swagger Stats Indexer for Blockscout Stats service.

Discovers the latest Stats service release, downloads the Stats swagger file
from the blockscout/swaggers repo, and builds a JSON endpoint index.

Usage:
    python swagger-stats-indexer.py

Output:
    blockscout-analysis/.build/swaggers/stats-service/endpoints_map.json
"""

import json
import sys
from pathlib import Path

from common import _get, index_swagger_file

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RELEASES_URL = "https://api.github.com/repos/blockscout/blockscout-rs/releases"
SWAGGER_RAW_URL = (
    "https://raw.githubusercontent.com/blockscout/swaggers/master"
    "/services/stats/{version}/swagger.yaml"
)

OUTPUT_DIR = Path("blockscout-analysis/.build/swaggers/stats-service")
SWAGGER_PATH = OUTPUT_DIR / "swagger.yaml"
ENDPOINTS_MAP_PATH = OUTPUT_DIR / "endpoints_map.json"


# ---------------------------------------------------------------------------
# Release discovery
# ---------------------------------------------------------------------------

def discover_latest_stats_version() -> str:
    """Return the latest stable Stats release version string (e.g. '2.14.0')."""
    response = _get(RELEASES_URL, params={"per_page": 20})
    if response.status_code == 403:
        reset = response.headers.get("X-RateLimit-Reset", "unknown")
        print(f"Error: GitHub API rate limit exceeded. Resets at: {reset}")
        sys.exit(1)
    response.raise_for_status()

    for release in response.json():
        tag = release.get("tag_name", "")
        if (
            not release.get("draft")
            and not release.get("prerelease")
            and tag.startswith("stats/")
        ):
            version = tag[len("stats/v"):]
            print(f"Discovered latest Stats release: {version}")
            return version

    print("Error: no stable Stats release found in blockscout/blockscout-rs.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def download_swagger(version: str) -> None:
    """Download swagger.yaml for the given Stats version and save to OUTPUT_DIR."""
    url = SWAGGER_RAW_URL.format(version=version)
    print("Downloading swagger.yaml ...", end=" ", flush=True)
    response = _get(url)

    if response.status_code == 404:
        print()
        print(f"Error: swagger.yaml for Stats version {version} not found (HTTP 404).")
        sys.exit(1)
    if not response.ok:
        print()
        print(f"Error: HTTP {response.status_code} fetching {url}.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SWAGGER_PATH.write_bytes(response.content)
    print("done")


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_map(endpoint_map: list[dict]) -> None:
    """Write endpoint_map as indented JSON to ENDPOINTS_MAP_PATH."""
    ENDPOINTS_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENDPOINTS_MAP_PATH.write_text(
        json.dumps(endpoint_map, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # Step 1: Discover latest Stats release version
    version = discover_latest_stats_version()

    # Step 2: Download swagger.yaml
    download_swagger(version)
    print()

    # Step 3: Index endpoints
    records = index_swagger_file(SWAGGER_PATH, "swagger.yaml", fatal_on_error=True)
    count = len(records)
    print(f"Indexing endpoints: {count} endpoints indexed")

    # Step 4: Save
    save_map(records)
    print("Saved endpoints_map.json")
    print()
    print(f"Complete. {count} endpoints indexed.")


if __name__ == "__main__":
    main()
