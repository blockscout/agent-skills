# Swagger Caching and Indexing

## When You Need This

Use swagger caching and indexing when:
- The user needs a PRO API endpoint not covered by MCP tools or `direct_api_call`
- You need exact parameter definitions or response schemas for an endpoint
- You need to discover what endpoints exist for a specific domain (addresses, tokens, contracts, etc.)

**Check first**: before fetching swagger files, verify the endpoint isn't already available through MCP tools or the `direct_api_call` catalog in [chain-specific-endpoints.md](chain-specific-endpoints.md).

---

## Swagger File Locations

### Blockscout Main API

**URL pattern**:
```
https://raw.githubusercontent.com/blockscout/swaggers/master/blockscout/{version}/{variant}/swagger.yaml
```

**Current stable version**: `9.3.5`

**Variants** (16 total):

| Variant | When to use |
|---------|-------------|
| `default` | **Start here** — covers all base API endpoints |
| `arbitrum` | Arbitrum-specific (batches, L1/L2 messages) |
| `ethereum` | Ethereum-specific (beacon, withdrawals) |
| `optimism` | Optimism-specific (batches, games, deposits) |
| `optimism-celo` | Celo on Optimism stack |
| `scroll` | Scroll-specific (batches, deposits) |
| `zksync` | zkSync-specific (batches) |
| `polygon_zkevm` | Polygon zkEVM-specific |
| `shibarium` | Shibarium-specific |
| `stability` | Stability-specific (validators) |
| `zilliqa` | Zilliqa-specific (validators) |
| `zetachain` | ZetaChain-specific |
| `rsk` | RSK-specific |
| `blackfort` | BlackFort-specific |
| `filecoin` | Filecoin-specific |
| `neon` | Neon-specific |

**Rule**: always fetch `default` first. Only fetch a chain-specific variant if you need endpoints unique to that chain family.

### Service Swaggers

**URL pattern**:
```
https://raw.githubusercontent.com/blockscout/swaggers/master/services/{name}/main/swagger.yaml
```

**Key services**:

| Name | Service |
|------|---------|
| `bens` | ENS service |
| `metadata` | Address tags/reputation |
| `stats` | Statistics |
| `multichain-aggregator` | Cross-chain search |

Service swaggers use the `main` branch, which always points to the latest version.

---

## Freshness Check

Before using cached swagger files, verify they are current:

```bash
bash scripts/swagger-freshness.sh
```

This compares the version in `cache/.version` against the latest Blockscout release on GitHub.

**Output**:
- `CURRENT: Cached version 9.3.5 matches latest release.` → safe to use cache
- `STALE: Cached version 9.3.4, latest release 9.3.5` → re-fetch and re-index

**How it works**:
1. Reads `cache/.version` (if exists)
2. Queries `https://api.github.com/repos/blockscout/blockscout/releases/latest` for the latest tag
3. Compares versions
4. Exit code: 0 = current, 1 = stale or no cache

For service swaggers (`main` branch): there is no version tracking — re-fetch periodically or when you encounter unexpected API behavior.

---

## Full Caching Workflow

### Step 1: Check freshness

```bash
cd .claude/skills/blockscout-analysis
bash scripts/swagger-freshness.sh
```

### Step 2: Fetch swagger file(s)

**Blockscout default API**:
```bash
mkdir -p cache/swaggers cache/indexes
curl -sL "https://raw.githubusercontent.com/blockscout/swaggers/master/blockscout/9.3.5/default/swagger.yaml" \
  -o cache/swaggers/blockscout-default.yaml
```

**Chain-specific variant** (only if needed):
```bash
curl -sL "https://raw.githubusercontent.com/blockscout/swaggers/master/blockscout/9.3.5/arbitrum/swagger.yaml" \
  -o cache/swaggers/blockscout-arbitrum.yaml
```

**Service swagger**:
```bash
curl -sL "https://raw.githubusercontent.com/blockscout/swaggers/master/services/metadata/main/swagger.yaml" \
  -o cache/swaggers/metadata.yaml
```

### Step 3: Generate index

```bash
python3 scripts/swagger-indexer.py cache/swaggers/blockscout-default.yaml \
  > cache/indexes/blockscout-default.idx
```

### Step 4: Update version marker

```bash
echo "9.3.5" > cache/.version
```

### Step 5: Verify

