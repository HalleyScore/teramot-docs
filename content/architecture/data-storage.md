---
title: "Where your data lives"
weight: 50
# The Getting Started section was removed; its URLs redirect here.
aliases:
  - /getting-started/aws-bucket-setup/
---

## Location

All customer data is stored in **Amazon Web Services, us-east-1 region** (N. Virginia, US). Teramot does not replicate customer data to other regions.

## What is stored and where

| Information | Where | Format |
|---|---|---|
| Raw data, processed data, and results tables | Data lake on Amazon S3 | Apache Iceberg (Parquet files) |
| Table schemas and locations | AWS Glue Data Catalog | One database per project |
| Configuration: workspaces, projects, members, sources, results tables, dashboards | Amazon Aurora PostgreSQL | Relational database |
| Credentials to access source systems | Platform database | Encrypted at rest; the API never returns them |
| Workflow execution state | Workflow orchestrator (Temporal Cloud) | Execution metadata |
| Technical records (logs) | Amazon CloudWatch | Retained for 365 days |

## Open format

Tables are stored in **Apache Iceberg**, an open, industry-standard table format, on top of **Parquet** files. This means that:

- Your data is **not locked into Teramot**. Iceberg and Parquet can be read with Spark, Trino, Athena, Snowflake, Databricks, DuckDB, and other engines.
- Writes are **transactional**: a table is never left in an intermediate state.
- Each table keeps **recent versions** (snapshots). If a load goes wrong, it can be rolled back to the previous version. See [Retention](/architecture/retention/).

## Isolation between customers and projects

Each project has:

- Its **own prefix** within the storage.
- Its **own database** in the catalog.

Access to data always goes through the Teramot API, which:

1. Resolves the project **from the user's identity, on the server**. The client never sends a tenant identifier.
2. Verifies that the user has the required role in that project.
3. Parses each SQL query before running it. It only accepts **a single read-only statement**, and rejects it if it references databases from another project.

A project can read tables from another project only through an explicit **data share**, created by an admin of the project that shares.

## Encryption

- **At rest**: object storage and databases are encrypted with AES-256.
- **In transit**: TLS 1.2 at a minimum on all public endpoints, with TLS 1.3 available. Internal communications between control plane services use mutual TLS.

See [Security and access control](/architecture/security/) for more detail.
