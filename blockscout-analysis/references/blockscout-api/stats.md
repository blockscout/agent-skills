## API Endpoints

### Chain Statistics

#### GET /api/v2/main-page/blocks

Retrieves a limited set of recent blocks for display on the main page or dashboard.

- **Parameters**

  *None*

#### GET /api/v2/main-page/indexing-status

Retrieves the current status of blockchain data indexing by the BlockScout instance.

- **Parameters**

  *None*

#### GET /api/v2/main-page/transactions

Retrieves a limited set of recent transactions displayed on the home page.

- **Parameters**

  *None*

#### GET /api/v2/main-page/transactions/watchlist

Retrieves a list of last 6 transactions from the current user's watchlist.

- **Parameters**

  *None*

#### GET /api/v2/stats

Retrieves blockchain network statistics including total blocks, transactions, addresses, average block time, market data, and network utilization.

- **Parameters**

  *None*

#### GET /api/v2/stats/charts/market

Retrieves time series data of market information (daily closing price, market cap) for rendering charts.

- **Parameters**

  *None*

#### GET /api/v2/stats/charts/secondary-coin-market

Returns market history for the secondary coin used for charting.

- **Parameters**

  *None*

#### GET /api/v2/stats/charts/transactions

Retrieves time series data of daily transaction counts for rendering charts.

- **Parameters**

  *None*

#### GET /api/v2/stats/hot-smart-contracts

Retrieves paginated list of hot smart-contracts

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `sort` | `string` | No | Sort results by:
* transactions_count - Sort by number of transactions
* total_gas_used - Sort by total gas used
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

Returns all available counter stats for the stats page.

- **Parameters**

  *None*

#### GET /stats-service/api/v1/lines

Returns metadata (title, description, available resolutions) for all
line charts, organized into sections.

- **Parameters**

  *None*

#### GET /stats-service/api/v1/lines/{name}

Returns data points for a specific line chart, with optional date range
and resolution filtering.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `name` | `string` | Yes | Identifier of the chart to retrieve (matches chart id). |
  | `from` | `string` | No | Default is first data point |
  | `to` | `string` | No | Default is last data point |
  | `resolution` | `string` | No |  |

#### GET /stats-service/api/v1/pages/contracts

Returns stats to be displayed on the contracts page.

- **Parameters**

  *None*

#### GET /stats-service/api/v1/pages/interchain/main

Returns interchain messaging stats to be displayed on the main page of interchain indexer.

- **Parameters**

  *None*

#### GET /stats-service/api/v1/pages/main

Returns stats to be displayed on the main page of indexer.

- **Parameters**

  *None*

#### GET /stats-service/api/v1/pages/multichain/main

Returns multichain-aggregated stats to be displayed on the main page of multichain indexer.

- **Parameters**

  *None*

#### GET /stats-service/api/v1/pages/transactions

Returns stats to be displayed on the transactions page.

- **Parameters**

  *None*

#### GET /stats-service/api/v1/update-status

Returns the current status of chart data updates, broken down by
indexing dependency type (independent, blocks, internal transactions, etc.).

- **Parameters**

  *None*
