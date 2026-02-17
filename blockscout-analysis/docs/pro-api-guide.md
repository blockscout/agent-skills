# PRO API Guide

## When to Use PRO API

Use the PRO API when:
- MCP tools do not cover the needed endpoint (search, address counters, internal txs, logs, verified contracts list, CSV exports)
- You need 50 items per page instead of MCP's 10 (bulk data collection)
- You need raw unfiltered JSON for custom processing in scripts
- You need CSV export endpoints
- You need JSON RPC or ETH RPC API channels

## Authentication

**Environment variable**: `$BLOCKSCOUT_API_KEY`

**Key format**: `proapi_xxxxxxxx`

**Two ways to authenticate**:

1. Query parameter:
```bash
curl "https://api.blockscout.com/1/api/v2/addresses/0x...?apikey=$BLOCKSCOUT_API_KEY"
```

2. Header:
```bash
curl -H "authorization: $BLOCKSCOUT_API_KEY" "https://api.blockscout.com/1/api/v2/addresses/0x..."
```

**Rate limits**: 5 requests/sec on free tier; higher with PRO key.

## URL Patterns

### REST API (most common)

```
https://api.blockscout.com/{chain_id}/api/v2/{path}
```

Examples:
- `https://api.blockscout.com/1/api/v2/addresses/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`
- `https://api.blockscout.com/137/api/v2/tokens/0x...`
- `https://api.blockscout.com/8453/api/v2/transactions/0x...`

### JSON RPC API

```
https://api.blockscout.com/v2/api?chain_id={chain_id}&module={module}&action={action}&{params}
```

7 modules: `account`, `logs`, `token`, `stats`, `block`, `contract`, `transaction`

Documentation: https://docs.blockscout.com/devs/apis/rpc.md

Example:
```bash
curl "https://api.blockscout.com/v2/api?chain_id=1&module=account&action=balance&address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&apikey=$BLOCKSCOUT_API_KEY"
```

### ETH RPC API

```
https://api.blockscout.com/{chain_id}/json-rpc
```

Standard Ethereum JSON-RPC. Documentation: https://docs.blockscout.com/devs/apis/rpc/eth-rpc.md

## Endpoint Discovery

When you need a PRO API endpoint:

### Option 1: Check direct_api_call catalog first
See [chain-specific-endpoints.md](chain-specific-endpoints.md). If the endpoint exists there, use MCP `direct_api_call` instead.

### Option 2: Use swagger index
If cached swagger indexes exist, search them:
```bash
grep -i "keyword" cache/indexes/blockscout-default.idx
```
Then read the line range from the cached swagger YAML for full parameter and response details.

See [swagger-caching-and-indexing.md](swagger-caching-and-indexing.md) for the full workflow.

### Option 3: Probe endpoint directly
Construct the URL from the REST pattern and call it:
```bash
curl -s "https://api.blockscout.com/1/api/v2/addresses/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045/counters?apikey=$BLOCKSCOUT_API_KEY"
```
Inspect the response to understand the structure. This works when you have a reasonable guess at the endpoint path.

## Response Handling

PRO API responses are **raw JSON** — verbose and not optimized for LLM consumption.

**Script responsibilities**:
1. Extract only fields relevant to the user's question
2. Flatten nested structures where possible
3. Convert raw values (e.g., divide token amounts by 10^decimals)
4. Format output as structured text or tables

### Pagination

Keyset-based, 50 items per page.

Response includes `next_page_params` when more data exists:
```json
{
  "items": [...],
  "next_page_params": {
    "block_number": 12345678,
    "index": 42,
    "items_count": 50
  }
}
```

Pass `next_page_params` values as query params in the next request:
```bash
curl "https://api.blockscout.com/1/api/v2/addresses/0x.../transactions?block_number=12345678&index=42&items_count=50&apikey=$BLOCKSCOUT_API_KEY"
```

## Common PRO API Endpoints Not in MCP

These endpoints are available through PRO API but not directly through MCP tools:

| Endpoint | Description |
|----------|-------------|
| `GET /api/v2/search?q={query}` | Search addresses, tokens, transactions, blocks |
| `GET /api/v2/addresses/{hash}/counters` | Address activity counters (tx count, token transfers count, etc.) |
| `GET /api/v2/addresses/{hash}/internal-transactions` | Internal (trace) transactions for an address |
| `GET /api/v2/addresses/{hash}/logs` | Event logs emitted by/to an address |
| `GET /api/v2/addresses/{hash}/token-balances` | All token balances for an address |
| `GET /api/v2/addresses/{hash}/coin-balance-history` | Historical native coin balance |
| `GET /api/v2/addresses/{hash}/coin-balance-history-by-day` | Daily native coin balance |
| `GET /api/v2/tokens` | Token list with filters (type, sort) |
| `GET /api/v2/tokens/{hash}/transfers` | All transfers for a specific token |
| `GET /api/v2/smart-contracts` | List of verified smart contracts |
| `GET /api/v2/smart-contracts/{hash}` | Detailed verified contract info |
| `GET /api/v2/smart-contracts/{hash}/methods-read` | Read methods for a contract |
| `GET /api/v2/smart-contracts/{hash}/methods-write` | Write methods for a contract |
| `GET /api/v2/transactions` | Recent transactions (no address filter) |
| `GET /api/v2/blocks` | Recent blocks list |
| `GET /api/v2/stats/charts/transactions` | Transaction count chart data |
| `GET /api/v2/stats/charts/market` | Market chart data (price, market cap) |

For full endpoint documentation, use the swagger index (see [swagger-caching-and-indexing.md](swagger-caching-and-indexing.md)).

## Example: Full PRO API Call in a Script

```bash
#!/usr/bin/env bash
# Fetch top token holders for USDT on Ethereum

CHAIN_ID=1
TOKEN="0xdAC17F958D2ee523a2206206994597C13D831ec7"
API_KEY="$BLOCKSCOUT_API_KEY"

response=$(curl -s "https://api.blockscout.com/${CHAIN_ID}/api/v2/tokens/${TOKEN}/holders?apikey=${API_KEY}")

# Extract relevant fields: address and value
echo "$response" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data.get('items', []):
    addr = item['address']['hash']
    value = int(item['value']) / 1e6  # USDT has 6 decimals
    print(f'{addr} | {value:,.2f} USDT')
"
```

## See Also

- [Swagger Caching and Indexing](swagger-caching-and-indexing.md) — discover additional endpoints
- [Decision Framework](decision-framework.md) — when PRO API vs MCP
- [MCP Server Guide](mcp-server-guide.md) — MCP tools for common queries
