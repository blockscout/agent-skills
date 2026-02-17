# Decision Framework

## Decision Tree

```
User asks a blockchain question
│
├─► Step 1: Identify the chain
│   ├─ Chain named → MCP get_chains_list (find chain_id)
│   ├─ Chain unknown → ask user, or default to Ethereum (chain_id=1)
│   └─ Need explorer URL → Chainscout GET /chains
│
├─► Step 2: Classify data type
│   │
│   ├─ Address / Balance / Tokens / NFTs
│   │   └─► MCP tools: get_address_info, get_tokens_by_address, nft_tokens_by_address
│   │
│   ├─ Transactions / Native transfers
│   │   └─► MCP: get_transactions_by_address (+ get_token_transfers_by_address for complete picture)
│   │
│   ├─ ERC-20 token transfers
│   │   └─► MCP: get_token_transfers_by_address
│   │
│   ├─ Transaction details (single tx)
│   │   └─► MCP: get_transaction_info
│   │
│   ├─ Block data
│   │   └─► MCP: get_block_info, get_block_number
│   │
│   ├─ Contract ABI / source code
│   │   └─► MCP: get_contract_abi, inspect_contract_code
│   │
│   ├─ Read contract state
│   │   └─► MCP: read_contract (prefer native MCP server for interactive use)
│   │
│   ├─ Token search
│   │   └─► MCP: lookup_token_by_symbol
│   │
│   ├─ Transaction logs / events
│   │   └─► MCP: direct_api_call → /api/v2/transactions/{hash}/logs
│   │
│   ├─ Token holders / NFT instances
│   │   └─► MCP: direct_api_call → /api/v2/tokens/{addr}/holders or /instances
│   │
│   ├─ Chain-specific data (L2 batches, beacon, epochs, validators)
│   │   └─► MCP: direct_api_call → see chain-specific-endpoints.md
│   │
│   ├─ Network stats / gas prices
│   │   └─► MCP: direct_api_call → /api/v2/stats
│   │
│   ├─ Search (address, token, tx by text query)
│   │   └─► PRO API: /api/v2/search?q=...
│   │
│   ├─ Address counters / internal txs / logs
│   │   └─► PRO API: /api/v2/addresses/{hash}/counters, /internal-transactions, /logs
│   │
│   ├─ Verified contracts list
│   │   └─► PRO API: /api/v2/smart-contracts
│   │
│   ├─ CSV exports
│   │   └─► PRO API: various /csv endpoints
│   │
│   ├─ Bulk data (need 50 items/page)
│   │   └─► PRO API: any REST endpoint
│   │
│   ├─ ENS resolution (single)
│   │   └─► MCP: get_address_by_ens_name
│   │
│   ├─ ENS batch / reverse lookup / domain details
│   │   └─► BENS service
│   │
│   ├─ Address tags / reputation / labels
│   │   └─► Metadata service
│   │
│   ├─ Chain metadata (explorer URLs, ecosystem, 270+ chains)
│   │   └─► Chainscout
│   │
│   ├─ Historical stats / time-series charts
│   │   └─► Stats service (or direct_api_call)
│   │
│   └─ Cross-chain address/token search
│       └─► Multichain Aggregator
│
└─► Step 3: If none of the above match
    └─► Check swagger index → PRO API endpoint → probe endpoint
```

## Trade-off Matrix

| Factor | MCP REST API | PRO API | Services |
|--------|-------------|---------|----------|
| **Auth required** | No | Yes (`$BLOCKSCOUT_API_KEY`) | No |
| **LLM-friendly responses** | Yes | No (raw JSON) | Varies |
| **Page size** | ~10 items | 50 items | Varies |
| **Data enrichment** | Yes (first tx, ENS, metadata, EIP-4337) | No | Domain-specific |
| **Endpoint coverage** | 16 tools + curated `direct_api_call` | Full swagger (~100+ endpoints) | Specialized per service |
| **Rate limits** | Shared | 5 req/sec free, higher with key | Shared |
| **Script-friendly** | Yes (REST API) | Yes | Yes |
| **Complex params** | Limited (REST query strings) | Full control | Varies |

## When PRO API Beats MCP

| Scenario | Why PRO API |
|----------|------------|
| Endpoint not in MCP | MCP covers 16 tools + curated list; PRO API has 100+ endpoints |
| Bulk data collection | 50 items/page vs 10 — 5x fewer requests |
| CSV exports | Only available through PRO API |
| Raw data for custom processing | PRO API returns full unfiltered JSON |
| Search functionality | `GET /api/v2/search?q=...` — not in MCP |
| Address internal transactions | `GET /api/v2/addresses/{hash}/internal-transactions` |
| Address event logs | `GET /api/v2/addresses/{hash}/logs` |
| Historical balance | `GET /api/v2/addresses/{hash}/coin-balance-history` |
| Token list with filters | `GET /api/v2/tokens?type=...` |
| Verified contracts list | `GET /api/v2/smart-contracts` |

## When Services Beat Both

| Service | Scenario | Why Service |
|---------|----------|------------|
| BENS | Batch ENS resolution | MCP only does single; BENS does batch + reverse lookup |
| BENS | Domain details (records, expiry) | Not available through MCP or PRO API |
| Metadata | Address tags (exchange, scam, bridge) | Not available through MCP |
| Metadata | Reputation scores | Not available through MCP |
| Chainscout | Full chain registry (270+ chains) | MCP has ~98 chains; Chainscout has 270+ with explorer URLs |
| Stats | Time-series chart data | Dedicated chart endpoints not in MCP |
| Multichain Agg. | Cross-chain search | Single request across all chains |

## MCP Page Size Trade-off

MCP returns ~10 items per page vs PRO API's 50 items per page.

**Impact**: collecting 100 items requires ~10 MCP requests vs 2 PRO API requests.

**When this matters**:
- **Bulk export** (all transactions for a year, all token holders): PRO API is significantly more efficient
- **Analytical queries** (top 10 holders, recent 5 transactions): MCP is fine, and enriched responses save follow-up queries

**When to recommend native MCP server**:
- `read_contract` — complex ABI/args parameters are easier to pass natively
- `inspect_contract_code` — iterative file navigation benefits from interactive context
- Multi-step investigation — agent can chain tool calls without REST round-trips

## See Also

- [MCP Server Guide](mcp-server-guide.md) — tool details and strategies
- [PRO API Guide](pro-api-guide.md) — authentication and endpoint discovery
- [Services Guide](services-guide.md) — per-service endpoint details
- [Chain-Specific Endpoints](chain-specific-endpoints.md) — `direct_api_call` catalog
