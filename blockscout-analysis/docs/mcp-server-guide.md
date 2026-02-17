# MCP Server Guide

## Initialization

Every session must start with the unlock call:

```bash
curl -s "https://mcp.blockscout.com/v1/unlock_blockchain_analysis"
```

This returns:
- Server version
- Error handling rules (retry 500s up to 3 times)
- Chain ID guidance with recommended chains
- Pagination rules
- Time-based query rules
- Binary search strategy for historical data
- Portfolio and funds movement analysis rules
- Data ordering and resumption rules
- The `direct_api_call` endpoint catalog (common + chain-specific)

Cache the response locally if you need to reference these rules during the session.

## REST API Interface

**Base URL**: `https://mcp.blockscout.com/v1/`

All 16 tools are available as GET endpoints:
```
GET https://mcp.blockscout.com/v1/{tool_name}?param1=value1&param2=value2
```

**Response format** (all endpoints):
```json
{
  "data": { ... },        // Primary query results
  "notes": "...",          // Contextual information
  "instructions": "...",   // Guidance for pagination or next steps
  "pagination": {          // Present only when more data exists
    "next_call": "..."     // Exact URL or tool call for next page
  }
}
```

## Native MCP Server

**Endpoint**: `https://mcp.blockscout.com/mcp`

Recommend user configure native MCP server for:
- `inspect_contract_code` — iterative source file navigation
- `read_contract` — requires ABI object + args, complex parameter passing
- Multi-step investigation workflows where the agent needs to chain tool calls interactively

For script-based automation, the REST API is preferred.

---

## Tool Catalog

### unlock_blockchain_analysis

**REST**: `GET /v1/unlock_blockchain_analysis`

**Params**: none

**Returns**: Server rules, chain catalog (98+ chains with name, chain_id, is_testnet, native_currency, ecosystem, settlement_layer), endpoint catalog for `direct_api_call`.

**Mandatory**: must be called before any other tool in each session.

---

### get_chains_list

**REST**: `GET /v1/get_chains_list`

**Params**: none

**Returns**: Array of supported chains with: name, chain_id, is_testnet, native_currency, ecosystem, settlement_layer_chain_id.

**Paginated**: No

**Notes**: Returns ~98 chains (subset of the 270+ in Chainscout). For the full registry including explorer URLs, use Chainscout instead.

---

### get_address_info

**REST**: `GET /v1/get_address_info?chain_id={id}&address={addr}`

**Params**: `chain_id` (required), `address` (required)

**Returns** (enriched beyond raw Blockscout API):
- Native token balance (raw, not adjusted by decimals)
- First transaction details (block number, timestamp) — useful for age calculation
- ENS name association (if any)
- Contract status (is_contract, is_verified)
- Proxy info (type, implementation addresses) — for proxy contracts
- Token details (if contract is a token): name, symbol, decimals, total_supply
- Metadata tags from Blockscout Metadata service

**Paginated**: No

**Key use**: starting point for address investigation. Always call this first when analyzing an address.

---

### get_address_by_ens_name

**REST**: `GET /v1/get_address_by_ens_name?name={ens_domain}`

**Params**: `name` (required) — ENS domain (e.g., `vitalik.eth`)

**Returns**: Resolved Ethereum address

**Paginated**: No

**Notes**: For batch resolution, use BENS service instead.

---

### get_tokens_by_address

**REST**: `GET /v1/get_tokens_by_address?chain_id={id}&address={addr}`

**Params**: `chain_id` (required), `address` (required), `cursor` (optional)

**Returns**: ERC-20 token holdings with:
- Token contract details (name, symbol, decimals)
- Market metrics (exchange_rate, market_cap, volume)
- Holders count
- Balance (raw, not adjusted by decimals)

**Paginated**: Yes (~10 items/page)

**Key use**: portfolio analysis. Always combine with `get_address_info` (native balance) for complete portfolio.

---

### nft_tokens_by_address

**REST**: `GET /v1/nft_tokens_by_address?chain_id={id}&address={addr}`

