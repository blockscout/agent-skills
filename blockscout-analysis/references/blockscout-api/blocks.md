## API Endpoints

### Blocks

#### GET /api/v2/blocks

Retrieves a paginated list of blocks with optional filtering by block type.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `type` | `string` | No | Filter by block type:
* block - Standard blocks in the main chain
* uncle - Uncle/ommer blocks (valid but not in main chain)
* reorg - Blocks from chain reorganizations
If omitted, default value "block" is used.
 |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/blocks/{block_hash_or_number_param}/internal-transactions

Retrieves internal transactions included in a specific block with optional filtering by type and call type.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `block_hash_or_number_param` | `string` | Yes | Block hash or number in the path |
  | `internal_type` | `string` | No | Filter internal transactions by type:
* all - Show all internal transactions (default)
* call - Only show call internal transactions
* create - Only show create internal transactions
* create2 - Only show create2 internal transactions
* reward - Only show reward internal transactions
* selfdestruct - Only show selfdestruct internal transactions
* stop - Only show stop internal transactions
* invalid - Only show invalid internal transactions (Arbitrum only)
 |
  | `call_type` | `string` | No | Filter internal transactions by call type:
* all - Show all internal transactions (default)
* call - Only show call internal transactions
* callcode - Only show callcode internal transactions
* delegatecall - Only show delegatecall internal transactions
* staticcall - Only show staticcall internal transactions
* invalid - Only show invalid internal transactions (Arbitrum only)
 |
  | `transaction_index` | `integer` | No | Transaction index for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/blocks/{block_hash_or_number_param}/transactions

Retrieves transactions included in a specific block, ordered by transaction index.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `block_hash_or_number_param` | `string` | Yes | Block hash or number in the path |
  | `type` | `string` | No | Filter by transaction type. Comma-separated list of:
* token_transfer - Token transfer transactions
* contract_creation - Contract deployment transactions
* contract_call - Contract method call transactions
* coin_transfer - Native coin transfer transactions
* token_creation - Token creation transactions
* blob_transaction - Only show blob transactions (Ethereum only)
 |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/blocks/{block_hash_or_number_param}/withdrawals

Retrieves withdrawals processed in a specific block (typically for proof-of-stake networks).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `block_hash_or_number_param` | `string` | Yes | Block hash or number in the path |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/blocks/{block_number_param}/countdown

Calculates the estimated time remaining until a specified block number is reached based on current block and average block time.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `block_number_param` | `integer` | Yes | Block number in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
