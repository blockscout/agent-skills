## API Endpoints

### Transactions

#### GET /api/v2/advanced-filters

Returns a paginated, mixed list of activity — native value transfers, internal transactions and token transfers — filtered by transaction type, contract method, time window, address relations, value range and/or token contract. The response also echoes the resolved human-readable names of the methods and tokens referenced in the request filters.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_types` | `string` | No | Comma-separated list of transaction types to include. Allowed values: `COIN_TRANSFER`, `CONTRACT_INTERACTION`, `CONTRACT_CREATION`, `ERC-20`, `ERC-404`, `ERC-721`, `ERC-1155`, `ERC-7984` (plus `ZRC-2` on Zilliqa). Values are matched case-insensitively; unknown entries are silently dropped. |
  | `methods` | `string` | No | Comma-separated list of 4-byte contract method selectors (lowercase, `0x`-prefixed). At most 20 unique entries are honored; invalid entries are dropped. |
  | `age_from` | `string` | No | Inclusive lower bound on `timestamp` (ISO 8601). |
  | `age_to` | `string` | No | Inclusive upper bound on `timestamp` (ISO 8601). |
  | `from_address_hashes_to_include` | `string` | No | Comma-separated list of sender address hashes to include. |
  | `from_address_hashes_to_exclude` | `string` | No | Comma-separated list of sender address hashes to exclude. |
  | `to_address_hashes_to_include` | `string` | No | Comma-separated list of recipient address hashes to include. |
  | `to_address_hashes_to_exclude` | `string` | No | Comma-separated list of recipient address hashes to exclude. |
  | `address_relation` | `string` | No | How to combine the `from_address_hashes_*` and `to_address_hashes_*` filters. Accepts `or` or `and` (case-insensitive). `or` (default) matches an item if either side matches; `and` requires both sides to match. Any other value is silently coerced to `nil` (no relation constraint). |
  | `amount_from` | `string` | No | Inclusive lower bound on the item's transferred amount (decimal string in the token's base units). |
  | `amount_to` | `string` | No | Inclusive upper bound on the item's transferred amount (decimal string in the token's base units). |
  | `token_contract_address_hashes_to_include` | `string` | No | Comma-separated list of token contract address hashes to include. Use the literal `native` to also include native coin transfers. Each list (include and exclude) is capped to 20 entries separately. |
  | `token_contract_address_hashes_to_exclude` | `string` | No | Comma-separated list of token contract address hashes to exclude. Use the literal `native` to also exclude native coin transfers. Each list (include and exclude) is capped to 20 entries separately. |
  | `methods_names` | `string` | No | Comma-separated list of human-readable method names corresponding to the `methods` selectors. |
  | `token_contract_symbols_to_include` | `string` | No | Comma-separated list of token symbols to include. |
  | `token_contract_symbols_to_exclude` | `string` | No | Comma-separated list of token symbols to exclude. |
  | `block_number` | `string` | No | Keyset cursor: block number of the last item from the previous page. |
  | `transaction_index` | `string` | No | Keyset cursor: transaction index within the block of the last item from the previous page. |
  | `internal_transaction_index` | `string` | No | Keyset cursor: internal-transaction index of the last item from the previous page. Use an empty string or the literal `null` when the previous item was not an internal transaction. |
  | `token_transfer_index` | `string` | No | Keyset cursor: token-transfer index of the last item from the previous page. Use an empty string or the literal `null` when the previous item was not a token transfer. |
  | `token_transfer_batch_index` | `string` | No | Keyset cursor: index within an ERC-1155 batch token transfer. Use an empty string or the literal `null` when the previous item was not part of a batch. |
  | `items_count` | `integer` | No | Cumulative number of items already returned across previous pages. |

#### GET /api/v2/advanced-filters/methods

Returns a list of known contract methods. When the `q` parameter is provided, searches for a single method by its 4-byte selector or name. Without `q`, returns the default list of popular methods.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `q` | `string` | No | Search string: either a 4-byte method selector (e.g. `0xa9059cbb`) or a method name (e.g. `transfer`). |

#### GET /api/v2/internal-transactions

Retrieves a paginated list of internal transactions. Internal transactions are generated during contract execution and not directly recorded on the blockchain.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash` | `string` | No | Transaction hash in the query |
  | `limit` | `integer` | No | Limit result items in the response |
  | `index` | `integer` | No | Item index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `transaction_index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions

Retrieves a paginated list of transactions with optional filtering by status, type, and method.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `filter` | `string` | No | Filter transactions by status:
* pending - Transactions waiting to be mined/validated
* validated - Confirmed transactions included in blocks
If omitted, default value "validated" is used.
 |
  | `type` | `string` | No | Filter by transaction type. Comma-separated list of:
* blob_transaction - Only show blob transactions
 |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Item index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `hash` | `string` | No | Transaction hash for paging |
  | `inserted_at` | `string` | No | Inserted at timestamp for paging (ISO8601) |

#### GET /api/v2/transactions/execution-node/{execution_node_hash_param}

Retrieves transactions that were executed on the specified execution node.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `execution_node_hash_param` | `string` | Yes | Execution node hash in the path |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Item index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/stats

Retrieves statistics for transactions, including counts and fee summaries for the last 24 hours.

- **Parameters**

  *None*

#### GET /api/v2/transactions/watchlist

Retrieves transactions in the authenticated user's watchlist.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Item index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/{transaction_hash_param}/external-transactions

Retrieves external transactions that are linked to the specified transaction (e.g., Solana transactions in `neon` chain type).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |

#### GET /api/v2/transactions/{transaction_hash_param}/fhe-operations

Retrieves Fully Homomorphic Encryption (FHE) operations parsed from transaction logs. Includes operation details, HCU (Homomorphic Compute Unit) costs, operation types, and related metadata.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |

#### GET /api/v2/transactions/{transaction_hash_param}/internal-transactions

Retrieves internal transactions generated during the execution of a specific transaction. Useful for analyzing contract interactions and debugging failed transactions.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `index` | `integer` | No | Item index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `transaction_index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/{transaction_hash_param}/logs

