# Chainscout API File Specification

## 1. Purpose

Defines the content and format of the Chainscout API reference file at `blockscout-analysis/references/chainscout-api.md`. This file documents the Chainscout API endpoint used by agents to resolve a chain ID to its Blockscout instance URL. It is a hand-authored file (not script-generated) and follows the format defined in `api-format-spec.md`.

## 2. Output

| Item | Value |
|------|-------|
| Output file | `blockscout-analysis/references/chainscout-api.md` |
| Index file | **None** — this specification produces only the API file, not an index file |

## 3. Chainscout API Context

**Chainscout** (`https://chains.blockscout.com/api`) is the Blockscout chain registry. It is a separate service from any individual Blockscout instance and is accessed via direct HTTP requests (e.g., WebFetch or curl) — **not** via the `direct_api_call` MCP tool, which proxies to a specific Blockscout instance.

The primary purpose of Chainscout access is to resolve a chain ID to its Blockscout explorer URL. Chain IDs must be obtained first from the `get_chains_list` MCP tool, which provides the authoritative list of supported chains with their IDs.

## 4. Endpoint to Document

Document the following single endpoint:

**`GET /chains/{chain_id}`** — Returns the descriptor for a specific chain. The `explorers` array in the response contains the Blockscout instance URL (`url`) and the hosting provider (`hostedBy`). Agents use `explorers[].url` where `hostedBy` is `"blockscout"` to obtain the Blockscout instance URL for direct API calls.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `chain_id` | `string` | Yes | Numeric chain ID (e.g. `42161` for Arbitrum One). Obtain valid IDs from the `get_chains_list` MCP tool. |

## 5. File Format

The output file follows the format conventions defined in `api-format-spec.md` and observed in existing files under `blockscout-analysis/references/blockscout-api/`:

- **H2** (`##`): top-level section heading — `## Chainscout API`
- **H3** (`###`): endpoint category — `### Chain Registry`
- **H4** (`####`): individual endpoint — path only, **no HTTP method prefix** (e.g. `#### /chains/{chain_id}`)
- **Parameters**: Markdown table following the `api-format-spec.md` schema
- **No Example Request section**: all parameters are scalar types and the method is GET; consistent with all existing reference files

## 6. Prescribed File Content

The file `blockscout-analysis/references/chainscout-api.md` must contain exactly the following:

```markdown
## Chainscout API

Base URL: `https://chains.blockscout.com/api`

### Chain Registry

#### GET /chains/{chain_id}

Returns the descriptor for the specified chain, including the Blockscout explorer URL in the `explorers` array. Use `explorers[].url` where `explorers[].hostedBy` is `"blockscout"` to obtain the Blockscout instance URL.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `chain_id` | `string` | Yes | Numeric chain ID of the target network (e.g. `42161` for Arbitrum One). Obtain valid IDs from the `get_chains_list` MCP tool. |
```
