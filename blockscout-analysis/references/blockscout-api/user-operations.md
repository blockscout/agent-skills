## API Endpoints

### User Operations

#### GET /api/v2/proxy/account-abstraction/accounts

Retrieves a list of account abstraction wallets.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `factory` | `string` | No | User operation factory address hash |
  | `page_size` | `integer` | No | Number of items returned per page |
  | `page_token` | `string` | No | Page token for paging |

#### GET /api/v2/proxy/account-abstraction/accounts/{address_hash_param}

Retrieves an account abstraction wallet by its address hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |

#### GET /api/v2/proxy/account-abstraction/bundlers

Retrieves a list of top bundlers.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `page_size` | `integer` | No | Number of items returned per page |
  | `page_token` | `string` | No | Page token for paging |

#### GET /api/v2/proxy/account-abstraction/bundlers/{address_hash_param}

Retrieves a bundler by its address hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |

#### GET /api/v2/proxy/account-abstraction/bundles

Retrieves a list of recent bundles.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `bundler` | `string` | No | User operation bundler address hash |
  | `entry_point` | `string` | No | User operation entry point address hash |
  | `page_size` | `integer` | No | Number of items returned per page |
  | `page_token` | `string` | No | Page token for paging |

#### GET /api/v2/proxy/account-abstraction/factories

Retrieves a list of top wallet factories.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `page_size` | `integer` | No | Number of items returned per page |
  | `page_token` | `string` | No | Page token for paging |

#### GET /api/v2/proxy/account-abstraction/factories/{address_hash_param}

Retrieves a factory by its address hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |

#### GET /api/v2/proxy/account-abstraction/operations

Retrieves a list of recent user operations.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `sender` | `string` | No | User operation sender address hash |
  | `bundler` | `string` | No | User operation bundler address hash |
  | `paymaster` | `string` | No | User operation paymaster address hash |
  | `factory` | `string` | No | User operation factory address hash |
  | `transaction_hash` | `string` | No | Transaction hash in the query |
  | `entry_point` | `string` | No | User operation entry point address hash |
  | `bundle_index` | `integer` | No | User operation bundle index |
  | `block_number` | `integer` | No | User operation block number |
  | `page_size` | `integer` | No | Number of items returned per page |
  | `page_token` | `string` | No | Page token for paging |

#### GET /api/v2/proxy/account-abstraction/operations/{operation_hash_param}

Retrieves a user operation by its hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `operation_hash_param` | `string` | Yes | User operation hash in the path |

#### GET /api/v2/proxy/account-abstraction/operations/{operation_hash_param}/summary

Retrieves a human-readable summary of what a user operation did, presented in natural language.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `operation_hash_param` | `string` | Yes | User operation hash in the path |
  | `just_request_body` | `boolean` | No | If true, returns only the request body in the summary endpoint |

#### GET /api/v2/proxy/account-abstraction/paymasters

Retrieves a list of top paymasters.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `page_size` | `integer` | No | Number of items returned per page |
  | `page_token` | `string` | No | Page token for paging |

#### GET /api/v2/proxy/account-abstraction/paymasters/{address_hash_param}

Retrieves a paymaster by its address hash.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address_hash_param` | `string` | Yes | Address hash in the path |

#### GET /api/v2/proxy/account-abstraction/status

Retrieves the status of the account abstraction microservice.

- **Parameters**

  *None*
