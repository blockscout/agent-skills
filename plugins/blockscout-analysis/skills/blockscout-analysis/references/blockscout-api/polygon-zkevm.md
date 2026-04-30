## API Endpoints

### Polygon zkEVM

#### GET /api/v2/transactions/zkevm-batch/{batch_number_param}

Retrieves L2 transactions bound to a specific Polygon ZkEVM batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/zkevm/batches/confirmed

Get the latest confirmed batches for zkEVM.

- **Parameters**

  *None*

#### GET /api/v2/zkevm/batches/{batch_number}

Get information for a specific zkEVM batch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number` | `integer` | Yes |  |

#### GET /api/v2/zkevm/deposits

Get deposits for zkEVM.

- **Parameters**

  *None*

#### GET /api/v2/zkevm/withdrawals

Get withdrawals for zkEVM.

- **Parameters**

  *None*
