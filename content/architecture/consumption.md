---
title: "Ways to consume data"
weight: 80
---

Teramot data can be consumed in four ways. All of them go through the same API, so **the same permissions** apply in every one.

```mermaid
flowchart LR
    U1[User] --> W[Web application]
    U2[Customer's AI assistant<br/>Claude, ChatGPT, Copilot] --> M[MCP server]
    U3[Integrations] --> K[API with project key]
    W & M & K --> API[Teramot API<br/>authentication and permissions]
    API --> D[(Project data)]
    API --> E[CSV export<br/>temporary link]
```

## Web application

The web application includes:

- **Conversational assistant**: natural-language questions about the project's data.
- **Sources**: creation, configuration, status, and refresh of connections.
- **Data explorer**: raw, processed, and results tables, with schema, preview, data-quality findings, and lineage.
- **SQL editor**: read-only queries over the project's tables.
- **Results tables**: creation, editing, and refresh.
- **Dashboards**: visualizations built on top of results tables. They are sanitized on the server and displayed in isolation in the browser.
- **Project knowledge**: business definitions that agents use.
- **Scheduling**: refresh frequency for each project.
- **Administration**: members, roles, data shares, activity log, and AI usage.

A conversation can be shared with other workspace members. A dashboard is shared with a link that requires signing in and having access to the project.

## AI assistants via MCP

Teramot publishes a **[Model Context Protocol](https://modelcontextprotocol.io)** server so you can use your data from the AI assistant you already have.

| | |
|---|---|
| **Endpoint** | `https://mcp.teramot.com/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | OAuth 2.1 with PKCE, or a personal key for clients that do not support OAuth |
| **Supported clients** | Claude (web, desktop, Team, Enterprise, and Claude Code), ChatGPT, GitHub Copilot in VS Code, Gemini, Cursor, and other MCP clients |

### How identity works

1. The administrator of your organization's AI tool adds the Teramot connector.
2. When a person uses it for the first time, the assistant redirects them to sign in to Teramot.
3. From then on, **each action runs as that person**, with their role in each workspace and project.

Making the connector available to the whole organization does not give anyone access: only people who have a Teramot user can use it, and each one sees only what their role allows.

OAuth redirects are accepted only to a closed list of destinations: the domains of the supported clients and local addresses for desktop applications.

### What you can do via MCP

| Capability | Minimum role |
|---|---|
| List workspaces and projects; read project knowledge | Read-only |
| Explore tables, view schemas, lineage, and findings; query with SQL; download results tables | Read-only |
| View dashboards | Read-only |
| Create, edit, and duplicate results tables and dashboards; edit project knowledge | Member |
| Launch refreshes; correct transformations; manage controls; delete dashboards | Admin |
| Delete projects and workspaces | Owner |

The complete tool reference and the per-client connection guide are in the [MCP server documentation](/product/mcp/overview/).

## API

For system-to-system integrations, a user can generate **project API keys**. Each key:

- Is tied to a workspace, a project, and a user.
- Inherits that user's current permissions **on every use**: if the user loses access, the key loses it too.
- Is stored as a hash: Teramot does not keep the key in plain text.

## Export

Results tables can be downloaded as **CSV**. The download uses a temporary link:

- **Private link** (default): expires after a few minutes and requires signing in with the same account that generated it.
- **Direct link**: a signed link that also expires after a few minutes.
