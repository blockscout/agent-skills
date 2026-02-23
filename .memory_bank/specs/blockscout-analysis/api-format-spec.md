# API Description File Format Specification

## Purpose

Defines the format for API description files used in the `api/` directory of the blockscout-analysis skill. These files document HTTP endpoints available via `direct_api_call` and are consumed by the agent at runtime to discover endpoint paths and parameters. They are produced during the skill preparation phase by processing Swagger/OpenAPI files or other API sources.

## Format

Files are written in Markdown. They focus on endpoint descriptions and input parameters. **Output parameters and response schemas are omitted.**

### Document Structure

```
## <Topic or "API Endpoints">

### <Category Name>

#### METHOD /path

<Description>

- **Parameters**

  <table or *None*>

- **Example Request**

  ```bash
  <curl command>
  ```
```

**Heading levels:**

| Level | Used for |
| ----- | -------- |
| H2 | Top-level section (e.g., `## API Endpoints` or a topic title) |
| H3 | Grouping of related endpoints (e.g., `### Block Tools`) |
| H4 | Individual endpoint entry |

A file may omit H3 groupings when all endpoints belong to a single category.

---

### Endpoint Entry

Each endpoint entry consists of the following elements, in order:

#### 1. Heading

```markdown
#### METHOD /path
```

The HTTP method and canonical path, written in plain text (e.g., `#### GET /api/v2/blocks/{block_number_or_hash}`). Path parameters use `{param_name}` notation. This doubles as the unique identifier for the endpoint within the file.

#### 2. Description

One or two sentences describing what the endpoint does. Must be concise and action-oriented.

#### 3. Parameters Section

```markdown
- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `param_name` | `type` | Yes/No | Description of the parameter. |
```

- The section header is always `- **Parameters**`, indented as a list item.
- The table is indented under the header (two additional spaces).
- **Columns**: `Name`, `Type`, `Required`, `Description` — exactly these four, in this order.
- `Name` values are wrapped in backticks.
- `Type` values are wrapped in backticks. Use: `string`, `boolean`, `integer`, `object`, `array`.
- `Required` is either `Yes` or `No`.
- If the endpoint takes no parameters, replace the table with `*None*`:

```markdown
- **Parameters**

  *None*
```

#### 4. Example Request

> **Why this section exists:** The heading and parameter table are sufficient for simple GET endpoints with scalar params. The Example Request is kept because it is the only place that concretely shows non-obvious serialization: `object`/`array` type params may use bracket syntax (`query_params[key]=value`) rather than JSON encoding, and non-GET endpoints require a request body with specific headers. Without an example, these calling conventions cannot be inferred from the parameter table alone. **Do not remove this section to save tokens** — omit individual examples only for endpoints where all params are scalar (`string`, `boolean`, `integer`) and the method is GET.

```markdown
- **Example Request**

  ```bash
  curl "<url with example values>"
  ```
```

- The section header is `- **Example Request**`, indented as a list item.
- The code block is indented under the header (two additional spaces).
- May be omitted for GET endpoints where all parameters are scalar types (`string`, `boolean`, `integer`).
- Uses `curl` with representative example values for all required parameters and, where useful, optional ones.
- Path parameters are substituted (e.g., `/transactions/0x...`); query parameters use `?key=value&key2=value2` syntax.
- Sensitive or variable values use placeholder notation such as `0x...` for addresses and hashes.

---

## Omissions

The following are **not** included in API description files:

- Response schemas or field descriptions.
- Authentication details (endpoints documented here do not require auth).
- Rate limiting information.
- SDK-specific usage examples (only `curl` examples).
- Inline comments within example requests.

---

## Conventions

| Element | Convention |
| ------- | ---------- |
| Parameter names | Backtick-wrapped in table cells: `` `chain_id` `` |
| Types | Backtick-wrapped in table cells: `` `string` `` |
| HTTP method and path in heading | Plain text, method in uppercase: `#### GET /api/v2/path` |
| Placeholder values | `0x...` for addresses/hashes, ISO 8601 strings for dates |
| Blank lines | One blank line between list items (Parameters, Example Request); one blank line after the heading and after the description |
