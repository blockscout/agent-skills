# Blockscout Analysis Skill — Specification

## Purpose

Create a modular AI agent skill for two equally important goals: (1) **blockchain activity analysis** using the Blockscout MCP Server, and (2) **building scripts, tools, and applications** that query blockchain data through the Blockscout MCP Server (native MCP tools and REST API). The skill must guide agents in selecting the right execution strategy — whether to make direct MCP tool calls, write and run a script calling the MCP REST API for deterministic multi-step flows, or use a combination of both.

## Infrastructure Components

### 1. Blockscout MCP Server

- **MCP endpoint**: `https://mcp.blockscout.com/mcp` (native MCP protocol)
- **REST API**: `https://mcp.blockscout.com/v1/{tool_name}?params` (HTTP GET)
- **Multichain**: The server is multichain; almost all tools accept a `chain_id` parameter to target a specific chain (use `get_chains_list` to discover supported chains).
- **16 tools**: unlock_blockchain_analysis, get_chains_list, get_address_info, get_address_by_ens_name, get_tokens_by_address, nft_tokens_by_address, get_transactions_by_address, get_token_transfers_by_address, get_block_info, get_block_number, get_transaction_info, get_contract_abi, inspect_contract_code, read_contract, lookup_token_by_symbol, direct_api_call
- **Responses**: LLM-friendly (pre-filtered, enriched), except for `direct_api_call`, which proxies raw Blockscout API responses.
- **`direct_api_call` response size limit**: The MCP server enforces a default response size limit (100,000 characters) on `direct_api_call` responses. When exceeded, a 413 error is returned. Native MCP calls strictly enforce this limit. REST API callers can bypass it by including the `X-Blockscout-Allow-Large-Response: true` HTTP header — but scripts using this bypass must still apply [response transformation](#response-transformation) before passing output to the LLM.
- **Response format equivalence**: Native MCP tool calls and REST API calls to the same tool return identical JSON response structures. When writing scripts that will call the REST API, the agent can use native MCP tool calls to probe and validate the expected response shape. This is especially useful when the agent's runtime environment cannot reach the REST API directly (e.g., network restrictions) but the script will run in an unrestricted environment.
- **Advantage**: Simplified cursor-based pagination more suitable for LLMs and scripts, and guidance in the responses to suggest the next step.

#### Mandatory `unlock_blockchain_analysis` (MCP prerequisite)

- **Rule**: Before calling any other Blockscout MCP tool, the agent must call `unlock_blockchain_analysis` first. This is mandatory for all MCP clients that do not reliably read the server’s tool instructions (e.g., many clients skip or ignore server-provided descriptions).
- **Exception**: When the agent runs in **Claude Code**, this call is optional. Claude Code reads MCP server instructions correctly; `unlock_blockchain_analysis` exists as a workaround for clients that do not.
- **Skill behavior**: The skill must instruct the agent to call `unlock_blockchain_analysis` once per session (or before the first MCP tool use) whenever the agent decides to use Blockscout MCP tools, unless the environment is known to be Claude Code.

#### MCP tool documentation and discovery

- **When MCP is configured**: If the Blockscout MCP server is configured (e.g., `https://mcp.blockscout.com/mcp`), tool names and descriptions are already supplied in the agent’s context by the MCP client; the agent may still use the API reference for parameter details and examples.
- **When MCP is not configured**: If the MCP server is not configured, the agent can discover tools and their schemas via the REST list endpoint: `GET https://mcp.blockscout.com/v1/tools`. The skill must instruct the agent to use this URL when tool descriptions are otherwise unavailable.

#### Pagination (MCP): opaque cursor and simplified model

MCP pagination is **simplified** compared to the raw Blockscout API so that agents and scripts don’t have to handle endpoint-specific keys.

Paginated MCP tools expose a single optional `cursor` parameter. To get the next page, the agent calls the same tool again with the same inputs and sets `cursor` to the value from the response (e.g., from `pagination.next_call.params.cursor`). There are no endpoint-specific query parameters or key names to remember—instead, a Base64URL-encoded cursor is passed.

### 2. Supporting Services

#### Chainscout

This is the Blockscout chain registry. It is a separate service from any individual Blockscout instance and is accessed via direct HTTP requests (e.g., WebFetch or curl)—**not** via the `direct_api_call` MCP tool, which proxies to a specific Blockscout instance.

The primary purpose of Chainscout access is to resolve a chain ID to its Blockscout explorer URL. Chain IDs must first be obtained from the `get_chains_list` MCP tool, which provides the authoritative list of supported chains with their IDs.

## Skill Preparation Phase

There are separate specifications that define preparation to produce API reference files. These reference files become part of the skill documentation (in `references`).

### Blockscout API

The specification is [`blockscout-api-composition-spec.md`](blockscout-api-composition-spec.md). It describes the pipeline to produce comprehensive API reference files in `references/blockscout-api/` and the index file in `references/blockscout-api-index.md`. The agent consults these when it needs to discover endpoints for use with `direct_api_call`.

### Chainscout

The specification is [`chainscout-api-spec.md`](chainscout-api-spec.md). It describes the preparation to produce the API reference file in `references/chainscout-api.md`. The agent consults it when it needs to discover the Blockscout instance URL for a specific chain.

### OpenAI Codex Agent Metadata

The specification is [`openai-yaml-spec.md`](openai-yaml-spec.md). It describes the `agents/openai.yaml` file that declares UI metadata and MCP server dependencies for the OpenAI Codex platform. This file enables Codex to automatically configure the Blockscout MCP server when the skill is installed.

### Claude Code Marketplace Plugin

The specification is [`marketplace-plugin-spec.md`](marketplace-plugin-spec.md). It describes the plugin entry in the Claude Code marketplace manifest (`.claude-plugin/marketplace.json`) that declares skill metadata and the Blockscout MCP server dependency. This entry enables Claude Code users to discover and install the skill via `/plugin marketplace add` and automatically configures the MCP server.

## Design Requirements

### Conformance to Agent Skills standard

The skill must conform to the [Agent Skills specification](https://agentskills.io/specification.md). The specification defines the directory structure, `SKILL.md` format (frontmatter and body), optional directories (`scripts/`, `references/`, `assets/`), file referencing conventions, and — critically — the **progressive disclosure** model that governs how agents load skill content:

1. **Metadata** (~100 tokens): `name` and `description` are loaded at startup for all skills.
2. **Instructions** (< 5000 tokens recommended): The full `SKILL.md` body is loaded when the skill is activated.
3. **Resources** (as needed): Files in `references/`, `scripts/`, and `assets/` are loaded only when required — with no guarantee they will be loaded at all.

### SKILL.md self-sufficiency

Because the progressive disclosure model guarantees that only `SKILL.md` is loaded at activation — while reference files may or may not be loaded during execution — `SKILL.md` must be **self-sufficient for correct agent behavior**:

- All instructions the agent needs to follow the right process — workflow phases, decision framework, security rules, disclaimers, response handling rules — must live in `SKILL.md` itself.
- An agent that reads only `SKILL.md` and never opens a reference file must still behave correctly.
- Reference files in `references/` are for **lookup data** the agent consults during task execution (e.g., API endpoint parameters, chain registry details). `SKILL.md` must give the agent a clear reason and trigger to read each reference file, so the agent understands why and when to load it.
- Content must only be moved from `SKILL.md` to `references/` when it is lookup or reference data by nature — not to meet the line budget by offloading behavioral instructions.

### Modular structure

The skill must use a hub-and-spoke pattern:

- `SKILL.md` — concise entry point with decision table (execution strategy) and quick references
- Supporting docs in `references/` — loaded on demand by the agent, one per topic
- API reference files in `references/` — produced during the [skill preparation phase](#skill-preparation-phase)
- **Ad-hoc script dependencies**: The skill must instruct the agent to write ad-hoc scripts using only the standard library of the chosen language and tools already available on the host. The agent must not install packages, create virtual environments, or add package manager files. When a task appears to require a third-party library (e.g., ABI encoding, hashing, address checksumming), the agent must use the corresponding MCP tool instead (e.g., `read_contract`, `get_contract_abi`). If after exhausting standard-library and MCP tool options a third-party package is still genuinely required, the agent may install it, but must clearly state in its output what was installed and why no alternative was viable.

### SKILL.md line budget

Per the [Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), the `SKILL.md` body (excluding frontmatter) should be kept **under 500 lines**. The modular hub-and-spoke structure supports this: if during skill preparation any content would push `SKILL.md` beyond this budget, **lookup and reference data** (not behavioral instructions) may be moved to a separate file in `references/` and referenced from `SKILL.md`, subject to the [self-sufficiency rule](#skillmd-self-sufficiency). The exact split is determined during the skill preparation process based on the content produced.

### README in skill directory

The skill must include a **README file in the skill directory** (e.g., `README.md` at the root of the skill folder). This file is the human-facing overview of the skill and must cover:

- **The skill’s goal** — what the skill is for and what outcomes it enables
- **Key ideas of the skill** — core concepts, decision framework (data source and execution strategy), and how the skill guides the agent
- **Directory structure** — a concise description or diagram of the skill directory layout (e.g., `SKILL.md`, `references/`, and how they are used)

The README must not duplicate long reference material that belongs in `SKILL.md` or `references/`; it should orient the reader and point to those resources where appropriate.

### SKILL.md frontmatter

The `SKILL.md` file must include YAML frontmatter as required by the [Agent Skills specification](https://agentskills.io/specification.md):

```yaml
---
name: blockscout-analysis
description: "MANDATORY — invoke this skill BEFORE making any Blockscout MCP tool calls or writing any blockchain data scripts, even when the Blockscout MCP server is already configured. Provides architectural rules, execution-strategy decisions, MCP REST API conventions for scripts, endpoint reference files, response transformation requirements, and output conventions that are not available from MCP tool descriptions alone. Use when the user asks about on-chain data, blockchain analysis, wallet balances, token transfers, contract interactions, on-chain metrics, wants to use the Blockscout API, or needs to build software that retrieves blockchain data via Blockscout. Covers all EVM chains."
license: MIT
metadata:
  author: blockscout.com
  version: "<current version>"
  github: https://www.github.com/blockscout/agent-skills
  support: https://discord.gg/blockscout
---
```

- **`name`**: Must match the skill directory name (`blockscout-analysis`).
- **`description`**: Must fully reflect the skill's [Purpose](#purpose) — covering all goals the skill serves — and describe when to use it, with specific keywords that help agents identify relevant tasks. The description is the agent's primary signal for skill activation; any purpose not represented in the description may fail to trigger the skill. The description must also include a mandatory invocation directive instructing the agent to invoke the skill BEFORE making any Blockscout MCP tool calls or writing blockchain data scripts, even when the MCP server is already configured, and must explain that the skill provides architectural rules, execution-strategy decisions, and conventions not available from MCP tool descriptions alone.
  - **Single-line format**: The `description` value must be a single-line YAML string (quoted if it contains special characters). While the [Agent Skills specification](https://agentskills.io/specification.md) permits multi-line YAML scalars, some skill-hosting platforms (notably OpenClaw) use frontmatter parsers that only support single-line keys. Using a single line ensures cross-platform compatibility at no cost to platforms that do support multi-line values.
- **`license`**: MIT.
- **`metadata.version`**: Skill version; must be updated on each release so that changes can be identified easily.
- **`metadata.author`**, **`metadata.github`**, **`metadata.support`**: Publisher and support information.

### MCP access strategy

- Scripts use the MCP REST API (`mcp.blockscout.com/v1/`) via HTTP
- **User-Agent requirement**: Every HTTP request to the MCP REST API must include the header `User-Agent: Blockscout-SkillGuidedScript/<skill-version>` (where `<skill-version>` is the value from `SKILL.md` frontmatter `metadata.version`). The CDN in front of the MCP REST API rejects requests without a recognized User-Agent with HTTP 403. Because standard-library HTTP clients (e.g., Python `urllib`) send a generic User-Agent that is blocked, the skill must explicitly instruct the agent to set this header in every script. This avoids the recurring failure pattern where the agent writes a script, gets a 403, and then installs a third-party HTTP library to work around it.
- For interactive tasks better suited to native MCP tool calls (contract analysis, `read_contract`, iterative investigation), the skill instructs the agent to ensure the native MCP server is available (see [MCP server availability](#mcp-server-availability) below)
- The choice between script-based HTTP calls and direct MCP tool calls is governed by the execution strategy (see [Execution strategy](#execution-strategy) below)

### MCP server availability

- When the skill leads the agent to use Blockscout MCP tools, the skill must instruct the agent to **ensure the Blockscout MCP server is available** before relying on MCP tool calls. The agent should either provide the user with instructions to install or enable the MCP server, or, if the agent has the ability, install or enable the server automatically.
- The specification is **agent-agnostic**: The skill does not prescribe environment-specific steps (e.g., which config file or UI to use). It motivates the agent to achieve availability, assuming the agent knows how to install or enable an MCP server in its host environment.

### Do not duplicate `unlock_blockchain_analysis` content in the skill

- The output of `unlock_blockchain_analysis` is maintained by the MCP server and may be extended or changed over time (e.g., new endpoints, chain families, or usage notes).
- **Skill docs (`SKILL.md` and files in `references/`) must not copy or paraphrase that content.** They may only:
  - Require calling `unlock_blockchain_analysis` first (per the rule above), and
  - Point to the canonical source—the tool itself.
- This keeps the skill stable when the server’s instructions change and avoids conflicting or outdated copies.

### Decision framework

The skill must guide the agent through selecting **how to execute** the query. The MCP Server is the sole runtime data source; the decision is about execution strategy.

#### Data source priority

All data access goes through the Blockscout MCP Server:

- **Dedicated MCP tools** first (LLM-friendly, enriched, no auth) — prefer these when a tool directly answers the data need
- **`direct_api_call`** for endpoints not covered by dedicated MCP tools — consult the `references/blockscout-api-index.md` API index file to discover available endpoints
- **Chainscout** (`chains.blockscout.com/api`) only for resolving a chain ID to its Blockscout instance URL

#### Execution strategy

Choose the execution method based on task complexity, determinism, and whether semantic reasoning is required:

| Signal | Strategy | When to use |
|--------|----------|-------------|
| Simple lookup, 1–3 calls, no post-processing | **Direct tool calls** (MCP tool or web fetch) | The answer is returned directly or nearly directly by an MCP tool. E.g., get a block number, resolve an ENS name, fetch address info. |
| Deterministic multi-step flow with loops, date ranges, aggregation, or conditional branching | **Script** (agent writes and executes a script calling MCP REST API via HTTP) | The logic is well-defined and would be inefficient or error-prone as a sequence of LLM-driven calls. E.g., iterate over months to compute APY changes, paginate through all token holders to count matches, scan transaction history with filtering. |
| Data retrieval is simple but output requires math, normalization, or filtering | **Hybrid** (tool call for retrieval + script for post-processing) | The API provides raw data that needs token-decimal normalization, USD conversion, sorting, deduplication, or threshold filtering. E.g., get token balances via MCP then normalize amounts and filter by value in a script. |
| Task requires semantic understanding, code analysis, or subjective judgment | **LLM reasoning over API results** (direct tool calls, agent analyzes) | The question cannot be answered by a deterministic algorithm—it needs interpretation of contract source code, verification of token authenticity, classification of transaction purpose, or tracing code flow. E.g., check if a contract has blacklisting functionality, determine if a token is official, categorize a transaction. |
| Large data volume with known filtering criteria | **Script with `direct_api_call`** (script handles pagination and filtering) | Need to process many pages of data with programmatic filters. Use `direct_api_call` via the MCP REST API to access paginated endpoints. |

**Combination patterns**: Many real-world queries require combining strategies. For example, a multi-chain token balance analysis might use direct tool calls to resolve an ENS name, then a script to iterate through chains and fetch/normalize balances, with the LLM providing final interpretation of which tokens are "stablecoins."

**Probe-then-script**: When the execution strategy is "Script" but the agent needs to understand response structures before writing the script, call the relevant MCP tools natively with representative parameters first. Use the observed response structure to write the script targeting the REST API. Do not fall back to third-party data sources (e.g., direct RPC endpoints, third-party libraries) when the MCP REST API covers the data need.

The skill's decision table in `SKILL.md` must present the execution strategy so the agent selects the appropriate method for each task.

#### Tool selection priority

When a data need can be fulfilled by either a dedicated MCP tool or `direct_api_call`, the agent must prefer the dedicated MCP tool (enriched, LLM-friendly responses). Choose `direct_api_call` instead when: (a) no dedicated tool covers the needed endpoint, or (b) the dedicated tool is known — from its description or schema — not to return a field required for the task. This selection is made upfront during Phase 4 (endpoint discovery), not after calling a dedicated tool and discovering a gap at runtime.

**No redundant calls**: Once a tool or endpoint is selected for a data need, the agent must not call alternative tools for the same data.

### Price data and financial disclaimer

Blockscout infrastructure may expose native coin or token prices in some responses (e.g., token holdings, market data). By its nature, these prices may not be up to date, may differ from actual market prices, and do not constitute historical price series.

- **No financial decisions on Blockscout prices alone**: The skill must instruct the agent **not** to make or suggest any financial advice or decisions based solely on prices returned by Blockscout.
- **Use of Blockscout prices**: The skill must instruct the agent to use prices returned by Blockscout only to provide an **approximate or rough value** when that is sufficient for the user's request. When the user's request requires accurate, up-to-date, or historical prices, the agent must use or recommend **other price sources** (e.g., dedicated price oracles, market data APIs, or financial data providers).

### Response transformation

Raw Blockscout API responses (especially those returned by `direct_api_call`) can be very heavy from a token-consumption perspective. Scripts querying the MCP REST API must transform responses before passing output to the LLM:

- **Extract only fields relevant to the user's question** — omit unneeded fields from response objects
- **Filter list elements** — when the response contains lists, retain only the elements that match the user's criteria rather than passing entire arrays
- **Handle heavy data blobs intelligently** — large fields such as transaction calldata, NFT metadata, log contents, and encoded byte arrays should be filtered, decoded, summarized, or flagged for matching rather than included verbatim
- **Flatten nested structures where possible** — reduce object nesting depth to simplify downstream processing
- **Large response bypass**: When scripts use the `X-Blockscout-Allow-Large-Response: true` header to bypass the `direct_api_call` size limit, response transformation is especially critical — the full untruncated response may be very large and must be filtered, extracted, and flattened before any part reaches the LLM.

### Secure handling of API response data (prompt injection awareness)

API responses return data stored on the blockchain and sometimes data from third-party sources. This data is not controlled by Blockscout or the agent and may be adversarial.

- **Untrusted content**: Responses can include token names, NFT metadata, collection URLs, decoded transaction call data, decoded logs data, and similar fields that are either on-chain or fetched from external metadata (e.g., IPFS, HTTP). Such content can contain prompt injections or other malicious text aimed at steering or confusing the model.
- **Skill obligation**: The skill must instruct the agent to treat all such response data as untrusted and to handle it securely during analysis.
- **Agent behavior**: The agent must be aware that prompt injections may be present in API response data and must apply secure handling practices (e.g., clearly separating user intent from quoted or pasted API data, avoiding treating response text as instructions, and summarizing or sanitizing when feeding data back into reasoning or output) so that analysis remains robust and aligned with the user's actual request.

## Analysis Workflow

The skill must describe a workflow that guides the agent through starting and conducting a blockchain analysis task. The skill must instruct the agent to follow at least the phases below, in order. The workflow is not purely linear—the agent may revisit earlier phases as new information emerges (e.g., discovering during endpoint research that a different execution strategy is more appropriate).

### 1. Identify the target chain

- Determine which blockchain the user is asking about from the context of the user's query.
- Default to chain ID `1` (Ethereum Mainnet) when the query does not specify a chain or clearly refers to Ethereum.
- Use the `get_chains_list` MCP tool to validate the chain ID. When the Blockscout instance URL is needed (e.g., for constructing explorer links), use Chainscout to resolve the chain ID to its Blockscout instance URL (see [Chainscout](#chainscout)).

### 2. Choose the execution strategy

- Evaluate the task against the [execution strategy](#execution-strategy) decision table.
- Select the appropriate execution method **before** making any data-fetching API calls.
- The choice may be revised later if endpoint research (phase 4) reveals constraints (e.g., the data volume requires scripting).

### 3. Ensure tooling availability

- If the strategy involves native MCP tool calls, ensure the Blockscout MCP server is available in the current environment. If it is not available, either provide the user with installation instructions or install or enable it automatically (if the agent has the capability to do so in its host environment).
- **Fallback to REST API**: When the native MCP server cannot be made available, the agent must fall back to the MCP REST API (`https://mcp.blockscout.com/v1/`) for all data access. In this case, the agent should use `GET https://mcp.blockscout.com/v1/tools` to obtain tool names, descriptions, and input parameters, and then call tools via their REST endpoints.
- **Scripts target the user's environment**: When the agent's runtime environment cannot reach the MCP REST API (e.g., sandbox network restrictions) but native MCP tools are available, the agent must still write scripts targeting the REST API — the script is intended to run in the user's environment, not the agent's sandbox. Use native MCP tool calls to validate response formats during script development (see [response format equivalence](#1-blockscout-mcp-server)).

### 4. Discover endpoints

For each data need identified in the task, determine whether a dedicated MCP tool can fulfill it. If not, discover the appropriate `direct_api_call` endpoint:

1. **Check dedicated MCP tools**: Review the available MCP tools. If a dedicated tool answers the data need, use it (per [tool selection priority](#tool-selection-priority)).
2. **Discover `direct_api_call` endpoints** (two-step process): When the task requires endpoints beyond what dedicated MCP tools cover, the agent must follow this sequence:
   1. **Read the index file** (`references/blockscout-api-index.md`): Locate the endpoint by name or category to identify which API reference file contains its full documentation.
   2. **Read the corresponding reference file** (`references/blockscout-api/{filename}.md`): Inspect the endpoint's parameters, types, and descriptions for use with `direct_api_call`.

   The agent must not skip the index step—it is the only reliable way to find which reference file documents a given endpoint.

### 5. Plan the actions

- Based on the chosen strategy and discovered endpoints, produce a concrete action plan before execution.
- For **script-based** strategies: outline what the script will do—which endpoints it will call, how it handles pagination, what filtering or aggregation it performs, and the expected output format.
- For **direct tool calls**: list the sequence of tool calls and what information each call provides.
- For **hybrid** approaches: specify which parts are handled by tool calls and which by a script.
- For **LLM reasoning** strategies: identify which data must be retrieved first and what kind of analysis the agent will perform on the results.

### 6. Execute

- Carry out the plan: make tool calls, write and run ad-hoc scripts, or both.
- Ad-hoc scripts must follow the dependency requirements from [Modular structure](#modular-structure): standard library and host-available tools only, with MCP tools as the escape hatch before considering any package installation.
- Scripts that call the MCP REST API (especially `direct_api_call`) must apply [response transformation](#response-transformation)—extract relevant fields, flatten nested structures, format output for token-efficient LLM consumption.
- After execution, the agent should interpret results in the context of the user's original question rather than simply presenting raw output.

## Implementation Notes

- The `direct_api_call` MCP tool is a proxy to Blockscout API endpoints and does not provide optimization or filtering.
- Some MCP tools automatically enrich responses by performing additional API calls internally (e.g., address info enriched with metadata and first transaction timestamp), so dedicated MCP tools can reduce the total number of calls compared to using `direct_api_call`.
- The MCP server simplifies complex cursor logic for paginated endpoints, making it more suitable for LLMs.
- MCP pagination uses ~10 items per page; enriched responses from dedicated tools may save follow-up queries.
- The `references/blockscout-api-index.md` and `references/blockscout-api/{filename}.md` files produced during the [skill preparation phase](#skill-preparation-phase) serve as the endpoint reference for `direct_api_call` usage—the agent consults them to discover endpoint paths and parameters.
