---
title: "Connecting your client"
weight: 30
---

Use these values to connect your MCP client to the Teramot MCP server.

| | |
| --- | --- |
| **MCP URL** | `https://mcp.teramot.com/mcp` |
| **Client ID** | `5nldf3wj83yz9f6zbrsjx` |

> [!NOTE]
> **Claude** and **ChatGPT** authenticate with OAuth — they only need the MCP URL (and Client ID
> if prompted). **Cursor**, **v0.dev**, and **Antigravity** use a static API key — generate one
> first on the **MCP → API Keys** page (see [Authentication](/api/authentication/#static-api-key)).

{{< tabs >}}

{{< tab name="Claude Code" >}}

Run this command in your terminal:

```bash
claude mcp add --transport http --client-id 5nldf3wj83yz9f6zbrsjx --callback-port 8090 teramot https://mcp.teramot.com/mcp
```

A browser window opens for you to authorize with Teramot. After that, the `teramot` tools are
available in Claude Code.

{{< /tab >}}

{{< tab name="Claude Desktop / Browser" >}}

1. Open **Settings → Developer → MCP Servers** (or **Edit Config**).
2. Add a new server with these values:
   - **Name:** `teramot`
   - **Transport:** `HTTP`
   - **URL:** `https://mcp.teramot.com/mcp`
   - **Client ID:** `5nldf3wj83yz9f6zbrsjx`
3. Save and restart Claude Desktop.
4. Open a new chat and activate the **teramot** connector.

{{< /tab >}}

{{< tab name="ChatGPT" >}}

In ChatGPT, open **Settings → Apps** (or **Apps & Connectors**), add a custom MCP app, and use
these values:

- **Server URL:** `https://mcp.teramot.com/mcp`
- **Client ID:** `5nldf3wj83yz9f6zbrsjx`

Step by step on ChatGPT Desktop / Browser:

1. Open ChatGPT and go to **Settings**.
2. Open **Apps** (or **Apps & Connectors**) and create/import a custom MCP app.
3. Configure the app with these values:
   - **Name:** `teramot`
   - **Transport:** `HTTP`
   - **URL:** `https://mcp.teramot.com/mcp`
   - **Client ID:** `5nldf3wj83yz9f6zbrsjx`
4. Save the configuration and complete authorization if prompted.
5. Open a new chat and enable the **teramot** app.

{{< /tab >}}

{{< tab name="Cursor" >}}

Cursor uses a **static API key**. First generate one on the **MCP → API Keys** page
(see [Authentication](/api/authentication/#static-api-key)), then add the server to your MCP
config (Settings → MCP, or `~/.cursor/mcp.json`):

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

{{< /tab >}}

{{< tab name="v0.dev" >}}

v0.dev uses a **static API key**. Generate one on the **MCP → API Keys** page
(see [Authentication](/api/authentication/#static-api-key)) and add the server with the
`Authorization: Bearer` header:

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

{{< /tab >}}

{{< tab name="Antigravity" >}}

Antigravity uses a **static API key**. Generate one on the **MCP → API Keys** page
(see [Authentication](/api/authentication/#static-api-key)) and configure the MCP server with
the `Authorization: Bearer` header:

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

{{< /tab >}}

{{< /tabs >}}

## Verify the connection

Once connected, ask your client to **list your workspaces** — it should call `list_workspaces`
and return them. From there you can explore projects, preview tables, and build results tables.
See the full **[Tools Reference](/api/tools-reference/)**.
