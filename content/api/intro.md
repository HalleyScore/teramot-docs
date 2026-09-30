---
title: "Teramot MCP — Overview"
weight: 10
---

The Teramot Model Context Protocol (MCP) server lets any MCP-compatible AI client
(Claude, ChatGPT, Cursor, and others) work directly with your Teramot data platform.
Once connected, the client can explore your workspaces, projects, and data sources,
preview and query tables, and build new results (gold) tables — all through natural language.

It implements the **Streamable HTTP** MCP transport with OAuth 2.0 (or a static token)
for authentication.

## Connection essentials

| | |
| --- | --- |
| **Endpoint** | `https://mcp.teramot.com/mcp` |
| **Transport** | Streamable HTTP (`POST` for JSON-RPC, `GET` for the SSE stream) |
| **Client ID** | `5nldf3wj83yz9f6zbrsjx` |
| **Authentication** | OAuth 2.0 + PKCE, or a static API key (Bearer token) |
| **Server** | `teramot-mcp` `v0.1.0` |

> [!TIP]
> Most users never touch the protocol directly — see **[Connecting your client](/api/connect-clients/)**
> for copy-paste setup for Claude, ChatGPT, Cursor, v0.dev, and Antigravity. This page documents the
> underlying protocol for custom integrations.

## How connecting works

1. The client points at `https://mcp.teramot.com/mcp` and (for OAuth clients) the Client ID above.
2. The client calls `initialize` and `tools/list` to discover capabilities — these require **no authentication**.
3. For any real work (`tools/call`), the client authenticates with a Bearer token, obtained either via
   the automatic OAuth flow or a static API key. See **[Authentication](/api/authentication/)**.

## Transport & endpoints

All traffic goes to a single endpoint, `https://mcp.teramot.com/mcp`.

### `POST /mcp`

Carries JSON-RPC 2.0 requests (`initialize`, `tools/list`, `tools/call`, …). Responses are
returned as `application/json` or, for streaming operations, as `text/event-stream`.

```http
POST /mcp HTTP/1.1
Host: mcp.teramot.com
Authorization: Bearer YOUR_TOKEN
Accept: application/json, text/event-stream
Content-Type: application/json
Mcp-Session-Id: SESSION_UUID   # echoed after initialize
```

### `GET /mcp`

Opens a Server-Sent Events stream for server-to-client messages. Requires the
`Mcp-Session-Id` header returned by `initialize`; without it the server responds
`401 Unauthorized` (`missing Mcp-Session-Id; re-initialize via POST`).

### Bootstrap methods (no authentication)

To let clients discover the server before authorizing, three methods skip auth:

- `initialize`
- `tools/list`
- `notifications/initialized`

Every other method requires a valid Bearer token.

## Session management

`initialize` returns an `Mcp-Session-Id` response header. Include it on subsequent
requests and on the `GET /mcp` stream. Sessions are held in memory and reset when the
server restarts — if a session is lost, simply call `initialize` again.

## MCP methods

### `initialize`

Negotiate protocol version and capabilities. **No authentication required.**

{{< tabs >}}
{{< tab name="Request" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "init-1",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": { "tools": {} },
    "clientInfo": { "name": "MyApp", "version": "1.0.0" }
  }
}
```

{{< /tab >}}
{{< tab name="Response" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "init-1",
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": { "tools": { "listChanged": true } },
    "serverInfo": { "name": "teramot-mcp", "version": "v0.1.0" },
    "instructions": "You are connected to the Teramot data platform. Help users explore their workspaces, projects, data sources, tables, and create results tables."
  }
}
```

{{< /tab >}}
{{< /tabs >}}

The response carries the `Mcp-Session-Id` header for subsequent requests.

### `tools/list`

List the available tools. **No authentication required** (part of the bootstrap flow).
See the full catalog in **[Tools Reference](/api/tools-reference/)**.

{{< tabs >}}
{{< tab name="Request" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "list-tools",
  "method": "tools/list"
}
```

{{< /tab >}}
{{< tab name="Response" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "list-tools",
  "result": {
    "tools": [
      {
        "name": "list_workspaces",
        "description": "Lists all workspaces the user has access to.",
        "inputSchema": { "type": "object", "properties": {} }
      },
      {
        "name": "preview_table",
        "description": "Preview the first 100 rows of a data table.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "table_name": { "type": "string", "description": "Name of the table to preview" }
          },
          "required": ["table_name"]
        }
      }
    ]
  }
}
```

{{< /tab >}}
{{< /tabs >}}

### `tools/call`

Execute a tool. **Authentication required** (Bearer token).

{{< tabs >}}
{{< tab name="Request" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "call-tool",
  "method": "tools/call",
  "params": {
    "name": "preview_table",
    "arguments": { "table_name": "sales" }
  }
}
```

{{< /tab >}}
{{< tab name="Response" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "call-tool",
  "result": {
    "content": [
      { "type": "text", "text": "{ \"columns\": [...], \"rows\": [...] }" }
    ]
  }
}
```

{{< /tab >}}
{{< /tabs >}}

## Error handling

Standard JSON-RPC 2.0 error codes apply:

```json
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "error": { "code": -32602, "message": "Invalid params" }
}
```

| Code | Meaning |
| --- | --- |
| `-32700` | Parse error (invalid JSON) |
| `-32600` | Invalid request (malformed JSON-RPC) |
| `-32601` | Method not found |
| `-32602` | Invalid params |
| `-32000` | Internal / authentication error |

At the HTTP layer, a missing or expired token returns `401 Unauthorized`.

## Next steps

- **[Authentication](/api/authentication/)** — OAuth 2.0 and static API keys.
- **[Connecting your client](/api/connect-clients/)** — Claude, ChatGPT, Cursor, v0.dev, Antigravity.
- **[Tools Reference](/api/tools-reference/)** — the full catalog of available tools.
