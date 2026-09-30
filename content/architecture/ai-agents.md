---
title: "AI agents"
weight: 70
---

Teramot uses AI agents at specific points in the flow. This page explains **what each agent does, what information it receives, and what controls it has**.

## Principles

- **The AI proposes and the system validates.** Every AI-generated transformation is run and checked before it is applied. See [Transformations](/architecture/transformations/).
- **Every result is visible SQL.** Agents do not produce opaque tables: every processed or results table has a query that the user can read and correct.
- **Agents act with the user's permissions.** An agent cannot do anything that the user who invokes it cannot do.
- **No training on customer data.** Teramot does not train its own models or fine-tune on customer data. Inference is contracted under terms that exclude API traffic from the providers' training.

## Agents and functions

| Agent | What it does | When it acts | What it receives |
|---|---|---|---|
| **Data cleaning** | Writes the SQL query that turns each raw table into its processed version. | When a source is set up, and when a table's schema changes. | The table schema, per-column statistics (null ratio, number of distinct values, most frequent values, numeric ratio), the declared keys, and a **sample of up to 100 rows**. |
| **Type reconciliation** | Aligns the type of the columns used to join tables. | When a source is set up, before the processed data is built. | Schemas and statistics of the columns involved. |
| **Documentation** | Generates table and column descriptions for the project catalog. | At the end of a source's setup. | Schemas, column descriptions, and cleaning queries. |
| **Results tables** | Translates a natural-language request into a SQL query over the processed data. | When the user asks for a new results table. | The user's request, the catalog of available tables, their schemas, and the project knowledge. |
| **Application assistant** | Talks with the user, explores tables, runs queries, and creates results tables and dashboards. | When the user types in the chat. | The conversation and the results of the tools it runs: schemas, queried rows, and results. |

> [!WARNING]
> **Real data in samples**
>
> To clean a table well, the agent needs to see real examples of its values. Those samples are sent to the model provider **unmasked**. If a table contains personal or sensitive data that is not needed for the analysis, we recommend not bringing it in, or excluding those columns at the source, for example with a view.

## The application assistant and external assistants

There are two ways to talk to your data:

| | Application assistant | Your own assistant via MCP |
|---|---|---|
| **Where the model reasons** | In Teramot, with the model providers that Teramot contracts | In your assistant (Claude, ChatGPT, Copilot, or another), with your provider and your contract |
| **Available tools** | The same tools that the MCP server exposes | The MCP server's tools |
| **Permissions** | Those of the connected user | Those of the connected user |
| **Where results go** | To Teramot's model provider | To your model provider |

Teramot's MCP server **does not use language models**. It only runs the tools that your assistant asks it to. See [Ways to consume data](/architecture/consumption/).

The application assistant also has a **topic filter** that can reject requests unrelated to data analysis.

## Controls on what the AI can run

- **Read-only queries**: any query run by an agent or a user is parsed and only accepted if it is a single read statement.
- **Project scope**: queries can only read tables from the active project, or tables that are explicitly shared.
- **Paginated results with a time limit**: conversational queries return results in pages and have a maximum execution time.
- **Role-based permissions**: creating or modifying results tables, launching refreshes, or correcting transformations requires the corresponding role. See [Roles](/architecture/security/#roles-and-permissions).
- **Activity log**: changes made from the assistant or via MCP are recorded in the project's activity log, under the name of the user who requested them.

## Model providers

| Provider | Use | Mode |
|---|---|---|
| **Anthropic** (Claude models) | Data agents and the application assistant | Anthropic API and Amazon Bedrock |
| **OpenAI** (GPT models) | Data agents, as an alternative provider | OpenAI API |

Data agents have **automatic failover between providers**: if one does not respond, the request goes to another. The specific model behind each agent may change over time as better models become available.

## AI traceability

To debug and improve the quality of the agents, Teramot records execution traces (what goes into the model and what comes out) in AI observability services:

| Service | What it receives |
|---|---|
| **LangSmith** | Traces from the data agents and the application assistant |
| **Langfuse** | Traces from the MCP server tools |

Traces may include schemas, data samples, and query results. They are kept for 14 days and are included in the deletion procedure when the contract ends. See [Retention and deletion](/architecture/retention/).
