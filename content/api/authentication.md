---
title: "Authentication"
weight: 20
---

The Teramot MCP server supports two authentication modes. Both pass a Bearer token to the
server; pick the one your client supports.

| Mode | Use it for |
| --- | --- |
| **OAuth 2.0 + PKCE** | Claude (Code, Desktop, Browser), ChatGPT, and any client that can complete an OAuth flow |
| **Static API key** | Cursor, v0.dev, Antigravity, and any client that only supports a static Bearer token |

Both modes coexist on the same endpoint, and both grant the same access. The discovery
methods `initialize` and `tools/list` require no token at all (see
[Overview → Bootstrap methods](/api/intro/#bootstrap-methods-no-authentication)).

> [!NOTE]
> Your connection is **account-wide**: the same credentials apply to every workspace and project
> on your Teramot account. You don't need a separate token per workspace.

## OAuth 2.0 + PKCE

This is the recommended path for clients that support it. You only configure two values —
the **MCP URL** (`https://mcp.teramot.com/mcp`) and the **Client ID**
(`5nldf3wj83yz9f6zbrsjx`). The client opens a browser window, you log in to Teramot, and the
client receives and refreshes tokens automatically.

Under the hood the server exposes the standard OAuth 2.0 metadata and endpoints, so most MCP
clients configure themselves with no extra input:

- `GET /.well-known/oauth-authorization-server` — authorization server metadata (RFC 8414)
- `GET /.well-known/oauth-protected-resource` — protected resource metadata (RFC 9728)
- `GET /authorize` — authorization endpoint
- `POST /token` — token endpoint
- `POST /register` — dynamic client registration

The flow uses PKCE (`S256`) and the scopes `openid email access offline_access`. See
**[Connecting your client](/api/connect-clients/)** for per-client steps.

## Static API key

For clients that can't complete the OAuth handshake (Cursor, v0.dev, Antigravity), generate a
static API key and send it as a Bearer token.

### Generate a key

1. Open the Teramot app and go to the **MCP** page.
2. In the **API Keys** section, enter a name (e.g. `cursor-work`) and click **Generate Key**.
3. **Copy the key now — it won't be shown again.**

You can create multiple keys (one per client/machine) and delete any of them later from the
same page.

### Use the key

Send it in the `Authorization` header:

```http
Authorization: Bearer YOUR_API_KEY
```

Most MCP clients accept a custom header in their server config:

```json
{
  "mcpServers": {
    "teramot": {
      "url": "https://mcp.teramot.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

> [!WARNING]
> Treat API keys like passwords. They grant full access to your account's data. If a key leaks,
> delete it from the **MCP → API Keys** page and generate a new one.

## Errors

| Situation | Result |
| --- | --- |
| No token on an authenticated method | `401 Unauthorized` |
| Expired or invalid token | `401 Unauthorized` |
| Missing `Mcp-Session-Id` on `GET /mcp` | `401 Unauthorized` (`missing Mcp-Session-Id; re-initialize via POST`) |
