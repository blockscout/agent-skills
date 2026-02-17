# Blockscout Infrastructure Overview

## Architecture

```
User Request
    │
    ▼
AI Agent
    │
    ├──► MCP Server REST API ──► Blockscout Instances (per chain)
    │    mcp.blockscout.com/v1/     ├─ eth.blockscout.com
    │    - 16 LLM-friendly tools    ├─ polygon.blockscout.com
    │    - Enriched responses        ├─ base.blockscout.com
    │    - 10 items/page             └─ ... (270+ chains)
    │    - No auth required
    │
    ├──► PRO API Gateway ──────► Same Blockscout Instances
    │    api.blockscout.com         (routes via chain_id)
    │    - Full REST/RPC API
    │    - 50 items/page
    │    - Requires $BLOCKSCOUT_API_KEY
    │    - Raw JSON responses
    │
    └──► Supporting Services
         ├─ BENS (ENS)       bens.services.blockscout.com
         ├─ Metadata          metadata.services.blockscout.com
         ├─ Chainscout        chains.blockscout.com
         ├─ Stats             (via direct_api_call or swagger)
         └─ Multichain Agg.  (via swagger)
```

## Instrument Comparison

| Aspect | MCP REST API | PRO API | Services |
|--------|-------------|---------|----------|
| Base URL | `mcp.blockscout.com/v1/` | `api.blockscout.com` | Per-service URLs |
| Auth | None | `$BLOCKSCOUT_API_KEY` | None |
| Response style | LLM-friendly JSON | Raw JSON (verbose) | Varies |
| Page size | ~10 items | 50 items | Varies |
| Pagination | Opaque cursors | Keyset (`next_page_params`) | Varies |
| Data enrichment | Yes (first tx, ENS, metadata, EIP-4337) | No | Domain-specific |
| Coverage | 16 tools + curated endpoints | Full swagger (~100+ endpoints) | Specialized per service |
| Rate limits | Shared | 5 req/sec free, higher with PRO key | Shared |

## MCP Server Access Modes

### REST API (for scripts)
- Base URL: `https://mcp.blockscout.com/v1/`
- All 16 tools available as GET endpoints
- Response: `{"data": ..., "notes": ..., "instructions": ..., "pagination": ...}`
- Use in curl, WebFetch, or any HTTP client

### Native MCP Server (for interactive agent use)
- Endpoint: `https://mcp.blockscout.com/mcp`
- Requires MCP server configuration in the agent environment
- Better for: contract analysis (`inspect_contract_code`, `read_contract`), iterative investigation workflows
- Recommend user configure this for complex interactive tasks

## Swagger Repository

API documentation for all Blockscout components lives at `github.com/blockscout/swaggers`.

### Blockscout Main API

Location: `blockscout/{version}/{variant}/swagger.yaml`

Current stable version: **9.3.5**

| Variant | Description |
|---------|-------------|
| `default` | Base API (all chains) — start here |
| `arbitrum` | Arbitrum-specific fields + endpoints |
| `ethereum` | Ethereum Mainnet-specific (beacon, withdrawals) |
| `optimism` | Optimism-specific (batches, games, deposits) |
| `scroll` | Scroll-specific (batches, deposits) |
| `zksync` | zkSync-specific (batches) |
| `polygon_zkevm` | Polygon zkEVM-specific |
| `shibarium` | Shibarium-specific |
| `stability` | Stability-specific (validators) |
| `zilliqa` | Zilliqa-specific (validators) |
| `zetachain` | ZetaChain-specific |
| `rsk` | RSK-specific |
| `blackfort` | BlackFort-specific |
| `filecoin` | Filecoin-specific |
| `neon` | Neon-specific |
| `optimism-celo` | Celo (Optimism-based)-specific |

Raw URL pattern:
```
https://raw.githubusercontent.com/blockscout/swaggers/master/blockscout/9.3.5/{variant}/swagger.yaml
```

### Service Swaggers

Location: `services/{name}/main/swagger.yaml`

| Service | Name in Repo | Base URL |
|---------|-------------|----------|
| BENS (ENS) | `bens` | `bens.services.blockscout.com/api/v1` |
| Metadata | `metadata` | `metadata.services.blockscout.com/api/v1` |
| Stats | `stats` | via `direct_api_call` |
| Multichain Aggregator | `multichain-aggregator` | via swagger |
| Sig Provider | `sig-provider` | Function signature DB |
| Visualizer | `visualizer` | Contract visualization |
| Smart Contract Verifier | `smart-contract-verifier` | Verification |
| ETH Bytecode DB | `eth-bytecode-db` | Bytecode matching |
| DA Indexer | `da-indexer` | Data availability |
| User Ops Indexer | `user-ops-indexer` | EIP-4337 indexing |
| Admin RS | `admin-rs` | Admin API |
| Autoscout | `autoscout` | Auto-discovery |
| Proxy Verifier | `proxy-verifier` | Proxy verification |
| Merits | `merits` | Merits system |
| TAC Operation Lifecycle | `tac-operation-lifecycle` | TAC ops |
| Interchain Indexer | `interchain-indexer` | Cross-chain indexing |

Raw URL pattern:
```
https://raw.githubusercontent.com/blockscout/swaggers/master/services/{name}/main/swagger.yaml
```

## See Also

- [MCP Server Guide](mcp-server-guide.md) — full tool catalog and strategies
- [PRO API Guide](pro-api-guide.md) — authentication, routing, examples
- [Services Guide](services-guide.md) — BENS, Metadata, Chainscout, Stats details
- [Decision Framework](decision-framework.md) — when to use which instrument
- [Swagger Caching and Indexing](swagger-caching-and-indexing.md) — endpoint discovery workflow
- [Chain-Specific Endpoints](chain-specific-endpoints.md) — L2/chain-family endpoints
