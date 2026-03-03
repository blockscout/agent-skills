## API Endpoints

### Mud

#### GET /api/v2/mud/worlds

Retrieves a paginated list of MUD worlds with basic stats.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `world` | `string` | No | MUD world address hash for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/mud/worlds/count

Retrieves the total number of known MUD worlds.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/mud/worlds/{world}/systems

Retrieves a list of MUD systems registered in the specific MUD world.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `world` | `string` | Yes | MUD world address hash in the path |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/mud/worlds/{world}/systems/{system}

Retrieves a list of MUD system ABI methods registered in the specific MUD world.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `world` | `string` | Yes | MUD world address hash in the path |
  | `system` | `string` | Yes | MUD system address hash in the path |

#### GET /api/v2/mud/worlds/{world}/tables

Retrieves a paginated list of MUD tables in the specific MUD world.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `world` | `string` | Yes | MUD world address hash in the path |
  | `q` | `string` | No | Search query filter |
  | `filter_namespace` | `string` | No | Filter by namespace |
  | `table_id` | `string` | No | MUD table ID for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/mud/worlds/{world}/tables/count

Retrieves the total number of known MUD tables in the specific MUD world.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `world` | `string` | Yes | MUD world address hash in the path |
  | `q` | `string` | No | Search query filter |
  | `filter_namespace` | `string` | No | Filter by namespace |

#### GET /api/v2/mud/worlds/{world}/tables/{table_id}/records

Retrieves a paginated list of records in the specific MUD world table.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `world` | `string` | Yes | MUD world address hash in the path |
  | `table_id` | `string` | Yes | MUD table ID in the path |
  | `filter_key0` | `string` | No | Filter by key0 |
  | `filter_key1` | `string` | No | Filter by key1 |
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
  | `key_bytes` | `string` | No | MUD record key_bytes for paging |
  | `key0` | `string` | No | MUD record key0 for paging |
  | `key1` | `string` | No | MUD record key1 for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/mud/worlds/{world}/tables/{table_id}/records/count

Retrieves the total number of records in the specific MUD world table.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `world` | `string` | Yes | MUD world address hash in the path |
  | `table_id` | `string` | Yes | MUD table ID in the path |
  | `filter_key0` | `string` | No | Filter by key0 |
  | `filter_key1` | `string` | No | Filter by key1 |

#### GET /api/v2/mud/worlds/{world}/tables/{table_id}/records/{record_id}

Retrieves a single record in the specific MUD world table.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `world` | `string` | Yes | MUD world address hash in the path |
  | `table_id` | `string` | Yes | MUD table ID in the path |
  | `record_id` | `string` | Yes | MUD record ID in the path |
