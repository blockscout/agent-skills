# API File Generator Script Specification

## 1. Purpose

A utility script that reads the endpoint maps produced by the swagger indexer scripts, classifies every endpoint into thematic API description files, and generates a master index file. The output files follow the format defined in `api-format-spec.md` and serve as the entry point for agents to discover which `direct_api_call` endpoints are available on the Blockscout MCP server.

## 2. Input Sources

| Source | Path |
|--------|------|
| Main indexer endpoint map | `blockscout-analysis/.build/swaggers/main-indexer/endpoints_map.json` |
| Stats service endpoint map | `blockscout-analysis/.build/swaggers/stats-service/endpoints_map.json` |
| Main indexer swagger files | `blockscout-analysis/.build/swaggers/main-indexer/{variant}/swagger.yaml` |
| Stats service swagger file | `blockscout-analysis/.build/swaggers/stats-service/swagger.yaml` |

Both endpoint map files are JSON arrays whose records follow the schema defined in the swagger indexer specifications. Key fields used by this script: `swagger_file`, `endpoint`, `method`, `description`, `start_line`, `end_line`.

## 3. Output File Layout

Per the Agent Skills specification, documentation files that agents load on demand belong in the `references/` directory. The index file sits at the `references/` root (one level deep from `SKILL.md`); the individual API files live one level deeper in `references/blockscout-api/`. Both names include the `blockscout-api` prefix to distinguish Blockscout instance REST API endpoints from the MCP server's own tool interface.

```
blockscout-analysis/
  references/
    blockscout-api-index.md   # Master entry point: all endpoints with descriptions, links to blockscout-api/ files
    blockscout-api/
      blocks.md             # Block and block-scoped sub-endpoints
      transactions.md       # Transaction, internal-transaction, and global token-transfer endpoints
      addresses.md          # Address endpoints
      tokens.md             # Token, NFT, and global token-transfer listing endpoints
      smart-contracts.md    # Smart contract endpoints
      search.md             # Search endpoints
      stats.md              # Chain statistics (main-page + stats) and Stats Service endpoints
      config.md             # Configuration endpoints (excluding CSV configuration)
      {chain}.md            # One file per chain-specific group identified by path classification
                            # (see Section 6.1 for the classification pipeline)
```

The **eight** topic files (`blocks.md` through `config.md`) and `stats.md` are always produced. There is no standalone `withdrawals.md` — validator withdrawal endpoints (`/v2/withdrawals`, `/v2/withdrawals/counters`) are classified to `ethereum.md` because they are specific to Ethereum proof-of-stake networks.

Chain-specific files are produced dynamically by path-based classification (Section 6.1). Adding new chain-prefixed endpoints or new swagger variants automatically produces new files without any script changes.

- The `references/` and `references/blockscout-api/` directories must be created if they do not exist.
- Before writing any files, **remove all existing `.md` files** from `references/blockscout-api/`. This ensures files created by a previous `mcp-unlock-patch.py` run (which the generator does not produce) do not survive and accumulate stale entries across generator–patch cycles.
- All output files are then written fresh on each run (idempotent operation).
- Encoding: UTF-8 for all files.

## 4. Path Transformation Rules

Each endpoint record in the map stores the raw swagger path. The script must transform it before writing to output files:

### 4.1 Main Indexer Endpoints

Prepend `/api` to the swagger endpoint path.

Since main-indexer swagger paths begin with `/v2/` or `/v1/`, the transformed paths will start with `/api/v2/` or `/api/v1/` respectively.

| Swagger path | Transformed path |
|---|---|
| `/v2/blocks/{block_hash_or_number_param}` | `/api/v2/blocks/{block_hash_or_number_param}` |
| `/v1/search` | `/api/v1/search` |

### 4.2 Stats Service Endpoints

Prepend `/stats-service` to the swagger endpoint path.

| Swagger path | Transformed path |
|---|---|
| `/api/v1/counters` | `/stats-service/api/v1/counters` |
| `/api/v1/lines/{name}` | `/stats-service/api/v1/lines/{name}` |