Retrieves event logs emitted during the execution of a specific transaction. Logs contain information about contract events and state changes.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `index` | `integer` | No | Item index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/{transaction_hash_param}/raw-trace

Retrieves the raw execution trace for a transaction, showing the step-by-step execution path and all contract interactions.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |

#### GET /api/v2/transactions/{transaction_hash_param}/state-changes

Retrieves state changes (balance changes, token transfers) caused by a specific transaction.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `state_changes` | `string` | No | State changes for paging |
  | `items_count` | `integer` | No | Cumulative number of items to skip for keyset-based pagination of state changes |

#### GET /api/v2/transactions/{transaction_hash_param}/summary

Retrieves a human-readable summary of what a transaction did, presented in natural language.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `just_request_body` | `boolean` | No | If true, returns only the request body in the summary endpoint |

#### GET /api/v2/transactions/{transaction_hash_param}/token-transfers

Retrieves token transfers that occurred within a specific transaction, with optional filtering by token type.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `type` | `string` | No | Filter by token type. Comma-separated list of:
* ERC-20 - Fungible tokens
* ERC-721 - Non-fungible tokens
* ERC-1155 - Multi-token standard
* ERC-404 - Hybrid fungible/non-fungible tokens


Example: `ERC-20,ERC-721` to show both fungible and NFT transfers
 |
  | `index` | `integer` | No | Item index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `batch_log_index` | `integer` | No | Batch log index for paging |
  | `batch_block_hash` | `string` | No | Batch block hash for paging |
  | `batch_transaction_hash` | `string` | No | Batch transaction hash for paging |
  | `index_in_batch` | `integer` | No | Index in batch for paging |

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
