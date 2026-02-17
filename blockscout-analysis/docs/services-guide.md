# Supporting Services Guide

## BENS (Blockchain ENS Service)

**Base URL**: `https://bens.services.blockscout.com/api/v1`

**Swagger**: `https://raw.githubusercontent.com/blockscout/swaggers/master/services/bens/main/swagger.yaml`

**When to use**: batch ENS resolution, reverse lookup (address → domain), domain details, domain search. The MCP `get_address_by_ens_name` tool handles single ENS-to-address resolution — use BENS for batch or advanced operations.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/domains/{name}` | Detailed domain info (owner, resolver, records, expiry) |
| POST | `/api/v1/addresses:batch-resolve` | Batch address → ENS name resolution |
| GET | `/api/v1/addresses:lookup?address={addr}` | Reverse lookup: address → associated domains |
| GET | `/api/v1/domains:lookup?name={query}` | Search domains by name pattern |

### Example: Batch Resolve Addresses

```bash
curl -X POST "https://bens.services.blockscout.com/api/v1/addresses:batch-resolve" \
  -H "Content-Type: application/json" \
  -d '{
    "addresses": [
      "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
      "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"
    ]
  }'
```

### Notes
- For the full endpoint catalog and request/response schemas, fetch and index the BENS swagger file
- BENS release versions are tagged with `bens` prefix in `github.com/blockscout/blockscout-rs/releases`

---

## Metadata Service

**Base URL**: `https://metadata.services.blockscout.com/api/v1`

**Swagger**: `https://raw.githubusercontent.com/blockscout/swaggers/master/services/metadata/main/swagger.yaml`

**When to use**: address tags (exchange, fund, scam, bridge), reputation scores, public labels. This data is not available through MCP tools.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/metadata?addresses={addr1,addr2}&chain_id={id}` | Tags and reputation for addresses |
| GET | `/api/v1/addresses?slug={slug}` | Find addresses by public tag slug |
| GET | `/api/v1/reputation?addresses={addr1,addr2}` | Reputation scores for addresses |
| GET | `/api/v1/tags:search?q={query}` | Search public tags |

### Example: Get Address Tags

```bash
curl -s "https://metadata.services.blockscout.com/api/v1/metadata?addresses=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&chain_id=1"
```

### Notes
- Tags include categories like: exchange, DeFi protocol, bridge, known scam, multisig, etc.
- Reputation scores help identify potentially malicious addresses
- Data is crowdsourced and curated by the Blockscout team

---

## Chainscout

**Base URL**: `https://chains.blockscout.com/api`

**Swagger**: none (API reverse-engineered from source at `github.com/blockscout/chainscout`)

**When to use**: chain metadata (explorer URLs, ecosystem classification, layer type), full chain registry (270+ chains vs MCP's ~98).

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/chains` | Full chain registry keyed by chain_id. Optional `?chain_ids=1,137,8453` filter. |
| GET | `/chains/list` | Simplified array: `[{"name": "Ethereum", "chainid": "1"}, ...]` |

### Response Fields (per chain in `/chains`)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Chain name (e.g., "Ethereum") |
| `description` | string | Short chain description |
| `logo` | string | URL to chain logo SVG |
| `ecosystem` | string | Ecosystem name (e.g., "Ethereum", "Polygon", "Arbitrum") |
| `isTestnet` | boolean | Whether it's a testnet |
| `layer` | number | Layer (1 or 2) |
| `rollupType` | string/null | Rollup type (null for L1s) |
| `native_currency` | string | Native currency symbol (e.g., "ETH") |
| `website` | string | Chain website URL |
| `explorers` | array | `[{"url": "https://eth.blockscout.com/", "hostedBy": "blockscout"}]` |

### Example: Get Explorer URL for a Chain

```bash
# Get Ethereum info including explorer URL
curl -s "https://chains.blockscout.com/api/chains?chain_ids=1" | python3 -c "
import json, sys
data = json.load(sys.stdin)
chain = data.get('1', {})
explorers = chain.get('explorers', [])
for e in explorers:
    print(f\"{e['hostedBy']}: {e['url']}\")
"
```

### Notes
- Returns 270+ chains (more comprehensive than MCP's `get_chains_list` which has ~98)
- Explorer URLs are useful for constructing direct Blockscout instance links
- The `/chains` endpoint returns a JSON object keyed by chain_id (strings), not an array

---

## Stats Service

**Swagger**: `https://raw.githubusercontent.com/blockscout/swaggers/master/services/stats/main/swagger.yaml`

**When to use**: historical aggregate statistics, time-series chart data, trend analysis.

### Access Methods

1. **Via MCP `direct_api_call`** (preferred for simple queries):
   - `/stats-service/api/v1/counters` — consolidated counters
   - `/api/v2/stats` — real-time network status

2. **Via swagger** (for full endpoint catalog):
   - Fetch and index the stats service swagger for available chart and counter endpoints

### Key Endpoints (from swagger)

| Endpoint | Description |
|----------|-------------|
| `/api/v1/counters` | Historical totals: transactions, accounts, contracts, verified contracts, ERC-4337 user ops, avg block time, fee aggregates |
| `/api/v1/lines/{chart_name}` | Time-series chart data. Chart names vary by instance. |

### Notes
- Chart names are instance-specific — probe the endpoint or check swagger for available charts
- Common charts: `txnsGrowth`, `activeAccounts`, `averageBlockTime`, `gasUsedGrowth`

---

## Multichain Aggregator

**Swagger**: `https://raw.githubusercontent.com/blockscout/swaggers/master/services/multichain-aggregator/main/swagger.yaml`

**When to use**: searching for the same address or token across multiple chains in a single request.

### Notes
- Release versions tagged with `multichain-aggregator` prefix in `github.com/blockscout/blockscout-rs/releases`
- Aggregates data from multiple Blockscout instances
- Useful for tracking cross-chain activity of an address
- For endpoint details, fetch and index the multichain-aggregator swagger

---

## Other Services (Rarely Needed for Activity Analysis)

| Service | Swagger Dir | Purpose |
|---------|-------------|---------|
| `sig-provider` | `services/sig-provider` | Function/event signature database (4-byte selectors → human-readable names) |
| `visualizer` | `services/visualizer` | Solidity contract source code visualization |
| `smart-contract-verifier` | `services/smart-contract-verifier` | Contract verification service |
| `eth-bytecode-db` | `services/eth-bytecode-db` | Bytecode matching database (find verified contracts by bytecode) |
| `user-ops-indexer` | `services/user-ops-indexer` | EIP-4337 User Operations indexing |
| `da-indexer` | `services/da-indexer` | Data availability layer indexing |
| `proxy-verifier` | `services/proxy-verifier` | Proxy contract verification |
| `interchain-indexer` | `services/interchain-indexer` | Cross-chain message indexing |

These are specialized services for contract development, verification, and infrastructure. Rarely needed for blockchain activity analysis.

---

## See Also

- [MCP Server Guide](mcp-server-guide.md) — MCP tools that overlap with some services
- [Infrastructure Overview](infrastructure-overview.md) — full service catalog with URLs
- [Decision Framework](decision-framework.md) — when to use services vs MCP vs PRO API
