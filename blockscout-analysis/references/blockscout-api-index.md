# Blockscout API Endpoints Index

Use this index to find available endpoints for the `direct_api_call` Blockscout MCP tool. Follow a two-step discovery process:

1. **Find the endpoint below** — locate it by name or category in this index.
2. **Read the linked detail file** — follow the section link (e.g., [Addresses](blockscout-api/addresses.md)) to get full parameter types and descriptions for use with `direct_api_call`.

## [Blocks](blockscout-api/blocks.md)

- `/api/v2/blocks`: Retrieves a paginated list of blocks ordered by descending block number.
- `/api/v2/blocks/{block_hash_or_number_param}/internal-transactions`: Retrieves internal transactions included in a specific block with optional filtering by type and call type.
- `/api/v2/blocks/{block_hash_or_number_param}/transactions`: Retrieves transactions included in a specific block, ordered by transaction index.
- `/api/v2/blocks/{block_hash_or_number_param}/withdrawals`: Retrieves withdrawals processed in a specific block (typically for proof-of-stake networks).
- `/api/v2/blocks/{block_number_param}/countdown`: Calculates the estimated time remaining until a specified block number is reached based on current block and average block time.

## [Transactions](blockscout-api/transactions.md)

- `/api/v2/advanced-filters`: Returns a paginated, mixed list of activity — native value transfers, internal transactions and token transfers — filtered by transaction type, contract method, time window, address relations, value range and/or token contract. The response also echoes the resolved human-readable names of the methods and tokens referenced in the request filters.
- `/api/v2/advanced-filters/methods`: Returns a list of known contract methods. When the `q` parameter is provided, searches for a single method by its 4-byte selector or name. Without `q`, returns the default list of popular methods.
- `/api/v2/internal-transactions`: Retrieves a paginated list of internal transactions. Internal transactions are generated during contract execution and not directly recorded on the blockchain.
- `/api/v2/transactions`: Retrieves a paginated list of transactions with optional filtering by status, type, and method.
- `/api/v2/transactions/execution-node/{execution_node_hash_param}`: Retrieves transactions that were executed on the specified execution node.
- `/api/v2/transactions/stats`: Retrieves statistics for transactions, including counts and fee summaries for the last 24 hours.
- `/api/v2/transactions/watchlist`: Retrieves transactions in the authenticated user's watchlist.
- `/api/v2/transactions/{transaction_hash_param}/external-transactions`: Retrieves external transactions that are linked to the specified transaction (e.g., Solana transactions in `neon` chain type).
- `/api/v2/transactions/{transaction_hash_param}/fhe-operations`: Retrieves Fully Homomorphic Encryption (FHE) operations parsed from transaction logs. Includes operation details, HCU (Homomorphic Compute Unit) costs, operation types, and related metadata.
- `/api/v2/transactions/{transaction_hash_param}/internal-transactions`: Retrieves internal transactions generated during the execution of a specific transaction. Useful for analyzing contract interactions and debugging failed transactions.
- `/api/v2/transactions/{transaction_hash_param}/logs`: Retrieves event logs emitted during the execution of a specific transaction. Logs contain information about contract events and state changes.
- `/api/v2/transactions/{transaction_hash_param}/raw-trace`: Retrieves the raw execution trace for a transaction, showing the step-by-step execution path and all contract interactions.
- `/api/v2/transactions/{transaction_hash_param}/state-changes`: Retrieves state changes (balance changes, token transfers) caused by a specific transaction.
- `/api/v2/transactions/{transaction_hash_param}/summary`: Retrieves a human-readable summary of what a transaction did, presented in natural language.
- `/api/v2/transactions/{transaction_hash_param}/token-transfers`: Retrieves token transfers that occurred within a specific transaction, with optional filtering by token type.
- `/api?module=logs&action=getLogs`: Returns event logs filtered by block range, optional contract address, and up to four topic values.

## [User Operations](blockscout-api/user-operations.md)

- `/api/v2/proxy/account-abstraction/accounts`: Retrieves a list of account abstraction wallets.
- `/api/v2/proxy/account-abstraction/accounts/{address_hash_param}`: Retrieves an account abstraction wallet by its address hash.
- `/api/v2/proxy/account-abstraction/bundlers`: Retrieves a list of top bundlers.
- `/api/v2/proxy/account-abstraction/bundlers/{address_hash_param}`: Retrieves a bundler by its address hash.
- `/api/v2/proxy/account-abstraction/bundles`: Retrieves a list of recent bundles.
- `/api/v2/proxy/account-abstraction/factories`: Retrieves a list of top wallet factories.
- `/api/v2/proxy/account-abstraction/factories/{address_hash_param}`: Retrieves a factory by its address hash.
- `/api/v2/proxy/account-abstraction/operations`: Retrieves a list of recent user operations.
- `/api/v2/proxy/account-abstraction/operations/{operation_hash_param}`: Retrieves a user operation by its hash.
- `/api/v2/proxy/account-abstraction/operations/{operation_hash_param}/summary`: Retrieves a human-readable summary of what a user operation did, presented in natural language.
- `/api/v2/proxy/account-abstraction/paymasters`: Retrieves a list of top paymasters.
- `/api/v2/proxy/account-abstraction/paymasters/{address_hash_param}`: Retrieves a paymaster by its address hash.
- `/api/v2/proxy/account-abstraction/status`: Retrieves the status of the account abstraction microservice.

