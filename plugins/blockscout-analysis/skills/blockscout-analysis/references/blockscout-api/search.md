## API Endpoints

### Search

#### GET /api/v1/search

Performs a unified search across multiple blockchain entity types including tokens, addresses, contracts, blocks, transactions and other resources.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `q` | `string` | No | Search query filter |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `next_page_params_type` | `string` | No | Next page params type for paging |
  | `label` | `object` | No | Label for paging in the search results |
  | `token` | `object` | No | Token for paging in the search results |
  | `contract` | `object` | No | Contract for paging in the search results |
  | `tac_operation` | `object` | No | TAC operation for paging in the search results |
  | `metadata_tag` | `object` | No | Metadata tag for paging in the search results |
  | `block` | `object` | No | Block for paging in the search results |
  | `blob` | `object` | No | Blob for paging in the search results |
  | `user_operation` | `object` | No | User operation for paging in the search results |
  | `address` | `object` | No | Address for paging in the search results |
  | `ens_domain` | `object` | No | ENS domain for paging in the search results |

- **Example Request**

  ```bash
  curl "{base_url}/api/v1/search"
  ```

#### GET /api/v2/search

Performs a unified search across multiple blockchain entity types including tokens, addresses, contracts, blocks, transactions and other resources.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `q` | `string` | No | Search query filter |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
  | `next_page_params_type` | `string` | No | Next page params type for paging |
  | `label` | `object` | No | Label for paging in the search results |
  | `token` | `object` | No | Token for paging in the search results |
  | `contract` | `object` | No | Contract for paging in the search results |
  | `tac_operation` | `object` | No | TAC operation for paging in the search results |
  | `metadata_tag` | `object` | No | Metadata tag for paging in the search results |
  | `block` | `object` | No | Block for paging in the search results |
  | `blob` | `object` | No | Blob for paging in the search results |
  | `user_operation` | `object` | No | User operation for paging in the search results |
  | `address` | `object` | No | Address for paging in the search results |
  | `ens_domain` | `object` | No | ENS domain for paging in the search results |

- **Example Request**

  ```bash
  curl "{base_url}/api/v2/search"
  ```

#### GET /api/v2/search/check-redirect

Checks if a search query redirects to a specific entity page rather than showing search results.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `q` | `string` | No | Search query filter |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |

#### GET /api/v2/search/quick

Performs a quick, unpaginated search for short queries.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `q` | `string` | No | Search query filter |
  | `apikey` | `string` | No | API key for rate limiting or for sensitive endpoints |
  | `key` | `string` | No | Secret key for getting access to restricted resources |
