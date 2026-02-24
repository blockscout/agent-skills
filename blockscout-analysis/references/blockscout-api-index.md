# Blockscout API Endpoints Index

Use this index to find available endpoints for the `direct_api_call` Blockscout MCP tool. Follow a two-step discovery process:

1. **Find the endpoint below** — locate it by name or category in this index.
2. **Read the linked detail file** — follow the section link (e.g., [Addresses](blockscout-api/addresses.md)) to get full parameter types, descriptions, and examples for use with `direct_api_call`.

## [Blocks](blockscout-api/blocks.md)

- `/api/v2/blocks`: Retrieves a paginated list of blocks with optional filtering by block type.
- `/api/v2/blocks/{block_hash_or_number_param}`: Retrieves detailed information for a specific block, including transactions, internal transactions, and metadata.
- `/api/v2/blocks/{block_hash_or_number_param}/internal-transactions`: Retrieves internal transactions included in a specific block with optional filtering by type and call type.
- `/api/v2/blocks/{block_hash_or_number_param}/transactions`: Retrieves transactions included in a specific block, ordered by transaction index.
- `/api/v2/blocks/{block_hash_or_number_param}/withdrawals`: Retrieves withdrawals processed in a specific block (typically for proof-of-stake networks).
- `/api/v2/blocks/{block_number_param}/countdown`: Calculates the estimated time remaining until a specified block number is reached based on current block and average block time.

## [Transactions](blockscout-api/transactions.md)

- `/api/v2/internal-transactions`: Retrieves a paginated list of internal transactions. Internal transactions are generated during contract execution and not directly recorded on the blockchain.
- `/api/v2/proxy/account-abstraction/operations/{user_operation_hash}`: Get details for a specific User Operation by its hash.
- `/api/v2/transactions`: Retrieves a paginated list of transactions with optional filtering by status, type, and method.
- `/api/v2/transactions/stats`: Retrieves statistics for transactions, including counts and fee summaries for the last 24 hours.
- `/api/v2/transactions/watchlist`: Retrieves transactions in the authenticated user's watchlist.
- `/api/v2/transactions/{transaction_hash_param}`: Retrieves detailed information for a specific transaction identified by its hash.
- `/api/v2/transactions/{transaction_hash_param}/external-transactions`: Retrieves external transactions that are linked to the specified transaction (e.g., Solana transactions in `neon` chain type).
- `/api/v2/transactions/{transaction_hash_param}/internal-transactions`: Retrieves internal transactions generated during the execution of a specific transaction. Useful for analyzing contract interactions and debugging failed transactions.
- `/api/v2/transactions/{transaction_hash_param}/logs`: Retrieves event logs emitted during the execution of a specific transaction. Logs contain information about contract events and state changes.
- `/api/v2/transactions/{transaction_hash_param}/raw-trace`: Retrieves the raw execution trace for a transaction, showing the step-by-step execution path and all contract interactions.
- `/api/v2/transactions/{transaction_hash_param}/state-changes`: Retrieves state changes (balance changes, token transfers) caused by a specific transaction.
- `/api/v2/transactions/{transaction_hash_param}/summary`: Retrieves a human-readable summary of what a transaction did, presented in natural language.
- `/api/v2/transactions/{transaction_hash_param}/token-transfers`: Retrieves token transfers that occurred within a specific transaction, with optional filtering by token type.
- `/api?module=logs&action=getLogs`: Returns event logs filtered by block range, optional contract address, and up to four topic values. Results are capped at 1,000 entries.

## [Addresses](blockscout-api/addresses.md)