```bash
head -10 cache/indexes/blockscout-default.idx
```

Expected output:
```
# Index: blockscout-default.yaml
# Generated: 2026-02-16T12:00:00Z
# Endpoints: 87
#
# FORMAT: METHOD /path | summary | line_start-line_end
DELETE /api/v2/addresses/{address_hash}/private-tags | ... | 245-260
GET /api/v2/addresses/{address_hash} | Get address info | 261-312
...
```

---

## Using the Index

### Search for endpoints

```bash
grep -i "gas" cache/indexes/blockscout-default.idx
grep -i "token" cache/indexes/blockscout-default.idx
grep -i "internal" cache/indexes/blockscout-default.idx
```

### Read endpoint details

Once you find a matching endpoint in the index, note the line range and read those lines from the cached swagger:

```bash
# Example: found "GET /api/v2/stats | Get stats | 2100-2180"
sed -n '2100,2180p' cache/swaggers/blockscout-default.yaml
```

This gives you the full endpoint definition including:
- Path parameters and their types
- Query parameters with descriptions
- Response schema with field definitions
- Required vs optional parameters

### Example: Finding the right endpoint

User asks: "What are the gas prices on Ethereum?"

1. Search the index:
   ```bash
   grep -i "gas\|stats" cache/indexes/blockscout-default.idx
   ```

2. Find: `GET /api/v2/stats | Get stats | 2100-2180`

3. Read details:
   ```bash
   sed -n '2100,2180p' cache/swaggers/blockscout-default.yaml
   ```

4. Construct the API call:
   ```bash
   curl -s "https://api.blockscout.com/1/api/v2/stats?apikey=$BLOCKSCOUT_API_KEY"
   ```

---

## Index File Format

```
# Index: <filename>
# Generated: <ISO 8601 timestamp>
# Endpoints: <count>
#
# FORMAT: METHOD /path | summary | line_start-line_end
GET /api/v2/addresses/{address_hash} | Get address info | 245-312
GET /api/v2/addresses/{address_hash}/counters | Get address counters | 313-358
POST /api/v2/addresses/{address_hash}/private-tags | Create private tag | 359-390
...
```

- One line per endpoint
- Sorted by path, then method (GET, POST, PUT, DELETE, PATCH)
- Pipe-separated for easy parsing
- Summary truncated to 80 characters
- Line ranges are 1-indexed, matching `sed -n 'start,end p'` syntax

---

## Alternative: Probing Endpoints Directly

If you don't want to cache swagger files, you can probe endpoints directly:

1. **Construct URL** from the REST pattern:
   ```bash
   curl -s "https://api.blockscout.com/1/api/v2/addresses/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045/counters?apikey=$BLOCKSCOUT_API_KEY"
   ```

2. **Inspect the response** to understand structure:
   ```bash
   curl -s "https://api.blockscout.com/1/api/v2/addresses/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045/counters?apikey=$BLOCKSCOUT_API_KEY" | python3 -m json.tool
   ```

**Advantages**: fast, no caching needed, see real data
**Limitations**: no parameter documentation, no response schema, no discovery of endpoints you don't already know about

**Best for**: quick verification that an endpoint exists and returns expected data when you have a reasonable guess at the path.

---

## Version Handling

### Blockscout version changes

The swagger version (currently `9.3.5`) changes with Blockscout releases:

1. If a fetch returns 404, the version may have changed
2. Check for newer versions: browse `https://github.com/blockscout/swaggers/tree/master/blockscout/`
3. Or check latest release: `curl -s https://api.github.com/repos/blockscout/blockscout/releases/latest | grep tag_name`
4. Update your fetch URLs and `cache/.version` accordingly

### Service swagger versions

Service swaggers use the `main` branch, which always reflects the latest API. No version tracking needed — just re-fetch when you need updated schemas.

Service-specific releases are tracked in `github.com/blockscout/blockscout-rs/releases` with prefixes:
- `bens-*` for BENS
- `multichain-aggregator-*` for Multichain Aggregator

---

## See Also

- [Infrastructure Overview](infrastructure-overview.md) — swagger repo structure and variant list
- [PRO API Guide](pro-api-guide.md) — endpoint discovery options
- [Chain-Specific Endpoints](chain-specific-endpoints.md) — curated endpoint catalog (no swagger needed)