Note: the `/health` path from the stats-service map is excluded by the filter in Section 6.0 and therefore never transformed or written to any output file.

## 5. Shared Classification Module (`common.py`)

The classification tables and core classification function are defined in the shared module `common.py` (`.memory_bank/specs/blockscout-analysis/tools/common.py`) so that both `api-file-generator.py` and `mcp-unlock-patch.py` operate on a single source of truth. This prevents the two scripts from drifting when prefix tables or heading overrides are updated.

### 5.0a Shared Constants

`common.py` exports the following classification data:

| Constant | Description |
|----------|-------------|
| `REFERENCES_DIR` | `Path("blockscout-analysis/references")` |
| `API_DIR` | `REFERENCES_DIR / "blockscout-api"` |
| `TOPIC_FILE_ORDER` | Ordered list of 8 canonical topic filenames |
| `TOPIC_HEADINGS` | Topic filename → display name / default H3 heading (stats.md maps to `"Stats"`) |
| `CHAIN_PREFIXES` | Pass 1 chain prefix table — raw swagger paths (no `/api` prefix), 24 entries |
| `CHAIN_KEYWORD_RULES` | Pass 2 keyword-in-segment rules (`celo`, `beacon`) |
| `TOPIC_PREFIXES` | Pass 3 topic prefix table — raw swagger paths, 12 entries |
| `CHAIN_FILE_CONFIG` | Chain file heading/preamble overrides (`ethereum.md`, `polygon-zkevm.md`, `zksync.md`) |

All prefix tables store raw swagger paths (e.g. `/v2/blocks/arbitrum-batch/`). The MCP unlock patch derives `/api`-prefixed variants at module load time.

### 5.0b Shared Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `sort_prefixes(table)` | `list[tuple[str,str]] → list[tuple[str,str]]` | Sort a prefix table by descending stripped length (longest match first) |
| `classify_endpoint(endpoint)` | `str → Optional[str]` | Unified 3-pass pipeline (chain prefix → keyword → topic prefix) on a raw swagger path; returns output filename or None |
| `chain_file_info(filename)` | `str → dict` | Return `{heading, preamble}` for a chain file, using `CHAIN_FILE_CONFIG` overrides or auto-deriving from filename |
| `heading_for(filename)` | `str → str` | Return H3 heading for any file (topic or chain), combining `TOPIC_HEADINGS`, `CHAIN_FILE_CONFIG`, and auto-derive |
| `format_index_line(path, desc)` | `(str, str) → str` | Format `` - `{path}`: {desc} `` or `` - `{path}` `` (omits colon when desc is empty) |

Scripts import these and use them directly. Script-specific constants (e.g. `STATS_CHAIN_SECTION`, `COMMON_GROUP_MAP`) remain in the consuming script.

## 6. Endpoint Classification

### 6.0 Endpoint Exclusion Filters

Applied in order, **before classification**. Excluded records are silently dropped (no warning).

1. **Method filter:** Skip all records where `method` is not `GET`. Applies to both endpoint maps.
2. **CSV export filter:** Skip main-indexer records whose swagger path ends with `/csv` (e.g., `/v2/addresses/{addr}/transactions/csv`). These bulk export endpoints are not useful for agent queries.
3. **CSV configuration filter:** Skip the main-indexer record with path `/v2/config/csv-export` exactly.
4. **Stats-service health filter:** Skip the stats-service record with path `/health` exactly.

Every remaining endpoint is assigned to exactly one output file. No endpoint appears in more than one file.

### 6.1 Unified Path-Based Classification (Main Indexer)

All main-indexer endpoints are classified by their **endpoint path** using `classify_endpoint()` from `common.py`, regardless of which swagger variant contributed them. This avoids misrouting when a single swagger variant bundles endpoints from multiple feature families (e.g., the `mud` variant containing both `/v2/mud/` and `/v2/optimism/` paths).

