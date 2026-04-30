## API Endpoints

### Arbitrum

#### GET /api/v2/arbitrum/batches/{batch_number}

Get information for a specific Arbitrum batch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number` | `integer` | Yes |  |

#### GET /api/v2/arbitrum/messages/from-rollup

Get L2 to L1 messages for Arbitrum.

- **Parameters**

  *None*

#### GET /api/v2/arbitrum/messages/to-rollup

Get L1 to L2 messages for Arbitrum.

- **Parameters**

  *None*

#### GET /api/v2/arbitrum/messages/withdrawals/{transaction_hash}

Get L2 to L1 messages for a specific transaction hash on Arbitrum.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash` | `string` | Yes |  |

#### GET /api/v2/blocks/arbitrum-batch/{batch_number_param}

Retrieves L2 blocks that are bound to a specific Arbitrum batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/main-page/arbitrum/batches/latest-number

Get the latest committed batch number for Arbitrum.

- **Parameters**

  *None*

#### GET /api/v2/transactions/arbitrum-batch/{batch_number_param}

Retrieves L2 transactions bound to a specific Arbitrum batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
