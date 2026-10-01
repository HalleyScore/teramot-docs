---
title: "Connector catalog"
weight: 140
---

Teramot connects to relational databases, warehouses (Databricks, Snowflake, BigQuery), SAP ECC and Odoo, SaaS applications such as Salesforce and HubSpot, MongoDB, Amazon S3, Google Sheets, OneDrive, and uploaded files. All of them are configured self-service from **Sources**, with no custom development, and the catalog grows continuously.

- The complete list, with what each connector asks for: [Connect your data](/product/connect-data/overview/#supported-connectors).
- How each one reaches your network: [Connectivity to your sources](/architecture/connectivity/).
- Which ones load incrementally: [Refresh and incremental loading](/architecture/refresh/#strategies-available-by-source-type).

In relational databases you can bring in **tables and views**; in PostgreSQL and Redshift, also materialized views.

## Data from another project

A project can read tables of another project, in the same workspace or another one, through a **data share**, without extracting them from the source again. An admin of the project that shares creates it. See [Data Shares](/product/use-the-app/data-shares/).

## Systems that are not on the list

The connector architecture is designed to add new systems easily. If the system you need does not appear on the list, contact us.

In the meantime, any system that can export its data to a database, an S3 bucket, or files can be brought in with the existing connectors.
