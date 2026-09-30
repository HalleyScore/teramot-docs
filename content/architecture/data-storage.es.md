---
title: "Dónde viven los datos"
weight: 50
# The Getting Started section was removed; its URLs redirect here.
aliases:
  - /getting-started/aws-bucket-setup/
---

## Ubicación

Todos los datos de clientes se guardan en **Amazon Web Services, región us-east-1** (Norte de Virginia, EE. UU.). Teramot no replica datos de clientes a otras regiones.

## Qué se guarda y dónde

| Información | Dónde | Formato |
|---|---|---|
| Datos crudos, procesados y tablas de resultados | Data lake en Amazon S3 | Apache Iceberg (archivos Parquet) |
| Esquemas y ubicación de las tablas | AWS Glue Data Catalog | Una base de datos por proyecto |
| Configuración: workspaces, proyectos, miembros, fuentes, tablas de resultados, dashboards | Amazon Aurora PostgreSQL | Base de datos relacional |
| Credenciales de acceso a los sistemas de origen | Base de datos de la plataforma | Cifradas en reposo; la API nunca las devuelve |
| Estado de las ejecuciones de los workflows | Orquestador de workflows (Temporal Cloud) | Metadatos de ejecución |
| Registros técnicos (logs) | Amazon CloudWatch | Retenidos 365 días |

## Formato abierto

Las tablas se guardan en **Apache Iceberg**, un formato de tabla abierto y estándar de la industria, sobre archivos **Parquet**. Esto implica que:

- Los datos **no quedan atados a Teramot**. Iceberg y Parquet se pueden leer con Spark, Trino, Athena, Snowflake, Databricks, DuckDB y otros motores.
- Las escrituras son **transaccionales**: una tabla nunca queda en un estado intermedio.
- Cada tabla mantiene **versiones recientes** (snapshots). Si una carga sale mal, se puede volver a la versión anterior. Ver [Retención](/es/architecture/retention/).

## Aislamiento entre clientes y proyectos

Cada proyecto tiene:

- Un **prefijo propio** dentro del almacenamiento.
- Una **base de datos propia** en el catálogo.

El acceso a los datos siempre pasa por la API de Teramot, que:

1. Resuelve el proyecto **a partir de la identidad del usuario, en el servidor**. El cliente nunca envía un identificador de tenant.
2. Verifica que el usuario tenga el rol necesario en ese proyecto.
3. Analiza cada consulta SQL antes de ejecutarla. Solo acepta **una sentencia de solo lectura**, y la rechaza si hace referencia a bases de datos de otro proyecto.

Un proyecto puede leer tablas de otro proyecto únicamente mediante un **data share** explícito, creado por un administrador y con vencimiento opcional.

## Cifrado

- **En reposo**: el almacenamiento de objetos y las bases de datos se cifran con AES-256.
- **En tránsito**: TLS 1.2 como mínimo en todos los endpoints públicos, con TLS 1.3 disponible. Las comunicaciones internas entre servicios del plano de control usan TLS mutuo.

Ver [Seguridad y control de acceso](/es/architecture/security/) para más detalle.
