## API Endpoints

### Zilliqa

#### GET /api/v2/validators/zilliqa

Retrieves the list of Zilliqa validators.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `index` | `integer` | No | Item index for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `sort` | `string` | No |  |
  | `order` | `string` | No |  |

#### GET /api/v2/validators/zilliqa/{bls_public_key}

Retrieves Zilliqa validator detailed info by the given BLS public key.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `bls_public_key` | `string` | Yes |  |
