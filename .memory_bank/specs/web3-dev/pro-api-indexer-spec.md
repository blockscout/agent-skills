# PRO API Indexer — Script Specification

## Purpose

Generate a markdown index file that lists every HTTP endpoint available in the
Blockscout PRO API. The index is intended to be embedded in agent skill
instructions so an AI agent can quickly determine which endpoint to call when
querying Blockscout data (transactions, blocks, addresses, token transfers,
etc.).

---

## Script location

```
.memory_bank/specs/web3-dev/tools/pro-api-indexer.py
```

---

## Input

The script takes the path to the OpenAPI JSON spec as its **first positional
argument**. The argument is **required** — there is no default. Invoking the
script with no argument is an error (argparse exits with code `2`). This is
deliberate: the script must not silently fall back to a stale or unexpected
input file.

The file is an **OpenAPI v3.0** JSON document. The relevant top-level key is
`paths`, which maps URL path strings to path-item objects. Each path-item
object maps HTTP method names (`get`, `post`, `put`, `patch`, `delete`) to
operation objects.

### Relevant operation fields

| Field | Usage |
|-------|-------|
| `summary` | Preferred short description |
| `description` | Fallback when `summary` is absent or empty |
| `tags` | List of strings used for grouping; first tag wins |

---

## Output

### File path

```
web3-dev/references/pro-api-index.md
```

Path is relative to the project root. The output path is fixed (not configurable via CLI argument).

### File format

```markdown
# PRO API Endpoint Index

## <tag-name>

<METHOD> <path>: <label>
<METHOD> <path>: <label>

## <next-tag-name>

<METHOD> <path>: <label>
```

- `<METHOD>` is the HTTP verb in **uppercase** (e.g. `GET`, `POST`).
- `<path>` is the raw path string from the OpenAPI spec (e.g.
  `/{chain_id}/api/legacy/block/get-block-number-by-time`).
- `<label>` is resolved according to the **label resolution rules** below.
- Tag sections are separated by a blank line.
- Within each section, endpoint lines are separated by single newlines (no
  blank lines between them).

#### Example output

```markdown
# PRO API Endpoint Index

## legacy

GET /{chain_id}/api/legacy/block/get-block-number-by-time: Get block number by time stamp
GET /{chain_id}/api/legacy/logs/get-logs: Get Event Logs by Address and/or Topic(s)

## transactions

GET /{chain_id}/api/v2/transactions: Get transactions list
GET /{chain_id}/api/v2/transactions/{transaction_hash}: Get transaction info

## Metadata

GET /services/metadata/api/v1/metadata: NO DESCRIPTION
```

---

## Label resolution rules

Apply in order; use the first non-empty result:

1. **`summary`** — use as-is if the field exists and is not blank after
   stripping whitespace.
2. **`description`** — collapse to a single line:
   - Replace every newline (`\n`) and carriage return (`\r`) with a single
     space.
   - Collapse runs of whitespace (spaces, tabs) that appear at the start of
     what was originally a new line into a single space (i.e. strip leading
     whitespace from each logical line before joining).
   - Strip the resulting string; use it if non-empty.
3. **`NO DESCRIPTION`** — literal string, used when both `summary` and
   `description` are absent or blank.

#### Collapsing description — algorithm

```
lines = raw_description.splitlines()
cleaned = " ".join(line.strip() for line in lines if line.strip())
```

This removes blank lines and leading/trailing whitespace from each line, then
joins with a single space.

---

## Grouping and ordering

### Grouping by tag

- Each operation belongs to the **first element** of its `tags` array.
- Operations with an **empty or missing** `tags` field are collected under a
  synthetic group named `untagged`.
- Each unique tag produces exactly one `## <tag>` section in the output.

### Section ordering

Tag sections appear in **alphabetical order** of the tag name (case-insensitive
sort, but the tag name is rendered with its original casing).

### Line ordering within a section

Within a section, lines are sorted first by **path** (lexicographic), then by
**HTTP method** (alphabetic). This produces a stable, deterministic output.

---

## Edge cases

| Situation | Behaviour |
|-----------|-----------|
| Path has multiple HTTP methods | Each method produces its own line |
| Path-item contains non-method keys (`summary`, `description`, `parameters`, `servers`) | Ignore; only iterate over known HTTP method keys |
| `tags` array has more than one entry | Only the first tag is used for grouping |
| Tag name contains leading/trailing whitespace | Strip before using as group key and heading |
| Duplicate `(method, path)` pairs in the spec | Treat each occurrence as a separate line (spec violation; emit both) |

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success; output file written |
| `1` | Input file not found or not readable |
| `2` | Input file is not valid JSON |
| `3` | Parsed JSON does not contain a `paths` key |

On error, print a human-readable message to **stderr** and exit with the
appropriate code. Do **not** write a partial output file on error.

---

## Implementation notes

- Use only Python standard library modules (`json`, `sys`, `pathlib`,
  `argparse`, `re`). No third-party dependencies.
- Open all files with explicit `encoding="utf-8"`.
- Known HTTP method names to iterate over (in this order for any internal
  processing, though output order follows the sort rule above):
  `get`, `post`, `put`, `patch`, `delete`, `head`, `options`, `trace`.