Classification runs a 5-pass pipeline. The first pass to match wins. Passes 1–3 are implemented in `classify_endpoint()` using the shared tables from `common.py`; Passes 4–5 are handled by the calling script.

#### Pass 1 — Chain-specific prefix (longest match first)

The chain prefix table is checked before topic prefixes so chain-scoped paths always route to their chain file even when a topic prefix would also match (e.g., `/v2/blocks/optimism-batch/` matches the `blocks/` topic prefix but must go to `optimism.md`).

| Swagger path prefix | Output file | Notes |
|---------------------|-------------|-------|
| `/v2/blocks/arbitrum-batch/` | `arbitrum.md` | Cross-cutting batch path |
| `/v2/blocks/optimism-batch/` | `optimism.md` | Cross-cutting batch path |
| `/v2/blocks/scroll-batch/` | `scroll.md` | Cross-cutting batch path |
| `/v2/transactions/arbitrum-batch/` | `arbitrum.md` | Cross-cutting batch path |
| `/v2/transactions/optimism-batch/` | `optimism.md` | Cross-cutting batch path |
| `/v2/transactions/scroll-batch/` | `scroll.md` | Cross-cutting batch path |
| `/v2/transactions/zkevm-batch/` | `polygon-zkevm.md` | Cross-cutting batch path |
| `/v2/transactions/zksync-batch/` | `zksync.md` | Cross-cutting batch path |
| `/v2/main-page/arbitrum/` | `arbitrum.md` | Main-page chain reference |
| `/v2/main-page/optimism-deposits` | `optimism.md` | Main-page chain reference |
| `/v2/main-page/zksync/` | `zksync.md` | Main-page chain reference |
| `/v2/validators/stability` | `stability.md` | Chain-specific validators |
| `/v2/validators/zilliqa` | `zilliqa.md` | Chain-specific validators |
| `/v2/arbitrum/` | `arbitrum.md` | Direct chain path |
| `/v2/beacon/` | `ethereum.md` | Beacon chain deposit data |
| `/v2/celo/` | `celo.md` | Direct chain path |
| `/v2/mud/` | `mud.md` | Direct chain path |
| `/v2/optimism/` | `optimism.md` | Direct chain path |
| `/v2/scroll/` | `scroll.md` | Direct chain path |
| `/v2/shibarium/` | `shibarium.md` | Direct chain path |
| `/v2/zkevm/` | `polygon-zkevm.md` | Direct chain path |
| `/v2/zksync/` | `zksync.md` | Direct chain path |
| `/v2/withdrawals` | `ethereum.md` | PoS validator withdrawals |

Prefix matching uses the same algorithm as Pass 3 (Section 6.2): strip trailing `/`, compare `p == pfx_base` or `p.startswith(pfx_base + '/')`, test longest first.

#### Pass 2 — Chain keyword in path segments

For endpoints not matched by Pass 1, check whether a chain keyword appears as a path segment (between slashes):

| Keyword | Output file | Example matches |
|---------|-------------|-----------------|
| `celo` | `celo.md` | `/v2/addresses/{addr}/celo/election-rewards`, `/v2/config/celo` |
| `beacon` | `ethereum.md` | `/v2/{base}/{param}/beacon/...` |

Additionally, if the path ends with `/blobs`, route to `ethereum.md` (EIP-4844 blob transaction data).

#### Pass 3 — Topic prefix

See Section 6.2.

#### Pass 4 — Variant name fallback

If Passes 1–3 found no match **and** the endpoint's `swagger_file` is not `default/swagger.yaml`, fall back to auto-deriving the output filename from the variant name:

- **Output filename:** `{variant_name.replace('_', '-')}.md`
- **H3 heading:** title-case of the variant name with underscores and hyphens replaced by spaces

This ensures new variants produce output files without code changes.

#### Pass 5 — Unknown (skip)

If the endpoint is from `default/swagger.yaml` and Passes 1–3 found no match, print a warning and skip it.

#### Chain file heading/preamble overrides

