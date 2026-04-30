# PRO API Endpoint Index

## account-abstraction

GET /{chain_id}/api/v2/proxy/account-abstraction/accounts: List of account abstraction wallets
GET /{chain_id}/api/v2/proxy/account-abstraction/accounts/{address_hash_param}: Get an account abstraction wallet by address hash
GET /{chain_id}/api/v2/proxy/account-abstraction/bundlers: List of top bundlers
GET /{chain_id}/api/v2/proxy/account-abstraction/bundlers/{address_hash_param}: Get a bundler by address hash
GET /{chain_id}/api/v2/proxy/account-abstraction/bundles: List of recent bundles
GET /{chain_id}/api/v2/proxy/account-abstraction/factories: List of top wallet factories
GET /{chain_id}/api/v2/proxy/account-abstraction/factories/{address_hash_param}: Get a factory by address hash
GET /{chain_id}/api/v2/proxy/account-abstraction/operations: List of recent user operations
GET /{chain_id}/api/v2/proxy/account-abstraction/operations/{operation_hash_param}: Get a user operation by hash
GET /{chain_id}/api/v2/proxy/account-abstraction/operations/{operation_hash_param}/summary: Get a human-readable, LLM-based user operation summary
GET /{chain_id}/api/v2/proxy/account-abstraction/paymasters: List of top paymasters
GET /{chain_id}/api/v2/proxy/account-abstraction/paymasters/{address_hash_param}: Get a paymaster by address hash
GET /{chain_id}/api/v2/proxy/account-abstraction/status: Get the status of the account abstraction microservice

## addresses

GET /{chain_id}/api/v2/addresses: List addresses holding native coins sorted by balance - top accounts
GET /{chain_id}/api/v2/addresses/{address_hash_param}: Retrieve detailed information about a specific address or contract
GET /{chain_id}/api/v2/addresses/{address_hash_param}/beacon/deposits: List Beacon Deposits for a specific address
GET /{chain_id}/api/v2/addresses/{address_hash_param}/blocks-validated: List blocks validated (mined) by a specific validator/miner address
GET /{chain_id}/api/v2/addresses/{address_hash_param}/celo/election-rewards: List Celo election rewards for a specific address
GET /{chain_id}/api/v2/addresses/{address_hash_param}/celo/election-rewards/csv: Export Celo election rewards as CSV
GET /{chain_id}/api/v2/addresses/{address_hash_param}/coin-balance-history: Get native coin balance history for an address showing all balance changes
GET /{chain_id}/api/v2/addresses/{address_hash_param}/coin-balance-history-by-day: Get daily native coin balance snapshots for an address from previous 10 days
GET /{chain_id}/api/v2/addresses/{address_hash_param}/counters: Get activity count stats for a specific address
GET /{chain_id}/api/v2/addresses/{address_hash_param}/internal-transactions: List all internal transactions involving a specific address
GET /{chain_id}/api/v2/addresses/{address_hash_param}/internal-transactions/csv: Export internal transactions as CSV
GET /{chain_id}/api/v2/addresses/{address_hash_param}/logs: List event logs emitted by or involving a specific address
GET /{chain_id}/api/v2/addresses/{address_hash_param}/logs/csv: Export logs as CSV
GET /{chain_id}/api/v2/addresses/{address_hash_param}/nft: List NFTs owned by a specific address with optional type filtering
GET /{chain_id}/api/v2/addresses/{address_hash_param}/nft/collections: List NFTs owned by an address grouped by collection/project
GET /{chain_id}/api/v2/addresses/{address_hash_param}/tabs-counters: Get counters for address tabs
GET /{chain_id}/api/v2/addresses/{address_hash_param}/token-balances: List all token balances held by a specific address
GET /{chain_id}/api/v2/addresses/{address_hash_param}/token-transfers: List token transfers involving a specific address with filtering options
GET /{chain_id}/api/v2/addresses/{address_hash_param}/token-transfers/csv: Export token transfers as CSV
GET /{chain_id}/api/v2/addresses/{address_hash_param}/tokens: List token balances for an address with pagination and type filtering
GET /{chain_id}/api/v2/addresses/{address_hash_param}/transactions: List transactions involving a specific address with to-from filtering
GET /{chain_id}/api/v2/addresses/{address_hash_param}/transactions/csv: Export transactions as CSV
GET /{chain_id}/api/v2/addresses/{address_hash_param}/withdrawals: List validator withdrawals involving a specific address

