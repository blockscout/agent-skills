## API Endpoints

### Smart Contracts

#### GET /api/v2/smart-contracts/

Retrieves a paginated list of verified smart contracts with optional filtering by proxy status or programming language.

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
  | `q` | `string` | No | Search query filter |
  | `filter` | `string` | No | Filter to apply |
  | `smart_contract_id` | `integer` | No | Smart-contract ID for paging |
  | `coin_balance` | `string` | No | Coin balance for paging |
  | `hash` | `string` | No | Address hash for paging |
  | `transactions_count` | `string` | No | Transactions count for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/smart-contracts/counters

Retrieves count statistics for smart contracts, including total contracts, verified contracts, and new contracts in the last 24 hours.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/smart-contracts/{address_hash_param}

Retrieves detailed information about a specific verified smart contract, including source code, ABI, and deployment details.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/smart-contracts/{address_hash_param}/audit-reports

Returns audit reports for a given smart contract address.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
