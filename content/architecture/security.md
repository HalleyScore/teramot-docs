---
title: "Security and access control"
weight: 90
---

This page describes how Teramot controls who can access what, and how the platform is protected. Teramot's formal commitments in this area are in [Security and confidentiality commitments](/compliance/Transparency/security-commitments/), and the status of certifications is in [Compliance](/compliance/about/).

## Authentication

- Sign-in is delegated to a **managed identity provider** compatible with OpenID Connect, using the authorization code flow with PKCE.
- On every request, the API validates the signature, issuer, audience, and subject of each token.
- External assistants authenticate with **OAuth 2.1**. See [Ways to consume data](/architecture/consumption/#ai-assistants-via-mcp).
- API keys and MCP access keys are stored as hashes.

## Roles and permissions

Every member of a workspace has one of four roles: **Owner**, **Admin**, **Analyst** and
**Read only**, each including what the ones below it can do. A person can also hold a role
in a single project, which takes precedence over their workspace role there; someone
invited only to a project sees that project and nothing else of the workspace. What each
role can do, action by action, is in
[Roles and permissions](/product/concepts/roles-and-permissions/).

Permissions are enforced in the API, which is the only entry point to the data. That is
why they apply equally in the web application, to an AI assistant via MCP, and in
integrations.

### Teramot staff access

Teramot staff do not access customers' business data during normal operation. When access is technically necessary to operate the platform or provide support, it is limited to authorized personnel and the actions are logged.

## Activity log

Each project has an **activity log**, visible to admins. It records the actions that modify the project, with author, action, and date, regardless of whether they were made from the web application, the API, or an assistant via MCP.

Read queries are not recorded in this log.

## Platform protection

| Area | Control |
|---|---|
| **Network** | Processing services and databases run in private subnets, with no direct access from the Internet. Only the load balancers and the CDN receive public traffic. |
| **Encryption in transit** | TLS 1.2 at a minimum and TLS 1.3 available on public endpoints; HTTP is redirected to HTTPS. Mutual TLS between internal services. |
| **Encryption at rest** | AES-256 in object storage, databases, and volumes. |
| **Source credentials** | Stored encrypted at rest, used only at connection time, not written to logs, and never returned by the API. |
| **Web application** | Strict Content Security Policy (CSP), HSTS, and protection against being embedded in other sites. |
| **Threat detection** | Continuous detection across the cloud account, network, storage, and services, with alerts to the security team. |
| **Infrastructure auditing** | Every cloud API call is recorded in an immutable log with integrity validation. Network and service logs are retained for 365 days. |
| **Changes** | All infrastructure is defined as code. Each change goes through review and is deployed first to development and staging. |
| **Continuity** | Databases with daily backups, a replica in a second availability zone, and deletion protection. |

## Providers that process data

| Provider | Function | What data it receives |
|---|---|---|
| **Amazon Web Services** | Infrastructure, storage, processing, and inference (Amazon Bedrock) | All service data |
| **Anthropic** | Language models | What is described in [AI agents](/architecture/ai-agents/) |
| **OpenAI** | Language models | What is described in [AI agents](/architecture/ai-agents/) |
| **LangSmith** | AI observability | Agent traces |
| **Langfuse** | AI observability | MCP tool traces |
| **Temporal Cloud** | Workflow orchestration | Execution metadata |
| **Identity provider (Logto)** | Authentication | Users' account data |
| **Sentry** | Error monitoring | Technical error information |
| **Stripe** | Billing | Billing data |
| **Microsoft Clarity** | Web application usage analytics | Browsing data in the application |
