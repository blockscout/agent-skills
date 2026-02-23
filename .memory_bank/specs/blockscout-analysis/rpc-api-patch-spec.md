# JSON-RPC Endpoint Integration Specification

## 1. Purpose

Defines the required changes to add two Blockscout JSON-RPC compatibility endpoints to their thematically appropriate topic API files and to the master index. These endpoints are accessed at `{instance_base_url}/api?module=<module>&action=<action>`, have no swagger source, and are absent from files produced by `api-file-generator.py`. This specification closes that gap.

## 2. When to Apply

Apply these changes (manually or via an AI agent) after running `api-file-generator.py` (which recreates all topic files from scratch) and, optionally, `mcp-unlock-patch.py`. The endpoints defined here are stable — they do not change when either of those processes runs.

If `api-file-generator.py` is re-run, re-apply the changes described in this spec.

The complete workflow that produces a fully documented API reference:

```
swagger-main-indexer.py    → produces .build/swaggers/main-indexer/endpoints_map.json
swagger-stats-indexer.py   → produces .build/swaggers/stats-service/endpoints_map.json
api-file-generator.py      → creates/overwrites all topic api files AND recreates blockscout-api-index.md
mcp-unlock-patch.py        → patches MCP-sourced endpoints into topic files and index (either order)
[apply this spec]          → patches JSON-RPC endpoints into topic files and index (either order)
```

## 3. Endpoints to Add

### 3.1 `GET /api?module=logs&action=getLogs`

**Target file:** `blockscout-analysis/references/blockscout-api/transactions.md`
**Target section:** `### JSON-RPC Compatibility` (create if absent; see Section 4)

**Entry to insert** (format per `api-format-spec.md`):

```markdown
#### GET /api?module=logs&action=getLogs

Returns event logs filtered by block range, optional contract address, and up to four topic values. Results are capped at 1,000 entries. When calling via `direct_api_call`, use `endpoint_path="/api"` and pass all parameters in `query_params`.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `fromBlock` | `integer` | Yes | Start block number. |
  | `toBlock` | `integer` | Yes | End block number. |
  | `address` | `string` | No | Contract address to filter logs for. |
  | `topic0` | `string` | No | Topic 0 hex value. |
  | `topic1` | `string` | No | Topic 1 hex value. |
  | `topic2` | `string` | No | Topic 2 hex value. |
  | `topic3` | `string` | No | Topic 3 hex value. |
  | `topic0_1_opr` | `string` | No | Boolean operator between topic0 and topic1: `and` or `or`. |
  | `topic0_2_opr` | `string` | No | Boolean operator between topic0 and topic2: `and` or `or`. |
  | `topic0_3_opr` | `string` | No | Boolean operator between topic0 and topic3: `and` or `or`. |
  | `topic1_2_opr` | `string` | No | Boolean operator between topic1 and topic2: `and` or `or`. |
  | `topic1_3_opr` | `string` | No | Boolean operator between topic1 and topic3: `and` or `or`. |
  | `topic2_3_opr` | `string` | No | Boolean operator between topic2 and topic3: `and` or `or`. |
```

### 3.2 `GET /api?module=account&action=eth_get_balance`

**Target file:** `blockscout-analysis/references/blockscout-api/addresses.md`
**Target section:** `### JSON-RPC Compatibility` (create if absent; see Section 4)

**Entry to insert:**

```markdown
#### GET /api?module=account&action=eth_get_balance

Returns the ETH balance of an address in an Ethereum-compatible hex format (0x-prefixed). **The returned value is hex-encoded and must be decoded from hexadecimal to obtain the balance in wei.** For example, `0xde0b6b3a7640000` decodes to `1000000000000000000` wei (1 ETH). Pass a specific block number in the `block` parameter to retrieve the historical balance at that block. When calling via `direct_api_call`, use `endpoint_path="/api"` and pass all parameters in `query_params`.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `address` | `string` | Yes | The address to check balance for. |
  | `block` | `string` | No | Block identifier: `latest`, `earliest`, `pending`, or a decimal block number as a string. Defaults to `latest`. Use a specific block number to query historical balance. |
```

## 4. Target Section Structure

If `### JSON-RPC Compatibility` does not already exist in the target file, append it at the end of the file with the following preamble immediately after the H3 heading and before the first endpoint entry:

```markdown
### JSON-RPC Compatibility

These are Etherscan-compatible legacy endpoints. When using `direct_api_call`, set `endpoint_path="/api"` and pass `module`, `action`, and any other parameters via `query_params`. The `module` and `action` values are part of the endpoint identity and are not listed in the parameter tables below.

<endpoint entries here, sorted alphabetically by path>
```

Multiple endpoint entries within the section are sorted alphabetically by path (case-insensitive).

## 5. Path Representation

The canonical path identifier for each endpoint is `/api?module=<module>&action=<action>`. This string is used verbatim in:

- H4 headings: `#### GET /api?module=logs&action=getLogs`
- Index line items: `- /api?module=logs&action=getLogs: ...`

`module` and `action` are encoded in the path string, not listed as query parameters.

## 6. Master Index Updates

After the topic files are updated, add the following line items to the master index `blockscout-analysis/references/blockscout-api-index.md` in the appropriate existing sections.

**In the `## [Transactions](blockscout-api/transactions.md)` section:**

```
- `/api?module=logs&action=getLogs`: Returns event logs filtered by block range, optional contract address, and up to four topic values. Results are capped at 1,000 entries.
```

**In the `## [Addresses](blockscout-api/addresses.md)` section:**

```
- `/api?module=account&action=eth_get_balance`: Returns the ETH balance of an address as a hex-encoded wei value (0x-prefixed). Decode from hexadecimal to get the decimal balance in wei. Supports historical queries via the `block` parameter (e.g. a decimal block number).
```

Insert each line item in sort order within its section. The path `/api?module=...` sorts after all `/api/v2/...` paths (ASCII: `?` > `/`), so these entries appear at the end of their respective sections.

## 7. Idempotency and Coordination with `mcp-unlock-patch.py`

Before inserting any entry, check whether it is already present:

- **In api files:** scan for the line `#### GET /api?module=<module>&action=<action>` — if found, skip that entry.
- **In the index:** scan for a line beginning with `` - `/api?module=<module>&action=<action>` `` — if found, skip that index entry.

`mcp-unlock-patch.py` sources its endpoints from the live MCP response and normalises paths based on `{param_name}` segments. It will never produce or remove entries of the form `/api?module=...`. The two processes are non-overlapping and safe to run in either order.

## 8. Verification

After applying all changes, verify:

1. `references/blockscout-api/transactions.md` contains `#### GET /api?module=logs&action=getLogs` under `### JSON-RPC Compatibility`.
2. `references/blockscout-api/addresses.md` contains `#### GET /api?module=account&action=eth_get_balance` with the hex-decode note under `### JSON-RPC Compatibility`.
3. `references/blockscout-api-index.md` Transactions section contains a line item for `/api?module=logs&action=getLogs`.
4. `references/blockscout-api-index.md` Addresses section contains a line item for `/api?module=account&action=eth_get_balance`.
5. Re-applying the spec a second time produces no duplicate entries (idempotency).
6. Running `mcp-unlock-patch.py` after applying this spec does not remove or duplicate these entries.
