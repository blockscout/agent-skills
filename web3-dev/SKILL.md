---
name: web3-dev
description: "Build web3 applications, scripts, CLIs, bots, mobile apps, and desktop apps that need blockchain data via the Blockscout PRO API — a single HTTP API spanning 100+ EVM chains. Invoke this skill whenever the user wants to read blockchain data over HTTP (transactions, blocks, addresses, tokens, NFTs, logs, contract context, internal txs, account abstraction, etc.) and is building software that calls an API directly. Trigger on direct mentions of `Blockscout PRO API`, `pro-api`, `proapi_`, `Blockscout API`, `block explorer API`, `api.blockscout.com`, or on broader phrasing like \"build a web3 app\", \"index/query on-chain data\", \"wallet history\", \"NFT inventory\", \"transaction logs across chains\", \"how much does the Blockscout API cost\", \"chain IDs supported by Blockscout\". Use this skill for direct HTTP integrations; the sibling `blockscout-analysis` skill covers the Blockscout MCP Server."
license: MIT
metadata: {"author":"blockscout.com","version":"0.1.0","github":"https://www.github.com/blockscout/agent-skills","support":"https://discord.gg/blockscout"}
---

# Web3 Dev — Blockscout PRO API

This skill teaches the agent how to build software (apps, scripts, CLIs, bots, mobile/desktop clients) that reads blockchain data through the **Blockscout PRO API** — a single HTTP API covering 100+ EVM chains (94+ L2s and scaling projects). One API key works on every supported chain; switch chains by changing the `chain_id` path parameter on the call.

The PRO API returns explorer-enriched data: indexed, decoded, and structured — token metadata, proxy implementations, internal transactions, contract context, and so on. Use it for dApps and wallets, AI agents and bots, analytics platforms, and operational tooling.

