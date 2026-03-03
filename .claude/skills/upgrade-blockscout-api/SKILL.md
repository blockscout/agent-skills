---
name: upgrade-blockscout-api
description: "Upgrade the blockscout-analysis skill's API reference files to the latest Blockscout backend and Stats service releases. Run when a new Blockscout version is issued to refresh swagger data, regenerate endpoint documentation, patch MCP-sourced and JSON-RPC endpoints, and remove MCP-duplicated entries."
disable-model-invocation: true
allowed-tools: Bash(python3 *), Bash(git *), Read, Edit, Grep, Glob
---

# Upgrade Blockscout API

Refresh the `blockscout-analysis` skill's API reference files to match the latest Blockscout backend release. The upgrade runs a 5-step sequential pipeline that downloads new swagger definitions, regenerates endpoint documentation, and applies patches.

## Prerequisites

- Python >= 3.9 with `pyyaml` and `requests` packages installed
- Network access to GitHub API (`api.github.com`, `raw.githubusercontent.com`) and Blockscout MCP (`mcp.blockscout.com`)
- Working directory must be the repository root (parent of `blockscout-analysis/`)

## Pipeline

Run every step in order. Each step depends on the output of the previous one. If a script fails, fix the issue before proceeding to the next step.

### Step 1 — Swagger Acquisition

Download swagger files for the latest Blockscout backend and Stats service releases.

```bash
python3 .memory_bank/specs/blockscout-analysis/tools/swagger-main-indexer.py
```

```bash
python3 .memory_bank/specs/blockscout-analysis/tools/swagger-stats-indexer.py
```

The **main indexer** discovers the latest stable release from `github.com/blockscout/blockscout/releases`, downloads all swagger variants (one per chain type), and writes `blockscout-analysis/.build/swaggers/main-indexer/endpoints_map.json`.

The **stats indexer** discovers the latest stats release from `github.com/blockscout/blockscout-rs/releases` (tag prefix `stats/`), downloads the stats swagger, and writes `blockscout-analysis/.build/swaggers/stats-service/endpoints_map.json`.

Both scripts print progress to stdout. Verify that each prints a "Complete" summary before moving on.

### Step 2 — Generate API Reference Files

```bash
python3 .memory_bank/specs/blockscout-analysis/tools/api-file-generator.py
```

Reads both endpoint maps from Step 1, classifies endpoints into thematic files, and **overwrites** all files under `blockscout-analysis/references/blockscout-api/` and the master index at `blockscout-analysis/references/blockscout-api-index.md`.

This step is destructive to existing reference files — patches applied by Steps 3–5 from a previous run are erased and must be reapplied.

### Step 3 — MCP Unlock Patch

```bash
python3 .memory_bank/specs/blockscout-analysis/tools/mcp-unlock-patch.py
```

Fetches the live `unlock_blockchain_analysis` MCP tool response from `https://mcp.blockscout.com/v1/unlock_blockchain_analysis`, identifies endpoints absent from the swagger-generated files, and patches them into the appropriate reference files and the master index.

### Step 4 — JSON-RPC Endpoint Patch

This step adds two Etherscan-compatible JSON-RPC endpoints that have no swagger source.

**Before making any changes**, read `.memory_bank/specs/blockscout-analysis/rpc-api-patch-spec.md` in full. It is the canonical source for the exact endpoint entries, parameter tables, section preamble, and index line items. Then apply the changes it defines:

1. **`GET /api?module=logs&action=getLogs`** — add to `blockscout-analysis/references/blockscout-api/transactions.md` under a `### JSON-RPC Compatibility` section.
2. **`GET /api?module=account&action=eth_get_balance`** — add to `blockscout-analysis/references/blockscout-api/addresses.md` under a `### JSON-RPC Compatibility` section.

If the `### JSON-RPC Compatibility` section does not exist in a target file, create it at the end of the file with the preamble text defined in the spec (Section 4).

Also add corresponding line items to the master index (`blockscout-analysis/references/blockscout-api-index.md`) in the Transactions and Addresses sections. The exact line item text is in Section 6 of the spec.

**Idempotency**: Before inserting any entry, check whether it already exists — scan for the `#### GET /api?module=...` heading in the topic file and the `` - `/api?module=...` `` line item in the index. Skip entries that are already present.

### Step 5 — Remove MCP-Duplicated Endpoints

Remove endpoints that duplicate dedicated MCP tools. Keeping them would mislead agents into using `direct_api_call` instead of the enriched dedicated tool.

**Before making any changes**, read `.memory_bank/specs/blockscout-analysis/mcp-duplicate-removal-spec.md` in full. It is the canonical source for which endpoints to remove, the removal scope in topic files, and the corresponding index updates. Then apply the changes it defines:

For each endpoint listed in the spec:

1. **Topic file**: Find the `#### GET <path>` heading and remove the entire entry — heading, description, and parameter table — up to the next `####`, `###`, or `##` heading (or end of file). Clean up any resulting double-blank-lines so remaining entries stay contiguous.
2. **Master index** (`references/blockscout-api-index.md`): Remove the line item starting with `` - `<path>`: `` from the matching section.

**Idempotency**: If an entry is already absent, skip it silently.

## Verification

After completing all five steps, confirm:

1. `blockscout-analysis/references/blockscout-api-index.md` exists and lists endpoints grouped by category.
2. Topic files in `blockscout-analysis/references/blockscout-api/` contain endpoint entries with parameter tables.
3. `addresses.md` does **not** contain `#### GET /api/v2/addresses/{address_hash_param}`.
4. `blocks.md` does **not** contain `#### GET /api/v2/blocks/{block_hash_or_number_param}`.
5. `transactions.md` does **not** contain `#### GET /api/v2/transactions/{transaction_hash_param}`.
6. `transactions.md` **does** contain `#### GET /api?module=logs&action=getLogs` under `### JSON-RPC Compatibility`.
7. `addresses.md` **does** contain `#### GET /api?module=account&action=eth_get_balance` under `### JSON-RPC Compatibility`.
8. Running any step a second time produces no changes (all steps are idempotent).

## Pipeline Reference

| Step | Method | Specification |
|------|--------|---------------|
| 1. Swagger acquisition | Script | `.memory_bank/specs/blockscout-analysis/swagger-main-indexer-spec.md`, `swagger-stats-indexer-spec.md` |
| 2. File generation | Script | `.memory_bank/specs/blockscout-analysis/api-file-generator-spec.md` |
| 3. MCP unlock patch | Script | `.memory_bank/specs/blockscout-analysis/mcp-unlock-patch-spec.md` |
| 4. JSON-RPC patch | Manual | `.memory_bank/specs/blockscout-analysis/rpc-api-patch-spec.md` |
| 5. Duplicate removal | Manual | `.memory_bank/specs/blockscout-analysis/mcp-duplicate-removal-spec.md` |

Full pipeline overview: `.memory_bank/specs/blockscout-analysis/blockscout-api-composition-spec.md`