- `/api/v2/addresses`: Retrieves a paginated list of addresses holding the native coin, sorted by balance.
- `/api/v2/addresses/{address_hash_param}`: Retrieves detailed information for a specific address, including balance, transaction count, and metadata.
- `/api/v2/addresses/{address_hash_param}/blocks-validated`: Retrieves blocks that were validated (mined) by a specific address. Useful for tracking validator/miner performance.
- `/api/v2/addresses/{address_hash_param}/coin-balance-history`: Retrieves historical native coin balance changes for a specific address, tracking how an address's balance has changed over time.
- `/api/v2/addresses/{address_hash_param}/coin-balance-history-by-day`: Retrieves daily snapshots of native coin balance for a specific address. Useful for generating balance-over-time charts.
- `/api/v2/addresses/{address_hash_param}/counters`: Retrieves count statistics for an address, including transactions, token transfers, gas usage, and validations.
- `/api/v2/addresses/{address_hash_param}/internal-transactions`: Retrieves all internal transactions involving a specific address, with optional filtering for internal transactions sent from or to the address.
- `/api/v2/addresses/{address_hash_param}/logs`: Retrieves event logs emitted by or involving a specific address.
- `/api/v2/addresses/{address_hash_param}/nft`: Retrieves a list of NFTs (non-fungible tokens) owned by a specific address, with optional filtering by token type.
- `/api/v2/addresses/{address_hash_param}/nft/collections`: Retrieves NFTs owned by a specific address, organized by collection. Useful for displaying an address's NFT portfolio grouped by project.
- `/api/v2/addresses/{address_hash_param}/tabs-counters`: Retrieves counters for various address-related entities (max counter value is 51).
- `/api/v2/addresses/{address_hash_param}/token-balances`: Retrieves all token balances held by a specific address, including ERC-20, ERC-721, ERC-1155, and ERC-404 tokens.
- `/api/v2/addresses/{address_hash_param}/token-transfers`: Retrieves token transfers involving a specific address, with optional filtering by token type, direction, and specific token.
- `/api/v2/addresses/{address_hash_param}/tokens`: Retrieves token balances for a specific address with pagination and filtering by token type. Useful for displaying large token portfolios.
- `/api/v2/addresses/{address_hash_param}/transactions`: Retrieves transactions involving a specific address, with optional filtering for transactions sent from or to the address.
- `/api/v2/addresses/{address_hash_param}/withdrawals`: Retrieves withdrawals involving a specific address, typically for proof-of-stake networks supporting validator withdrawals.
- `/api?module=account&action=eth_get_balance`: Returns the ETH balance of an address as a hex-encoded wei value (0x-prefixed). Decode from hexadecimal to get the decimal balance in wei. Supports historical queries via the `block` parameter (e.g. a decimal block number).

## [Tokens](blockscout-api/tokens.md)

- `/api/v2/token-transfers`: Retrieves a paginated list of token transfers across all token types (ERC-20, ERC-721, ERC-1155).
- `/api/v2/tokens/`: Retrieves a paginated list of tokens with optional filtering by name, symbol, or type.
- `/api/v2/tokens/{address_hash_param}`: Retrieves detailed information for a specific token identified by its contract address.
- `/api/v2/tokens/{address_hash_param}/counters`: Retrieves count statistics for a specific token, including holders count and transfers count.
- `/api/v2/tokens/{address_hash_param}/holders`: Retrieves addresses holding a specific token, sorted by balance. Useful for analyzing token distribution.
- `/api/v2/tokens/{address_hash_param}/instances`: Retrieves instances of NFTs for a specific token contract. This endpoint is primarily for ERC-721 and ERC-1155 tokens.
- `/api/v2/tokens/{address_hash_param}/instances/{token_id_param}`: Retrieves detailed information about a specific NFT instance, identified by its token contract address and token ID.
- `/api/v2/tokens/{address_hash_param}/instances/{token_id_param}/holders`: Retrieves current holders of a specific NFT instance. For ERC-721, this will typically be a single address. For ERC-1155, multiple addresses may hold the same token ID.
- `/api/v2/tokens/{address_hash_param}/instances/{token_id_param}/transfers`: Retrieves token transfers for a specific token instance (by token address and token ID).
- `/api/v2/tokens/{address_hash_param}/instances/{token_id_param}/transfers-count`: Retrieves the total number of transfers for a specific NFT instance. Useful for determining how frequently an NFT has changed hands.
- `/api/v2/tokens/{address_hash_param}/transfers`: Retrieves transfer history for a specific NFT instance, showing ownership changes over time.

## [Smart Contracts](blockscout-api/smart-contracts.md)

- `/api/v2/smart-contracts/`: Retrieves a paginated list of verified smart contracts with optional filtering by proxy status or programming language.
- `/api/v2/smart-contracts/counters`: Retrieves count statistics for smart contracts, including total contracts, verified contracts, and new contracts in the last 24 hours.
- `/api/v2/smart-contracts/{address_hash_param}`: Retrieves detailed information about a specific verified smart contract, including source code, ABI, and deployment details.
- `/api/v2/smart-contracts/{address_hash_param}/audit-reports`: Returns audit reports for a given smart contract address.

## [Search](blockscout-api/search.md)

