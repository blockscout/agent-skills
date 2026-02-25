## API Endpoints

### Transactions

#### GET /api/v2/internal-transactions

Retrieves a paginated list of internal transactions. Internal transactions are generated during contract execution and not directly recorded on the blockchain.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `transaction_hash` | `string` | No | Transaction hash in the query |
  | `limit` | `integer` | No | Limit result items in the response |
  | `index` | `integer` | No | Transaction index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `transaction_index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions

Retrieves a paginated list of transactions with optional filtering by status, type, and method.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `filter` | `string` | No | Filter transactions by status:
* pending - Transactions waiting to be mined/validated
* validated - Confirmed transactions included in blocks
If omitted, default value "validated" is used.
 |
  | `type` | `string` | No | Filter by transaction type. Comma-separated list of:
* blob_transaction - Only show blob transactions
 |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `hash` | `string` | No | Transaction hash for paging |
  | `inserted_at` | `string` | No | Inserted at timestamp for paging (ISO8601) |

#### GET /api/v2/transactions/stats

Retrieves statistics for transactions, including counts and fee summaries for the last 24 hours.

- **Parameters**

  *None*

#### GET /api/v2/transactions/watchlist

Retrieves transactions in the authenticated user's watchlist.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/{transaction_hash_param}/external-transactions

Retrieves external transactions that are linked to the specified transaction (e.g., Solana transactions in `neon` chain type).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/transactions/{transaction_hash_param}/internal-transactions

Retrieves internal transactions generated during the execution of a specific transaction. Useful for analyzing contract interactions and debugging failed transactions.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `index` | `integer` | No | Transaction index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `transaction_index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/{transaction_hash_param}/logs

Retrieves event logs emitted during the execution of a specific transaction. Logs contain information about contract events and state changes.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `index` | `integer` | No | Transaction index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/{transaction_hash_param}/raw-trace

Retrieves the raw execution trace for a transaction, showing the step-by-step execution path and all contract interactions.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/transactions/{transaction_hash_param}/state-changes

Retrieves state changes (balance changes, token transfers) caused by a specific transaction.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `state_changes` | `string` | No | State changes for paging |
  | `items_count` | `integer` | No | Cumulative number of items to skip for keyset-based pagination of state changes |

#### GET /api/v2/transactions/{transaction_hash_param}/summary

Retrieves a human-readable summary of what a transaction did, presented in natural language.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `just_request_body` | `boolean` | No | If true, returns only the request body in the summary endpoint |

#### GET /api/v2/transactions/{transaction_hash_param}/token-transfers

Retrieves token transfers that occurred within a specific transaction, with optional filtering by token type.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `type` | `string` | No | Filter by token type. Comma-separated list of:
* ERC-20 - Fungible tokens
* ERC-721 - Non-fungible tokens
* ERC-1155 - Multi-token standard
* ERC-404 - Hybrid fungible/non-fungible tokens


Example: `ERC-20,ERC-721` to show both fungible and NFT transfers
 |
  | `index` | `integer` | No | Transaction index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `batch_log_index` | `integer` | No | Batch log index for paging |
  | `batch_block_hash` | `string` | No | Batch block hash for paging |
  | `batch_transaction_hash` | `string` | No | Batch transaction hash for paging |
  | `index_in_batch` | `integer` | No | Index in batch for paging |

### User Operations

#### GET /api/v2/proxy/account-abstraction/operations/{user_operation_hash}

Get details for a specific User Operation by its hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `user_operation_hash` | `string` | Yes |  |

### JSON-RPC Compatibility

These are Etherscan-compatible legacy endpoints. When using `direct_api_call`, set `endpoint_path="/api"` and pass `module`, `action`, and any other parameters via `query_params`. The `module` and `action` values are part of the endpoint identity and are not listed in the parameter tables below.

#### GET /api?module=logs&action=getLogs

Returns event logs filtered by block range, optional contract address, and up to four topic values. Results are capped at 1,000 entries. When calling via `direct_api_call`, use `endpoint_path="/api"` and pass all parameters in `query_params`.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `fromBlock` | `integer` | Yes | Start block number. |
  | `toBlock` | `integer` | Yes | End block number. |
  | `address` | `string` | No | Contract address to filter logs for. |
  | `topic0` | `string` | No | Topic 0 hex value. |
  | `topic1` | `string` | No | Topic 1 hex value. |
  | `topic2` | `string` | No | Topic 2 hex value. |
  | `topic3` | `string` | No | Topic 3 hex value. |
  | `topic0_1_opr` | `string` | No | Boolean operator between topic0 and topic1: `and` or `or`. |
  | `topic0_2_opr` | `string` | No | Boolean operator between topic0 and topic2: `and` or `or`. |
  | `topic0_3_opr` | `string` | No | Boolean operator between topic0 and topic3: `and` or `or`. |
  | `topic1_2_opr` | `string` | No | Boolean operator between topic1 and topic2: `and` or `or`. |
  | `topic1_3_opr` | `string` | No | Boolean operator between topic1 and topic3: `and` or `or`. |
  | `topic2_3_opr` | `string` | No | Boolean operator between topic2 and topic3: `and` or `or`. |
