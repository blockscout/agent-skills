## API Endpoints

### Tokens

#### GET /api/v2/token-transfers

Retrieves a paginated list of token transfers across all token types (ERC-20, ERC-721, ERC-1155).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `type` | `string` | No | Filter by token type. Comma-separated list of:
* ERC-20 - Fungible tokens
* ERC-721 - Non-fungible tokens
* ERC-1155 - Multi-token standard
* ERC-404 - Hybrid fungible/non-fungible tokens


Example: `ERC-20,ERC-721` to show both fungible and NFT transfers
 |
  | `limit` | `integer` | No | Limit result items in the response |
  | `index` | `integer` | No | Transaction index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `batch_log_index` | `integer` | No | Batch log index for paging |
  | `batch_block_hash` | `string` | No | Batch block hash for paging |
  | `batch_transaction_hash` | `string` | No | Batch transaction hash for paging |
  | `index_in_batch` | `integer` | No | Index in batch for paging |

#### GET /api/v2/tokens/

Retrieves a paginated list of tokens with optional filtering by name, symbol, or type.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `type` | `string` | No | Filter by token type. Comma-separated list of:
* ERC-20 - Fungible tokens
* ERC-721 - Non-fungible tokens
* ERC-1155 - Multi-token standard
* ERC-404 - Hybrid fungible/non-fungible tokens


Example: `ERC-20,ERC-721` to show both fungible and NFT transfers
 |
  | `q` | `string` | No | Search query filter |
  | `limit` | `integer` | No | Limit result items in the response |
  | `sort` | `string` | No | Sort transactions by:
* block_number - Sort by block number
* value - Sort by transaction value
* fee - Sort by transaction fee
* balance - Sort by account balance
* transactions_count - Sort by number of transactions on address
* fiat_value - Sort by fiat value of the token transfer
* holders_count - Sort by number of token holders
* circulating_market_cap - Sort by circulating market cap of the token
Should be used together with `order` parameter.
 |
  | `order` | `string` | No | Sort order:
* asc - Ascending order
* desc - Descending order
Should be used together with `sort` parameter.
 |
  | `contract_address_hash` | `string` | No | Contract address hash for paging |
  | `fiat_value` | `string` | No | Fiat value for paging |
  | `holders_count` | `string` | No | Number of holders returned per page |
  | `is_name_null` | `boolean` | No | Is name null for paging |
  | `market_cap` | `string` | No | Market cap for paging |
  | `name` | `string` | No | Name for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/tokens/{address_hash_param}

Retrieves detailed information for a specific token identified by its contract address.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/tokens/{address_hash_param}/counters

Retrieves count statistics for a specific token, including holders count and transfers count.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/tokens/{address_hash_param}/holders

Retrieves addresses holding a specific token, sorted by balance. Useful for analyzing token distribution.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `address_hash` | `string` | No | Address hash for paging |
  | `value` | `string` | No | Transaction value for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/tokens/{address_hash_param}/instances

Retrieves instances of NFTs for a specific token contract. This endpoint is primarily for ERC-721 and ERC-1155 tokens.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `holder_address_hash` | `string` | No | Token holder address hash in the query |
  | `unique_token` | `string` | No | Token ID for paging |

#### GET /api/v2/tokens/{address_hash_param}/instances/{token_id_param}

Retrieves detailed information about a specific NFT instance, identified by its token contract address and token ID.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `token_id_param` | `string` | Yes | Token ID for ERC-721/1155/404 tokens |

#### GET /api/v2/tokens/{address_hash_param}/instances/{token_id_param}/holders

Retrieves current holders of a specific NFT instance. For ERC-721, this will typically be a single address. For ERC-1155, multiple addresses may hold the same token ID.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `token_id_param` | `string` | Yes | Token ID for ERC-721/1155/404 tokens |
  | `address_hash` | `string` | No | Address hash for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `token_id` | `string` | No | Token ID for paging |
  | `value` | `string` | No | Transaction value for paging |

#### GET /api/v2/tokens/{address_hash_param}/instances/{token_id_param}/transfers

Retrieves token transfers for a specific token instance (by token address and token ID).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `token_id_param` | `string` | Yes | Token ID for ERC-721/1155/404 tokens |
  | `index` | `integer` | No | Transaction index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `token_id` | `string` | No | Token ID for paging |

#### GET /api/v2/tokens/{address_hash_param}/instances/{token_id_param}/transfers-count

Retrieves the total number of transfers for a specific NFT instance. Useful for determining how frequently an NFT has changed hands.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `token_id_param` | `string` | Yes | Token ID for ERC-721/1155/404 tokens |

#### GET /api/v2/tokens/{address_hash_param}/transfers

Retrieves transfer history for a specific NFT instance, showing ownership changes over time.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `index` | `integer` | No | Transaction index for paging |
  | `block_number` | `integer` | No | Block number for paging |
  | `batch_log_index` | `integer` | No | Batch log index for paging |
  | `batch_block_hash` | `string` | No | Batch block hash for paging |
  | `batch_transaction_hash` | `string` | No | Batch transaction hash for paging |
  | `index_in_batch` | `integer` | No | Index in batch for paging |