**Params**: `chain_id` (required), `address` (required), `cursor` (optional)

**Returns**: NFT tokens grouped by collection. Per collection: type, address, name, symbol, total_supply, holder_count. Per instance: id, name, description, external_url, metadata attributes.

**Paginated**: Yes

---

### get_transactions_by_address

**REST**: `GET /v1/get_transactions_by_address?chain_id={id}&address={addr}&age_from={date}`

**Params**: `chain_id` (required), `address` (required), `age_from` (required, ISO 8601), `age_to` (optional), `methods` (optional, method signature like `0x304e6ade`), `cursor` (optional)

**Returns**: Native currency transfers and smart contract interactions (calls, internal txs).

**EXCLUDES token transfers** — use `get_token_transfers_by_address` for ERC-20 transfers. You will see calls *to* token contracts, but not the `Transfer` events.

**Paginated**: Yes

**Data ordering**: DESC (newest first) by (block_number, transaction_index, internal_transaction_index)

---

### get_token_transfers_by_address

**REST**: `GET /v1/get_token_transfers_by_address?chain_id={id}&address={addr}&age_from={date}`

**Params**: `chain_id` (required), `address` (required), `age_from` (required, ISO 8601), `age_to` (optional), `token` (optional, token contract address), `cursor` (optional)

**Returns**: ERC-20 token transfer events.

**Paginated**: Yes

**Data ordering**: DESC by (block_number, transaction_index, token_transfer_batch_index, token_transfer_index)

**Key use**: token transfer tracking. Always combine with `get_transactions_by_address` for complete funds movement picture.

---

### get_block_info

**REST**: `GET /v1/get_block_info?chain_id={id}&number_or_hash={block}`

**Params**: `chain_id` (required), `number_or_hash` (required), `include_transactions` (optional, default false)

**Returns**: Block data: timestamp, gas_used, burnt_fees, transaction_count. Optionally includes transaction hash list.

**Paginated**: No

**Notes**: Request `include_transactions=true` only when needed — on high-traffic chains the list may be large.

---

### get_block_number

**REST**: `GET /v1/get_block_number?chain_id={id}&datetime={iso_date}`

**Params**: `chain_id` (required), `datetime` (optional, ISO 8601)

**Returns**: Block number and timestamp. If `datetime` provided, finds the block immediately preceding that time. If omitted, returns latest block.

**Paginated**: No

---

### get_transaction_info

**REST**: `GET /v1/get_transaction_info?chain_id={id}&transaction_hash={hash}`

**Params**: `chain_id` (required), `transaction_hash` (required), `include_raw_input` (optional, default false)

**Returns** (enriched):
- Decoded input parameters (if contract is verified)
- Token transfers with token metadata
- Fee breakdown (priority fees, burnt fees)
- Transaction type categorization
- EIP-4337 user operation IDs (if applicable)

**Paginated**: No

**Notes**: Raw input is omitted by default when decoded version is available. Set `include_raw_input=true` only when you need the hex data.

---

### get_contract_abi

**REST**: `GET /v1/get_contract_abi?chain_id={id}&address={addr}`

**Params**: `chain_id` (required), `address` (required)

**Returns**: Contract ABI (JSON array of function/event definitions). Only works for verified contracts.

**Paginated**: No

---

### inspect_contract_code

**REST**: `GET /v1/inspect_contract_code?chain_id={id}&address={addr}&file_name={file}`

**Params**: `chain_id` (required), `address` (required), `file_name` (optional)

**Returns**: If `file_name` omitted: contract metadata + list of source files. If `file_name` provided: source code content.

**Paginated**: No

**Recommendation**: For iterative source file exploration, native MCP server is preferred. The REST API works for single-file retrieval.

---

### read_contract

**REST**: `GET /v1/read_contract?chain_id={id}&address={addr}&function_name={fn}&abi={json}&args={json}`

**Params**: `chain_id` (required), `address` (required), `abi` (required, JSON ABI object for the function), `function_name` (required), `args` (optional, JSON array), `block` (optional, default "latest")