## beacon_deposits

GET /{chain_id}/api/v2/beacon/deposits: Lists all beacon deposits
GET /{chain_id}/api/v2/beacon/deposits/count: Gets total count of beacon deposits

## blocks

GET /{chain_id}/api/v2/blocks: List blocks with optional filtering by block type
GET /{chain_id}/api/v2/blocks/arbitrum-batch/{batch_number_param}: List L2 blocks in an Arbitrum batch
GET /{chain_id}/api/v2/blocks/optimism-batch/{batch_number_param}: List L2 blocks in an Optimism batch
GET /{chain_id}/api/v2/blocks/scroll-batch/{batch_number_param}: List L2 blocks in a Scroll batch
GET /{chain_id}/api/v2/blocks/{block_hash_or_number_param}: Retrieves detailed information for a specific block identified by its number or hash.
GET /{chain_id}/api/v2/blocks/{block_hash_or_number_param}/beacon/deposits: List beacon deposits in a specific block
GET /{chain_id}/api/v2/blocks/{block_hash_or_number_param}/internal-transactions: List internal transactions in a specific block
GET /{chain_id}/api/v2/blocks/{block_hash_or_number_param}/transactions: List transactions and tx details included in a specific block
GET /{chain_id}/api/v2/blocks/{block_hash_or_number_param}/withdrawals: List validator withdrawals including amounts, index and receiver details processed in a specific block
GET /{chain_id}/api/v2/blocks/{block_number_param}/countdown: Get countdown information for a target block number

## celo

GET /{chain_id}/api/v2/celo/epochs: List Celo epochs.
GET /{chain_id}/api/v2/celo/epochs/{number}: Get Celo epoch details.
GET /{chain_id}/api/v2/celo/epochs/{number}/election-rewards/{type}: List Celo epoch election rewards.

## ClusterExplorerService

GET /services/multichain/api/v1/clusters/{cluster_id}/search/addresses: Full-text search for addresses by query string; optional chain filter and pagination.
GET /services/multichain/api/v1/clusters/{cluster_id}/search/block-numbers: Full-text search for block numbers (returns chain + block number); optional chain filter and pagination.
GET /services/multichain/api/v1/clusters/{cluster_id}/search/blocks: Full-text search for blocks (returns block hashes); optional chain filter and pagination.
GET /services/multichain/api/v1/clusters/{cluster_id}/search/domains: Full-text search for domains; optional chain filter and pagination.
GET /services/multichain/api/v1/clusters/{cluster_id}/search/nfts: Full-text search for NFTs by query string; optional chain filter and pagination.
GET /services/multichain/api/v1/clusters/{cluster_id}/search/tokens: Full-text search for tokens; optional chain filter and pagination.
GET /services/multichain/api/v1/clusters/{cluster_id}/search/transactions: Full-text search for transactions (returns transaction hashes); optional chain filter and pagination.
GET /services/multichain/api/v1/clusters/{cluster_id}/search:quick: Unified quick search across addresses, blocks, transactions, block numbers, dapps, tokens, NFTs, and domains; supports unlimited results per chain.

## csv-export

GET /{chain_id}/api/v2/csv-exports/{uuid_param}: Get CSV export

## internal-transactions

GET /{chain_id}/api/v2/internal-transactions: List internal transactions generated during smart contract execution

## legacy

GET /{chain_id}/api/legacy/block/eth-block-number: Get the latest block number
GET /{chain_id}/api/legacy/block/get-block-number-by-time: Get block number by time stamp
GET /{chain_id}/api/legacy/logs/get-logs: Get Event Logs by Address and/or Topic(s)

## main-page

GET /{chain_id}/api/v2/main-page/blocks: Retrieve recent blocks as displayed on Blockscout homepage
GET /{chain_id}/api/v2/main-page/indexing-status: Check if indexing is finished with indexing ratio
GET /{chain_id}/api/v2/main-page/transactions: Retrieve recent transactions as displayed on Blockscout homepage
GET /{chain_id}/api/v2/main-page/transactions/watchlist: Last 6 transactions from the current user's watchlist

## Metadata

GET /services/metadata/api/v1/metadata: NO DESCRIPTION

## mud

