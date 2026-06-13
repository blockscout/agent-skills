## API Endpoints

### Scroll

#### GET /api/v2/blocks/scroll-batch/{batch_number_param}

Retrieves L2 blocks that are bound to a specific Scroll batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/scroll/batches

Retrieves a paginated list of batches.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `number` | `integer` | No | Number for paging |

#### GET /api/v2/scroll/batches/count

Retrieves a size of the batch list.

- **Parameters**

  *None*

#### GET /api/v2/scroll/batches/{number}

Retrieves batch info by the given number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `number` | `string` | Yes | Batch number in the path. |

#### GET /api/v2/scroll/deposits

Retrieves a paginated list of deposits.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `id` | `integer` | No | ID for paging |

#### GET /api/v2/scroll/deposits/count

Retrieves a size of the deposits list.

- **Parameters**

  *None*

#### GET /api/v2/scroll/withdrawals

Retrieves a paginated list of withdrawals.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `id` | `integer` | No | ID for paging |

#### GET /api/v2/scroll/withdrawals/count

Retrieves a size of the withdrawals list.

- **Parameters**

  *None*

#### GET /api/v2/transactions/scroll-batch/{batch_number_param}

Retrieves L2 transactions bound to a specific Scroll batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Item index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
