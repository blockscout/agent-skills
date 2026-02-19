# MCP Tools Cache Guide

When the Blockscout MCP server is not configured in your agent's environment, use the cached tools list to discover available tools and their parameters without making live requests.

## Purpose

The MCP tools cache stores the full output of `GET https://mcp.blockscout.com/v1/tools` (all tool names, descriptions, and input schemas) in a local file with a grep-friendly index. This enables:

- Offline tool discovery when the MCP server is not configured.
- Reduced latency by avoiding repeated `/v1/tools` calls.
- Context-efficient lookups — read only the section for the tool you need.

## Fetching Tools

Use `scripts/fetch-mcp-tools.sh` to download and cache the tools list:

```bash
# Download with freshness check
./scripts/fetch-mcp-tools.sh

# Force re-download
./scripts/fetch-mcp-tools.sh --force
```

The script:
1. Calls `unlock_blockchain_analysis` to get the current MCP server version.
2. Compares with the cached version.
3. Downloads and pretty-prints `tools.json` if the version differs or no cache exists.

## Indexing Tools

Use `scripts/index-mcp-tools.py` to build the index:

```bash
./scripts/index-mcp-tools.py
```

This reads `cache/mcp-tools/tools.json` and produces `cache/mcp-tools/tools.index`.

## Using the Cache

The index format is:

```
tool_name | description | line_start-line_end
```

**Workflow to look up a tool:**

1. **Search the index** for the tool name:
   ```
   grep "get_transaction_info" cache/mcp-tools/tools.index
   ```
   Result:
   ```
   get_transaction_info | Get comprehensive transaction information. | 2850-3140
   ```

2. **Read only that line range** from the cached JSON for full details:
   ```
   sed -n '2850,3140p' cache/mcp-tools/tools.json
   ```
   This gives you the complete tool definition: description, inputSchema (all parameters with types and descriptions), outputSchema, and annotations — without loading the entire ~4000-line file.

## Freshness Checking

Freshness is based on the MCP server version:

1. The `fetch-mcp-tools.sh` script calls `unlock_blockchain_analysis` (via REST: `GET /v1/unlock_blockchain_analysis`) to get the `data.version` field.
2. It compares this with the `mcp_server_version` stored in `cache/mcp-tools/version.json`.
3. If versions differ, the cache is re-downloaded and re-indexed.

```json
{
  "mcp_server_version": "0.14.0",
  "tools_count": 16,
  "fetched_at": "2026-02-18T12:00:00Z"
}
```

## Cache Directory Structure

```
cache/mcp-tools/
├── version.json    # Server version and fetch timestamp
├── tools.json      # Pretty-printed full tools list (~4000 lines)
└── tools.index     # Grep-friendly: tool_name | description | line_range
```
