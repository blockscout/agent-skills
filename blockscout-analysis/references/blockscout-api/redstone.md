## API Endpoints

### Redstone

#### GET /api/v2/mud/worlds

Get a list of MUD worlds for Redstone.

- **Parameters**

  *None*

#### GET /api/v2/mud/worlds/{contract_address}/tables

Get tables for a specific MUD world on Redstone.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `contract_address` | `string` | Yes |  |

#### GET /api/v2/mud/worlds/{contract_address}/tables/{table_id}/records

Get records for a specific MUD world table on Redstone.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `contract_address` | `string` | Yes |  |
  | `table_id` | `string` | Yes |  |

#### GET /api/v2/mud/worlds/{contract_address}/tables/{table_id}/records/{record_id}

Get a specific record from a MUD world table on Redstone.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `contract_address` | `string` | Yes |  |
  | `table_id` | `string` | Yes |  |
  | `record_id` | `string` | Yes |  |
