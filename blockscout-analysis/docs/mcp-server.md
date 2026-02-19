# MCP Server

The Blockscout MCP Server provides LLM-friendly, enriched blockchain data with simplified pagination. It is the preferred data source for most tasks.

## Endpoints

| Protocol | URL | Notes |
|----------|-----|-------|
| Native MCP | `https://mcp.blockscout.com/mcp` | For agents with MCP client support |
| REST API | `https://mcp.blockscout.com/v1/{tool_name}` | HTTP GET, usable from scripts |

All operational tools accept a `chain_id` parameter (default: `1` — Ethereum Mainnet).

## Ensuring MCP Server Availability

When your task requires native MCP tool calls (e.g. `read_contract`, iterative contract investigation), ensure the Blockscout MCP server is configured in your environment **before** relying on MCP tools:

1. Check if Blockscout MCP tools (e.g. `get_address_info`, `get_transaction_info`) are available.
2. If not available, instruct the user to add the Blockscout MCP server (`https://mcp.blockscout.com/mcp`) to their agent's MCP configuration — or install/enable it automatically if you have that capability.
3. If native MCP is unavailable and cannot be configured, use the REST API (`https://mcp.blockscout.com/v1/`) via HTTP instead.

## `unlock_blockchain_analysis` Prerequisite

**Before calling any other Blockscout MCP tool**, call `unlock_blockchain_analysis` once per session (or before the first MCP tool use, if session boundaries are unclear).

- This is mandatory for all MCP clients that do not reliably read server-provided tool descriptions.
- **Exception**: In **Claude Code**, this call is optional — Claude Code reads MCP server instructions correctly.
- **Defer the call** until MCP tools are actually needed — do not call it preemptively at session start if no MCP tools will be used.
- The tool's response contains operational rules, chain guidance, and the direct API endpoint catalog. **That content is the canonical source** — do not duplicate it; refer to it when needed.

## Tool Catalog

| Tool | Key Params | Paginated | Purpose |
|------|-----------|-----------|---------|
| `get_chains_list` | — | No | List supported chains |
| `get_address_info` | chain_id, address | No | Address details, balance, contract status, metadata |
| `get_address_by_ens_name` | name | No | Resolve ENS domain to address |
| `get_tokens_by_address` | chain_id, address | Yes | ERC-20 token holdings with market data |
| `nft_tokens_by_address` | chain_id, address | Yes | NFT holdings grouped by collection |
| `get_transactions_by_address` | chain_id, address, age_from | Yes | Native transfers and contract calls |
| `get_token_transfers_by_address` | chain_id, address, age_from | Yes | ERC-20 token transfers |
| `get_transaction_info` | chain_id, transaction_hash | No | Enriched transaction details with decoded input |
| `get_block_info` | chain_id, number_or_hash | No | Block details, optionally with tx hashes |
| `get_block_number` | chain_id | No | Latest block or block at a specific datetime |
| `get_contract_abi` | chain_id, address | No | Smart contract ABI |
| `inspect_contract_code` | chain_id, address | No | Verified contract source code and metadata |
| `read_contract` | chain_id, address, abi, function_name | No | Call a contract function (view/pure) |
| `lookup_token_by_symbol` | chain_id, symbol | No | Search tokens by symbol or name |
| `direct_api_call` | chain_id, endpoint_path | Yes | Proxy to any Blockscout API endpoint |

**Note on `direct_api_call`**: Unlike other MCP tools, `direct_api_call` is a raw proxy — it does not enrich, filter, or optimize responses. Expect raw Blockscout API JSON, similar to PRO API responses.

This table summarizes tool names and interfaces. For operational rules, chain guidance, and the complete direct API endpoint catalog, consult the `unlock_blockchain_analysis` output.

## REST API Usage Pattern

Call any tool via HTTP GET:

```
GET https://mcp.blockscout.com/v1/{tool_name}?param1=value1&param2=value2
```

All responses follow a standard envelope:

```json
{
  "data": { ... },
  "data_description": ["..."],
  "notes": ["..."],
  "instructions": ["..."],
  "pagination": { "next_call": { "tool_name": "...", "params": { "cursor": "..." } } }
}
```

- `data` — the main payload (tool-specific)
- `data_description` — optional field descriptions
- `notes` — optional warnings or context
- `instructions` — optional suggested follow-up actions
- `pagination` — present only when more pages exist

## Pagination

MCP uses opaque cursor-based pagination (~10 items per page):

1. Make the initial call without a `cursor` parameter.
2. If the response includes `pagination.next_call`, pass the `cursor` value from `pagination.next_call.params.cursor` in your next call.
3. Repeat until no `pagination` field is returned.

The cursor is an opaque string — never parse or construct it. Just pass it through.

**Trade-off**: MCP returns ~10 items per page (vs PRO API's 50), but responses are enriched and may save follow-up queries.

## When MCP Is Not Configured

If the MCP server is not configured in your environment:

- Use the REST API directly via HTTP (`https://mcp.blockscout.com/v1/`).
- Discover available tools via `GET https://mcp.blockscout.com/v1/tools`.
- Or use the cached tools index — see [MCP Tools Cache Guide](mcp-tools-cache-guide.md).

## API Reference

For full tool documentation including parameters, response shapes, and examples:
- [MCP Server API Reference](https://raw.githubusercontent.com/blockscout/mcp-server/refs/heads/main/API.md)

**Even when MCP is configured** and tool names are available in your context, consult this reference for parameter details and usage examples that may not be in the tool descriptions.

## Chain-Specific Endpoints

Certain Blockscout API endpoints are available only for specific chain families (e.g. beacon deposits for Ethereum, batches for Arbitrum/Optimism/zkSync, epochs for Celo).

These endpoints are accessible via `direct_api_call` and are cataloged in the response of `unlock_blockchain_analysis`. **Consult that tool's output for the current chain-specific endpoint catalog** — it is maintained by the MCP server and may change over time.
