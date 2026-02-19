# Tool Equivalence Groups

Multiple API surfaces often expose tools that answer the same question. This document defines equivalence groups to prevent redundant calls and guide selection.

## Priority Chain

When multiple tools can fulfill a data need, prefer them in this order:

> **MCP tool → MCP `direct_api_call` → PRO REST API → JSON RPC API → ETH RPC API**

Select the highest-priority tool that (a) is available in your environment and (b) returns the fields your task requires.

## No Redundant Calls Rule

Once you select a tool for a data need, **do not** call equivalent tools on other API surfaces for the same data. The only exception: when the selected tool's response is confirmed to lack a required field.

## Equivalence Groups

### Address Info

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_address_info` | Enriched: includes first tx timestamp, ENS, metadata tags, proxy info |
| 2 | PRO REST `/{chain_id}/api/v2/addresses/{hash}` | Raw; includes counters (tx count, token transfers) |
| 3 | JSON RPC `module=account&action=balance` | Balance only |
| 4 | ETH RPC `eth_getBalance` | Raw balance in hex, standard format |

**Deviate to PRO REST** when you need address counters. **Deviate to ETH RPC** when you need raw balance for tooling compatibility (e.g. feeding into web3 libraries).

### Transaction Details

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_transaction_info` | Enriched: decoded input, token transfers with metadata, fee breakdown |
| 2 | PRO REST `/{chain_id}/api/v2/transactions/{hash}` | Raw; may include internal transactions and raw traces |
| 3 | JSON RPC `module=transaction&action=gettxinfo` | Etherscan-compatible format with logs |
| 4 | ETH RPC `eth_getTransactionByHash` | Standard Ethereum format |

**Deviate to PRO REST** when you need raw traces MCP omits. **Deviate to ETH RPC** for standard format expected by external tooling.

### Transaction Receipt

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_transaction_info` | Includes status as part of enriched response |
| 2 | PRO REST `/{chain_id}/api/v2/transactions/{hash}` | Full receipt data |
| 3 | JSON RPC `module=transaction&action=gettxreceiptstatus` | Status only (0/1) |
| 4 | ETH RPC `eth_getTransactionReceipt` | Full receipt with logs in standard format |

**Deviate to ETH RPC** when you need the raw receipt with log topics for event parsing.

### Block Info

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_block_info` | Enriched: gas, burnt fees, tx count; optionally includes tx hashes |
| 2 | PRO REST `/{chain_id}/api/v2/blocks/{number}` | Raw block data |
| 3 | JSON RPC `module=block&action=getblockreward` | Block reward and uncle data |
| 4 | ETH RPC `eth_getBlockByNumber` | Standard Ethereum block format with uncle data |

**Deviate to ETH RPC** when you need uncle/ommer data or standard format.

### Token Balances (Portfolio)

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_tokens_by_address` | Enriched: market data, holder count, exchange rate |
| 2 | PRO REST `/{chain_id}/api/v2/addresses/{hash}/tokens` | Raw token list |
| 3 | JSON RPC `module=account&action=tokenlist` | Simpler flat format |

**Deviate to JSON RPC** when you need a simpler format for quick token listing.

### Token Transfers

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_token_transfers_by_address` | Enriched: token metadata, time-bounded |
| 2 | PRO REST `/{chain_id}/api/v2/addresses/{hash}/token-transfers` | 50 items/page |
| 3 | JSON RPC `module=account&action=tokentx` | Etherscan-compatible, up to 10,000 results |

**Deviate to PRO REST** for bulk workflows (50 items/page vs MCP's 10). **Deviate to JSON RPC** when you need block-range filtering (`startblock`/`endblock`).

### Transaction List

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_transactions_by_address` | Enriched, time-bounded via age_from/age_to |
| 2 | PRO REST `/{chain_id}/api/v2/addresses/{hash}/transactions` | 50 items/page |
| 3 | JSON RPC `module=account&action=txlist` | Block-range filtering, up to 10,000 results |

**Deviate to PRO REST** for bulk retrieval. **Deviate to JSON RPC** for `startblock`/`endblock` filtering.

### Contract ABI

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_contract_abi` | Direct ABI retrieval |
| 2 | PRO REST `/{chain_id}/api/v2/smart-contracts/{hash}` | ABI + source + settings in one call |
| 3 | JSON RPC `module=contract&action=getabi` | ABI as JSON string |

**Deviate to PRO REST** when you also need source code and compiler settings.

### Contract Source Code

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `inspect_contract_code` | File listing + individual file retrieval |
| 2 | PRO REST `/{chain_id}/api/v2/smart-contracts/{hash}` | All files in one response |
| 3 | JSON RPC `module=contract&action=getsourcecode` | Source code as string |

**Deviate to PRO REST** when you need all source files in a single call.

### ENS Resolution

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_address_by_ens_name` | Single-name resolution |
| — | BENS `POST /addresses:batch-resolve` | Batch resolution (no MCP equivalent) |

**Use BENS directly** for batch resolution or reverse lookup.

### Token Search

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `lookup_token_by_symbol` | Searches by symbol or name, returns token matches |
| 2 | PRO REST `/{chain_id}/api/v2/search?q=...` | Broader search (addresses, tokens, transactions) |

**Deviate to PRO REST** when you need a general search across multiple entity types.

### Transaction Logs

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `direct_api_call` with `/api/v2/transactions/{hash}/logs` | Proxied access |
| 2 | PRO REST `/{chain_id}/api/v2/transactions/{hash}/logs` | Direct access |
| 3 | ETH RPC `eth_getLogs` | Block-range log queries with topic filtering |

**Deviate to ETH RPC** when you need log queries across block ranges (not per-transaction).

### Token Holders

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `direct_api_call` with `/api/v2/tokens/{addr}/holders` | ~10 items/page |
| 2 | PRO REST `/{chain_id}/api/v2/tokens/{addr}/holders` | 50 items/page |

**Deviate to PRO REST** for bulk holder enumeration.

### Chain List

| Priority | Tool / Endpoint | Distinguishing Trait |
|----------|----------------|---------------------|
| 1 | MCP `get_chains_list` | Supported chains with metadata |
| — | Chainscout `GET /chains` | Full registry with **explorer URLs** |

**Use Chainscout directly** when you need the Blockscout explorer URL for a chain (MCP `get_chains_list` does not return URLs).
