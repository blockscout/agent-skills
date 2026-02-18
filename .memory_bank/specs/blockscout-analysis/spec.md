# Blockscout Analysis Skill — Specification

## Purpose

Create a modular AI agent skill for blockchain activity analysis using Blockscout infrastructure. The skill must guide agents through two key decisions: (1) selecting the right data source, and (2) selecting the right execution strategy — whether to make direct MCP/API tool calls, write and run a script for deterministic multi-step flows, or use a combination of both. The skill must also handle transforming verbose API responses into LLM-friendly output.

## Infrastructure Components

### 1. Blockscout MCP Server

- **MCP endpoint**: `https://mcp.blockscout.com/mcp` (native MCP protocol)
- **REST API**: `https://mcp.blockscout.com/v1/{tool_name}?params` (HTTP GET)
- **LLMs description**: `https://mcp.blockscout.com/llms.txt`
- **Multichain**: the server is multichain; almost all tools accept a `chain_id` parameter to target a specific chain (use `get_chains_list` to discover supported chains).
- **16 tools**: unlock_blockchain_analysis, get_chains_list, get_address_info, get_address_by_ens_name, get_tokens_by_address, nft_tokens_by_address, get_transactions_by_address, get_token_transfers_by_address, get_block_info, get_block_number, get_transaction_info, get_contract_abi, inspect_contract_code, read_contract, lookup_token_by_symbol, direct_api_call
- **Responses**: LLM-friendly (pre-filtered, enriched), except `direct_api_call` which proxies raw Blockscout API
- **Pagination**: opaque cursors, ~10 items/page (vs 50 for raw API)
- **Enrichment examples**: address info includes first tx timestamp + ENS + metadata tags; block info includes tx hashes; transaction info includes EIP-4337 user operation IDs
- **Centralized services access** (used internally by MCP tools; agents can also call them via `direct_api_call` or HTTP if needed):
  - **BENS** (`bens.services.blockscout.com/api/v1`) — utilized by `get_address_by_ens_name` for ENS resolution.
  - **Metadata** (`metadata.services.blockscout.com/api/v1/`) — utilized by `get_address_info` to attach address metadata (tags, reputation, labels).
  - **Chainscout** (`chains.blockscout.com/api/`) — utilized by `get_chains_list` for initial information about chains hosted by the Blockscout team. The list returned by `get_chains_list` does not include the Blockscout instance URL per chain; when that is needed, call the Chainscout API with the specific chain id directly. Note: chains hosted by the Blockscout team are a subset of all instances registered in Chainscout.
- **Advantage**: simplified cursor-based pagination more suitable for LLMs and scripts
- **Disadvantage**: short pages (10 items vs 50) — requires 5x more requests for equivalent data volume

#### Pagination (MCP): opaque cursor and simplified model

MCP pagination is **simplified** compared to the raw Blockscout/PRO API so that agents and scripts don’t have to handle endpoint-specific keys.

