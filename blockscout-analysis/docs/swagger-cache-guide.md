# Swagger Cache Guide

Swagger files are the primary source of truth for PRO API and service endpoint documentation. They are large (up to 10,000+ lines), so this skill caches them locally and provides grep-friendly indices for fast endpoint discovery.

## Supported Services

| Service | Swagger Repo Location | Version Source |
|---------|----------------------|---------------|
| blockscout | `blockscout/{version}/default/swagger.yaml` | GitHub `blockscout/blockscout` releases |
| bens | `services/bens/{version}/swagger.yaml` | GitHub `blockscout/blockscout-rs` releases (`bens/v*`) |
| metadata | `services/metadata/{version}/swagger.yaml` | `hosted_versions.txt` in swaggers repo |
| stats | `services/stats/{version}/swagger.yaml` | GitHub `blockscout/blockscout-rs` releases (`stats/v*`) |
| multichain-aggregator | `services/multichain-aggregator/{version}/swagger.yaml` | GitHub `blockscout/blockscout-rs` releases (`multichain-aggregator/v*`) |

All swagger files are in the [blockscout/swaggers](https://github.com/blockscout/swaggers) repository.

## Fetching Swaggers

Use `scripts/fetch-swagger.sh` to download and cache swagger files:

```bash
# Fetch a single service
./scripts/fetch-swagger.sh blockscout

# Fetch all services
./scripts/fetch-swagger.sh --all

# Force re-download (skip freshness check)
./scripts/fetch-swagger.sh --all --force

# Fetch a chain-specific variant (blockscout only)
./scripts/fetch-swagger.sh blockscout --variant arbitrum
```

The script checks freshness against the latest GitHub release for each service. If the cached version matches, it skips the download.

## Indexing Swaggers

Use `scripts/index-swagger.py` to build compact, grep-friendly indices:

```bash
# Index a single file
./scripts/index-swagger.py cache/swagger/blockscout/swagger.yaml --output cache/swagger/blockscout/swagger.index

# Index all cached swaggers
./scripts/index-swagger.py --batch
```

## Using the Index

The index format is:

```
METHOD /path | summary_or_operationId | line_start-line_end
```

**Workflow to discover an endpoint:**

1. **Search the index** for keywords:
   ```
   grep -i "token" cache/swagger/blockscout/swagger.index
   ```
   Result:
   ```
   GET /v2/tokens/{address_hash_param} | getToken | 4562-4617
   GET /v2/tokens/{address_hash_param}/holders | getTokenHolders | 4618-4748
   ```

2. **Extract the line range** from the matching line (e.g. `4562-4617`).

3. **Read only that range** from the cached swagger:
   ```
   sed -n '4562,4617p' cache/swagger/blockscout/swagger.yaml
   ```
   This gives you the full endpoint declaration: parameters, request/response schemas, description — without loading the entire 10,000+ line file.

## Freshness Checking

The `fetch-swagger.sh` script stores version metadata in `cache/swagger/version.json`:

```json
{
  "blockscout": {"version": "9.3.5", "fetched_at": "2026-02-18T12:00:00Z"},
  "bens": {"version": "1.6.4", "fetched_at": "2026-02-18T12:00:00Z"}
}
```

On each run, the script compares the cached version against the latest release on GitHub. Re-download occurs only when versions differ or `--force` is used.

## Cache Directory Structure

```
cache/swagger/
├── version.json
├── blockscout/
│   ├── swagger.yaml
│   └── swagger.index
├── bens/
│   ├── swagger.yaml
│   └── swagger.index
├── metadata/
│   ├── swagger.yaml
│   └── swagger.index
├── stats/
│   ├── swagger.yaml
│   └── swagger.index
└── multichain-aggregator/
    ├── swagger.yaml
    └── swagger.index
```

## Alternative: Direct API Probing

When the swagger cache is unavailable or stale, you can discover endpoint response shapes by making HTTP requests directly and inspecting the response. This is useful for quick checks but does not provide parameter documentation.
