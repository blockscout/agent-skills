## API Endpoints

### Optimism

#### GET /api/v2/blocks/optimism-batch/{batch_number_param}

Retrieves L2 blocks that are bound to a specific Optimism batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/optimism/batches

Get the latest committed batches for Optimism.

- **Parameters**

  *None*

#### GET /api/v2/optimism/batches/{batch_number}

Get information for a specific Optimism batch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number` | `integer` | Yes |  |

#### GET /api/v2/optimism/deposits

Get L1 to L2 messages (deposits) for Optimism.

- **Parameters**

  *None*

#### GET /api/v2/optimism/games

Get dispute games for Optimism.

- **Parameters**

  *None*

#### GET /api/v2/optimism/withdrawals

Get L2 to L1 messages (withdrawals) for Optimism.

- **Parameters**

  *None*

#### GET /api/v2/transactions/optimism-batch/{batch_number_param}

Retrieves L2 transactions bound to a specific Optimism batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