- **Opaque cursor**: The server turns the backend’s `next_page_params` (e.g. `block_number`, `index`, `items_count`) into a single string: the params are serialized to JSON and Base64URL-encoded. The agent only ever sees and passes this one **cursor** value; it never parses or constructs the underlying keys. That reduces context use and avoids wrong or partial params on the next call.
- **Simplified cursor-based pagination**: Paginated MCP tools expose a single optional `cursor` parameter. To get the next page, the agent calls the same tool again with the same inputs and sets `cursor` to the value from the response (e.g. from `pagination.next_call.params.cursor`). No endpoint-specific query params or key names to remember.
- **Contrast with PRO API**: The [PRO API](#pagination-pro-api) uses **keyset pagination** with a visible `next_page_params` object; the client must pass each of its keys (e.g. `block_number`, `index`, `items_count`) as query parameters, and the key set varies by endpoint. MCP hides that behind the opaque cursor and a uniform “pass cursor for next page” contract.

#### Mandatory `unlock_blockchain_analysis` (MCP prerequisite)

- **Rule**: Before calling any other Blockscout MCP tool, the agent must call `unlock_blockchain_analysis` first. This is mandatory for all MCP clients that do not reliably read the server’s tool instructions (e.g. many clients skip or ignore server-provided descriptions).
- **Exception**: When the agent runs in **Claude Code**, this call is optional. Claude Code reads MCP server instructions correctly; `unlock_blockchain_analysis` exists as a workaround for clients that do not.
- **Skill behavior**: The skill must instruct the agent to call `unlock_blockchain_analysis` once per session (or before the first MCP tool use) whenever the agent decides to use Blockscout MCP tools, unless the environment is known to be Claude Code.

### 2. Blockscout PRO API

- **Base URL**: `https://api.blockscout.com`
- **Registration**: https://dev.blockscout.com
- **Documentation**: https://docs.blockscout.com/devs/pro-api.md
- **Auth**: `$BLOCKSCOUT_API_KEY` environment variable (`proapi_xxxxxxxx` format), via `apikey` query param or `Authorization` header
- **Multi-chain**: addresses chains through chain_id in URL path
- **Route patterns**:
  - REST: `/{chain_id}/api/v2/{path}`
  - JSON RPC: `/v2/api?chain_id={chain_id}&module=X&action=Y`
  - ETH RPC: `/{chain_id}/json-rpc`
- **Pagination**: keyset-based, 50 items/page; see [Pagination (PRO API)](#pagination-pro-api) below
- **Responses**: raw JSON, NOT LLM-friendly — scripts must filter and transform
- **Coverage**: almost full set of API endpoints available on individual Blockscout instances

#### User instructions (PRO API key)

The skill must instruct the user to:

1. **Obtain an API key**: Go to the [Blockscout Development Portal](https://dev.blockscout.com) and generate an API key there.
2. **Configure the environment**: Configure the current environment so the key is available for the agent and for scripts written by the agent (e.g. by setting `$BLOCKSCOUT_API_KEY` or equivalent in the shell or project environment).

#### Pagination (PRO API)

PRO API uses **keyset pagination**: each response includes a `next_page_params` object. To get the next page, pass those parameters as query arguments on the same endpoint.

- **Page size**: 50 items per page (default; `items_count` in `next_page_params` is typically 50).
- **Initial request**: no pagination params. Example: `GET /{chain_id}/api/v2/transactions`.
- **Next pages**: add the fields from `next_page_params` as query params. Exact keys depend on the endpoint (e.g. transactions use `block_number`, `index`, `items_count`).

**Example — transactions (`api/v2/transactions`):**

1. **Initial call** (no query params):

   Response:
   ```json
   {
     "items": [ ... ],
     "next_page_params": {
       "items_count": 50,
       "block_number": 24479322,
       "index": 238
     }
   }
   ```

2. **Next page**: call the same path with `next_page_params` as query string:
   `api/v2/transactions?block_number=24479322&index=238&items_count=50`

   Response:
   ```json
   {
     "items": [ ... ],
     "next_page_params": {
       "items_count": 50,
       "block_number": 24479322,
       "index": 188
     }
   }
   ```

3. **Further pages**: keep using the new `next_page_params` from each response (e.g. next request: `block_number=24479322&index=188&items_count=50`). Stop when the response has no `next_page_params` or `items` is empty.

Other paginated endpoints may use different keys in `next_page_params`; always take the object from the response and pass it as query parameters for the next request.

### 3. Supporting Services

| Service | Base URL | Purpose |
|---------|---------|---------|
| BENS | `https://bens.services.blockscout.com/api/v1` | ENS domains, batch resolution, reverse lookup |
| Metadata | `https://metadata.services.blockscout.com/api/v1` | Address tags, reputation, public labels |
| Chainscout | `https://chains.blockscout.com/api` | Registry where Blockscout is deployed, explorer URLs |
| Stats | via `direct_api_call` (under `stats-service` path) | Historical counters, time-series charts |
| Multichain Aggregator | via swagger | Cross-chain address/token search |

## API Documentation Sources

### REST API (most complex)

- **Swagger files**: `https://github.com/blockscout/swaggers/tree/master/blockscout/{version}/{variant}/swagger.yaml`
- **Current stable version**: identify from `https://github.com/blockscout/blockscout/releases` (e.g., 9.3.5)
- **Default variant**: covers base API for all chains — start here
- **Chain-specific variants**: arbitrum, ethereum, optimism, scroll, zksync, polygon_zkevm, shibarium, stability, zilliqa, zetachain, rsk, blackfort, filecoin, neon, optimism-celo — add extra endpoints/fields
- **Note**: swagger files do not reflect the full amount of chain-specific endpoints; the MCP `unlock_blockchain_analysis` tool output contains a more complete catalog

### JSON RPC API

- Documentation: https://docs.blockscout.com/devs/apis/rpc.md
- Modules: account, logs, token, stats, block, contract, transaction
- Per-module docs: https://docs.blockscout.com/devs/apis/rpc/{module}.md

### ETH RPC API

- Documentation: https://docs.blockscout.com/devs/apis/rpc/eth-rpc.md
- Standard Ethereum JSON-RPC

### Service Swaggers

- BENS: `https://github.com/blockscout/swaggers/tree/master/services/bens` (releases prefixed `bens` in `https://github.com/blockscout/blockscout-rs/releases`)
- Metadata: `https://github.com/blockscout/swaggers/tree/master/services/metadata`
- Multichain Aggregator: `https://github.com/blockscout/swaggers/tree/master/services/multichain-aggregator` (releases prefixed `multichain-aggregator` in `https://github.com/blockscout/blockscout-rs/releases`)
- Stats: `https://github.com/blockscout/swaggers/tree/master/services/stats` (releases prefixed `stats` in `https://github.com/blockscout/blockscout-rs/releases`)

### Chainscout

- No swagger — API reverse-engineered from source: `https://github.com/blockscout/chainscout/tree/main/app/api/chains`
- Endpoints: `GET /chains` (full registry), `GET /chains/list` (simplified)

## Design Requirements

### Modular structure

The skill must use a hub-and-spoke pattern:
- `SKILL.md` — concise entry point with decision tables (data source + execution strategy) and quick references
- Supporting docs in `docs/` — loaded on demand by the agent, one per topic
- Scripts in `scripts/` — reusable deterministic tooling only (swagger processing, common analysis patterns). The skill must **not** mix these tools with ad-hoc scripts.
- Ad-hoc scripts — agent-generated at runtime for task-specific multi-step flows — must be stored in a **separate directory** (e.g. `artifacts/`), not in `scripts/`.

### Version in SKILL.md

The skill must declare its version in the `SKILL.md` file (e.g. at the top or in a dedicated section) so that updates can be identified easily.

### MCP access strategy

- Scripts use the MCP REST API (`mcp.blockscout.com/v1/`) or PRO API (`api.blockscout.com`) via HTTP
- For interactive tasks better suited to native MCP tool calls (contract analysis, `read_contract`, iterative investigation), the skill instructs the agent to ensure the native MCP server is available (see [MCP server availability](#mcp-server-availability) below)
- The choice between script-based HTTP calls and direct MCP tool calls is governed by the execution strategy (see [Execution strategy](#execution-strategy) below)

### MCP server availability

- When the skill leads the agent to use Blockscout MCP tools, the skill must instruct the agent to **ensure the Blockscout MCP server is available** before relying on MCP tool calls. The agent should either provide the user with instructions to install or enable the MCP server, or, if the agent has the ability, install or enable the server automatically.
- The specification is **agent-agnostic**: the skill does not prescribe environment-specific steps (e.g. which config file or UI to use). It motivates the agent to achieve availability, assuming the agent knows how to install or enable an MCP server in its host environment.

### Do not duplicate `unlock_blockchain_analysis` content in the skill

- The output of `unlock_blockchain_analysis` is maintained by the MCP server and may be extended or changed over time (e.g. new endpoints, chain families, or usage notes).
- **Skill docs (SKILL.md and files in `docs/`) must not copy or paraphrase that content.** They may only:
  - Require calling `unlock_blockchain_analysis` first (per the rule above), and
  - Point to the canonical source - the tool itself.
- This keeps the skill stable when the server’s instructions change and avoids conflicting or outdated copies.

### Swagger caching and indexing

- Swagger files are large (10,000+ lines) — the skill must instruct the agent to cache them
- A deterministic script must index cached swagger files
- Index format: `METHOD /path | summary | line_start-line_end` — compact, grep-friendly
- Index files enable quick endpoint discovery; agent reads the swagger line range for full details
- Freshness check: compare cached version against latest Blockscout release on GitHub
- Alternative approach: probe API endpoints directly with HTTP requests to inspect response structure

### Decision framework

The skill must guide the agent through two orthogonal decisions: **which data source** to use and **how to execute** the query.

#### Data source selection

Choose the data source based on coverage and response quality:
- MCP REST API first (LLM-friendly, enriched, no auth)
- PRO API as fallback (full coverage, 50-item pages, auth required)
- Services for specialized data (tags, batch ENS, stats, cross-chain)

#### Execution strategy

Choose the execution method based on task complexity, determinism, and whether semantic reasoning is required:

| Signal | Strategy | When to use |
|--------|----------|-------------|
| Simple lookup, 1–3 calls, no post-processing | **Direct tool calls** (MCP tool or web fetch) | The answer is returned directly or nearly directly by an API endpoint. E.g. get a block number, resolve an ENS name, fetch latest cross-chain message. |
| Deterministic multi-step flow with loops, date ranges, aggregation, or conditional branching | **Script** (agent writes and executes a script calling MCP REST or PRO API via HTTP) | The logic is well-defined and would be inefficient or error-prone as a sequence of LLM-driven calls. E.g. iterate over months to compute APY changes, paginate through all token holders to count matches, scan transaction history with filtering. |
| Data retrieval is simple but output requires math, normalization, or filtering | **Hybrid** (tool call for retrieval + script for post-processing) | API provides raw data that needs token-decimal normalization, USD conversion, sorting, deduplication, or threshold filtering. E.g. get token balances via API then normalize amounts and filter by value in a script. |
| Task requires semantic understanding, code analysis, or subjective judgment | **LLM reasoning over API results** (direct tool calls, agent analyzes) | The question cannot be answered by a deterministic algorithm — it needs interpretation of contract source code, verification of token authenticity, classification of transaction purpose, or tracing code flow. E.g. check if a contract has blacklisting functionality, determine if a token is official, categorize a transaction. |
| Large data volume with known filtering criteria | **Script against PRO API** (50 items/page, script handles pagination and filtering) | Need to process many pages of data with programmatic filters. PRO API's 50-item pages are 5x more efficient than MCP's 10-item pages for bulk retrieval. |

**Combination patterns**: Many real-world queries require combining strategies. For example, a multi-chain token balance analysis might use direct tool calls to resolve an ENS name, then a script to iterate chains and fetch/normalize balances, with the LLM providing final interpretation of which tokens are "stablecoins."

The skill's decision table in `SKILL.md` must present both dimensions so the agent selects data source and execution strategy together.

### Response transformation

Scripts querying PRO API must:
- Extract only fields relevant to the user's question
- Flatten nested structures where possible
- Format output for token-efficient LLM consumption

## Chain-Specific Endpoints

The MCP `unlock_blockchain_analysis` tool returns a catalog of chain-family-specific API endpoints accessible via `direct_api_call`:

- **Common (all chains)**: stats counters, network stats, user operations (EIP-4337), transaction logs, token holders, NFT instances
- **Ethereum/Gnosis**: beacon deposits, withdrawals
- **Arbitrum**: batches, L1↔L2 messages
- **Optimism**: batches, dispute games, deposits/withdrawals
- **Celo**: epochs, election rewards (group/validator/voter)
- **zkSync**: batches
- **zkEVM**: batches, deposits/withdrawals
- **Scroll**: batches, blocks by batch, deposits/withdrawals
- **Shibarium**: deposits/withdrawals
- **Stability**: validators
- **Zilliqa**: validators
- **Redstone (MUD)**: worlds, tables, records

## Implementation Notes

- PRO API dev portal does not provide documentation for REST API endpoints — swagger files are the primary source of truth
- The `direct_api_call` MCP tool is a proxy to Blockscout API endpoints and does not provide optimization or filtration
- Some MCP tools automatically enrich responses by performing the necessary additional API calls internally (e.g., address info enriched with metadata and first transaction timestamp), so using MCP endpoints can reduce the total number of calls compared to querying the PRO API directly.
- MCP server simplifies complex cursor logic for paginated endpoints, making it more suitable for LLMs
- MCP pagination trade-off: 10 items/page (5x more requests than PRO API's 50) but enriched responses may save follow-up queries
