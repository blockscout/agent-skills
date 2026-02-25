# Blockscout API Endpoint Files — Composition Specification

## Purpose

This specification covers the composition of the list of API endpoints that agents can use to request blockchain data through the `direct_api_call` tool of the Blockscout MCP server. The result is a set of markdown API reference files that agents load on demand to discover which endpoints are available.

## Pipeline

The API files are produced through a sequential pipeline. Each step is defined in a dedicated specification that describes the approach for that step:

1. **Swagger acquisition**
   - [`swagger-main-indexer-spec.md`](swagger-main-indexer-spec.md) — approach to obtain swagger files describing the endpoints supported by individual Blockscout backend instances.
   - [`swagger-stats-indexer-spec.md`](swagger-stats-indexer-spec.md) — approach to obtain swagger files describing the endpoints of the Blockscout Stats service.

2. **Initial file generation**
   [`api-file-generator-spec.md`](api-file-generator-spec.md) — approach to build the initial set of markdown API files from the swagger files produced in step 1.

3. **Patch with MCP-mentioned endpoints**
   [`mcp-unlock-patch-spec.md`](mcp-unlock-patch-spec.md) — approach to extend the API files with the endpoints returned by the `unlock_blockchain_analysis` MCP tool that are absent from the swagger files.

4. **Patch with JSON-RPC endpoints**
   [`rpc-api-patch-spec.md`](rpc-api-patch-spec.md) — approach to extend the API files with two endpoints provided by Blockscout instances but not defined in the swagger files.

5. **Remove MCP tool duplicates**
   [`mcp-duplicate-removal-spec.md`](mcp-duplicate-removal-spec.md) — approach to remove API endpoints that completely duplicate dedicated MCP Server tools, enforcing the tool selection priority principle.

## Output Format

All produced API files follow the format defined in [`api-format-spec.md`](api-format-spec.md).
