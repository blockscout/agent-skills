# Chain-Specific API Endpoints

All endpoints below are accessible via the MCP `direct_api_call` tool or the PRO API.

**MCP REST API**: `GET https://mcp.blockscout.com/v1/direct_api_call?chain_id={id}&endpoint_path={path}`

**PRO API**: `GET https://api.blockscout.com/{chain_id}/api/v2/{path}?apikey=$BLOCKSCOUT_API_KEY`

---

## Common Endpoints (All Chains)

### Stats
| Endpoint | Description |
|----------|-------------|
| `/stats-service/api/v1/counters` | Consolidated historical + recent counters (totals, 24h/30m rollups for txs, accounts, contracts, verified contracts, ERC-4337 ops), avg block time, fee aggregates |
| `/api/v2/stats` | Real-time network status: gas price tiers, utilization, daily txs, avg block time, coin price/market cap |

### User Operations (EIP-4337)
| Endpoint | Description |
|----------|-------------|
| `/api/v2/proxy/account-abstraction/operations/{user_operation_hash}` | Details for a specific User Operation |

### Transaction Logs
| Endpoint | Description |
|----------|-------------|
| `/api/v2/transactions/{transaction_hash}/logs` | Event logs for a specific transaction |

### Tokens & NFTs
| Endpoint | Description |
|----------|-------------|
| `/api/v2/tokens/{token_contract_address}/holders` | Token holder list |
| `/api/v2/tokens/{token_contract_address}/instances` | All NFT instances for a token contract |
| `/api/v2/tokens/{token_contract_address}/instances/{instance_id}` | Specific NFT instance details |
| `/api/v2/tokens/{token_contract_address}/instances/{instance_id}/transfers` | Transfer history for a specific NFT instance |

---

## Ethereum Mainnet & Gnosis

Applicable chains: Ethereum (chain_id: `1`), Gnosis (chain_id: `100`)

### Beacon Chain Deposits
| Endpoint | Description |
|----------|-------------|
| `/api/v2/addresses/{account_address}/beacon/deposits` | Beacon Chain deposits for an address |
| `/api/v2/blocks/{block_number}/beacon/deposits` | Beacon Chain deposits in a specific block |

### Withdrawals
| Endpoint | Description |
|----------|-------------|
| `/api/v2/addresses/{account_address}/withdrawals` | Beacon Chain withdrawals for an address |
| `/api/v2/blocks/{block_number}/withdrawals` | Beacon Chain withdrawals in a specific block |

---

## Arbitrum

Applicable chains: Arbitrum One Nitro (chain_id: `42161`)

### Batches
| Endpoint | Description |
|----------|-------------|
| `/api/v2/main-page/arbitrum/batches/latest-number` | Latest committed batch number |
| `/api/v2/arbitrum/batches/{batch_number}` | Specific batch info |

### L1 ↔ L2 Messages
| Endpoint | Description |
|----------|-------------|
| `/api/v2/arbitrum/messages/to-rollup` | L1 → L2 messages |
| `/api/v2/arbitrum/messages/from-rollup` | L2 → L1 messages |
| `/api/v2/arbitrum/messages/withdrawals/{transaction_hash}` | L2 → L1 messages for a specific tx |

---

## Optimism

Applicable chains: OP Mainnet (chain_id: `10`), and other OP Stack chains

### Batches
| Endpoint | Description |
|----------|-------------|
| `/api/v2/optimism/batches` | Latest committed batches |
| `/api/v2/optimism/batches/{batch_number}` | Specific batch info |

### Dispute Games
| Endpoint | Description |
|----------|-------------|
| `/api/v2/optimism/games` | Dispute games list |

### Deposits & Withdrawals
| Endpoint | Description |
|----------|-------------|
| `/api/v2/optimism/deposits` | L1 → L2 deposits |
| `/api/v2/optimism/withdrawals` | L2 → L1 withdrawals |

---

## Celo

Applicable chains: Celo (chain_id: `42220`)