GET /{chain_id}/api/v2/mud/worlds: List of MUD worlds.
GET /{chain_id}/api/v2/mud/worlds/count: Number of known MUD worlds.
GET /{chain_id}/api/v2/mud/worlds/{world}/systems: List of MUD world systems.
GET /{chain_id}/api/v2/mud/worlds/{world}/systems/{system}: List of MUD world system ABI methods.
GET /{chain_id}/api/v2/mud/worlds/{world}/tables: List of MUD world tables.
GET /{chain_id}/api/v2/mud/worlds/{world}/tables/count: Number of known MUD world tables.
GET /{chain_id}/api/v2/mud/worlds/{world}/tables/{table_id}/records: List of MUD world table records.
GET /{chain_id}/api/v2/mud/worlds/{world}/tables/{table_id}/records/count: Number of known MUD world table records.
GET /{chain_id}/api/v2/mud/worlds/{world}/tables/{table_id}/records/{record_id}: Single MUD world table record.

## MultichainAggregatorService

GET /services/multichain/api/v1/search:quick: Unified quick search across addresses, blocks, transactions, block numbers, dapps, tokens, NFTs, and domains; supports unlimited results per chain.

## optimism

GET /{chain_id}/api/v2/main-page/optimism-deposits: List deposits on the main page.
GET /{chain_id}/api/v2/optimism/batches: List batches.
GET /{chain_id}/api/v2/optimism/batches/count: Number of batches in the list.
GET /{chain_id}/api/v2/optimism/batches/da/celestia/{height}/{commitment}: Batch by celestia blob.
GET /{chain_id}/api/v2/optimism/batches/{number}: Batch by its number.
GET /{chain_id}/api/v2/optimism/deposits: List deposits.
GET /{chain_id}/api/v2/optimism/deposits/count: Number of deposits in the list.
GET /{chain_id}/api/v2/optimism/games: List games.
GET /{chain_id}/api/v2/optimism/games/count: Number of games in the list.
GET /{chain_id}/api/v2/optimism/output-roots: List output roots.
GET /{chain_id}/api/v2/optimism/output-roots/count: Number of output roots in the list.
GET /{chain_id}/api/v2/optimism/withdrawals: List withdrawals.
GET /{chain_id}/api/v2/optimism/withdrawals/count: Number of withdrawals in the list.

## scroll

GET /{chain_id}/api/v2/scroll/batches: List batches.
GET /{chain_id}/api/v2/scroll/batches/count: Number of batches in the list.
GET /{chain_id}/api/v2/scroll/batches/{number}: Batch by its number.
GET /{chain_id}/api/v2/scroll/deposits: List deposits.
GET /{chain_id}/api/v2/scroll/deposits/count: Number of deposits in the list.
GET /{chain_id}/api/v2/scroll/withdrawals: List withdrawals.
GET /{chain_id}/api/v2/scroll/withdrawals/count: Number of withdrawals in the list.

## search

GET /{chain_id}/api/v1/search: Search for tokens, addresses, contracts, blocks, or transactions by identifier
GET /{chain_id}/api/v2/search: Search for tokens, addresses, contracts, blocks, or transactions by identifier
GET /{chain_id}/api/v2/search/check-redirect: Check if search query should redirect to a specific entity page
GET /{chain_id}/api/v2/search/quick: Quick (unpaginated) search

## smart-contracts

GET /{chain_id}/api/v2/smart-contracts/: List verified smart contracts with optional filtering options
GET /{chain_id}/api/v2/smart-contracts/counters: Get count statistics (new & newly verified) for deployed smart contracts
GET /{chain_id}/api/v2/smart-contracts/{address_hash_param}: Retrieve detailed information about a verified smart contract
GET /{chain_id}/api/v2/smart-contracts/{address_hash_param}/audit-reports: Audit reports list

## stats

GET /{chain_id}/api/v2/stats: Retrieve blockchain network statistics and metrics
GET /{chain_id}/api/v2/stats/charts/market: Get daily closing price and market cap for native coin
GET /{chain_id}/api/v2/stats/charts/secondary-coin-market: Secondary coin market history chart data
GET /{chain_id}/api/v2/stats/charts/transactions: Get daily transaction counts
GET /{chain_id}/api/v2/stats/hot-smart-contracts: Retrieve hot smart-contracts

## StatsService

