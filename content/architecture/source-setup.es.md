---
title: "Preparar las fuentes"
weight: 110
# The Getting Started section was removed; its URLs redirect here.
aliases:
  - /getting-started/connect-your-data/
---

Esta página describe qué tiene que preparar el cliente en cada sistema de origen antes de conectarlo: el usuario, los permisos mínimos y los datos que pide el formulario. Los scripts son ejemplos para adaptar: reemplace los nombres de base, esquema, usuario y contraseña por los propios.

Para el acceso de red (IPsec, SSH o lista blanca de IP) y los puertos, ver [Conectividad con las fuentes](/es/architecture/connectivity/).

## Recomendaciones generales

- **Un usuario dedicado para Teramot.** Facilita auditar sus consultas y revocar el acceso sin afectar a otros sistemas.
- **Solo lectura.** Teramot solo ejecuta consultas de lectura sobre el origen: no crea tablas, ni tablas temporales, ni modifica datos.
- **Solo lo que se va a incorporar.** Otorgue permisos únicamente sobre los esquemas o tablas que se van a traer. Si una tabla tiene columnas sensibles que no hacen falta, cree una vista sin ellas y otorgue permiso sobre la vista.
- **Réplica de lectura para bases críticas.** Si la base de producción es sensible a la carga, conecte una réplica de lectura.
- **Carga incremental.** Requiere una clave única y una columna de modificación en cada tabla. Las vistas no tienen clave declarada y se cargan completas. Ver [Actualización y carga incremental](/es/architecture/refresh/).

## PostgreSQL

**Datos del formulario:** host, puerto (5432), base de datos, esquema (por defecto `public`), usuario y contraseña.

```sql
CREATE USER teramot WITH PASSWORD '<contraseña>';
GRANT CONNECT ON DATABASE <base> TO teramot;
GRANT USAGE ON SCHEMA <esquema> TO teramot;
GRANT SELECT ON ALL TABLES IN SCHEMA <esquema> TO teramot;
-- Para que las tablas nuevas también sean visibles:
ALTER DEFAULT PRIVILEGES IN SCHEMA <esquema> GRANT SELECT ON TABLES TO teramot;
```

Se pueden incorporar tablas, vistas y vistas materializadas.

## Amazon Redshift

**Datos del formulario:** host, puerto (5439), base de datos, esquema, usuario y contraseña. La conexión usa TLS por defecto.

```sql
CREATE USER teramot PASSWORD '<contraseña>';
GRANT USAGE ON SCHEMA <esquema> TO teramot;
GRANT SELECT ON ALL TABLES IN SCHEMA <esquema> TO teramot;
ALTER DEFAULT PRIVILEGES IN SCHEMA <esquema> GRANT SELECT ON TABLES TO teramot;
```

## MySQL y MariaDB

**Datos del formulario:** host, puerto (3306), base de datos, usuario y contraseña. Se descubren las tablas y vistas de la base indicada.

```sql
CREATE USER 'teramot'@'%' IDENTIFIED BY '<contraseña>';
GRANT SELECT, SHOW VIEW ON <base>.* TO 'teramot'@'%';
```

