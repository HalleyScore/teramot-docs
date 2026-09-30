---
title: "Actualización e incremental"
weight: 120
---

## Frecuencia de actualización

Cada proyecto tiene una programación de actualización configurable:

| Opción | Ejemplos |
|---|---|
| **Diaria** | Todos los días a las 07:00 |
| **Semanal** | Los lunes a las 06:00 |
| **Mensual** | El día 1 de cada mes |
| **Cada N horas** | Cada 1 a 23 horas |
| **Expresión cron** | Cualquier programación personalizada, con un máximo de una ejecución por hora |

La zona horaria se define en la programación. También se puede programar una actualización única para una fecha y hora, o lanzar una actualización manual en cualquier momento.

Algunas opciones, como la carga incremental y las expresiones cron, dependen del plan contratado.

> [!TIP]
> **Elegir la frecuencia**
>
> La frecuencia define cuánto dato se mueve. Una tabla grande que se recarga completa cada hora se mueve 24 veces por día. Para la mayoría de los análisis de negocio alcanza con una actualización diaria. Si hace falta más frecuencia, lo recomendable es combinarla con carga incremental.

## Estrategias de carga

Cada tabla se actualiza con una de estas estrategias:

| Estrategia | Cómo funciona | Cuándo conviene |
|---|---|---|
| **Completa** | Se vuelve a leer toda la tabla y se reemplaza. | Tablas chicas o medianas, o sin columnas que indiquen cambios. |
| **Incremental** | Se leen solo las filas nuevas o modificadas desde la última carga, y se combinan con las existentes por clave. | Tablas grandes que cambian poco en proporción a su tamaño. |
| **Ventana móvil** | Se vuelve a leer un período reciente (por ejemplo, los últimos 30 días) y se reemplaza ese período. | Tablas donde los registros recientes todavía se modifican y los viejos no. |
| **Delta por cabecera (SAP)** | Se leen los documentos cuya cabecera cambió, con todas sus posiciones. | Tablas de documentos de SAP. |
| **Relectura con combinación** | Se vuelve a leer todo y se combina por clave. | Aplicaciones SaaS que no exponen fecha de modificación. |

Siempre se puede forzar una **recarga completa puntual** de una tabla incremental, por ejemplo después de una corrección masiva en el origen.

## Requisitos para la carga incremental

Para que una tabla se pueda cargar de forma incremental, necesita:

1. **Una clave única**: una columna, o una combinación de columnas, que identifique cada fila.
2. **Una columna de modificación**: una fecha-hora (o un valor creciente) que se actualice cada vez que la fila cambia, por ejemplo `updated_at` o `fecha_modificacion`.

Además:

- Cada lectura incremental **se superpone con la anterior** unos minutos, para no perder cambios que se confirmaron tarde en el origen.
- Si la tabla tiene una columna de **borrado lógico** (por ejemplo, `deleted = true`), esos borrados se reflejan en los datos procesados.

> [!WARNING]
> **Borrados físicos**
>
> La carga incremental **no detecta filas borradas físicamente** en el origen, porque ya no están para leerlas. Si el origen borra filas en lugar de marcarlas, conviene programar una recarga completa periódica o usar una ventana móvil.

## Estrategias disponibles por tipo de fuente

| Tipo de fuente | Estrategias |
|---|---|
| Bases de datos y warehouses (PostgreSQL, Oracle, SQL Server, Databricks, Snowflake, BigQuery y otros) | Completa, incremental, ventana móvil |
| SAP ECC (RFC) | Completa, incremental, delta por cabecera, ventana móvil |
| Salesforce, HubSpot, Odoo, MongoDB | Completa, incremental |
| Monday.com, Airtable | Relectura con combinación |
| Amazon S3, archivos, Google Sheets, OneDrive | Completa |

## Qué pasa después de extraer

Los datos procesados se actualizan de la misma forma que los crudos: en las tablas incrementales se combinan solo los cambios, conservando la versión más reciente de cada fila. Después se recalculan las tablas de resultados que dependen de ellos. Ver [Flujo de los datos](/es/architecture/data-flow/#3-actualizaciones).
