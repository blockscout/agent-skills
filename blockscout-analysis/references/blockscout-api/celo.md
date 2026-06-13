## API Endpoints

### Celo

#### GET /api/v2/addresses/{address_hash_param}/celo/election-rewards

Retrieves Celo election rewards for a specific address.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `epoch_number` | `string` | No | Epoch number for paging |
  | `amount` | `string` | No | Amount for paging |
  | `associated_account_address_hash` | `string` | No | Associated account address hash for paging |
  | `type` | `string` | No | Type for paging |

#### GET /api/v2/celo/epochs

Retrieves a paginated list of Celo epochs.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `number` | `integer` | No | Number for paging |
  | `items_count` | `integer` | No | Number of items returned per page |

#### GET /api/v2/celo/epochs/{number}

Retrieves detailed information about a Celo epoch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `number` | `string` | Yes | Epoch number in the path. |

#### GET /api/v2/celo/epochs/{number}/election-rewards/{type}

Retrieves a paginated list of election rewards for a Celo epoch and reward type.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `number` | `string` | Yes | Epoch number in the path. |
  | `type` | `string` | Yes | Reward type in the path. |
  | `amount` | `string` | No | Amount for paging |
  | `account_address_hash` | `string` | No | Account address hash for paging |
  | `associated_account_address_hash` | `string` | No | Associated account address hash for paging |
  | `items_count` | `integer` | No | Number of items returned per page |