The `CHAIN_FILE_CONFIG` constant in `common.py` overrides the auto-derived heading and/or adds a preamble for chain files that need custom treatment:

| Output file | Override |
|-------------|----------|
| `ethereum.md` | Heading: `Ethereum PoS Chains`; Preamble: see Section 10.3 |
| `polygon-zkevm.md` | Heading: `Polygon zkEVM` (auto-derive produces `Polygon Zkevm`) |
| `zksync.md` | Heading: `ZkSync` (auto-derive produces `Zksync`) |

When no override exists for a chain file, the heading is auto-derived from the filename: `filename.replace('.md', '').replace('-', ' ').title()`. The `heading_for()` function in `common.py` encapsulates this logic.

### 6.2 Topic-File Prefix Table (Pass 3)

This pass runs only after the chain-specific passes (1 and 2) found no match. It classifies endpoints into the eight fixed topic files by longest matching prefix on the raw swagger path (before transformation). The table is defined as `TOPIC_PREFIXES` in `common.py`.

| Swagger path prefix | Output file | Notes |
|---------------------|-------------|-------|
| `/v2/blocks/` | `blocks.md` | Block-scoped sub-endpoints |
| `/v2/internal-transactions` | `transactions.md` | Top-level internal-tx list |
| `/v2/transactions/` | `transactions.md` | |
| `/v2/token-transfers` | `tokens.md` | Global token-transfer list belongs with tokens |
| `/v2/addresses/` | `addresses.md` | |
| `/v2/tokens/` | `tokens.md` | |
| `/v2/smart-contracts/` | `smart-contracts.md` | |
| `/v2/search/` | `search.md` | |
| `/v1/search` | `search.md` | |
| `/v2/stats` | `stats.md` | |
| `/v2/main-page/` | `stats.md` | |
| `/v2/config/` | `config.md` | |

Note: `/v2/withdrawals` is **not** in this table — it is handled by Pass 1 (chain prefix) which routes it to `ethereum.md`.

Note: `/v2/main-page/` is checked in Pass 3 because Passes 1–2 already claimed chain-specific main-page paths (e.g., `/v2/main-page/arbitrum/`); the remaining generic main-page endpoints correctly fall through to `stats.md`.

Prefix matching algorithm: For each prefix `pfx` in the table, compute `pfx_base = pfx.rstrip('/')`. A path `p` matches this prefix if `p == pfx_base` or `p.startswith(pfx_base + '/')`. Test prefixes in order from longest `pfx_base` to shortest. Use the first match.

This handles both base paths (e.g., `/v2/blocks` matches prefix `/v2/blocks/` because `p == pfx_base`) and sub-paths (e.g., `/v2/blocks/{hash}` matches because `p.startswith('/v2/blocks/')`).

### 6.3 Stats Service Endpoints

All surviving records (after Section 6.0 filters) from `blockscout-analysis/.build/swaggers/stats-service/endpoints_map.json` are classified to `stats.md`, regardless of path.

### 6.4 Unknown Endpoints

If a `default/swagger.yaml` endpoint is not matched by any of Passes 1–3, print a warning to stdout and skip it (Pass 5). It will not appear in any output file or in the index.

If a non-default endpoint is not matched by Passes 1–3, apply the variant name fallback (Pass 4) — auto-derive the output filename from the swagger variant directory name. No non-default endpoint is ever silently dropped.

## 7. Description Extraction

The `description` field in each endpoint map record holds the full text from the swagger method's `description` field. For stats-service endpoints this field is consistently empty (the stats swagger does not use `description`).

When the `description` field is an empty string, the script must fall back to the swagger YAML file and read the `summary` field of the corresponding method. Procedure:

1. Load the swagger YAML file (see Section 8 for loading rules).
2. Navigate to `data['paths'][swagger_path][http_method_lowercase]`.
3. Read the `summary` field. If present and non-empty, use it as the description.
4. If `summary` is also absent or empty, use an empty string.

Descriptions must be stored and written **in full without any truncation**, regardless of length. This applies to the API files and to the index file.

