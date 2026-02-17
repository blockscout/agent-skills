---
name: blockscout-analysis
description: >
  Blockchain activity analysis using Blockscout infrastructure (MCP server,
  PRO API, BENS, Metadata, Chainscout, Stats). Use when analyzing on-chain
  data, addresses, transactions, tokens, contracts, or chain-specific data
  across 270+ EVM chains.
allowed-tools: WebFetch, Bash, Read, Write, Glob, Grep
---

# Blockscout Blockchain Analysis

This skill provides structured guidance for analyzing blockchain activity using the Blockscout infrastructure ecosystem. It is modular — read the supporting docs in `docs/` on demand rather than loading everything upfront.

## Three Primary Instruments

1. **MCP Server REST API** (`https://mcp.blockscout.com/v1/`) — 16 LLM-friendly tools for common queries. Use in scripts via HTTP GET requests. For interactive tasks like contract analysis or `read_contract`, recommend the user configure the native MCP server (`https://mcp.blockscout.com/mcp`).
2. **PRO API** (`https://api.blockscout.com`) — Full Blockscout REST/RPC API. Requires `$BLOCKSCOUT_API_KEY` env var. Responses are raw JSON — scripts must filter fields for LLM consumption.
3. **Supporting Services** — BENS (ENS), Metadata (tags/reputation), Chainscout (chain registry), Stats, Multichain Aggregator.

---

## Quick Decision Table

Use this table to select the right instrument for each data need.

| Data Need | Instrument | Endpoint / Tool |
|-----------|-----------|-----------------|
| Address info, balance, contract status | MCP REST | `get_address_info` |
| ENS → address (single) | MCP REST | `get_address_by_ens_name` |
| ERC-20 token holdings | MCP REST | `get_tokens_by_address` |
| NFT holdings | MCP REST | `nft_tokens_by_address` |
| Native coin transactions | MCP REST | `get_transactions_by_address` |
| ERC-20 token transfers | MCP REST | `get_token_transfers_by_address` |
| Transaction details (decoded) | MCP REST | `get_transaction_info` |
| Block data | MCP REST | `get_block_info` / `get_block_number` |
| Contract ABI | MCP REST | `get_contract_abi` |
| Contract source code | MCP REST | `inspect_contract_code` |
| Read contract state | Native MCP* | `read_contract` |
| Token search by name/symbol | MCP REST | `lookup_token_by_symbol` |
| Chain list | MCP REST | `get_chains_list` |
| Transaction logs/events | MCP REST | `direct_api_call` → `/api/v2/transactions/{hash}/logs` |
| Token holders | MCP REST | `direct_api_call` → `/api/v2/tokens/{addr}/holders` |
| NFT instances/transfers | MCP REST | `direct_api_call` → `/api/v2/tokens/{addr}/instances` |
| Chain-specific (L2 batches, beacon, epochs) | MCP REST | `direct_api_call` → see [chain-specific-endpoints.md](docs/chain-specific-endpoints.md) |
| Network stats, gas prices | MCP REST | `direct_api_call` → `/api/v2/stats` |
| Search addresses/tokens/txs | PRO API | `/api/v2/search?q=...` |
| Address counters, internal txs, logs | PRO API | `/api/v2/addresses/{hash}/counters`, etc. |
| Verified contracts list | PRO API | `/api/v2/smart-contracts` |
| CSV exports | PRO API | Various `/csv` endpoints |
| Bulk data (50 items/page) | PRO API | Any REST endpoint |
| ENS batch resolution | BENS | `POST /api/v1/addresses:batch-resolve` |
| Address tags, reputation, labels | Metadata | `GET /api/v1/metadata?addresses=...` |
| Chain registry (270+ chains, explorer URLs) | Chainscout | `GET /chains` |
| Historical stats, time-series charts | Stats | `/stats-service/api/v1/counters` |
| Cross-chain address/token search | Multichain | See [services-guide.md](docs/services-guide.md) |

*\* `read_contract` requires ABI + args; recommend native MCP server for interactive use.*

**Rule**: always try MCP REST API first. Fall back to PRO API when MCP lacks the endpoint or you need higher page sizes. Use services for specialized data (tags, batch ENS, stats, cross-chain).

---

## MCP Server Quick Reference

**REST API**: `GET https://mcp.blockscout.com/v1/{tool_name}?param1=value1&param2=value2`

**Response format**: `{"data": ..., "notes": ..., "instructions": ..., "pagination": ...}`

**Initialization**: call `GET /v1/unlock_blockchain_analysis` before any other tool in each session.

### Tools (16 total)

| Tool | Key Params | Paginated | Notes |
|------|-----------|-----------|-------|
| `unlock_blockchain_analysis` | — | No | Mandatory first call; returns rules + endpoint catalog |
| `get_chains_list` | — | No | 98+ supported chains |
| `get_address_info` | `chain_id`, `address` | No | Enriched: balance, first tx, ENS, contract, proxy, token |
| `get_address_by_ens_name` | `name` | No | ENS domain → 0x address |
| `get_tokens_by_address` | `chain_id`, `address` | Yes | ERC-20 portfolio with market data |
| `nft_tokens_by_address` | `chain_id`, `address` | Yes | NFTs grouped by collection |
| `get_transactions_by_address` | `chain_id`, `address`, `age_from` | Yes | Native transfers + calls; EXCLUDES token transfers |
| `get_token_transfers_by_address` | `chain_id`, `address`, `age_from` | Yes | ERC-20 transfers; optional `token` filter |
| `get_block_info` | `chain_id`, `number_or_hash` | No | Optional `include_transactions` |
| `get_block_number` | `chain_id` | No | Optional `datetime`; returns block at time or latest |
| `get_transaction_info` | `chain_id`, `transaction_hash` | No | Decoded input, token transfers, EIP-4337 ops |
| `get_contract_abi` | `chain_id`, `address` | No | ABI for verified contracts |
| `inspect_contract_code` | `chain_id`, `address` | No | Source code or file list |
| `read_contract` | `chain_id`, `address`, `abi`, `function_name` | No | Call view/pure functions |
| `lookup_token_by_symbol` | `chain_id`, `symbol` | No | Search tokens by name/symbol |
| `direct_api_call` | `chain_id`, `endpoint_path` | Yes | Raw Blockscout API proxy |