- `/api/v1/search`: Performs a unified search across multiple blockchain entity types including tokens, addresses, contracts, blocks, transactions and other resources.
- `/api/v2/search`: Performs a unified search across multiple blockchain entity types including tokens, addresses, contracts, blocks, transactions and other resources.
- `/api/v2/search/check-redirect`: Checks if a search query redirects to a specific entity page rather than showing search results.
- `/api/v2/search/quick`: Performs a quick, unpaginated search for short queries.

## [Stats](blockscout-api/stats.md)

- `/api/v2/main-page/blocks`: Retrieves a limited set of recent blocks for display on the main page or dashboard.
- `/api/v2/main-page/indexing-status`: Retrieves the current status of blockchain data indexing by the BlockScout instance.
- `/api/v2/main-page/transactions`: Retrieves a limited set of recent transactions displayed on the home page.
- `/api/v2/main-page/transactions/watchlist`: Retrieves a list of last 6 transactions from the current user's watchlist.
- `/api/v2/stats`: Retrieves blockchain network statistics including total blocks, transactions, addresses, average block time, market data, and network utilization.
- `/api/v2/stats/charts/market`: Retrieves time series data of market information (daily closing price, market cap) for rendering charts.
- `/api/v2/stats/charts/secondary-coin-market`: Returns market history for the secondary coin used for charting.
- `/api/v2/stats/charts/transactions`: Retrieves time series data of daily transaction counts for rendering charts.
- `/api/v2/stats/hot-smart-contracts`: Retrieves paginated list of hot smart-contracts
- `/stats-service/api/v1/counters`:
- `/stats-service/api/v1/lines`:
- `/stats-service/api/v1/lines/{name}`:
- `/stats-service/api/v1/pages/contracts`:
- `/stats-service/api/v1/pages/interchain/main`:
- `/stats-service/api/v1/pages/main`:
- `/stats-service/api/v1/pages/multichain/main`:
- `/stats-service/api/v1/pages/transactions`:
- `/stats-service/api/v1/update-status`:

## [Configuration](blockscout-api/config.md)

- `/api/v2/config/backend-version`: Returns application backend version string.
- `/api/v2/config/indexer`: Returns config of indexer.
- `/api/v2/config/public-metrics`: Returns update period / configuration for public metrics.
- `/api/v2/config/smart-contracts/languages`: Returns list of smart contract languages supported by the database schema.

## [Arbitrum](blockscout-api/arbitrum.md)

- `/api/v2/arbitrum/batches/{batch_number}`: Get information for a specific Arbitrum batch.
- `/api/v2/arbitrum/messages/from-rollup`: Get L2 to L1 messages for Arbitrum.
- `/api/v2/arbitrum/messages/to-rollup`: Get L1 to L2 messages for Arbitrum.
- `/api/v2/arbitrum/messages/withdrawals/{transaction_hash}`: Get L2 to L1 messages for a specific transaction hash on Arbitrum.
- `/api/v2/blocks/arbitrum-batch/{batch_number_param}`: Retrieves L2 blocks that are bound to a specific Arbitrum batch number.
- `/api/v2/main-page/arbitrum/batches/latest-number`: Get the latest committed batch number for Arbitrum.
- `/api/v2/transactions/arbitrum-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific Arbitrum batch number.

## [Celo](blockscout-api/celo.md)

- `/api/v2/addresses/{address_hash_param}/celo/election-rewards`: Retrieves Celo election rewards for a specific address.
- `/api/v2/celo/epochs`: Get the latest finalized epochs for Celo.
- `/api/v2/celo/epochs/{epoch_number}`: Get information for a specific Celo epoch.
- `/api/v2/celo/epochs/{epoch_number}/election-rewards/group`: Get validator group rewards for a specific Celo epoch.
- `/api/v2/celo/epochs/{epoch_number}/election-rewards/validator`: Get validator rewards for a specific Celo epoch.
- `/api/v2/celo/epochs/{epoch_number}/election-rewards/voter`: Get voter rewards for a specific Celo epoch.
- `/api/v2/config/celo`: Returns Celo-specific configuration (l2 migration block).

## [Ethereum PoS Chains](blockscout-api/ethereum.md)

These endpoints are only available on chains that use Ethereum proof-of-stake consensus, such as **Ethereum Mainnet** and **Gnosis Chain**. They expose beacon chain deposit tracking and EIP-4844 blob transaction data that do not exist on other EVM networks.

- `/api/v2/addresses/{address_hash_param}/beacon/deposits`: Retrieves Beacon deposits for a specific address.
- `/api/v2/beacon/deposits`: Retrieves a paginated list of all beacon deposits.
- `/api/v2/beacon/deposits/count`: Retrieves the total count of beacon deposits.
- `/api/v2/blocks/{block_hash_or_number_param}/beacon/deposits`: Retrieves beacon deposits included in a specific block with pagination support.
- `/api/v2/transactions/{transaction_hash_param}/beacon/deposits`: Retrieves beacon deposits included in a specific transaction with pagination support.
- `/api/v2/transactions/{transaction_hash_param}/blobs`: Retrieves blobs for a specific transaction (Ethereum only).
- `/api/v2/withdrawals`: Retrieves a paginated list of withdrawals, typically for proof-of-stake networks supporting validator withdrawals.
- `/api/v2/withdrawals/counters`: Returns total withdrawals count and sum from cache.

## [Optimism](blockscout-api/optimism.md)

- `/api/v2/blocks/optimism-batch/{batch_number_param}`: Retrieves L2 blocks that are bound to a specific Optimism batch number.
- `/api/v2/optimism/batches`: Get the latest committed batches for Optimism.
- `/api/v2/optimism/batches/{batch_number}`: Get information for a specific Optimism batch.
- `/api/v2/optimism/deposits`: Get L1 to L2 messages (deposits) for Optimism.
- `/api/v2/optimism/games`: Get dispute games for Optimism.
- `/api/v2/optimism/withdrawals`: Get L2 to L1 messages (withdrawals) for Optimism.
- `/api/v2/transactions/optimism-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific Optimism batch number.

