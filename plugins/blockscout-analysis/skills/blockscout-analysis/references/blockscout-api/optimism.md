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

#### GET /api/v2/main-page/optimism-deposits

Retrieves a list of deposits for the main page.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/optimism/batches

Retrieves a paginated list of batches.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `id` | `integer` | No | ID for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/optimism/batches/count

Retrieves a size of the batch list.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/optimism/batches/da/celestia/{height}/{commitment}

Retrieves batch detailed info by the given celestia blob metadata (height and commitment).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `height` | `string` | Yes | Celestia blob height in the path. |
  | `commitment` | `string` | Yes | Celestia blob commitment in the path. |

#### GET /api/v2/optimism/batches/{number}

Retrieves batch detailed info by the given number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `number` | `string` | Yes | Batch number in the path. |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/optimism/deposits

Retrieves a paginated list of deposits.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `l1_block_number` | `integer` | No | L1 block number for paging |
  | `transaction_hash` | `string` | No | Transaction hash for paging |

#### GET /api/v2/optimism/deposits/count

Retrieves a size of the deposits list.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/optimism/games

Retrieves a paginated list of games.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/optimism/games/count

Retrieves a size of the games list.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/optimism/output-roots

Retrieves a paginated list of output roots.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `index` | `integer` | No | Transaction index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/optimism/output-roots/count

Retrieves a size of the output roots list.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/optimism/withdrawals

Retrieves a paginated list of withdrawals.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `nonce` | `string` | No | Nonce for paging |

#### GET /api/v2/optimism/withdrawals/count

Retrieves a size of the withdrawals list.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

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