Si el acceso es por lista blanca de IP, puede reemplazar `'%'` por cada una de las [IP de salida de Teramot](/es/architecture/connectivity/#acceso-por-internet-con-lista-blanca-de-ip).

## SQL Server y Azure SQL Database

**Datos del formulario:** host, puerto (1433), base de datos, esquema, usuario y contraseña.

```sql
-- En master (SQL Server) o en la base (usuario contenido en Azure SQL):
CREATE LOGIN teramot WITH PASSWORD = '<contraseña>';

-- En la base de origen:
CREATE USER teramot FOR LOGIN teramot;
GRANT SELECT ON SCHEMA::<esquema> TO teramot;
GRANT VIEW DEFINITION ON SCHEMA::<esquema> TO teramot;
```

`VIEW DEFINITION` permite leer las claves primarias e índices, que se usan para la carga incremental. Si configura el cifrado como obligatorio (`require`), Teramot verifica que la sesión esté cifrada y necesita además `VIEW SERVER STATE` (en Azure SQL, `VIEW DATABASE STATE`).

## Oracle

**Datos del formulario:** host, puerto (1521), nombre de servicio o SID, **esquema**, usuario y contraseña.

```sql
CREATE USER teramot IDENTIFIED BY "<contraseña>";
GRANT CREATE SESSION TO teramot;
-- Una sentencia por tabla a incorporar:
GRANT SELECT ON <esquema>.<tabla> TO teramot;
```

> [!TIP]
> **El esquema es el dueño de las tablas**
>
> En Oracle, el esquema es el usuario dueño (`OWNER`) de las tablas, no el usuario con el que se conecta Teramot. Indíquelo en el formulario: si queda vacío, solo se ven las tablas propias del usuario de Teramot, que normalmente no tiene ninguna.

No hace falta `SELECT_CATALOG_ROLE` ni acceso a las vistas `DBA_*`: Teramot lee el catálogo por las vistas `ALL_*`, que muestran exactamente las tablas otorgadas.

La conexión directa a Oracle no usa TLS. Para sistemas que no están en una red privada, se recomienda [IPsec o un túnel SSH](/es/architecture/connectivity/).

## SAP HANA

**Datos del formulario:** host, puerto (30015), base de datos, esquema, usuario y contraseña. Se incorporan tablas, no vistas.

```sql
CREATE USER TERAMOT PASSWORD "<contraseña>" NO FORCE_FIRST_PASSWORD_CHANGE;
GRANT SELECT ON SCHEMA <ESQUEMA> TO TERAMOT;
```

## Teradata

**Datos del formulario:** host, puerto (1025), base de datos, usuario y contraseña.

```sql
CREATE USER teramot AS PERM = 0, PASSWORD = "<contraseña>";
GRANT SELECT ON <base> TO teramot;
```

## Databricks

**Datos del formulario:** host del SQL warehouse, HTTP path, token de acceso, catálogo de Unity Catalog y esquema.

Se recomienda crear un **service principal** para Teramot, generar su token y otorgarle:

```sql
GRANT USE CATALOG ON CATALOG <catálogo> TO `<service-principal>`;
GRANT USE SCHEMA, SELECT ON SCHEMA <catálogo>.<esquema> TO `<service-principal>`;
```

Además, el service principal necesita el permiso **CAN USE** sobre el SQL warehouse indicado.

## Snowflake

**Datos del formulario:** cuenta, usuario, contraseña, warehouse, base de datos, esquema y rol (opcional).

```sql
CREATE ROLE teramot;
GRANT USAGE ON WAREHOUSE <warehouse> TO ROLE teramot;
GRANT USAGE ON DATABASE <base> TO ROLE teramot;
GRANT USAGE ON SCHEMA <base>.<esquema> TO ROLE teramot;
GRANT SELECT ON ALL TABLES IN SCHEMA <base>.<esquema> TO ROLE teramot;
GRANT SELECT ON ALL VIEWS IN SCHEMA <base>.<esquema> TO ROLE teramot;
GRANT SELECT ON FUTURE TABLES IN SCHEMA <base>.<esquema> TO ROLE teramot;

CREATE USER teramot PASSWORD = '<contraseña>' DEFAULT_ROLE = teramot DEFAULT_WAREHOUSE = <warehouse>;
GRANT ROLE teramot TO USER teramot;
```

## Google BigQuery

**Datos del formulario:** proyecto de Google Cloud, dataset y una cuenta de servicio (archivo JSON), o autorización con una cuenta de Google.

La cuenta de servicio o el usuario necesita estos roles:

| Rol | Dónde | Para qué |
|---|---|---|
| `roles/bigquery.dataViewer` | Dataset de origen | Leer las tablas y su esquema |
| `roles/bigquery.jobUser` | Proyecto | Ejecutar las consultas de lectura |
| `roles/bigquery.readSessionUser` | Proyecto | Opcional: lectura más rápida con la Storage Read API |

Teramot no escribe en los datasets del cliente.

## MongoDB

**Datos del formulario:** una URI de conexión, o host, puerto (27017), usuario y contraseña. Se admiten TLS, certificados de CA y de cliente, y autenticación X.509.

```javascript
use <base>
db.createUser({
  user: "teramot",
  pwd: "<contraseña>",
  roles: [{ role: "read", db: "<base>" }]
})
```

## SAP ECC (RFC)

**Datos del formulario:** mandante, usuario, contraseña e idioma. Para el servidor, un servidor de aplicación (host y número de sistema) o un servidor de mensajes (host, grupo e ID de sistema). SNC es opcional.

Teramot lee las tablas por RFC, con el módulo de función estándar `RFC_READ_TABLE`. El usuario de comunicación (tipo *System* o *Communication*) necesita:

- **S_RFC**: ejecutar los módulos `RFC_PING`, `RFC_READ_TABLE` y `EM_GET_NUMBER_OF_ENTRIES`.
- **S_TABU_NAM** (o **S_TABU_DIS**) con actividad de visualización: sobre las tablas a incorporar y sobre las tablas de diccionario `DD02L`, `DD03L`, `TFDIR` y `FUPARAREF`.

Si la organización usa un módulo de lectura propio (por ejemplo `ZRFC_READ_TABLE`), se puede indicar en la configuración de la fuente.

## Aplicaciones SaaS y archivos

Salesforce, HubSpot, Odoo, Monday.com, Airtable, Google Sheets y OneDrive se conectan con OAuth o con un token de acceso desde el formulario, sin preparación previa en el sistema. Ver el [catálogo de conectores](/es/architecture/connectors/).
