## API Endpoints

### Addresses

#### GET /api/v2/addresses

Retrieves a paginated list of addresses holding the native coin, sorted by balance.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
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
  | `fetched_coin_balance` | `string` | No | Fetched coin balance for paging |
  | `hash` | `string` | No | Address hash for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `transactions_count` | `string` | No | Transactions count for paging |

#### GET /api/v2/addresses/{address_hash_param}

Retrieves detailed information for a specific address, including balance, transaction count, and metadata.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/addresses/{address_hash_param}/blocks-validated

Retrieves blocks that were validated (mined) by a specific address. Useful for tracking validator/miner performance.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/addresses/{address_hash_param}/coin-balance-history

Retrieves historical native coin balance changes for a specific address, tracking how an address's balance has changed over time.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/addresses/{address_hash_param}/coin-balance-history-by-day

Retrieves daily snapshots of native coin balance for a specific address. Useful for generating balance-over-time charts.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/addresses/{address_hash_param}/counters

Retrieves count statistics for an address, including transactions, token transfers, gas usage, and validations.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/addresses/{address_hash_param}/internal-transactions

Retrieves all internal transactions involving a specific address, with optional filtering for internal transactions sent from or to the address.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `filter` | `string` | No | Filter transactions by direction:
* to - Only show transactions sent to this address
* from - Only show transactions sent from this address
If omitted, all transactions involving the address are returned.
 |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `transaction_index` | `integer` | No | Transaction index for paging |

#### GET /api/v2/addresses/{address_hash_param}/logs

Retrieves event logs emitted by or involving a specific address.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `topic` | `string` | No | Log topic param in the query |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/addresses/{address_hash_param}/nft

Retrieves a list of NFTs (non-fungible tokens) owned by a specific address, with optional filtering by token type.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `type` | `string` | No | Filter by token type. Comma-separated list of:
* ERC-721 - Non-fungible tokens
* ERC-1155 - Multi-token standard
* ERC-404 - Hybrid fungible/non-fungible tokens

Example: `ERC-721,ERC-1155` to show both NFT and multi-token transfers
 |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `token_contract_address_hash` | `string` | No | Token contract address hash for paging |
  | `token_id` | `string` | No | Token ID for paging |
  | `token_type` | `string` | No | Token type for paging |

#### GET /api/v2/addresses/{address_hash_param}/nft/collections

Retrieves NFTs owned by a specific address, organized by collection. Useful for displaying an address's NFT portfolio grouped by project.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `type` | `string` | No | Filter by token type. Comma-separated list of:
* ERC-721 - Non-fungible tokens
* ERC-1155 - Multi-token standard
* ERC-404 - Hybrid fungible/non-fungible tokens

Example: `ERC-721,ERC-1155` to show both NFT and multi-token transfers
 |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `token_contract_address_hash` | `string` | No | Token contract address hash for paging |
  | `token_type` | `string` | No | Token type for paging |

#### GET /api/v2/addresses/{address_hash_param}/tabs-counters

Retrieves counters for various address-related entities (max counter value is 51).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/addresses/{address_hash_param}/token-balances

Retrieves all token balances held by a specific address, including ERC-20, ERC-721, ERC-1155, and ERC-404 tokens.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/addresses/{address_hash_param}/token-transfers

Retrieves token transfers involving a specific address, with optional filtering by token type, direction, and specific token.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `filter` | `string` | No | Filter transactions by direction:
* to - Only show transactions sent to this address
* from - Only show transactions sent from this address
If omitted, all transactions involving the address are returned.
 |
  | `type` | `string` | No | Filter by token type. Comma-separated list of:
* ERC-20 - Fungible tokens
* ERC-721 - Non-fungible tokens
* ERC-1155 - Multi-token standard
* ERC-404 - Hybrid fungible/non-fungible tokens


Example: `ERC-20,ERC-721` to show both fungible and NFT transfers
 |
  | `token` | `string` | No | Filter token transfers by token contract address. |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `batch_log_index` | `integer` | No | Batch log index for paging |
  | `batch_block_hash` | `string` | No | Batch block hash for paging |
  | `batch_transaction_hash` | `string` | No | Batch transaction hash for paging |
  | `index_in_batch` | `integer` | No | Index in batch for paging |

#### GET /api/v2/addresses/{address_hash_param}/tokens

Retrieves token balances for a specific address with pagination and filtering by token type. Useful for displaying large token portfolios.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `type` | `string` | No | Filter by token type. Comma-separated list of:
* ERC-20 - Fungible tokens
* ERC-721 - Non-fungible tokens
* ERC-1155 - Multi-token standard
* ERC-404 - Hybrid fungible/non-fungible tokens


Example: `ERC-20,ERC-721` to show both fungible and NFT transfers
 |
  | `fiat_value` | `string` | No | Fiat value for paging |
  | `id` | `integer` | No | ID for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `value` | `string` | No | Transaction value for paging |

#### GET /api/v2/addresses/{address_hash_param}/transactions

Retrieves transactions involving a specific address, with optional filtering for transactions sent from or to the address.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `filter` | `string` | No | Filter transactions by direction:
* to - Only show transactions sent to this address
* from - Only show transactions sent from this address
If omitted, all transactions involving the address are returned.
 |
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
  | `block_number` | `string` | No | Block number for paging |
  | `index` | `string` | No | Transaction index for paging |
  | `inserted_at` | `string` | No | Inserted at timestamp for paging (ISO8601) |
  | `hash` | `string` | No | Transaction hash for paging |
  | `value` | `string` | No | Transaction value for paging |
  | `fee` | `string` | No | Transaction fee for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/addresses/{address_hash_param}/withdrawals

Retrieves withdrawals involving a specific address, typically for proof-of-stake networks supporting validator withdrawals.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

### JSON-RPC Compatibility

These are Etherscan-compatible legacy endpoints. When using `direct_api_call`, set `endpoint_path="/api"` and pass `module`, `action`, and any other parameters via `query_params`. The `module` and `action` values are part of the endpoint identity and are not listed in the parameter tables below.

#### GET /api?module=account&action=eth_get_balance

Returns the ETH balance of an address in an Ethereum-compatible hex format (0x-prefixed). **The returned value is hex-encoded and must be decoded from hexadecimal to obtain the balance in wei.** For example, `0xde0b6b3a7640000` decodes to `1000000000000000000` wei (1 ETH). Pass a specific block number in the `block` parameter to retrieve the historical balance at that block. When calling via `direct_api_call`, use `endpoint_path="/api"` and pass all parameters in `query_params`.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address` | `string` | Yes | The address to check balance for. |
  | `block` | `string` | No | Block identifier: `latest`, `earliest`, `pending`, or a decimal block number as a string. Defaults to `latest`. Use a specific block number to query historical balance. |
