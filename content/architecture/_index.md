---
title: "Teramot technical architecture"
linkTitle: "Overview"
weight: 20
cascade:
  type: docs
# The Getting Started section was removed; its URLs redirect here.
aliases:
  - /getting-started/
  - /getting-started/getting-started/
  - /getting-started/poc-guide/
  - /getting-started/model-deployment/
  - /getting-started/faq/
  - /getting-started/multi-tenant-deployment/
---

This section explains how Teramot works under the hood. It covers what the platform does, how data moves through it, which transformations are applied, where data is stored, and who can access it.

It is written for the IT, data, architecture, and security teams that are evaluating Teramot or already use it, and you can use it as a reference document.

## What Teramot does

Teramot is an AI-assisted data engineering platform. It solves a specific problem: bringing data scattered across many systems (databases, ERPs, data warehouses, SaaS applications, and files) into a single, clean, queryable place, without your organization having to build or maintain pipelines.

In practice, Teramot:

1. **Connects** to your source systems with read-only credentials.
2. **Copies** the tables you choose into storage dedicated to your project, with scheduled updates.
3. **Cleans and normalizes** each table with AI agents, and validates every transformation before applying it.
4. **Builds results tables**: metrics, cross-system joins, and reports defined in natural language or SQL.
5. **Serves** that data through the web application, a conversational assistant, external AI assistants via MCP (Claude, ChatGPT, Copilot, among others), and exports.

## Core concepts

| Concept | What it is |
|---|---|
| **Workspace** | Your organization's space. It groups projects, members, and connections. It is the main access boundary. |
| **Project** | A unit of work within a workspace, for example "Sales" or "Supply chain". Each project has its own storage and its own table catalog, isolated from the others. |
| **Source** | A connection to a source system, such as an Oracle database, a Databricks workspace, or a Salesforce account. |
| **Raw data** | The faithful copy of the source tables, exactly as they arrive. |
| **Processed data** | The same tables, cleaned and with consistent types. This is the foundation you work on. |
| **Results tables** | Saved, recalculable analyses built on top of processed data: a metric, a join across systems, or a report. |
| **Dashboard** | A visualization built on top of results tables. |
| **Project knowledge** | Business documentation for the project (definitions, rules, glossary) that agents use to answer with context. |

## How to read this section

| If you need to know… | Go to |
|---|---|
| Which components the platform has and where they run | [Platform architecture](/architecture/platform/) |
| The path of a piece of data from the source to an answer | [Data flow](/architecture/data-flow/) |
| What changes are made to the data | [Transformations](/architecture/transformations/) |
| Where the data is stored and in what format | [Where your data lives](/architecture/data-storage/) |
| What we store, what we share with third parties, and for how long | [What we store and share](/architecture/data-handling/) |
| What the AI does and what information it receives | [AI agents](/architecture/ai-agents/) |
| How the data is queried | [Ways to consume data](/architecture/consumption/) |
| Authentication, roles, encryption, and auditing | [Security and access control](/architecture/security/) |
| How to connect systems that are on a private network | [Connectivity to your sources](/architecture/connectivity/) |
| Which user and permissions to create on each source system | [Preparing your sources](/architecture/source-setup/) |
| Refresh frequencies and incremental loading | [Refresh and incremental loading](/architecture/refresh/) |
| How long data is kept and how it is deleted | [Retention and deletion](/architecture/retention/) |
| Which systems you can connect | [Connector catalog](/architecture/connectors/) |

> [!NOTE]
> **Related documentation**
>
> - [MCP server reference](/product/mcp/overview/): how to connect AI assistants to Teramot.
> - [Security and confidentiality commitments](/compliance/Transparency/security-commitments/).
> - [Compliance](/compliance/about/): SOC 2 and security policies.