## [Polygon zkEVM](blockscout-api/polygon-zkevm.md)

- `/api/v2/transactions/zkevm-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific Polygon ZkEVM batch number.
- `/api/v2/zkevm/batches/confirmed`: Get the latest confirmed batches for zkEVM.
- `/api/v2/zkevm/batches/{batch_number}`: Get information for a specific zkEVM batch.
- `/api/v2/zkevm/deposits`: Get deposits for zkEVM.
- `/api/v2/zkevm/withdrawals`: Get withdrawals for zkEVM.

## [Redstone](blockscout-api/redstone.md)

- `/api/v2/mud/worlds`: Get a list of MUD worlds for Redstone.
- `/api/v2/mud/worlds/{contract_address}/tables`: Get tables for a specific MUD world on Redstone.
- `/api/v2/mud/worlds/{contract_address}/tables/{table_id}/records`: Get records for a specific MUD world table on Redstone.
- `/api/v2/mud/worlds/{contract_address}/tables/{table_id}/records/{record_id}`: Get a specific record from a MUD world table on Redstone.

## [Scroll](blockscout-api/scroll.md)

- `/api/v2/blocks/scroll-batch/{batch_number_param}`: Retrieves L2 blocks that are bound to a specific Scroll batch number.
- `/api/v2/scroll/batches`: Get the latest committed batches for Scroll.
- `/api/v2/scroll/batches/{batch_number}`: Get information for a specific Scroll batch.
- `/api/v2/scroll/deposits`: Get L1 to L2 messages (deposits) for Scroll.
- `/api/v2/scroll/withdrawals`: Get L2 to L1 messages (withdrawals) for Scroll.
- `/api/v2/transactions/scroll-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific Scroll batch number.

## [Shibarium](blockscout-api/shibarium.md)

- `/api/v2/shibarium/deposits`: Get L1 to L2 messages (deposits) for Shibarium.
- `/api/v2/shibarium/withdrawals`: Get L2 to L1 messages (withdrawals) for Shibarium.

## [Stability](blockscout-api/stability.md)

- `/api/v2/validators/stability`: Get the list of validators for Stability.

## [Zilliqa](blockscout-api/zilliqa.md)

- `/api/v2/validators/zilliqa`: Get the list of validators for Zilliqa.
- `/api/v2/validators/zilliqa/{validator_public_key}`: Get information for a specific Zilliqa validator.

## [ZkSync](blockscout-api/zksync.md)

- `/api/v2/main-page/zksync/batches/latest-number`: Get the latest committed batch number for zkSync.
- `/api/v2/transactions/zksync-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific ZkSync batch number.
- `/api/v2/zksync/batches/{batch_number}`: Get information for a specific zkSync batch.
