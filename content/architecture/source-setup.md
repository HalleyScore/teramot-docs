---
title: "Preparing your sources"
weight: 110
# The Getting Started section was removed; its URLs redirect here.
aliases:
  - /getting-started/connect-your-data/
---

This page describes what you need to prepare on each source system before connecting it: the user, the minimum permissions, and the details the form asks for. The scripts are examples to adapt: replace the database, schema, user, and password names with your own.

For network access (IPsec, SSH, or IP allowlist) and ports, see [Connectivity to your sources](/architecture/connectivity/).

## General recommendations

- **A dedicated user for Teramot.** It makes it easier to audit its queries and to revoke access without affecting other systems.
- **Read-only.** Teramot only runs read queries on the source: it does not create tables or temporary tables, and it does not modify data.
- **Only what you will bring in.** Grant permissions only on the schemas or tables you plan to bring in. If a table has sensitive columns that are not needed, create a view without them and grant permission on the view.
- **A read replica for critical databases.** If the production database is sensitive to load, connect a read replica.
- **Incremental loading.** It requires a unique key and a modification column in each table. Views have no declared key and are loaded in full. See [Refresh and incremental loading](/architecture/refresh/).

## PostgreSQL

**Form details:** host, port (5432), database, schema (`public` by default), username, and password.

```sql
CREATE USER teramot WITH PASSWORD '<password>';
GRANT CONNECT ON DATABASE <database> TO teramot;
GRANT USAGE ON SCHEMA <schema> TO teramot;
GRANT SELECT ON ALL TABLES IN SCHEMA <schema> TO teramot;
-- So that new tables are also visible:
ALTER DEFAULT PRIVILEGES IN SCHEMA <schema> GRANT SELECT ON TABLES TO teramot;
```

Tables, views, and materialized views can be brought in.

## Amazon Redshift

**Form details:** host, port (5439), database, schema, username, and password. The connection uses TLS by default.

```sql
CREATE USER teramot PASSWORD '<password>';
GRANT USAGE ON SCHEMA <schema> TO teramot;
GRANT SELECT ON ALL TABLES IN SCHEMA <schema> TO teramot;
ALTER DEFAULT PRIVILEGES IN SCHEMA <schema> GRANT SELECT ON TABLES TO teramot;
```

## MySQL and MariaDB

**Form details:** host, port (3306), database, username, and password. The tables and views of the given database are discovered.

```sql
CREATE USER 'teramot'@'%' IDENTIFIED BY '<password>';
GRANT SELECT, SHOW VIEW ON <database>.* TO 'teramot'@'%';
```