**Pagination**: opaque cursors, ~10 items/page. Follow `pagination.next_call` for next page.

**Default chain**: Ethereum Mainnet (`chain_id=1`) if unspecified.

For full tool details, strategies (binary search, portfolio analysis, funds movement), and the complete `direct_api_call` endpoint catalog, read [mcp-server-guide.md](docs/mcp-server-guide.md).

---

## PRO API Quick Reference

**Base URL**: `https://api.blockscout.com`

**Auth**: `$BLOCKSCOUT_API_KEY` environment variable (`proapi_xxxxxxxx` format)
- Query param: `?apikey=$BLOCKSCOUT_API_KEY`
- Header: `authorization: $BLOCKSCOUT_API_KEY`

**Route patterns**:
- REST: `https://api.blockscout.com/{chain_id}/api/v2/{path}`
- JSON RPC: `https://api.blockscout.com/v2/api?chain_id={chain_id}&module=X&action=Y`
- ETH RPC: `https://api.blockscout.com/{chain_id}/json-rpc`

**Pagination**: keyset-based, 50 items/page. Response includes `next_page_params` — pass as query params in next request.

**Responses are raw JSON** — not LLM-friendly. Scripts must extract relevant fields and format output for token-efficient consumption.

For endpoint discovery, authentication details, and examples, read [pro-api-guide.md](docs/pro-api-guide.md).

---

## Swagger Indexing Quick Reference

Swagger files document every PRO API endpoint with parameters and response schemas.

**Cached files**: `cache/swaggers/` (YAML files), `cache/indexes/` (.idx index files)

**Freshness check**:
```bash
bash scripts/swagger-freshness.sh
```
Compares `cache/.version` against the latest Blockscout release on GitHub.

**Index format**: `METHOD /path | summary | line_start-line_end` — one line per endpoint, grep-friendly.

**Alternative**: probe endpoints directly with curl/WebFetch to inspect response structure without swagger.

For the full caching, indexing, and search workflow, read [swagger-caching-and-indexing.md](docs/swagger-caching-and-indexing.md).

---

## Supporting Services Quick Reference

| Service | Base URL | Purpose |
|---------|---------|---------|
| BENS | `https://bens.services.blockscout.com/api/v1` | ENS domains, batch resolution |
| Metadata | `https://metadata.services.blockscout.com/api/v1` | Address tags, reputation, labels |
| Chainscout | `https://chains.blockscout.com/api` | Chain registry (270+ chains), explorer URLs |
| Stats | via `direct_api_call` or swagger | Historical counters, time-series charts |
| Multichain Aggregator | via swagger | Cross-chain address/token search |

For endpoint details, read [services-guide.md](docs/services-guide.md).

---

## Chain-Specific Endpoints

Blockscout exposes chain-family-specific API endpoints accessible via `direct_api_call`:

- **Ethereum/Gnosis**: beacon deposits, withdrawals
- **Arbitrum**: batches, L1↔L2 messages
- **Optimism**: batches, dispute games, deposits/withdrawals
- **Celo**: epochs, election rewards
- **zkSync/zkEVM/Scroll**: batches, deposits/withdrawals
- **Shibarium/Stability/Zilliqa/Redstone**: chain-specific endpoints

For the complete endpoint catalog, read [chain-specific-endpoints.md](docs/chain-specific-endpoints.md).

---

## Workflow: Answering a Blockchain Question

Follow these steps when a user asks about blockchain data:

### Step 1: Identify the chain
- If chain is named: use `get_chains_list` to find `chain_id`
- If chain is unknown: ask the user, or default to Ethereum (`chain_id=1`)
- For chain metadata (explorer URLs, ecosystem): use Chainscout `GET /chains`

### Step 2: Identify data type
Classify the request: address/balance, transactions, tokens, contract, block, chain-specific, stats, ENS, tags.

### Step 3: Select instrument
Check the Quick Decision Table above. Priority: MCP REST → `direct_api_call` → PRO API → Services.

### Step 4: Execute the query

**MCP REST API**:
```bash
curl -s "https://mcp.blockscout.com/v1/{tool}?chain_id={id}&{params}"
```
Parse the `data` field from JSON response. Check `pagination` for more pages.

**PRO API**:
```bash
curl -s "https://api.blockscout.com/{chain_id}/api/v2/{path}?apikey=$BLOCKSCOUT_API_KEY"
```
Extract relevant fields. Check `next_page_params` for pagination.

**Services**:
```bash
curl -s "https://{service}.services.blockscout.com/api/v1/{path}"
```

### Step 5: Handle pagination
- MCP: follow `pagination.next_call` (opaque cursors, ~10 items/page)
- PRO API: pass `next_page_params` values as query params (50 items/page)
- Collect all pages if user needs comprehensive data; stop early if question is answered

### Step 6: Transform for LLM consumption
- Extract only fields relevant to the user's question
- Flatten nested structures where possible
- Summarize large result sets (counts, top-N, notable entries)
- Format as structured text or tables for readability