## [Addresses](blockscout-api/addresses.md)

- `/api/v2/addresses`: Retrieves a paginated list of addresses holding the native coin, sorted by balance.
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
- `/api?module=account&action=eth_get_balance`: Returns the ETH balance of an address in an Ethereum-compatible hex format (0x-prefixed).

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
- `/stats-service/api/v1/counters`: Returns all available counter stats for the stats page.
- `/stats-service/api/v1/lines`: Returns metadata (title, description, available resolutions) for all line charts, organized into sections.
- `/stats-service/api/v1/lines/{name}`: Returns data points for a specific line chart, with optional date range and resolution filtering.
- `/stats-service/api/v1/pages/contracts`: Returns stats to be displayed on the contracts page.
- `/stats-service/api/v1/pages/interchain/main`: Returns interchain messaging stats to be displayed on the main page of interchain indexer.
- `/stats-service/api/v1/pages/main`: Returns stats to be displayed on the main page of indexer.
- `/stats-service/api/v1/pages/multichain/main`: Returns multichain-aggregated stats to be displayed on the main page of multichain indexer.
- `/stats-service/api/v1/pages/transactions`: Returns stats to be displayed on the transactions page.
- `/stats-service/api/v1/update-status`: Returns the current status of chart data updates, broken down by indexing dependency type (independent, blocks, internal transactions, etc.).

## [Arbitrum](blockscout-api/arbitrum.md)

