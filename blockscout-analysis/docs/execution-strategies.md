# Execution Strategies

Choose the execution method based on task complexity, determinism, and whether semantic reasoning is required.

## Strategy Matrix

| Signal | Strategy | When to Use | Example |
|--------|----------|-------------|---------|
| Simple lookup, 1–3 calls, no post-processing | **Direct tool calls** | Answer returned directly by an API endpoint | Get a block number, resolve an ENS name, fetch a transaction |
| Deterministic multi-step flow with loops, date ranges, aggregation | **Script** | Logic is well-defined; inefficient as sequential LLM calls | Iterate over months to compute APY, paginate all token holders, scan tx history with filters |
| Simple retrieval + math, normalization, or filtering | **Hybrid** (tool call + script) | API provides raw data needing computation | Get token balances via API, then normalize decimals and filter by value in a script |
| Semantic understanding, code analysis, subjective judgment | **LLM reasoning over results** | Cannot be answered by a deterministic algorithm | Check if a contract has blacklisting, determine if a token is official, classify a transaction |
| Large data volume with known filtering criteria | **Script against PRO API** | 50-item pages are 5x more efficient than MCP's 10 | Process many pages of data with programmatic filters |

## Combination Patterns

Real-world queries often require combining strategies:

- **Multi-chain token balance analysis**: Direct tool call to resolve ENS name → script to iterate chains and fetch/normalize balances → LLM reasoning to classify which tokens are stablecoins.
- **Contract security audit**: Direct tool calls to fetch ABI and source → LLM reasoning to analyze code for vulnerabilities → script to check specific function selectors across transaction history.
- **Historical DeFi activity**: Script against PRO API to paginate through months of transactions → hybrid post-processing to normalize token amounts → LLM interpretation of the activity pattern.

## Script Guidelines

When writing ad-hoc scripts for a task:

1. **Store in `artifacts/`** — never in `scripts/` (which is reserved for deterministic tooling).
2. **Resolve dependencies before writing** — check what's available on the host.
3. **Prefer existing tools** — use libraries, packages, or CLI tools already installed rather than suggesting new installs. Suggest installation only when no alternative exists.
4. **Apply response transformation** — extract relevant fields, flatten nested structures, format output for token-efficient LLM consumption.
5. **Use MCP REST API** (`https://mcp.blockscout.com/v1/`) for HTTP calls from scripts when possible — no auth required, simplified pagination.
6. **Use PRO API** when MCP lacks the endpoint or when 50-item pages are needed for bulk retrieval.

## MCP REST vs PRO API in Scripts

| Factor | MCP REST API | PRO API |
|--------|-------------|---------|
| Auth | None required | `$BLOCKSCOUT_API_KEY` required |
| Pagination | Opaque cursor, ~10 items/page | Keyset, ~50 items/page |
| Responses | Enriched, LLM-friendly | Raw JSON, verbose |
| Coverage | 16 tools + `direct_api_call` | Full Blockscout endpoint set |
| Best for | Simple queries, enriched data | Bulk retrieval, full coverage |

**Rule of thumb**: Start with MCP REST. Switch to PRO API when you need endpoints MCP doesn't cover or when page size matters for performance.

## When to Revise the Strategy

The workflow is iterative. Revise your strategy when:

- Endpoint research reveals that a needed field is only available on a different API surface.
- Data volume turns out larger than expected, making script-based pagination more efficient.
- The task requires semantic analysis that wasn't apparent initially.
- A simpler approach becomes apparent after seeing the first API response.