### Epochs
| Endpoint | Description |
|----------|-------------|
| `/api/v2/celo/epochs` | Latest finalized epochs |
| `/api/v2/celo/epochs/{epoch_number}` | Specific epoch info |

### Election Rewards
| Endpoint | Description |
|----------|-------------|
| `/api/v2/celo/epochs/{epoch_number}/election-rewards/group` | Validator group rewards |
| `/api/v2/celo/epochs/{epoch_number}/election-rewards/validator` | Validator rewards |
| `/api/v2/celo/epochs/{epoch_number}/election-rewards/voter` | Voter rewards |

---

## zkSync

Applicable chains: zkSync Era (chain_id: `324`)

### Batches
| Endpoint | Description |
|----------|-------------|
| `/api/v2/main-page/zksync/batches/latest-number` | Latest committed batch number |
| `/api/v2/zksync/batches/{batch_number}` | Specific batch info |

---

## zkEVM

Applicable chains: Polygon zkEVM and compatible chains

### Batches
| Endpoint | Description |
|----------|-------------|
| `/api/v2/zkevm/batches/confirmed` | Latest confirmed batches |
| `/api/v2/zkevm/batches/{batch_number}` | Specific batch info |

### Deposits & Withdrawals
| Endpoint | Description |
|----------|-------------|
| `/api/v2/zkevm/deposits` | Deposits |
| `/api/v2/zkevm/withdrawals` | Withdrawals |

---

## Scroll

Applicable chains: Scroll (chain_id: `534352`)

### Batches
| Endpoint | Description |
|----------|-------------|
| `/api/v2/scroll/batches` | Latest committed batches |
| `/api/v2/scroll/batches/{batch_number}` | Specific batch info |
| `/api/v2/blocks/scroll-batch/{batch_number}` | Blocks in a specific batch |

### Deposits & Withdrawals
| Endpoint | Description |
|----------|-------------|
| `/api/v2/scroll/deposits` | L1 → L2 deposits |
| `/api/v2/scroll/withdrawals` | L2 → L1 withdrawals |

---

## Shibarium

### Deposits & Withdrawals
| Endpoint | Description |
|----------|-------------|
| `/api/v2/shibarium/deposits` | L1 → L2 deposits |
| `/api/v2/shibarium/withdrawals` | L2 → L1 withdrawals |

---

## Stability

### Validators
| Endpoint | Description |
|----------|-------------|
| `/api/v2/validators/stability` | Validator list |

---

## Zilliqa

### Validators
| Endpoint | Description |
|----------|-------------|
| `/api/v2/validators/zilliqa` | Validator list |
| `/api/v2/validators/zilliqa/{validator_public_key}` | Specific validator info |

---

## Redstone (MUD)

### MUD Worlds
| Endpoint | Description |
|----------|-------------|
| `/api/v2/mud/worlds` | List of MUD worlds |
| `/api/v2/mud/worlds/{contract_address}/tables` | Tables for a MUD world |
| `/api/v2/mud/worlds/{contract_address}/tables/{table_id}/records` | Records for a table |
| `/api/v2/mud/worlds/{contract_address}/tables/{table_id}/records/{record_id}` | Specific record |

---

## Notes

- This catalog comes from the MCP `unlock_blockchain_analysis` tool output. The swagger files for each chain variant may contain additional endpoints not listed here.
- Use `direct_api_call` for these endpoints when working through MCP. Use the PRO API URL pattern for direct access.
- Pagination is supported on list endpoints. Follow `pagination.next_call` (MCP) or `next_page_params` (PRO API).
- The swagger files at `blockscout/9.3.5/{variant}/swagger.yaml` provide full parameter and response schema documentation for these endpoints.

## See Also

- [MCP Server Guide](mcp-server-guide.md) — tool usage including `direct_api_call`
- [Swagger Caching and Indexing](swagger-caching-and-indexing.md) — discover additional endpoints via swagger
- [Infrastructure Overview](infrastructure-overview.md) — swagger file locations