- `/api/v2/arbitrum/batches`: Retrieves a paginated list of Arbitrum batches committed to the Parent chain.
- `/api/v2/arbitrum/batches/count`: Retrieves the total count of Arbitrum batches committed to the Parent chain.
- `/api/v2/arbitrum/batches/da/anytrust/{data_hash}`: Retrieves an Arbitrum batch associated with the given AnyTrust data hash. By default, returns the most recently associated batch. When `type=all`, returns a paginated list of all batches referencing this data hash.
- `/api/v2/arbitrum/batches/da/celestia/{height}/{transaction_commitment}`: Retrieves an Arbitrum batch whose data availability blob is identified by the given Celestia block height and transaction commitment hash.
- `/api/v2/arbitrum/batches/da/eigenda/{data_hash}`: Retrieves an Arbitrum batch associated with the given EigenDA data hash. By default, returns the most recently associated batch. When `type=all`, returns a paginated list of all batches referencing this data hash.
- `/api/v2/arbitrum/batches/{batch_number}`: Retrieves detailed information about an Arbitrum batch by its number.
- `/api/v2/arbitrum/messages/claim/{message_id}`: Returns the ABI-encoded calldata and outbox contract address required to execute a Rollup withdrawal on the Parent chain.
- `/api/v2/arbitrum/messages/withdrawals/{transaction_hash}`: Returns the list of Rollup withdrawal messages (L2ToL1Tx events) emitted by the given transaction.
- `/api/v2/arbitrum/messages/{direction}`: Retrieves a paginated list of Arbitrum cross-chain messages filtered by the specified direction.
- `/api/v2/arbitrum/messages/{direction}/count`: Retrieves the total count of Arbitrum cross-chain messages for the specified direction.
- `/api/v2/blocks/arbitrum-batch/{batch_number_param}`: Retrieves L2 blocks that are bound to a specific Arbitrum batch number.
- `/api/v2/main-page/arbitrum/batches/committed`: Retrieves a list of Arbitrum batches that have been committed to the Parent chain, displayed on the main page.
- `/api/v2/main-page/arbitrum/batches/latest-number`: Retrieves the number of the most recent Arbitrum batch submitted to the Parent chain. Returns 0 if no batches exist.
- `/api/v2/main-page/arbitrum/messages/to-rollup`: Retrieves the most recent relayed messages from Parent chain to Rollup, displayed on the main page.
- `/api/v2/transactions/arbitrum-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific Arbitrum batch number.

## [Celo](blockscout-api/celo.md)

- `/api/v2/addresses/{address_hash_param}/celo/election-rewards`: Retrieves Celo election rewards for a specific address.
- `/api/v2/celo/epochs`: Retrieves a paginated list of Celo epochs.
- `/api/v2/celo/epochs/{number}`: Retrieves detailed information about a Celo epoch.
- `/api/v2/celo/epochs/{number}/election-rewards/{type}`: Retrieves a paginated list of election rewards for a Celo epoch and reward type.

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

## [Mud](blockscout-api/mud.md)

- `/api/v2/mud/worlds`: Retrieves a paginated list of MUD worlds with basic stats.
- `/api/v2/mud/worlds/count`: Retrieves the total number of known MUD worlds.
- `/api/v2/mud/worlds/{world}/systems`: Retrieves a list of MUD systems registered in the specific MUD world.
- `/api/v2/mud/worlds/{world}/systems/{system}`: Retrieves a list of MUD system ABI methods registered in the specific MUD world.
- `/api/v2/mud/worlds/{world}/tables`: Retrieves a paginated list of MUD tables in the specific MUD world.
- `/api/v2/mud/worlds/{world}/tables/count`: Retrieves the total number of known MUD tables in the specific MUD world.
- `/api/v2/mud/worlds/{world}/tables/{table_id}/records`: Retrieves a paginated list of records in the specific MUD world table.
- `/api/v2/mud/worlds/{world}/tables/{table_id}/records/count`: Retrieves the total number of records in the specific MUD world table.
- `/api/v2/mud/worlds/{world}/tables/{table_id}/records/{record_id}`: Retrieves a single record in the specific MUD world table.

## [Optimism](blockscout-api/optimism.md)

- `/api/v2/blocks/optimism-batch/{batch_number_param}`: Retrieves L2 blocks that are bound to a specific Optimism batch number.
- `/api/v2/main-page/optimism-deposits`: Retrieves a list of deposits for the main page.
- `/api/v2/optimism/batches`: Retrieves a paginated list of batches.
- `/api/v2/optimism/batches/count`: Retrieves a size of the batch list.
- `/api/v2/optimism/batches/da/celestia/{height}/{commitment}`: Retrieves batch detailed info by the given celestia blob metadata (height and commitment).
- `/api/v2/optimism/batches/{number}`: Retrieves batch detailed info by the given number.
- `/api/v2/optimism/deposits`: Retrieves a paginated list of deposits.
- `/api/v2/optimism/deposits/count`: Retrieves a size of the deposits list.
- `/api/v2/optimism/games`: Retrieves a paginated list of games.
- `/api/v2/optimism/games/count`: Retrieves a size of the games list.
- `/api/v2/optimism/output-roots`: Retrieves a paginated list of output roots.
- `/api/v2/optimism/output-roots/count`: Retrieves a size of the output roots list.
- `/api/v2/optimism/withdrawals`: Retrieves a paginated list of withdrawals.
- `/api/v2/optimism/withdrawals/count`: Retrieves a size of the withdrawals list.
- `/api/v2/transactions/optimism-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific Optimism batch number.

## [Scroll](blockscout-api/scroll.md)

- `/api/v2/blocks/scroll-batch/{batch_number_param}`: Retrieves L2 blocks that are bound to a specific Scroll batch number.
- `/api/v2/scroll/batches`: Retrieves a paginated list of batches.
- `/api/v2/scroll/batches/count`: Retrieves a size of the batch list.
- `/api/v2/scroll/batches/{number}`: Retrieves batch info by the given number.
- `/api/v2/scroll/deposits`: Retrieves a paginated list of deposits.
- `/api/v2/scroll/deposits/count`: Retrieves a size of the deposits list.
- `/api/v2/scroll/withdrawals`: Retrieves a paginated list of withdrawals.
- `/api/v2/scroll/withdrawals/count`: Retrieves a size of the withdrawals list.
- `/api/v2/transactions/scroll-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific Scroll batch number.

## [Shibarium](blockscout-api/shibarium.md)

- `/api/v2/shibarium/deposits`: Get L1 to L2 messages (deposits) for Shibarium.
- `/api/v2/shibarium/withdrawals`: Get L2 to L1 messages (withdrawals) for Shibarium.

## [Stability](blockscout-api/stability.md)

- `/api/v2/validators/stability`: Get the list of validators for Stability.

## [Zilliqa](blockscout-api/zilliqa.md)

- `/api/v2/validators/zilliqa`: Retrieves the list of Zilliqa validators.
- `/api/v2/validators/zilliqa/{bls_public_key}`: Retrieves Zilliqa validator detailed info by the given BLS public key.

## [ZkSync](blockscout-api/zksync.md)

- `/api/v2/main-page/zksync/batches/latest-number`: Get the latest committed batch number for zkSync.
- `/api/v2/transactions/zksync-batch/{batch_number_param}`: Retrieves L2 transactions bound to a specific ZkSync batch number.
- `/api/v2/zksync/batches/{batch_number}`: Get information for a specific zkSync batch.