For data the explorer has **not** pre-indexed — most importantly **live or historical contract state at a specific block** (e.g. `balanceOf(addr)` against a token contract at block `N`, `totalSupply()` at a past block, any view-function call, contract storage reads) — the PRO API also exposes `eth_call` through its JSON-RPC gateway. See [Reading contract state](#reading-contract-state--eth_call-via-the-json-rpc-gateway). The same Bearer-token auth covers both surfaces; you do **not** need a separate RPC endpoint for historical contract reads.

The bundled files in `references/` are the **single source of truth** for which endpoints exist and how to call them:

| File | Purpose |
|------|---------|
| `references/pro-api-index.md` | One-line summary of every endpoint, grouped by OpenAPI tag. Always start here. |
| `references/pro-api.json` | Full OpenAPI v3 specification (~24,000 lines). **Do not read whole** — query it with `oastools`. |

Do not classify endpoints into your own "families" or steer the user toward a subset. Every endpoint listed in the index is callable, and every endpoint uses the same authentication scheme described below.

## API key — mandatory pre-flight

A PRO API key is **required** for every PRO API call. Run the following pre-flight before issuing the first request in a session.

### Pre-flight check (in this order)

1. Look for a key in the agent's environment, in this order of preference:
   - An exported environment variable, default name `BLOCKSCOUT_PRO_API_KEY`.
   - A project-local secrets file appropriate to the artefact: `.env` for Node/Python apps, `.env.local` for Next.js, `local.properties` for Android, `*.xcconfig` or Keychain for iOS, `secrets.toml` for some Python frameworks, a CI secret store, etc.
   - A key the user previously placed in the agent's stored memory or persistent profile (e.g. a saved-secrets/preferences store the agent has access to across sessions).

   **Do not ask the user to paste the key into the conversation.** A pasted value lands in the LLM transcript and can leak via provider logs, exported chats, screenshots, or training corpora. Steer the user to `export` or a gitignored `.env` instead (see step 5).
2. **Never invent or guess a key.** If the agent has no record of one, do not fabricate one or pull one from training data.
3. **Confirm before reusing a key from stored memory or a prior session.** A key the user has intentionally saved is a legitimate source — but reusing it silently is not. Before issuing the first request with such a key, show the user *which* stored key the agent intends to use (e.g. "the key saved as `BLOCKSCOUT_PRO_API_KEY` in your agent profile, last 4 chars `…abcd`") and ask them to confirm. Never echo the full key value back. Keys found in the current session's environment or project secrets file do not need this extra confirmation step — they are by construction intentional for the current task.
4. If a key is found (and confirmed where required by step 3), validate loosely — it should start with `proapi_` — and proceed.
5. If no key is found anywhere, **stop and hand control back to the user immediately.** This is a hard interrupt, not a soft warning. Specifically, the agent must not:
   - write or sketch code that calls (or will eventually call) the PRO API;
   - "prepare a script for when the key arrives" or do any preparatory endpoint inspection / parameter walk;
   - propose alternative data sources or an external RPC URL as a stopgap;
   - narrate hypothetical next steps as if the key situation were resolved.

   The reason this is a hard interrupt — not just discipline — is that **the agent needs the key for its own research and debug calls**, not only for the user's eventual code. Probing an endpoint to confirm its real response shape, validating a parameter combination by trying it, and debugging why a previous call returned unexpected data are all live PRO API calls the agent makes during planning and iteration. Without a key, the agent cannot do that exploratory work, which means it cannot reliably design the user's code in the first place. "Build the script now, run it later when the key arrives" therefore produces code that was never validated against the actual API.

   Send a brief message that (a) names the missing key, (b) points the user at **https://dev.blockscout.com** (free tier, no credit card), and (c) offers two paste-free paths: `export BLOCKSCOUT_PRO_API_KEY=proapi_…` in the current shell, or a gitignored `.env` in the project root. **Do not ask the user to paste the key into the conversation** — that puts the value in the LLM transcript. Then wait.

   - ❌ Wrong: *"No API key found in environment. Let me check the endpoint parameters and build the script — it'll use the Blockscout PRO API for token transfers (when a key is available)."*
   - ✅ Right: *"I couldn't find a Blockscout PRO API key. Generate one at https://dev.blockscout.com (free tier, no credit card), then either run `export BLOCKSCOUT_PRO_API_KEY=proapi_…` in this shell, or add it to a gitignored `.env` in the project root. The value won't appear in our conversation either way. Tell me when you're done."*

### On-boarding instructions when the key is missing

Deliver these steps, in order, when the user has no key:

1. Open the developer portal at **https://dev.blockscout.com** and create an account. The free tier does not require a credit card.
2. From the portal, generate an API key. The key is prefixed `proapi_…`. An account can hold up to 50 keys, and the portal shows a real-time usage dashboard.
3. **Recommend the most appropriate place to store the key** for the user's specific situation. Propose, do not impose — pick the option that is most secure *and* most convenient given what is being built. The right choice is case-by-case, not a fixed list. Examples of how to think about it:

   - **One-off interactive script** the user runs locally → an exported shell variable in the current session, or a shell-rc entry if they will reuse it.
   - **Node.js, Python, or Go application or CLI** → a project-local `.env` file loaded at startup, with `.env` added to `.gitignore`.
   - **Frontend, mobile, or desktop app where the binary ships to end users** → **never embed the key in the client**. Either route requests through a server-side proxy that holds the key, or have each end user supply their own key via the app's settings UI (stored in OS Keychain / Android Keystore / equivalent secure store).
   - **CI/CD pipeline** → the platform's encrypted secret store (GitHub Actions secrets, GitLab CI variables, etc.).
   - **Containerised deployment** → a secrets manager (AWS Secrets Manager, GCP Secret Manager, Vault, …) injected at runtime.

   When the deployment shape is ambiguous, **ask a clarifying question** before recommending a storage location. If the user asks to embed the key in committed code or in a client-shipped binary, flag that as insecure and propose an alternative.

4. Re-run the original request once the key is in place.

### Key handling rules

These rules apply for the rest of the session and for every code sample the skill produces:

- **Never log the key, never include it in committed code, never echo it back to the user once provided.**
- Always read the key indirectly at runtime — environment variable, secrets file, or secret manager. Do not hardcode it in scripts or examples; reference it by variable name only (e.g. `process.env.BLOCKSCOUT_PRO_API_KEY`, `os.environ["BLOCKSCOUT_PRO_API_KEY"]`).
- If a `.env` (or equivalent secrets file) is created or modified, ensure the file is git-ignored and warn the user if it is not.
- Treat `HTTP 401`/`403` responses as a signal that the key is invalid, missing, or revoked — stop, surface the failure to the user, and re-run the on-boarding flow above.
- If the user pastes a key into the conversation despite the advice not to, accept it for the current session, but warn them that the value is now in the transcript and recommend they rotate the key after the session and use `export`/`.env` next time.

## Base URL and URL construction

The base URL is **`https://api.blockscout.com`**. There is no API version prefix or other implicit path component — every operation path in the OpenAPI spec is **relative to this base**.

**Build the full URL by concatenating the base URL with the operation's path string taken verbatim from `references/pro-api-index.md`** (which is in turn taken verbatim from `references/pro-api.json`). After concatenation, substitute any `{templated}` segments (e.g. `{chain_id}`, `{transaction_hash_param}`, `{address_hash_param}`) with their actual values, then append query parameters from the operation's `parameters` schema.

Worked example. The index lists:

```
GET /{chain_id}/api/v2/blocks/{block_number_or_hash}
```

For chain `1` (Ethereum mainnet) and block `10000000`, the final URL is:

```
https://api.blockscout.com  +  /1/api/v2/blocks/10000000
=  https://api.blockscout.com/1/api/v2/blocks/10000000
```

Strict rules for path construction — these prevent the most common integration bugs:

- **Take the path verbatim from the index.** Do not invent, prefix, rewrite, or reorder it. Specifically: do not insert an extra `/api/v2` prefix, do not splice the host into the path, do not move `{chain_id}` to a different position.
- **Resolve `{templated}` segments and query parameters by inspecting the endpoint's `parameters` definition** with `oastools walk parameters` — see [Endpoint detail lookup](#endpoint-detail-lookup-pro-apijson-via-oastools) below. The OpenAPI spec is authoritative on which parameters are path-templated, which are query, and which are required.

## Authentication

The PRO API uses **a single authentication scheme for every endpoint**: the API key is sent as a **Bearer token** in the `Authorization` request header.

```
curl --request GET \
  --url 'https://api.blockscout.com/1/api/v2/blocks/10000000' \
  --header "Authorization: Bearer ${BLOCKSCOUT_PRO_API_KEY}"
```

Hard rules:

- **Always** authenticate with `Authorization: Bearer proapi_…`. This is the only authentication scheme the skill uses.
- Never log the key, never embed it in a code snippet committed to a repo, never echo it back. Read it at runtime from an environment variable or equivalent secret store and reference it by variable name.

## Required request headers (beyond auth)

The PRO API is CDN-fronted. On every request, set `User-Agent: <name>/<version>` (e.g. `my-wallet-app/1.4.2`) and `Accept: application/json`. Bare HTTP-library defaults — Python `urllib`'s `Python-urllib/3.x`, plain Java `HttpURLConnection`, ad-hoc Go `net/http` without a configured client, etc. — can be blocked at the CDN edge; higher-level clients (`requests`, `httpx`, `fetch`, `undici`, OkHttp, …) usually pass, but setting both headers explicitly is portable and CDN-resilient.

If `curl` works but a script gets `403` (often with a Cloudflare `1010` page in the body, sometimes an empty body or a reset) on the same URL, the request never reached the API — it is a header issue, not a credentials one. Re-running the on-boarding flow will not help.

## Endpoint discovery — `references/pro-api-index.md`

The index groups every endpoint by its OpenAPI tag (`addresses`, `blocks`, `transactions`, `tokens`, chain-specific groups like `optimism`/`arbitrum`/`zkevm`, `legacy`, etc.). Each entry has the form:

```
<METHOD> <path>: <short description>
```

Workflow:

1. **Always consult `references/pro-api-index.md` first** to pick a candidate endpoint for the user's data need. Skim the relevant tag(s); a single data need often maps to several similarly-named endpoints, and the one-line descriptions are usually enough to pick the right one.
2. Use the path string from the index **verbatim** when querying the OpenAPI spec — the same string is the value passed to the `oastools` `-path` flag below.

Every endpoint listed in the index is callable and uses the same auth scheme — including endpoints under the `legacy` tag. Do not steer the user toward or away from any subset based on tag name; pick the endpoint whose description matches the data need.

### Prefer a direct endpoint over a derived chain of calls

Before writing multi-step data-fetching logic, **scan the index (legacy entries included) for a single purpose-built endpoint** that answers the question directly. This is a firm rule — chaining derived calls when a direct endpoint exists wastes credits, multiplies latency, and invites off-by-one bugs.

Example: to resolve a Unix timestamp `T` to a block number, do **not** binary-search `/api/v2/blocks/{block_hash_or_number_param}`. The index already has a purpose-built endpoint:

```
GET /{chain_id}/api/legacy/block/get-block-number-by-time
# Etherscan-compatible form:
GET /{chain_id}/api?module=block&action=getblocknobytime&timestamp=<T>&closest=before
```

Generalise: when a request decomposes into "fetch X, derive Y, aggregate Z", look for an endpoint that returns Y or Z directly before chaining.

**Index limits — recognise contract-state requests.** The index lists endpoints that return explorer-indexed data. It will **not** contain an endpoint for arbitrary contract state at a specific block — historical `balanceOf`, `totalSupply`, view-function calls, contract storage reads. Those go through `eth_call` on the [JSON-RPC gateway](#reading-contract-state--eth_call-via-the-json-rpc-gateway) — same Bearer auth, same credit accounting. Recognise this case **before** declaring "no match in the index" and **before** considering an external RPC URL: there is no need for one.

### Disambiguating candidates with full descriptions

When index one-liners are ambiguous, shortlist plausible candidates and read their full operation descriptions before giving up — the OpenAPI description usually spells out accepted inputs, populated response fields, and chain-type applicability that the index summary omits. Use the `oastools walk operations` command from [Endpoint detail lookup](#endpoint-detail-lookup-pro-apijson-via-oastools). Only after that step is exhausted should you surface a no-match to the user — and even then, do not silently substitute a third-party data source.

## Endpoint detail lookup — `references/pro-api.json` via `oastools`

The OpenAPI document is large (~24,000 lines). **Never read `pro-api.json` whole** — it will exhaust context and contributes nothing the index does not already summarise. Instead, query it with `oastools` piped through `jq`.

### Tooling

The skill works best when **`oastools`** is installed locally. Installation options (Homebrew, prebuilt binaries, `go install`, …) are documented at https://github.com/erraggy/oastools/blob/main/README.md. **`jq`** is also required.

If `oastools` is not installed, recommend installing it before doing endpoint-detail lookups; falling back to grepping `pro-api.json` is fragile and tends to miss `$ref` indirection.

> **Flag style.** Use **single-dash** flags throughout: `-detail`, `-format`, `-method`, `-path`, `-name`, `-status`. Go's `flag` package accepts both `-x` and `--x`, but `oastools` help renders single-dash, so use that canonical form.

### Canonical commands

The commands assume the working directory is the skill directory; otherwise substitute the correct relative path to `pro-api.json`.

- **Full operation description** for an endpoint:
  ```
  oastools walk operations -detail -format json -path '<PATH>' references/pro-api.json \
    | jq '.operation.description'
  ```

- **Parameter specification** for an endpoint (drop the noisy `path` key):
  ```
  oastools walk parameters -detail -format json -method get -path '<PATH>' references/pro-api.json \
    | jq 'del(.path)'
  ```

- **Successful response (HTTP 200) format**:
  ```
  oastools walk responses -status 200 -detail -format json -method get -path '<PATH>' references/pro-api.json \
    | jq 'del(.path)'
  ```

- **Schema by name** — used to follow `$ref` pointers. The schema name is the last segment of a `$ref` value (e.g. `Log` for `#/components/schemas/Log`):
  ```
  oastools walk schemas -detail -format json -name <SCHEMA_NAME> references/pro-api.json \
    | jq 'del(.jsonPath)'
  ```

`<PATH>` is the path string from the index, verbatim, including its `{templated}` segments. Quote it with single quotes to keep the shell from interpreting the braces.

### Context-efficient traversal rules

The reason these rules matter: some endpoints have very deep schema dependency trees, and resolving everything in one shot can dump hundreds of KB into the agent's context — leaving no room for the actual task.

1. **Do not pass `-resolve-refs`** to `oastools walk parameters`, `oastools walk responses`, or `oastools walk schemas`. Resolving `$ref`s eagerly is the single most common way to blow the context budget on this API.
2. **Always inspect `parameters` before calling an endpoint.** This is non-negotiable — it is the only reliable way to know which parameters are path-templated, which are query, which are required, and what their accepted values are.
3. **Do not always inspect the full response schema.** When the task only needs a few fields from the response, prefer **incremental traversal**: read the top-level response schema, then follow only the `$ref`s needed for the target fields by calling `oastools walk schemas -name <SCHEMA_NAME>` for each. This keeps context usage bounded and tracks closely to what the script or app actually consumes.
4. Inspect the **full schema tree** only when the task genuinely requires it — e.g. building a typed client model, generating bindings, or producing comprehensive documentation. In that case it is fine to walk every referenced schema in turn.

## Calling the API

A minimal `curl` call looks like:

```
curl --request GET \
  --url 'https://api.blockscout.com/1/api/v2/transactions/0xabc…/logs' \
  --header "Authorization: Bearer ${BLOCKSCOUT_PRO_API_KEY}"
```

The exact path, the position of `{chain_id}`, which segments are path-templated, and which parameters are query-string come from `references/pro-api-index.md` (for path discovery) and `references/pro-api.json` (for parameter detail). Do not generalise about path shape beyond what the index and spec say.

### Resolving `chain_id`

Most PRO API endpoints require a numeric `chain_id`. The list of supported chain IDs is published at:

```
GET https://api.blockscout.com/api/json/config        (no API key required)
```

This same response also contains the **per-call credit cost table**. Query this endpoint when:

- the user names a chain by symbol or name (e.g. "Optimism", "Base", "Polygon zkEVM") and you need its numeric chain ID;
- you need to confirm a chain is supported by the PRO API before writing code that targets it;
- you are estimating cost — combine the per-call cost table here with the expected number of calls.

### Reading `x-credits-remaining`

Every PRO API response carries an **`x-credits-remaining`** response header that shows the credits left on the account *after* the call has been billed. In code that issues many calls (batch scripts, indexers, cron jobs):

- **Read `x-credits-remaining` from each response.** Surface it to the user when it crosses meaningful thresholds — for example, when the remaining credits are no longer enough to cover the rest of a planned batch, or after a long-running job to confirm what was consumed.
- **Treat zero or rapidly-falling `x-credits-remaining` as a stop condition for batch scripts.** Better to stop cleanly with a clear message than to issue calls that will start failing once the daily allowance is exhausted.

## Handling response verbosity

PRO API responses are explorer-enriched and can be hundreds of KB — a single transaction's logs, an enriched address page, a paginated list of token transfers. **Dumping a raw response into the agent's reading will exhaust the context window**, so apply the same "never read whole, project narrowly" discipline you apply to `pro-api.json`. Two recipes:

- **You know what you need** → pipe `curl` through `jq` with the smallest projection that satisfies the task: `curl … | jq '{n: .height, t: .timestamp}'`. Drop heavy fields you don't need (decoded calldata, NFT metadata, raw input bytes).
- **You're exploring or debugging an unfamiliar response** → first inspect the *schema* with `oastools walk responses` (zero credits, bounded), or save the response to disk with `curl -o /tmp/r.json` and probe it with `wc -c r.json`, `jq 'keys'`, `jq '.items[0] | keys'`, or `head -c 1000` — never `cat` the file or read it whole. Saving to disk lets you re-probe without re-fetching, but the budget rule is unchanged: only narrow projections reach the conversation.

## Reading contract state — `eth_call` via the JSON-RPC gateway

The PRO API's OpenAPI spec covers data the explorer has already indexed; it does not define contract-read methods. To read live contract state, the PRO API exposes a JSON-RPC gateway at:

```
POST https://api.blockscout.com/{chain_id}/json-rpc
```

`eth_call` is available through this gateway and uses the **same `Authorization: Bearer …` header** as every other PRO API call — credit accounting, rate limits, and key handling all apply identically.

Example:

```
curl --request POST \
  --url 'https://api.blockscout.com/1/json-rpc' \
  --header "Authorization: Bearer ${BLOCKSCOUT_PRO_API_KEY}" \
  --header 'Content-Type: application/json' \
  --data '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"eth_call",
    "params":[{"to":"0x…","data":"0x…"}, "latest"]
  }'
```

For any data the explorer has already indexed — balances, token holdings, transactions, logs, decoded events, contract metadata, NFT inventories, account abstraction objects, etc. — use the corresponding REST endpoint from the index. The indexed REST path is invariably more efficient than synthesising the same data from RPC primitives.

## Pagination

Many list endpoints in the PRO API are paginated — `transactions`, `logs`, `token-transfers`, `holders`, NFT inventories, block lists, and similar endpoints commonly return one page at a time. The OpenAPI spec is authoritative on the exact cursor mechanism for each endpoint; do not assume a single call returns everything.

Before writing code that fetches a list, inspect the endpoint's response schema with `oastools walk responses` and look for the cursor field (typically `next_page_params`). Then:

- Pass the cursor back as query parameters on subsequent calls.
- Loop until the cursor is empty / the response indicates no more pages, or until you have collected enough data for the user's request.
- For batch jobs that walk a large history (a wallet's full transaction history, a token's holder set, contract logs over a date range), paginate explicitly — `x-credits-remaining` and the plan RPS limit still apply across the loop.

If a list-shaped response has no cursor field at all, treat the single response as the complete set.

## Polling for change detection (bots, monitors, indexers)

The PRO API is request/response only — there is no webhook, websocket, or push channel. For "watch for new X" use cases (new transactions on an address, new blocks, new contract events, balance changes), build a polling loop:

- **Cadence** — poll on an interval comfortably under the plan's RPS limit. For a single watcher, 1 request every few seconds is usually fine on the free tier; many watchers in the same process should share a token bucket so the aggregate RPS stays under the plan limit.
- **High-water mark** — persist the last seen marker between iterations: latest block number, latest transaction hash, latest log index, etc. Fetch only what is newer than the marker on each pass.
- **Cursor through gaps** — if the watcher was offline and many new items accumulated, paginate forward from the last seen marker rather than re-fetching everything.
- **Credit budget** — a polling watcher consumes credits continuously; estimate per-day credit usage (`requests_per_day × per-call credits`) up-front from `/api/json/config` and pick a poll interval that fits the plan.

## Plans, credits, and cost estimation

Two **unauthenticated** endpoints expose the live billing schema. Prefer them over hard-coded numbers — pricing tiers and per-call credit costs change.

| URL | Returns | Auth |
|-----|---------|------|
| `https://api.blockscout.com/api/json/plans` | All plan tiers and their daily credit allowances / rate limits | None |
| `https://api.blockscout.com/api/json/config` | Per-endpoint credit cost table **and the list of supported chain IDs** | None |

For background context, the public docs currently advertise these tiers — **treat the numbers as a snapshot**; query `/api/json/plans` for authoritative current values:

| Tier | Daily credits | Rate limit | Price |
|------|---------------|------------|-------|
| Free | 100,000 | 5 RPS | $0 |
| Standard | 100,000,000 | 15 RPS | $49/mo |
| Professional | 500,000,000 | 30 RPS | $199/mo |
| Enterprise | Custom | Custom | Custom |

When the user asks about pricing, plan limits, or how expensive a script will be to run:

1. Call `/api/json/plans` and `/api/json/config` (no API key needed) and report current values.
2. Estimate script cost by multiplying the **expected number of calls** by the **per-call credit cost** from `/api/json/config` for each endpoint involved. State both the credits and the implied plan tier when relevant.

## Rate limits and HTTP errors

Per-plan **RPS limits** apply (see `/api/json/plans`). Scripts must throttle accordingly. Standard handling per status:

| Status | Meaning | Handling |
|--------|---------|----------|
| `200` | Success | Read body and `x-credits-remaining` header. |
| `401` / `403` (PRO API JSON body) | Invalid or missing API key | Stop. Surface clearly. Do not retry. Re-run the on-boarding flow. |
| `403` (Cloudflare HTML body, `error code: 1010`, or `curl`-works-but-script-fails) | CDN edge block — request never reached the API | Set [`User-Agent` and `Accept` headers](#required-request-headers-beyond-auth). Not an auth issue. |
| `402` (or body indicating credit exhaustion) | Daily credit allowance exceeded | Stop and report. Suggest upgrading the plan or waiting for the daily reset. |
| `429` | Rate-limited | Back off with exponential delay and retry — do not retry tightly in a loop. |
| `5xx` | Transient server error | Retry with backoff, capped attempts. |

## Putting it together — recommended workflow

For each new data need the user describes:

1. **Pre-flight the API key** if this is the first PRO API call in the session (see [API key — mandatory pre-flight](#api-key--mandatory-pre-flight)).
2. **Resolve the target chain ID** if the user named a chain by symbol/name — query `/api/json/config`.
3. **Route the request.** Decide which surface answers the data need:
   - **Explorer-indexed data** (transactions, balances, blocks, logs, tokens, NFTs, decoded events, contract metadata, account abstraction objects, …) → REST endpoint from `references/pro-api-index.md`. Continue with steps 4–6.
   - **Live or historical contract state at a specific block** (`balanceOf(addr)` at block `N`, `totalSupply()` at a past block, any view function, contract storage reads) → `eth_call` via the [JSON-RPC gateway](#reading-contract-state--eth_call-via-the-json-rpc-gateway). Skip to step 7. Do **not** introduce a separate RPC endpoint — the gateway is part of the PRO API and uses the same Bearer auth.
4. **Find the REST endpoint** in `references/pro-api-index.md`. Copy the path string verbatim.
5. **Inspect the endpoint's parameters** with `oastools walk parameters`. Build the URL by concatenating `https://api.blockscout.com` with the path string and substituting `{templated}` segments. **Inspect the response schema only as deep as the task needs** — use `oastools walk responses` for the top-level shape, then follow specific `$ref`s with `oastools walk schemas -name <SCHEMA_NAME>` for the fields you actually consume.
6. **Call the endpoint** with `Authorization: Bearer ${BLOCKSCOUT_PRO_API_KEY}`, a meaningful `User-Agent`, `Accept: application/json` (see [Required request headers](#required-request-headers-beyond-auth)), and any required query parameters. Read `x-credits-remaining` from the response and **project the body narrowly** (see [Handling response verbosity](#handling-response-verbosity)) — do not dump it whole.
7. **For `eth_call` requests:** `POST` to `https://api.blockscout.com/{chain_id}/json-rpc` with the same Bearer auth and a JSON-RPC body — see [Reading contract state](#reading-contract-state--eth_call-via-the-json-rpc-gateway).
8. **For long-running or batch work**, surface `x-credits-remaining` to the user at meaningful checkpoints, throttle to stay under the plan's RPS limit, and stop cleanly when credits run low.
