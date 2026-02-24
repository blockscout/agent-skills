## API Endpoints

### Celo

#### GET /api/v2/addresses/{address_hash_param}/celo/election-rewards

Retrieves Celo election rewards for a specific address.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `address_hash_param` | `string` | Yes | Address hash in the path |
  | `items_count` | `integer` | No | Number of items returned per page |
  | `epoch_number` | `string` | No | Epoch number for paging |
  | `amount` | `string` | No | Amount for paging |
  | `associated_account_address_hash` | `string` | No | Associated account address hash for paging |
  | `type` | `string` | No | Type for paging |

#### GET /api/v2/celo/epochs

Get the latest finalized epochs for Celo.

- **Parameters**

  *None*

#### GET /api/v2/celo/epochs/{epoch_number}

Get information for a specific Celo epoch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `epoch_number` | `integer` | Yes |  |

#### GET /api/v2/celo/epochs/{epoch_number}/election-rewards/group

Get validator group rewards for a specific Celo epoch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `epoch_number` | `integer` | Yes |  |

#### GET /api/v2/celo/epochs/{epoch_number}/election-rewards/validator

Get validator rewards for a specific Celo epoch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `epoch_number` | `integer` | Yes |  |

#### GET /api/v2/celo/epochs/{epoch_number}/election-rewards/voter

Get voter rewards for a specific Celo epoch.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `epoch_number` | `integer` | Yes |  |

#### GET /api/v2/config/celo

Returns Celo-specific configuration (l2 migration block).

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