If access is through an IP allowlist, you can replace `'%'` with each of the [Teramot egress IPs](/architecture/connectivity/#internet-access-with-an-ip-allowlist).

## SQL Server and Azure SQL Database

**Form details:** host, port (1433), database, schema, username, and password.

```sql
-- In master (SQL Server) or in the database (contained user in Azure SQL):
CREATE LOGIN teramot WITH PASSWORD = '<password>';

-- In the source database:
CREATE USER teramot FOR LOGIN teramot;
GRANT SELECT ON SCHEMA::<schema> TO teramot;
GRANT VIEW DEFINITION ON SCHEMA::<schema> TO teramot;
```

`VIEW DEFINITION` allows reading primary keys and indexes, which are used for incremental loading. If you set encryption as required (`require`), Teramot checks that the session is encrypted and also needs `VIEW SERVER STATE` (in Azure SQL, `VIEW DATABASE STATE`).

## Oracle

**Form details:** host, port (1521), service name or SID, **schema**, username, and password.

```sql
CREATE USER teramot IDENTIFIED BY "<password>";
GRANT CREATE SESSION TO teramot;
-- One statement per table to bring in:
GRANT SELECT ON <schema>.<table> TO teramot;
```

> [!TIP]
> **The schema is the owner of the tables**
>
> In Oracle, the schema is the user that owns (`OWNER`) the tables, not the user Teramot connects with. Enter it in the form: if it is left empty, only the Teramot user's own tables are visible, and that user normally has none.

Neither `SELECT_CATALOG_ROLE` nor access to the `DBA_*` views is needed: Teramot reads the catalog through the `ALL_*` views, which show exactly the granted tables.

The direct connection to Oracle does not use TLS. For systems that are not on a private network, we recommend [IPsec or an SSH tunnel](/architecture/connectivity/).

## SAP HANA

**Form details:** host, port (30015), database, schema, username, and password. Tables are brought in, not views.

```sql
CREATE USER TERAMOT PASSWORD "<password>" NO FORCE_FIRST_PASSWORD_CHANGE;
GRANT SELECT ON SCHEMA <SCHEMA> TO TERAMOT;
```

## Teradata

**Form details:** host, port (1025), database, username, and password.

```sql
CREATE USER teramot AS PERM = 0, PASSWORD = "<password>";
GRANT SELECT ON <database> TO teramot;
```

## Databricks

**Form details:** SQL warehouse host, HTTP path, access token, Unity Catalog catalog, and schema.

We recommend creating a **service principal** for Teramot, generating its token, and granting it:

```sql
GRANT USE CATALOG ON CATALOG <catalog> TO `<service-principal>`;
GRANT USE SCHEMA, SELECT ON SCHEMA <catalog>.<schema> TO `<service-principal>`;
```

The service principal also needs the **CAN USE** permission on the SQL warehouse.

## Snowflake

**Form details:** account, username, password, warehouse, database, schema, and role (optional).

```sql
CREATE ROLE teramot;
GRANT USAGE ON WAREHOUSE <warehouse> TO ROLE teramot;
GRANT USAGE ON DATABASE <database> TO ROLE teramot;
GRANT USAGE ON SCHEMA <database>.<schema> TO ROLE teramot;
GRANT SELECT ON ALL TABLES IN SCHEMA <database>.<schema> TO ROLE teramot;
GRANT SELECT ON ALL VIEWS IN SCHEMA <database>.<schema> TO ROLE teramot;
GRANT SELECT ON FUTURE TABLES IN SCHEMA <database>.<schema> TO ROLE teramot;

CREATE USER teramot PASSWORD = '<password>' DEFAULT_ROLE = teramot DEFAULT_WAREHOUSE = <warehouse>;
GRANT ROLE teramot TO USER teramot;
```

## Google BigQuery

**Form details:** Google Cloud project, dataset, and a service account (JSON file), or authorization with a Google account.

The service account or user needs these roles:

| Role | Where | Purpose |
|---|---|---|
| `roles/bigquery.dataViewer` | Source dataset | Read the tables and their schema |
| `roles/bigquery.jobUser` | Project | Run the read queries |
| `roles/bigquery.readSessionUser` | Project | Optional: faster reads with the Storage Read API |

Teramot does not write to your datasets.

## MongoDB

**Form details:** a connection URI, or host, port (27017), username, and password. TLS, CA and client certificates, and X.509 authentication are supported.

```javascript
use <database>
db.createUser({
  user: "teramot",
  pwd: "<password>",
  roles: [{ role: "read", db: "<database>" }]
})
```

## SAP ECC (RFC)

**Form details:** client, username, password, and language. For the server, an application server (host and system number) or a message server (host, group, and system ID). SNC is optional.

Teramot reads tables over RFC, with the standard function module `RFC_READ_TABLE`. The communication user (*System* or *Communication* type) needs:

- **S_RFC**: to run the `RFC_PING`, `RFC_READ_TABLE`, and `EM_GET_NUMBER_OF_ENTRIES` modules.
- **S_TABU_NAM** (or **S_TABU_DIS**) with display activity: on the tables to bring in and on the dictionary tables `DD02L`, `DD03L`, `TFDIR`, and `FUPARAREF`.

If your organization uses its own read module (for example `ZRFC_READ_TABLE`), it can be set in the source configuration.

## SaaS applications and files

Salesforce, HubSpot, Odoo, Monday.com, Airtable, Google Sheets, and OneDrive are connected with OAuth or an access token from the form, with no prior preparation on the system. See the [connector catalog](/architecture/connectors/).
