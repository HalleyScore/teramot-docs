---
title: "Retention and deletion"
weight: 130
---

## How long data is kept

| Information | Retention |
|---|---|
| Raw data, processed data, and results tables | For as long as the source or project exists, during the term of the contract |
| Previous versions of each table (snapshots) | 3 days; the current version is always kept |
| Metadata database backups | 7 days |
| AI agent traces | 14 days |
| Project activity log | Viewable in the application for the last 90 days |
| Infrastructure and network technical logs | 365 days |

Teramot keeps **the most recent version** of each table, plus a short history that allows a failed load to be rolled back. It is not a historical archive of the source. If you need to preserve the history of changes, you can build results tables that accumulate it.

## What happens on deletion

### A source

1. Running executions for that source are canceled.
2. Its raw and processed tables are deleted, along with their files in storage.
3. The results tables that depended on it are marked as **outdated**, so that the user can review them.

If deletion fails midway, the source stays marked as deleted and the deletion can be retried.

### A project

Its results tables, sources, data shares, **its entire space in storage**, its database in the catalog, and its schedule are deleted.

### A workspace

Deletion propagates to all of its projects. If the workspace has active IPsec private connections, they must be deleted first.

## End of contract

When the contract ends, Teramot runs a **documented deletion procedure**. It covers object storage, the data catalog, application metadata, usage records, and traces, and ends with a **written confirmation of destruction**. See [Security and confidentiality commitments](/compliance/Transparency/security-commitments/).

While the contract is in effect, you can export your results tables as CSV from the application or via MCP.