GET /{chain_id}/stats-service/api/v1/counters: Returns all available counter stats for the stats page.
GET /{chain_id}/stats-service/api/v1/lines: Returns metadata (title, description, available resolutions) for all
line charts, organized into sections.
GET /{chain_id}/stats-service/api/v1/lines/{name}: Returns data points for a specific line chart, with optional date range
and resolution filtering.
GET /{chain_id}/stats-service/api/v1/pages/contracts: Returns stats to be displayed on the contracts page.
GET /{chain_id}/stats-service/api/v1/pages/interchain/main: Returns interchain messaging stats to be displayed on the main page of interchain indexer.
GET /{chain_id}/stats-service/api/v1/pages/main: Returns stats to be displayed on the main page of indexer.
GET /{chain_id}/stats-service/api/v1/pages/multichain/main: Returns multichain-aggregated stats to be displayed on the main page of multichain indexer.
GET /{chain_id}/stats-service/api/v1/pages/transactions: Returns stats to be displayed on the transactions page.

## token-transfers

GET /{chain_id}/api/v2/token-transfers: List token transfers across all token types (ERC-20, ERC-721, ERC-1155)

## tokens

GET /{chain_id}/api/v2/tokens/: List tokens with optional filtering by name, symbol, or type
GET /{chain_id}/api/v2/tokens/{address_hash_param}: Retrieve detailed information about a specific token
GET /{chain_id}/api/v2/tokens/{address_hash_param}/counters: Get holder and transfer count statistics for a specific token
GET /{chain_id}/api/v2/tokens/{address_hash_param}/holders: List addresses holding a specific token sorted by balance
GET /{chain_id}/api/v2/tokens/{address_hash_param}/holders/csv: Export token holders as CSV
GET /{chain_id}/api/v2/tokens/{address_hash_param}/instances: List individual NFT instances for a token contract
GET /{chain_id}/api/v2/tokens/{address_hash_param}/instances/{token_id_param}: Retrieve detailed information about a specific NFT
GET /{chain_id}/api/v2/tokens/{address_hash_param}/instances/{token_id_param}/holders: List current holders of a specific NFT
GET /{chain_id}/api/v2/tokens/{address_hash_param}/instances/{token_id_param}/transfers: List token transfers for a specific token instance
GET /{chain_id}/api/v2/tokens/{address_hash_param}/instances/{token_id_param}/transfers-count: Get total number of ownership transfers for a specific NFT
GET /{chain_id}/api/v2/tokens/{address_hash_param}/transfers: List ownership transfer history for a specific NFT

## transactions

GET /{chain_id}/api/v2/transactions: List blockchain transactions with filtering options for status, type, and method
GET /{chain_id}/api/v2/transactions/arbitrum-batch/{batch_number_param}: List L2 transactions in an Arbitrum batch
GET /{chain_id}/api/v2/transactions/execution-node/{execution_node_hash_param}: List transactions executed on a specific execution node
GET /{chain_id}/api/v2/transactions/optimism-batch/{batch_number_param}: List L2 transactions in an Optimism batch
GET /{chain_id}/api/v2/transactions/scroll-batch/{batch_number_param}: List L2 transactions in a Scroll batch
GET /{chain_id}/api/v2/transactions/stats: Get transaction statistics
GET /{chain_id}/api/v2/transactions/watchlist: List transactions in a user's watchlist
GET /{chain_id}/api/v2/transactions/zksync-batch/{batch_number_param}: List L2 transactions in a ZkSync batch
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}: Retrieve detailed information about a specific transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/beacon/deposits: List beacon deposits in a transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/blobs: List blobs for a transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/external-transactions: List external transactions linked to a transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/fhe-operations: List FHE operations for a specific transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/internal-transactions: List internal transactions triggered during a specific transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/logs: List event logs emitted during a specific transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/raw-trace: Get step-by-step execution trace for a specific transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/state-changes: Get on-chain state changes caused by a specific transaction
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/summary: Get a human-readable, LLM-based transaction summary
GET /{chain_id}/api/v2/transactions/{transaction_hash_param}/token-transfers: List token transfers within a specific transaction

## withdrawals

GET /{chain_id}/api/v2/withdrawals: List validator withdrawal details on proof-of-stake networks
GET /{chain_id}/api/v2/withdrawals/counters: Withdrawals counters

## zilliqa

GET /{chain_id}/api/v2/validators/zilliqa: Zilliqa validators list.
GET /{chain_id}/api/v2/validators/zilliqa/{bls_public_key}: Zilliqa validator by its BLS public key.
