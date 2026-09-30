---
title: "Platform architecture"
weight: 20
---

Teramot is offered as a service (SaaS) on **Amazon Web Services**, in the **us-east-1** region (N. Virginia, US). All infrastructure is defined as code, and there are separate development, staging, and production environments, each in its own AWS account.

The platform is divided into four blocks:

- **Control plane**: the web application, the API, and the MCP server. It manages users, permissions, projects, sources, and schedules.
- **Data plane**: extracts, transforms, stores, and queries the data.
- **AI services**: the agents that clean data, generate results tables, and answer questions.
- **Consumption channels**: the entry points through which users and systems access the data.

## Overview diagram

![Teramot architecture: customer systems connect over IPsec, SSH, or TLS to the extractors; the data plane, in private subnets, stores data in S3 with Apache Iceberg and transforms it with Amazon Athena; the control plane exposes the API, the web application, and the MCP server to users and AI assistants.](/img/architecture/platform.svg)

## Control plane

The control plane is the part of Teramot that people interact with.

| Component | Function |
|---|---|
| **Web application** | A single-page application served by a CDN (Amazon CloudFront). It includes the conversational assistant, source management, the table explorer, the SQL editor, lineage, dashboards, schedules, and workspace administration. |
| **API** | A service that holds all the business logic and **enforces permissions**. Everything goes through it: the web application, the MCP server, and integrations. |
| **MCP server** | Exposes Teramot's capabilities to external AI assistants using the [Model Context Protocol](https://modelcontextprotocol.io) standard. It has no permissions of its own: each action runs against the API with the identity of the user who requests it. |
| **Metadata database** | Amazon Aurora PostgreSQL. It stores configuration: workspaces, projects, members, source definitions, results tables, dashboards, and activity logs. **It does not store business data**, which lives in the data lake. |
| **Scheduler** | An AWS managed scheduling service triggers the periodic refreshes of each project. |
| **Identity** | A managed identity provider based on OpenID Connect. See [Security](/architecture/security/). |

Control plane services run in containers on Amazon ECS. They are exposed externally only through load balancers with TLS.

## Data plane

The data plane is where data is moved and transformed.

| Component | Function |
|---|---|
| **Workflow orchestrator** | Coordinates each run: extract, validate, transform, build results. It uses [Temporal](https://temporal.io), a durable workflow engine. If a step fails, it is retried without repeating the previous ones. |
| **Extractors** | Read the source tables. They run in serverless functions (AWS Lambda) and, for large loads, in containers (AWS Fargate). They work in private subnets and process data as a stream, without loading it entirely into memory. |
| **Data lake** | Amazon S3, with tables in the open **Apache Iceberg** format on top of Parquet files. See [Where your data lives](/architecture/data-storage/). |
| **Catalog** | AWS Glue Data Catalog registers each table and its schema. Each project has its own database in the catalog. |
| **SQL engine** | Amazon Athena (Trino dialect) runs the transformations and queries. Processed tables and results tables are materialized with `CREATE TABLE AS SELECT` statements. |

All Teramot transformations are **standard SQL over open tables**. There are no opaque processes: every processed or results table has a SQL query that defines it, visible to the user.

## AI services

The AI agents use third-party language models (Anthropic and OpenAI) through their APIs. Teramot does not train its own models or fine-tune on customer data. The details of what each agent does and what information it receives are in [AI agents](/architecture/ai-agents/).

## Service model

Teramot is a **multi-tenant** platform with logical isolation per project. All customers share the infrastructure, but:

- Each project has its **own storage prefix** and its **own database in the catalog**.
- The project's identity is resolved **on the server**, from the user's token. No API operation accepts a tenant identifier sent by the client.
- Each SQL query is parsed before it runs. If it references a database that does not belong to the project, it is rejected.

The platform can also be purchased through **AWS Marketplace**.
