# MCP Tool Duplicate Removal Specification

## 1. Purpose

Defines the required changes to remove API endpoints from the topic API files and the master index that completely duplicate dedicated MCP Server tools. When an endpoint's data need is fully served by a dedicated MCP tool — which returns enriched, LLM-friendly responses — keeping that endpoint in the API reference files is counterproductive: it may lead agents to use `direct_api_call` for queries better served by the dedicated tool. This specification closes that gap by removing three such duplicate entries.

## 2. When to Apply

Apply these changes (manually or via an AI agent) as the **final step** in the API file composition pipeline — after `api-file-generator.py`, `mcp-unlock-patch.py`, and the RPC patch have all been applied. This ensures that any duplicate endpoint introduced or reintroduced by earlier steps is caught and removed.

If `api-file-generator.py` is re-run, re-apply the entire pipeline including this step last.

The complete workflow that produces a fully documented API reference:

```
swagger-main-indexer.py    → produces .build/swaggers/main-indexer/endpoints_map.json
swagger-stats-indexer.py   → produces .build/swaggers/stats-service/endpoints_map.json
api-file-generator.py      → creates/overwrites all topic api files AND recreates blockscout-api-index.md
mcp-unlock-patch.py        → patches MCP-sourced endpoints into topic files and index
[apply rpc-api-patch-spec] → patches JSON-RPC endpoints into topic files and index
[apply this spec]          → removes endpoints that duplicate dedicated MCP tools
```

## 3. Endpoints to Remove

Three endpoints duplicate dedicated MCP Server tools and must be removed from both their topic API files and the master index.

| MCP Tool | Duplicated Endpoint Path | Topic File |
|---|---|---|
| `get_address_info` | `/api/v2/addresses/{address_hash_param}` | `blockscout-analysis/references/blockscout-api/addresses.md` |
| `get_block_info` | `/api/v2/blocks/{block_hash_or_number_param}` | `blockscout-analysis/references/blockscout-api/blocks.md` |
| `get_transaction_info` | `/api/v2/transactions/{transaction_hash_param}` | `blockscout-analysis/references/blockscout-api/transactions.md` |

For each row, remove the complete H4 endpoint entry identified by the heading `#### GET <endpoint_path>` — the heading itself, its description, and the parameter table — from the corresponding topic file.

## 4. Removal Scope in Topic Files

An H4 endpoint entry spans from the `####` heading line to the line immediately before the next `####` heading or the next `###`/`##` heading or end of file — whichever comes first. Remove the entire span, including any trailing blank lines that separated it from the next entry (but do not remove the blank line that precedes the next entry's heading if one exists).

After removal, the remaining entries in the section must remain contiguous with a single blank line between each H4 entry, consistent with the existing file format.

## 5. Master Index Updates

After the topic files are updated, remove the corresponding line items from the master index `blockscout-analysis/references/blockscout-api-index.md`. For each endpoint in the table above, remove the line beginning with `` - `<endpoint_path>` `` from the matching section (`## [Blocks]`, `## [Transactions]`, or `## [Addresses]`).

After removal, no blank lines should be left between adjacent list items within a section.

## 6. Idempotency and Coordination with `api-file-generator.py`

Before removing any entry, check whether it is present:

- **In topic files:** scan for a line matching `#### GET <endpoint_path>` — if not found, skip that entry silently.
- **In the index:** scan for a line beginning with `` - `<endpoint_path>` `` — if not found, skip that index entry silently.

If all entries are already absent, the entire step is a no-op.

`api-file-generator.py` recreates all topic files and the index from scratch on every run, reintroducing the duplicate entries from swagger data. This spec must therefore be re-applied after every run of `api-file-generator.py`.

## 7. Verification

After applying all changes, verify:

1. `references/blockscout-api/addresses.md` does **not** contain `#### GET /api/v2/addresses/{address_hash_param}`.
2. `references/blockscout-api/blocks.md` does **not** contain `#### GET /api/v2/blocks/{block_hash_or_number_param}`.
3. `references/blockscout-api/transactions.md` does **not** contain `#### GET /api/v2/transactions/{transaction_hash_param}`.
4. `references/blockscout-api-index.md` Addresses section does **not** contain a line item for `/api/v2/addresses/{address_hash_param}`.
5. `references/blockscout-api-index.md` Blocks section does **not** contain a line item for `/api/v2/blocks/{block_hash_or_number_param}`.
6. `references/blockscout-api-index.md` Transactions section does **not** contain a line item for `/api/v2/transactions/{transaction_hash_param}`.
7. Re-applying the spec a second time produces no changes (idempotency).
8. All remaining entries in the affected topic files and index sections are still correctly formatted and contiguous.
