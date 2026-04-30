## API Endpoints

### Chain Statistics

#### GET /api/v2/main-page/blocks

Retrieves a limited set of recent blocks for display on the main page or dashboard.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/main-page/indexing-status

Retrieves the current status of blockchain data indexing by the BlockScout instance.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/main-page/transactions

Retrieves a limited set of recent transactions displayed on the home page.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/main-page/transactions/watchlist

Retrieves a list of last 6 transactions from the current user's watchlist.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/stats

Retrieves blockchain network statistics including total blocks, transactions, addresses, average block time, market data, and network utilization.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/stats/charts/market

Retrieves time series data of market information (daily closing price, market cap) for rendering charts.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/stats/charts/secondary-coin-market

Returns market history for the secondary coin used for charting.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/stats/charts/transactions

Retrieves time series data of daily transaction counts for rendering charts.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/stats/hot-smart-contracts

Retrieves paginated list of hot smart-contracts

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
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
  | `scale` | `string` | Yes | Time scale for hot contracts aggregation (5m=5 minutes, 1h=1 hour, 3h=3 hours, 1d=1 day, 7d=7 days, 30d=30 days) |
  | `transactions_count` | `integer` | No | Transactions count for paging |
  | `total_gas_used` | `integer` | No | Total gas used for paging |
  | `contract_address_hash` | `string` | No | Contract address hash for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

### Stats Service

#### GET /stats-service/api/v1/counters

- **Parameters**

  *None*

#### GET /stats-service/api/v1/lines

- **Parameters**

  *None*

#### GET /stats-service/api/v1/lines/{name}

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `name` | `string` | Yes |  |
  | `from` | `string` | No | Default is first data point |
  | `to` | `string` | No | Default is last data point |
  | `resolution` | `string` | No |  |

#### GET /stats-service/api/v1/pages/contracts

- **Parameters**

  *None*

#### GET /stats-service/api/v1/pages/interchain/main

- **Parameters**

  *None*

#### GET /stats-service/api/v1/pages/main

- **Parameters**

  *None*

#### GET /stats-service/api/v1/pages/multichain/main

- **Parameters**

  *None*

#### GET /stats-service/api/v1/pages/transactions

- **Parameters**

  *None*

#### GET /stats-service/api/v1/update-status

- **Parameters**

  *None*
