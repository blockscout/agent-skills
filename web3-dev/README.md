# Web3 Dev

AI agent skill for building web3 software — applications, scripts, CLIs, bots, mobile, and desktop apps — that reads blockchain data through the Blockscout PRO API. One HTTP API spans 100+ EVM chains (94+ L2s and scaling projects); switching chains is a path-parameter change.

## What this skill does

The skill gives an agent everything it needs to integrate the Blockscout PRO API into software it builds:

1. **API key on-boarding** — locating an existing key in the environment or guiding the user through key creation, with case-by-case storage recommendations (env var, `.env`, server-side proxy, secrets manager, etc.).
2. **Endpoint discovery** — picking the right endpoint from the bundled index, then looking up parameters and response shapes in the OpenAPI specification.
3. **Code generation** — emitting idiomatic, secure HTTP client code for the user's target stack (Node, Python, Go, mobile, desktop, etc.) that authenticates correctly and handles `chain_id` properly.

## Key ideas

- **Single data source**: All data access goes through the Blockscout PRO API over HTTPS. No MCP server, no fallbacks — this skill is for direct HTTP integrations.
- **Multichain by path parameter**: Every endpoint takes a `chain_id`. One API key works across every supported chain.
- **Bundled reference is source of truth**: `references/pro-api-index.md` and `references/pro-api.json` together list every callable endpoint and its full schema. The agent does not invent endpoints.
- **Index first, spec on demand**: The agent always starts from the small markdown index and only queries the large OpenAPI JSON (via `oastools`) when it needs the parameters or response shape for a specific endpoint.
- **Security-first key handling**: API keys are never embedded in client binaries, never echoed in full, and never reused from stored memory without confirmation.

## Directory structure

```
web3-dev/
├── SKILL.md                           # Agent entry point — on-boarding, endpoint
│                                      #   selection, and all behavioral instructions
├── README.md                          # This file (human overview)
└── references/                        # Lookup data consulted during execution
    ├── pro-api-index.md               # One-line summary of every endpoint, grouped by tag
    └── pro-api.json                   # Full Blockscout PRO API OpenAPI v3 specification
```

- **`SKILL.md`** is the self-contained agent entry point. An agent that reads only this file has everything it needs to behave correctly.
- **`references/`** contains the endpoint index and full OpenAPI spec the agent consults at runtime.

## Setup

The skill itself has no install step beyond making the `web3-dev/` directory available to your agent. To actually call the PRO API, the user needs an API key (prefix `proapi_…`) from **https://dev.blockscout.com**. The free tier does not require a credit card. The skill will guide the agent through key acquisition and storage if no key is present in the environment.

## License

[MIT](../LICENSE)