## 8. Parameter Extraction

The endpoint map records do not include parameter details. For each endpoint, the script must load the corresponding swagger YAML file and extract parameters.

### 8.1 Loading Swagger Files

- Load each swagger YAML file at most once per script run; cache the parsed object in memory keyed by its path.
- Parse using `yaml.safe_load()`.
- The swagger YAML path is derived from the endpoint map's `swagger_file` field:
  - Main indexer: `blockscout-analysis/.build/swaggers/main-indexer/{swagger_file}`
  - Stats service: `blockscout-analysis/.build/swaggers/stats-service/{swagger_file}`

### 8.2 Navigating to the Method Object

```
method_obj = data['paths'][swagger_endpoint_path][http_method_lowercase]
```

Where `http_method_lowercase` is the `method` field from the endpoint map converted to lowercase (e.g., `"GET"` → `"get"`).

If the path or method key is absent, treat the endpoint as having no parameters and write `*None*` in the parameters section (print a warning).

### 8.3 URL Parameters

Extract from `method_obj.get('parameters', [])`.

For each entry where `in` is `path` or `query`:

| Source field | Parameter table column | Notes |
|---|---|---|
| `name` | `Name` (backtick-wrapped) | |
| `in` | — | Used to determine Required for path params |
| `required` (boolean) | `Required` (`Yes`/`No`) | Path params (`in: path`) are always `Yes` regardless of this field |
| `schema.type` (OpenAPI 3.0) or `type` (Swagger 2.0) | `Type` (backtick-wrapped) | Fallback to `string` if absent |
| `description` | `Description` | Empty string if absent |

Skip entries where `in` is `header` or `cookie`.

### 8.4 Parameter Table Output

Produce a Markdown table following the `api-format-spec.md` schema:

```markdown
  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `param_name` | `string` | Yes | Description text. |
```

If the method has no parameters and no request body, write `*None*` instead of a table.

## 9. Example Request Section

Since only GET endpoints are processed (Section 6.0), include an **Example Request** section only when any extracted parameter has type `object` or `array`. For endpoints where all parameters are `string`, `integer`, or `boolean`, omit the section entirely.

When included, generate a `curl` command:

