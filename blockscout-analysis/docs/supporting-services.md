# Supporting Services

Specialized Blockscout services for ENS resolution, address metadata, chain registry, statistics, and cross-chain search.

## Overview

| Service | Base URL | Purpose | Swagger |
|---------|----------|---------|---------|
| BENS | `https://bens.services.blockscout.com/api/v1` | ENS domains, batch resolution, reverse lookup | Yes |
| Metadata | `https://metadata.services.blockscout.com/api/v1` | Address tags, reputation, public labels | Yes |
| Chainscout | `https://chains.blockscout.com/api` | Chain registry, explorer URLs | No |
| Stats | via `direct_api_call` on instances | Historical counters, time-series charts | Yes |
| Multichain Aggregator | via swagger (no standalone public URL) | Cross-chain address/token search | Yes |

## BENS (Blockchain ENS Service)

Resolves ENS domains and provides batch operations.

**Base URL**: `https://bens.services.blockscout.com/api/v1`

**Key endpoints**:
- `GET /api/v1/addresses/{address}` — resolve address to ENS domain(s)
- `POST /api/v1/addresses:batch-resolve` — batch resolution (multiple addresses)
- `GET /api/v1/domains/{name}` — lookup domain details
- `GET /api/v1/{chain_id}/addresses:lookup` — chain-scoped reverse lookup

**Note**: The MCP tool `get_address_by_ens_name` uses BENS internally for single-name resolution. Use BENS directly for **batch resolution** or **reverse lookup**.

## Metadata

Address tags, reputation scores, and public labels.

**Base URL**: `https://metadata.services.blockscout.com/api/v1`

**Key endpoints**:
- `GET /api/v1/addresses` — public tag addresses
- `GET /api/v1/tags/search` — search tags

**Note**: The MCP tool `get_address_info` automatically enriches responses with metadata (tags, labels). Use the Metadata service directly when you need tag search or bulk tag operations.

## Chainscout

Registry of all chains where Blockscout is deployed. Provides explorer URLs.

**Base URL**: `https://chains.blockscout.com/api`

**Endpoints**:
- `GET /chains` — full chain data with optional `?chain_ids=1,137,8453` filter
- `GET /chains/list` — simplified list: `[{"name": "...", "chainid": "..."}]`

**No swagger** — API reverse-engineered from [source](https://github.com/blockscout/chainscout/tree/main/app/api/chains).

**Important**: The MCP tool `get_chains_list` returns chain IDs and names but does **not** return Blockscout explorer URLs. When you need the explorer URL for a specific chain, call the Chainscout API directly with `GET /chains?chain_ids={id}`.

## Stats

Historical counters and time-series charts for individual Blockscout instances.

**Access**: Via `direct_api_call` MCP tool using the stats-service paths on individual instances. The `unlock_blockchain_analysis` response catalogs available stats endpoints.

**Key paths** (via `direct_api_call`):
- `/api/v2/stats` — current network stats
- `/api/v2/stats/charts/transactions` — transaction count chart

**Swagger**: Available in [blockscout/swaggers](https://github.com/blockscout/swaggers/tree/master/services/stats) repo. Use the [Swagger Cache Guide](swagger-cache-guide.md) for endpoint discovery.

## Multichain Aggregator

Cross-chain address and token search across all Blockscout-indexed chains.

**Swagger**: Available in [blockscout/swaggers](https://github.com/blockscout/swaggers/tree/master/services/multichain-aggregator) repo.

**Key capabilities**:
- Cross-chain address search
- Cross-chain token search
- Cluster-based multichain data
- Block lookups across chains

Use the [Swagger Cache Guide](swagger-cache-guide.md) for endpoint discovery.

## Swagger Documentation

For BENS, Metadata, Stats, and Multichain Aggregator swagger files, use the caching and indexing system described in the [Swagger Cache Guide](swagger-cache-guide.md).
