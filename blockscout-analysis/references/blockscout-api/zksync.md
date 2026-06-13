## API Endpoints

### ZkSync

#### GET /api/v2/main-page/zksync/batches/latest-number

Get the latest committed batch number for zkSync.

- **Parameters**

  *None*

#### GET /api/v2/transactions/zksync-batch/{batch_number_param}

Retrieves L2 transactions bound to a specific ZkSync batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Item index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/zksync/batches/{batch_number}

Get information for a specific zkSync batch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number` | `integer` | Yes |  |