**Returns**: Decoded function return value.

**Paginated**: No

**Recommendation**: Due to complex ABI/args parameter passing, native MCP server is strongly preferred for interactive use. REST API works for scripted calls where ABI is known in advance.

---

### lookup_token_by_symbol

**REST**: `GET /v1/lookup_token_by_symbol?chain_id={id}&symbol={query}`

**Params**: `chain_id` (required), `symbol` (required)

**Returns**: Multiple potential matches with token address, name, symbol. Limited to first N results.

**Paginated**: No

---

### direct_api_call

**REST**: `GET /v1/direct_api_call?chain_id={id}&endpoint_path={path}`

**Params**: `chain_id` (required), `endpoint_path` (required), `query_params` (optional, JSON object), `cursor` (optional)

**Returns**: Raw Blockscout API response. Unlike other MCP tools, this does NOT provide LLM-friendly optimization or filtration.

**Paginated**: Yes (when the underlying endpoint supports it)

**Notes**: Use only for endpoints in the curated catalog (see [chain-specific-endpoints.md](chain-specific-endpoints.md)). Do NOT include query strings in `endpoint_path` — pass via `query_params`.

---

## Pagination

- Page size: ~10 items (vs 50 for raw Blockscout API)
- Cursor format: opaque — never construct cursors manually
- When `pagination` field is present in response, more data exists
- Follow `pagination.next_call` exactly to get the next page
- For REST API: `pagination.next_call` contains the full URL to call
- Continue paginating until no `pagination` field or user's question is answered

### Trade-off

5x more requests than PRO API for the same data volume. However:
- MCP responses are pre-filtered and enriched — less post-processing needed
- For analysis tasks (understanding activity, finding patterns), MCP pagination is acceptable
- For bulk data collection (exporting all transactions), PRO API's 50-item pages are more efficient

---

## Key Strategies

### Binary Search for Historical Data

Never paginate to find temporal boundaries. Use binary search with `age_from`/`age_to`:

```
get_transactions_by_address(age_from=START, age_to=MID)
├── Results found → search earlier half: [START, MID]
└── No results → search later half: [MID, END]
```

Example — find first transaction for an address:
1. `age_from=2015-07-30, age_to=2015-12-31` → found
2. `age_from=2015-07-30, age_to=2015-09-12` → not found
3. `age_from=2015-09-12, age_to=2015-10-03` → found
4. `age_from=2015-09-27, age_to=2015-09-30` → found at 2015-09-28
5. `age_from=2015-07-30, age_to=2015-09-28T08:24:42` → not found → confirmed first tx

Result: 5 API calls instead of hundreds of pagination calls.

### Portfolio Analysis

Always check BOTH:
1. `get_address_info` — native coin balance (ETH, MATIC, etc.)
2. `get_tokens_by_address` — ERC-20 token holdings

When ranking by USD value, include native coin as a candidate alongside ERC-20 tokens.

### Funds Movement Analysis

Always check BOTH:
1. `get_transactions_by_address` — native transfers + contract calls
2. `get_token_transfers_by_address` — ERC-20 token transfers

Do not assume "transactions" means only native coin transfers.

### Data Ordering & Resumption

Time-ordered tools return results in **DESC** order (newest first).

Ordering keys:
- `get_transactions_by_address`: (block_number, transaction_index, internal_transaction_index)
- `get_token_transfers_by_address`: (block_number, transaction_index, token_transfer_batch_index, token_transfer_index)
- `direct_api_call` (logs): (block_number, index)

To resume from an anchor item: use anchor's block timestamp as time boundary, then client-side filter by the complete ordering key to avoid duplicates.

---

## See Also

- [Chain-Specific Endpoints](chain-specific-endpoints.md) — full `direct_api_call` catalog
- [Decision Framework](decision-framework.md) — when MCP vs PRO API
- [Infrastructure Overview](infrastructure-overview.md) — architecture context
