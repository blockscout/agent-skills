## API Endpoints

### Configuration

#### GET /api/v2/config/backend-version

Returns application backend version string.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/config/indexer

Returns config of indexer.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/config/public-metrics

Returns update period / configuration for public metrics.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/config/smart-contracts/languages

Returns list of smart contract languages supported by the database schema.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