- Base URL: `{base_url}` placeholder (representing the chain's Blockscout hostname)
- Use the full transformed path (with `/api` or `/stats-service` prefix)
- Substitute path parameters with realistic placeholder values:
  - Address or hash: `0xabc...`
  - Block number: `1000000`
  - Token ID: `1`
  - Batch number: `12345`
  - Name/string: `usd` or a representative literal

## 10. API File Content Format

Each API output file follows the structure defined in `api-format-spec.md`.

### 10.1 General Structure

```markdown
## API Endpoints

### <Section Name>

#### METHOD /api/v2/path

Description text.

- **Parameters**

  <table or *None*>

- **Example Request** (when applicable)

  ```bash
  curl "..."
  ```
```

### 10.2 Section Names (H3)

**Topic files** use fixed H3 headings:

| Output file | H3 section name(s) |
|---|---|
| `blocks.md` | `### Blocks` |
| `transactions.md` | `### Transactions` |
| `addresses.md` | `### Addresses` |
| `tokens.md` | `### Tokens` |
| `smart-contracts.md` | `### Smart Contracts` |
| `search.md` | `### Search` |
| `stats.md` | `### Chain Statistics` followed by `### Stats Service` |
| `config.md` | `### Configuration` |

`stats.md` has two sections: `### Chain Statistics` contains endpoints from the main-indexer default variant (paths starting with `/v2/stats` and `/v2/main-page/`); `### Stats Service` contains all stats-service endpoints.

**Chain-specific files** use the H3 heading produced by the `CHAIN_FILE_CONFIG` override or auto-derived from the filename (Section 6.1). The heading is determined at classification time and stored alongside the endpoint records before any file is written.

### 10.3 Ethereum Preamble

The `ethereum.md` file must include an introductory paragraph immediately after the `## API Endpoints` heading and before the first `### Ethereum PoS Chains` section:

```
These endpoints are only available on chains that use Ethereum proof-of-stake consensus, such as **Ethereum Mainnet** and **Gnosis Chain**. They expose beacon chain deposit tracking and EIP-4844 blob transaction data that do not exist on other EVM networks.
```

### 10.4 Endpoint Entry Order

Within each H3 section, sort endpoint entries first by transformed endpoint path (alphabetical, case-insensitive), then by HTTP method alphabetically (`DELETE` < `GET` < `PATCH` < `POST` < `PUT`) for entries sharing the same path.

## 11. Index File Format

The index file `blockscout-analysis/references/blockscout-api-index.md` lists every endpoint across all output files, grouped by output file. It is the agent's primary entry point for discovering `direct_api_call` endpoints (referenced directly from `SKILL.md`).

### 11.1 Structure

```markdown
# Blockscout API Endpoints Index

Use this index to find available endpoints for the `direct_api_call` Blockscout MCP tool. Follow a two-step discovery process:

1. **Find the endpoint below** — locate it by name or category in this index.
2. **Read the linked detail file** — follow the section link (e.g., [Addresses](blockscout-api/addresses.md)) to get full parameter types, descriptions, and examples for use with `direct_api_call`.

## [Blocks](blockscout-api/blocks.md)

- `/api/v2/blocks`: Retrieves a paginated list of blocks with optional filtering by block type.
- `/api/v2/blocks/{block_hash_or_number_param}`: Retrieves detailed information for a specific block, including transactions, internal transactions, and metadata.
...

## [Stats](blockscout-api/stats.md)

- `/api/v2/stats`: Retrieves blockchain network statistics including total blocks, transactions, addresses, average block time, market data, and network utilization.
...
- `/stats-service/api/v1/counters`: Returns counters for the chain.
...

## [Ethereum PoS Chains](blockscout-api/ethereum.md)

These endpoints are only available on chains that use Ethereum proof-of-stake consensus, such as **Ethereum Mainnet** and **Gnosis Chain**. They expose beacon chain deposit tracking and EIP-4844 blob transaction data that do not exist on other EVM networks.

- `/api/v2/withdrawals`: Retrieves a paginated list of withdrawals, typically for proof-of-stake networks supporting validator withdrawals.
- `/api/v2/withdrawals/counters`: Returns total withdrawals count and sum from cache.
...
```

### 11.2 Rules

- Section headers are H2 with a markdown link to the file using a relative path from `references/blockscout-api-index.md`: `## [Display Name](blockscout-api/filename.md)`.
- **Sections appear in this order:**
  1. **Topic files** in fixed order: Blocks, Transactions, Addresses, Tokens, Smart Contracts, Search, Stats, Configuration. (These are always present. There is no Withdrawals topic file — those endpoints appear in the Ethereum PoS Chains section.)
  2. **Chain-specific files** sorted alphabetically by filename (e.g., `arbitrum.md` before `celo.md` before `ethereum.md`). Only files that contain at least one endpoint are included.
- **Display name** for a section is the H3 section heading associated with that file (derived at classification time per Section 6.1 / Section 10.2). Examples: `Blocks`, `Ethereum PoS Chains`, `Arbitrum`.
- **Preamble in index:** For any chain-specific file that has a preamble defined in `CHAIN_FILE_CONFIG` (Section 6.1 / Section 10.3), include the same preamble text immediately after the H2 section heading and before the first endpoint line item. This ensures agents reading the index understand the context of those endpoints without opening the file. Currently only `ethereum.md` has a preamble.
- Each line item format: `` - `/full/transformed/path`: <description> `` — path only, **no HTTP method prefix**.
- The description must be the **full, untruncated** text — use the value resolved by the description extraction procedure in Section 7 (with summary fallback).
- Endpoints with no resolved description omit the colon and description suffix entirely, producing `` - `/full/transformed/path` `` with no trailing whitespace.
- Within each section, endpoints follow the same sort order as in the API file (Section 10.4).
- When new variants are added and new chain-specific files are generated, they appear automatically in the index in their correct alphabetical position — no spec or code changes required.

## 12. Script Interface

- **Script location:** `.memory_bank/specs/blockscout-analysis/tools/api-file-generator.py`
- **Invocation:** `python .memory_bank/specs/blockscout-analysis/tools/api-file-generator.py`
- **Arguments:** None. The script is fully automatic.
- **Working directory:** Repository root (paths in this spec are relative to the repository root).
- **Exit code:** `0` on success, non-zero on failure.

## 13. Dependencies

| Dependency | Version | Purpose |
|---|---|---|
| Python | >= 3.9 | Runtime |
| PyYAML | >= 6.0 | YAML parsing of swagger files |

Standard library modules used: `json`, `os`, `pathlib`, `collections`.

## 14. Error Handling

| Scenario | Behavior |
|---|---|
| Endpoint map JSON file not found | Print error naming the missing file; exit with code 1 |
| Endpoint map JSON is malformed | Print error with parse message; exit with code 1 |
| Swagger YAML file not found for a variant | Print warning; skip parameter extraction for all affected endpoints (write `*None*` in parameter section) |
| Swagger YAML file is invalid | Print warning naming the file; skip parameter extraction for affected endpoints |
| Endpoint path or method key not found in swagger YAML | Print warning identifying the endpoint; write `*None*` in parameter section and continue |
| Endpoint from `default/swagger.yaml` matches no path prefix | Print warning with the endpoint path; skip the endpoint |

## 15. Console Output

The script must print structured progress messages to stdout. Example:

```
Reading main-indexer endpoint map: 94 endpoints loaded
Reading stats-service endpoint map: 11 endpoints loaded

Classifying endpoints...
  blocks.md:          6 endpoints
  transactions.md:    12 endpoints
  addresses.md:       16 endpoints
  tokens.md:          11 endpoints
  smart-contracts.md: 4 endpoints
  search.md:          4 endpoints
  stats.md:           18 endpoints (9 chain stats + 9 stats service)
  config.md:          4 endpoints
  arbitrum.md:        2 endpoints
  celo.md:            2 endpoints
  ethereum.md:        8 endpoints
  optimism.md:        2 endpoints
  polygon-zkevm.md:   1 endpoint
  scroll.md:          2 endpoints
  zksync.md:          1 endpoint

Writing API files...
  Written: blocks.md
  Written: transactions.md
  ...
  Written: zksync.md

Writing blockscout-api-index.md: 93 total endpoints

Done.
```

## 16. File System Layout

As of the current endpoint maps, the script produces:

```
blockscout-analysis/
  references/
    blockscout-api-index.md     # Master entry point (one level deep from SKILL.md)
    blockscout-api/
      blocks.md
      transactions.md
      addresses.md
      tokens.md
      smart-contracts.md
      search.md
      stats.md
      config.md
      arbitrum.md               # path-classified: /v2/arbitrum/, batch paths, main-page
      celo.md                   # path-classified: /v2/celo/, keyword match on /celo segment
      ethereum.md               # path-classified: /v2/beacon/, /v2/withdrawals, /blobs; custom heading + preamble
      mud.md                    # path-classified: /v2/mud/ only
      optimism.md               # path-classified: /v2/optimism/, batch paths, main-page
      polygon-zkevm.md          # path-classified: /v2/zkevm/, batch paths; heading override
      scroll.md                 # path-classified: /v2/scroll/, batch paths
      zksync.md                 # path-classified: /v2/zksync/, batch paths, main-page; heading override
```

The exact set of chain-specific files grows automatically as new chain paths or variants are indexed.

## 17. Non-Requirements

- **No tests required.** This is a utility script, not a product component.
- **No CI/CD integration.** The script is run manually after swagger indexers have been run.
- **No network access.** The script reads only from local files on disk.
- **No authentication.** All inputs are local files.
- **No support for partial runs.** The script always regenerates all files on each invocation.
