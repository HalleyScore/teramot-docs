---
title: "Connector catalog"
weight: 140
---

These are some of the systems you can connect from the application. All of them are configured self-service from **Sources**, with no custom development. The catalog grows continuously. Connection methods are described in [Connectivity to your sources](/architecture/connectivity/).

## Relational databases

| System | Authentication | Incremental |
|---|---|---|
| PostgreSQL | Username and password | Yes |
| MySQL | Username and password | Yes |
| MariaDB | Username and password | Yes |
| Microsoft SQL Server | Username and password | Yes |
| Azure SQL Database | Username and password | Yes |
| Oracle | Username and password, with service name or SID | Yes |
| SAP HANA | Username and password | Yes |
| Teradata | Username and password | Yes |
| ClickHouse | Username and password | Yes |
| Amazon Redshift | Username and password | Yes |

In relational databases you can bring in **tables and views**; in PostgreSQL and Redshift, also materialized views.

## Data warehouses and data platforms

| System | Authentication | What you configure | Incremental |
|---|---|---|---|
| **Databricks** | Access token | SQL warehouse host, HTTP path, and Unity Catalog catalog | Yes |
| **Snowflake** | Username and password | Account, warehouse, and role (optional) | Yes |
| **Google BigQuery** | Service account (JSON) or Google OAuth | Google Cloud project | Yes |

## ERP

| System | Authentication | What you configure | Incremental |
|---|---|---|---|
| **SAP ECC (RFC)** | Username and password, with optional SNC | Application server or message server; table reads over RFC | Yes, including document header delta |
| **Odoo** | API key | URL and database | Yes |

## SaaS applications and NoSQL databases

| System | Authentication | What it brings in | Incremental |
|---|---|---|---|
| **Salesforce** | Username, password, and security token | Salesforce objects | Yes |
| **HubSpot** | OAuth | Contacts, companies, deals, and tickets | Yes |
| **Monday.com** | API token | Boards | Full re-read with merge |
| **Airtable** | Access token | Bases and tables | Full re-read with merge |
| **MongoDB** | Connection URI or credentials; TLS and X.509 certificates | Collections | Yes |

## Files and storage

| System | Authentication | What it brings in | Incremental |
|---|---|---|---|
| **File upload** | User session | CSV, Parquet, Excel (XLSX and XLS) | Not applicable |
| **Amazon S3** | Bucket path | CSV, Parquet, and Excel files | Full |
| **Google Sheets** | Google OAuth | A spreadsheet or a folder | Full |
| **Microsoft OneDrive** | Microsoft OAuth | A file or a folder | Full |

## Data from another project

A project can use tables from another project in the same workspace through a **data share**, without extracting them from the source again. An admin creates it, and it can have an expiration date.

## Systems that are not on the list

The connector architecture is designed to add new systems easily. If the system you need does not appear on this list, contact us.

In the meantime, any system that can export its data to a database, an S3 bucket, or files can be brought in with the existing connectors.
