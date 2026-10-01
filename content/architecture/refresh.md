---
title: "Refresh and incremental loading"
weight: 120
---

## Refresh frequency

Each project has one refresh schedule, which refreshes all its sources, and any source can
also be refreshed by hand. The schedule options, and which plan includes each one, are in
[Refresh your data](/product/use-the-app/refresh/).

> [!TIP]
> **Choosing the frequency**
>
> The frequency determines how much data is moved. A large table that is fully reloaded every hour is moved 24 times per day. For most business analyses, a daily refresh is enough. If you need a higher frequency, we recommend combining it with incremental loading.

## Load strategies

Each table is refreshed with one of these strategies:

| Strategy | How it works | When to use it |
|---|---|---|
| **Full load** | The entire table is read again and replaced. | Small or medium tables, or tables without columns that indicate changes. |
| **Incremental load** | Only the new or modified rows since the last load are read, and they are merged with the existing ones by key. | Large tables that change little relative to their size. |
| **Rolling window** | A recent period (for example, the last 30 days) is read again and that period is replaced. | Tables where recent records are still being modified and old ones are not. |
| **Header delta (SAP)** | Documents whose header changed are read, with all of their line items. | SAP document tables. |
| **Full re-read with merge** | Everything is read again and merged by key. | SaaS applications that do not expose a modification date. |

You can always force a **one-off full reload** of an incremental table, for example after a mass correction in the source.

## Requirements for incremental loading

For a table to be loaded incrementally, it needs:

1. **A unique key**: a column, or a combination of columns, that identifies each row.
2. **A modification column**: a datetime (or an increasing value) that is updated every time the row changes, for example `updated_at` or `fecha_modificacion`.

In addition:

- Each incremental read **overlaps the previous one** by a few minutes, so that changes committed late in the source are not missed.
- If the table has a **soft-delete** column (for example, `deleted = true`), those deletions are reflected in the processed data.

> [!WARNING]
> **Hard deletes**
>
> Incremental loading **does not detect rows that were physically deleted** in the source, because they are no longer there to be read. If the source deletes rows instead of flagging them, we recommend scheduling a periodic full reload or using a rolling window.

## Strategies available by source type

| Source type | Strategies |
|---|---|
| Databases and warehouses (PostgreSQL, Oracle, SQL Server, Databricks, Snowflake, BigQuery, and others) | Full load, incremental load, rolling window |
| SAP ECC (RFC) | Full load, incremental load, header delta, rolling window |
| Salesforce, HubSpot, Odoo, MongoDB | Full load, incremental load |
| Monday.com, Airtable | Full re-read with merge |
| Amazon S3, files, Google Sheets, OneDrive | Full load |

## What happens after extraction

Processed data is refreshed in the same way as raw data: in incremental tables, only the changes are merged, keeping the most recent version of each row. The results tables that depend on it are then recalculated. See [Data flow](/architecture/data-flow/#3-refreshes).
