# PRO API

The Blockscout PRO API provides full endpoint coverage with 50-item pages. Use it when MCP tools lack the required endpoint or when bulk data retrieval is needed.

## Base URL

```
https://api.blockscout.com
```

**Documentation**: [PRO API docs](https://docs.blockscout.com/devs/pro-api.md)

Multichain: chain ID is specified in the URL path.

## Authentication

An API key is required. Format: `proapi_xxxxxxxx`.

**Obtaining a key**: Register at [Blockscout Development Portal](https://dev.blockscout.com).

**Passing the key** (either method works):
- Query parameter: `?apikey=$BLOCKSCOUT_API_KEY`
- Header: `Authorization: $BLOCKSCOUT_API_KEY`

**Environment variable**: Configure `$BLOCKSCOUT_API_KEY` in your shell so scripts can access it.

## Route Patterns

| API Surface | URL Pattern | Use Case |
|-------------|------------|----------|
| REST API | `/{chain_id}/api/v2/{path}` | Primary. Full endpoint set, structured JSON responses |
| JSON RPC | `/v2/api?chain_id={chain_id}&module=X&action=Y` | Etherscan-compatible queries |
| ETH RPC | `/{chain_id}/json-rpc` | Standard Ethereum JSON-RPC |

## Rate Limiting

Standard tier: **5 requests per second**.

## Pagination

PRO API uses **keyset pagination** with 50 items per page.

Each paginated response includes a `next_page_params` object. To get the next page, pass all fields from `next_page_params` as query parameters:

**Example — transactions:**

1. Initial: `GET /1/api/v2/transactions`
   ```json
   {
     "items": [...],
     "next_page_params": {
       "block_number": 24479322,
       "index": 238,
       "items_count": 50
     }
   }
   ```

2. Next page: `GET /1/api/v2/transactions?block_number=24479322&index=238&items_count=50`

3. Continue until `next_page_params` is absent or `items` is empty.

**Note**: The key names in `next_page_params` vary by endpoint. Always take the full object from the response and pass its fields as query parameters.

## JSON RPC Modules

| Module | Key Actions | Description |
|--------|------------|-------------|
| account | `balance`, `balancemulti`, `txlist`, `txlistinternal`, `tokentx`, `tokenlist`, `getminedblocks` | Address balances, transactions, token activity |
| logs | `getLogs` | Event log queries |
| token | `getToken`, `getTokenHolders` | Token metadata, holder lists |
| stats | `ethprice`, `tokensupply`, `ethsupply` | Network and token statistics |
| block | `getblockreward`, `getblockcountdown`, `getblocknobytime`, `eth_block_number` | Block data and lookups |
| contract | `getabi`, `getsourcecode`, `listcontracts` | Contract ABI and source |
| transaction | `gettxinfo`, `gettxreceiptstatus`, `getstatus` | Transaction details and status |

Query format: `?module={module}&action={action}&{params}`

**Full parameter docs**: [JSON RPC API overview](https://docs.blockscout.com/devs/apis/rpc.md) and per-module docs at `https://docs.blockscout.com/devs/apis/rpc/{module}.md` (e.g. [account](https://docs.blockscout.com/devs/apis/rpc/account.md), [transaction](https://docs.blockscout.com/devs/apis/rpc/transaction.md), [block](https://docs.blockscout.com/devs/apis/rpc/block.md)).

## ETH RPC Methods

Standard Ethereum JSON-RPC methods supported via `/{chain_id}/json-rpc`:

`eth_blockNumber`, `eth_getBalance`, `eth_getTransactionCount`, `eth_getCode`, `eth_getStorageAt`, `eth_gasPrice`, `eth_maxPriorityFeePerGas`, `eth_chainId`, `eth_getTransactionByHash`, `eth_getTransactionReceipt`, `eth_sendRawTransaction`, `eth_getBlockByNumber`, `eth_getBlockByHash`, `eth_call`, `eth_estimateGas`, `eth_getLogs`

**Full ETH RPC docs**: [ETH RPC API reference](https://docs.blockscout.com/devs/apis/rpc/eth-rpc.md)

## Endpoint Discovery via Swagger

PRO API endpoint documentation is available through swagger files, not through the dev portal. Use the swagger cache to discover endpoints:

1. Run `scripts/fetch-swagger.sh blockscout` to download the latest swagger.
2. Run `scripts/index-swagger.py --batch` to build the index.
3. Search the index for the endpoint you need.

See [Swagger Cache Guide](swagger-cache-guide.md) for the full workflow.

## Response Transformation

PRO API responses are **raw JSON** — verbose, deeply nested, and not optimized for LLM consumption. Scripts that query the PRO API must:

1. **Extract** only fields relevant to the user's question.
2. **Flatten** nested structures where possible.
3. **Format** output for token-efficient LLM consumption (e.g. compact tables, summary objects).
