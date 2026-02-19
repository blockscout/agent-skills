# Analysis Workflow

Follow these phases when conducting a blockchain analysis task. The workflow is iterative — you may revisit earlier phases as new information emerges.

## Phase 1: Identify the Target Chain

Determine which blockchain the user is asking about from the context of their query.

- **Default**: chain ID `1` (Ethereum Mainnet) when the query does not specify a chain or clearly refers to Ethereum.
- **Validate**: Use `get_chains_list` (MCP) or the [Chainscout API](supporting-services.md#chainscout) to confirm the chain ID.
- **Explorer URL**: If you need the Blockscout explorer URL for a chain, call Chainscout directly — `get_chains_list` does not return URLs.

## Phase 2: Choose the Execution Strategy

Evaluate the task against the [execution strategy matrix](execution-strategies.md) and the data source priority (MCP → PRO API → Services).

**Select both the data source and execution method before making any data-fetching calls.**

Key questions:
- Can the answer be obtained in 1–3 tool calls? → Direct tool calls
- Does the task involve loops, date ranges, or aggregation? → Script
- Is semantic understanding needed? → LLM reasoning
- Is the data volume large? → Script against PRO API (50 items/page)

The choice may be revised in Phase 4 if endpoint research reveals constraints.

## Phase 3: Ensure Tooling Availability

### MCP Tools

If your strategy involves native MCP tool calls:

1. Check if Blockscout MCP tools are available in your environment.
2. If not, instruct the user to configure the MCP server (`https://mcp.blockscout.com/mcp`) — or install/enable it automatically if possible.
3. If MCP cannot be configured, use the REST API via HTTP or the [MCP tools cache](mcp-tools-cache-guide.md).

### PRO API

If your strategy involves the PRO API:

1. Check if `$BLOCKSCOUT_API_KEY` is set in the environment.
2. If not, instruct the user to obtain a key from the [Blockscout Development Portal](https://dev.blockscout.com) and set it as `$BLOCKSCOUT_API_KEY`. See [PRO API docs](pro-api.md#authentication).

## Phase 4: Discover and Disambiguate Tools/Endpoints

### 4a. Inventory Candidates

For each data need in your task, identify candidate tools and endpoints across all accessible API surfaces (MCP tools, PRO REST, JSON RPC, ETH RPC, supporting services).

### 4b. Resolve Overlap

When multiple candidates serve the same data need, consult the [tool equivalence groups](tool-equivalence-groups.md). Select the highest-priority tool that is available and covers the required fields. **Do not call redundant tools** on other API surfaces for the same data.

### 4c. Discover Additional Endpoints

When the task requires endpoints beyond what MCP tools or known endpoints cover:

1. **Check swagger cache freshness** — run `scripts/fetch-swagger.sh` for the relevant service(s) if not cached or stale.
2. **Build/update the index** — run `scripts/index-swagger.py --batch`.
3. **Search the index** — grep for path, method, or summary keywords. See [Swagger Cache Guide](swagger-cache-guide.md#using-the-index).
4. **Read the endpoint declaration** — use the line range from the index to read only the relevant section of the swagger file.

## Phase 5: Plan the Actions

Produce a concrete action plan before execution:

- **Script-based**: Outline which endpoints the script will call, how it handles pagination, what filtering/aggregation it performs, expected output format.
- **Direct tool calls**: List the sequence of calls and what information each provides.
- **Hybrid**: Specify which parts are tool calls and which are scripted.
- **LLM reasoning**: Identify which data must be retrieved first and what analysis follows.

## Phase 6: Execute

Carry out the plan:

1. **Make tool calls** or **write and run ad-hoc scripts** (or both).
2. Ad-hoc scripts go in `artifacts/` — resolve dependencies before writing, prefer existing host tools.
3. Scripts querying any REST or JSON RPC endpoint (PRO API, MCP REST, BENS, Metadata, Multichain Aggregator, Stats, Chainscout) must apply **response transformation** — extract relevant fields, flatten nested structures, format for LLM consumption.
4. **Interpret results** in the context of the user's original question rather than presenting raw output.

## Iteration

The workflow is not purely linear:

- Phase 4 may reveal that a different data source or strategy is better → revisit Phase 2.
- Phase 6 results may uncover new data needs → re-enter Phase 4.
- Always align back with the user's original question.
