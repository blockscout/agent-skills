## API Endpoints

These endpoints are only available on chains that use Ethereum proof-of-stake consensus, such as **Ethereum Mainnet** and **Gnosis Chain**. They expose beacon chain deposit tracking and EIP-4844 blob transaction data that do not exist on other EVM networks.

### Ethereum PoS Chains

#### GET /api/v2/addresses/{address_hash_param}/beacon/deposits

Retrieves Beacon deposits for a specific address.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `index` | `integer` | No | Deposit index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/beacon/deposits

Retrieves a paginated list of all beacon deposits.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `index` | `integer` | No | Deposit index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/beacon/deposits/count

Retrieves the total count of beacon deposits.

- **Parameters**

  *None*

#### GET /api/v2/blocks/{block_hash_or_number_param}/beacon/deposits

Retrieves beacon deposits included in a specific block with pagination support.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `block_hash_or_number_param` | `string` | Yes | Block hash or number in the path |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/{transaction_hash_param}/beacon/deposits

Retrieves beacon deposits included in a specific transaction with pagination support.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/transactions/{transaction_hash_param}/blobs

Retrieves blobs for a specific transaction (Ethereum only).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash_param` | `string` | Yes | Transaction hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/withdrawals

Retrieves a paginated list of withdrawals, typically for proof-of-stake networks supporting validator withdrawals.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/withdrawals/counters

Returns total withdrawals count and sum from cache.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
