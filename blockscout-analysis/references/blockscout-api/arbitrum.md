## API Endpoints

### Arbitrum

#### GET /api/v2/arbitrum/batches

Retrieves a paginated list of Arbitrum batches committed to the Parent chain.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_numbers` | `array` | No | Optional list of specific batch numbers to retrieve. |
  | `number` | `integer` | No | Number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/arbitrum/batches/count

Retrieves the total count of Arbitrum batches committed to the Parent chain.

- **Parameters**

  *None*

#### GET /api/v2/arbitrum/batches/da/anytrust/{data_hash}

Retrieves an Arbitrum batch associated with the given AnyTrust data hash. By default, returns the most recently associated batch. When `type=all`, returns a paginated list of all batches referencing this data hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `data_hash` | `string` | Yes | AnyTrust data hash. |
  | `type` | `string` | No | When set to `all`, returns a paginated list of all batches for this data hash. |
  | `number` | `integer` | No | Number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/arbitrum/batches/da/celestia/{height}/{transaction_commitment}

Retrieves an Arbitrum batch whose data availability blob is identified by the given Celestia block height and transaction commitment hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `height` | `integer` | Yes | Celestia block height. |
  | `transaction_commitment` | `string` | Yes | Celestia transaction commitment hash. |

#### GET /api/v2/arbitrum/batches/da/eigenda/{data_hash}

Retrieves an Arbitrum batch associated with the given EigenDA data hash. By default, returns the most recently associated batch. When `type=all`, returns a paginated list of all batches referencing this data hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `data_hash` | `string` | Yes | EigenDA data hash (Keccak-256 of the blob header). |
  | `type` | `string` | No | When set to `all`, returns a paginated list of all batches for this data hash. |
  | `number` | `integer` | No | Number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/arbitrum/batches/{batch_number}

Retrieves detailed information about an Arbitrum batch by its number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number` | `integer` | Yes | Batch number. |

#### GET /api/v2/arbitrum/messages/claim/{message_id}

Returns the ABI-encoded calldata and outbox contract address required to execute a Rollup withdrawal on the Parent chain.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `message_id` | `integer` | Yes | Withdrawal message ID. |

#### GET /api/v2/arbitrum/messages/withdrawals/{transaction_hash}

Returns the list of Rollup withdrawal messages (L2ToL1Tx events) emitted by the given transaction.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `transaction_hash` | `string` | Yes | Transaction hash. |

#### GET /api/v2/arbitrum/messages/{direction}

Retrieves a paginated list of Arbitrum cross-chain messages filtered by the specified direction.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `direction` | `string` | Yes | Message direction: `from-rollup` for Rollup to Parent chain, `to-rollup` for Parent chain to Rollup. |
  | `id` | `integer` | No | ID for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/arbitrum/messages/{direction}/count

Retrieves the total count of Arbitrum cross-chain messages for the specified direction.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `direction` | `string` | Yes | Message direction: `from-rollup` for Rollup to Parent chain, `to-rollup` for Parent chain to Rollup. |

#### GET /api/v2/blocks/arbitrum-batch/{batch_number_param}

Retrieves L2 blocks that are bound to a specific Arbitrum batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/main-page/arbitrum/batches/committed

Retrieves a list of Arbitrum batches that have been committed to the Parent chain, displayed on the main page.

- **Parameters**

  *None*

#### GET /api/v2/main-page/arbitrum/batches/latest-number

Retrieves the number of the most recent Arbitrum batch submitted to the Parent chain. Returns 0 if no batches exist.

- **Parameters**

  *None*

#### GET /api/v2/main-page/arbitrum/messages/to-rollup

Retrieves the most recent relayed messages from Parent chain to Rollup, displayed on the main page.

- **Parameters**

  *None*

#### GET /api/v2/transactions/arbitrum-batch/{batch_number_param}

Retrieves L2 transactions bound to a specific Arbitrum batch number.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `batch_number_param` | `integer` | Yes | Batch number |
  | `block_number` | `integer` | No | Block number for paging |
  | `index` | `integer` | No | Item index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
