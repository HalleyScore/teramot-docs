---
title: "Catálogo de conectores"
weight: 140
---

Estos son algunos de los sistemas que se pueden conectar desde la aplicación. Todos se configuran de forma autónoma desde **Fuentes**, sin desarrollo a medida. El catálogo crece de forma continua. Los métodos de conexión se describen en [Conectividad con las fuentes](/es/architecture/connectivity/).

## Bases de datos relacionales

| Sistema | Autenticación | Incremental |
|---|---|---|
| PostgreSQL | Usuario y contraseña | Sí |
| MySQL | Usuario y contraseña | Sí |
| MariaDB | Usuario y contraseña | Sí |
| Microsoft SQL Server | Usuario y contraseña | Sí |
| Azure SQL Database | Usuario y contraseña | Sí |
| Oracle | Usuario y contraseña, con service name o SID | Sí |
| SAP HANA | Usuario y contraseña | Sí |
| Teradata | Usuario y contraseña | Sí |
| ClickHouse | Usuario y contraseña | Sí |
| Amazon Redshift | Usuario y contraseña | Sí |

En las bases de datos relacionales se pueden incorporar **tablas y vistas**; en PostgreSQL y Redshift, también vistas materializadas.

## Data warehouses y plataformas de datos

| Sistema | Autenticación | Qué se configura | Incremental |
|---|---|---|---|
| **Databricks** | Token de acceso | Host del SQL warehouse, HTTP path y catálogo de Unity Catalog | Sí |
| **Snowflake** | Usuario y contraseña | Cuenta, warehouse y rol (opcional) | Sí |
| **Google BigQuery** | Cuenta de servicio (JSON) u OAuth de Google | Proyecto de Google Cloud | Sí |

## ERP

| Sistema | Autenticación | Qué se configura | Incremental |
|---|---|---|---|
| **SAP ECC (RFC)** | Usuario y contraseña, con SNC opcional | Servidor de aplicación o message server; lectura de tablas por RFC | Sí, incluido delta por cabecera de documento |
| **Odoo** | Clave de API | URL y base de datos | Sí |

## Aplicaciones SaaS y bases NoSQL

| Sistema | Autenticación | Qué trae | Incremental |
|---|---|---|---|
| **Salesforce** | Usuario, contraseña y token de seguridad | Objetos de Salesforce | Sí |
| **HubSpot** | OAuth | Contactos, empresas, negocios y tickets | Sí |
| **Monday.com** | Token de API | Tableros | Relectura con combinación |
| **Airtable** | Token de acceso | Bases y tablas | Relectura con combinación |
| **MongoDB** | URI de conexión o credenciales; TLS y certificados X.509 | Colecciones | Sí |

## Archivos y almacenamiento

| Sistema | Autenticación | Qué trae | Incremental |
|---|---|---|---|
| **Carga de archivos** | Sesión del usuario | CSV, Parquet, Excel (XLSX y XLS) | No aplica |
| **Amazon S3** | Ruta del bucket | Archivos CSV, Parquet y Excel | Completa |
| **Google Sheets** | OAuth de Google | Una hoja de cálculo o una carpeta | Completa |
| **Microsoft OneDrive** | OAuth de Microsoft | Un archivo o una carpeta | Completa |

## Datos de otro proyecto

Un proyecto puede usar tablas de otro proyecto del mismo workspace mediante un **data share**, sin volver a extraerlas del origen. Lo crea un administrador y puede tener fecha de vencimiento.

## Sistemas que no están en la lista

La arquitectura de conectores está pensada para sumar sistemas nuevos con facilidad. Si el sistema que necesita no aparece en esta lista, consúltenos.

Mientras tanto, cualquier sistema que pueda exportar sus datos a una base de datos, a un bucket de S3 o a archivos se puede incorporar con los conectores existentes.
