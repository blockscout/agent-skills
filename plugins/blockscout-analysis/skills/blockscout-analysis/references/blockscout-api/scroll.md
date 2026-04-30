## API Endpoints

### Scroll

#### GET /api/v2/blocks/scroll-batch/{batch_number_param}

Retrieves L2 blocks that are bound to a specific Scroll batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/scroll/batches

Get the latest committed batches for Scroll.

- **Parameters**

  *None*

#### GET /api/v2/scroll/batches/{batch_number}

Get information for a specific Scroll batch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number` | `integer` | Yes |  |

#### GET /api/v2/scroll/deposits

Get L1 to L2 messages (deposits) for Scroll.

- **Parameters**

  *None*

#### GET /api/v2/scroll/withdrawals

Get L2 to L1 messages (withdrawals) for Scroll.

- **Parameters**

  *None*

#### GET /api/v2/transactions/scroll-batch/{batch_number_param}

Retrieves L2 transactions bound to a specific Scroll batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
