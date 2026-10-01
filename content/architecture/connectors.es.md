---
title: "Catálogo de conectores"
weight: 140
---

Teramot se conecta a bases de datos relacionales, warehouses (Databricks, Snowflake, BigQuery), SAP ECC y Odoo, aplicaciones SaaS como Salesforce y HubSpot, MongoDB, Amazon S3, Google Sheets, OneDrive y archivos subidos. Todos se configuran de forma autónoma desde **Fuentes**, sin desarrollo a medida, y el catálogo crece de forma continua.

- La lista completa, con lo que pide cada conector: [Conectá tus datos](/es/product/connect-data/overview/#conectores-compatibles).
- Cómo llega cada uno a tu red: [Conectividad con las fuentes](/es/architecture/connectivity/).
- Cuáles cargan de forma incremental: [Actualización e incremental](/es/architecture/refresh/#estrategias-disponibles-por-tipo-de-fuente).

En las bases de datos relacionales se pueden traer **tablas y vistas**; en PostgreSQL y Redshift, también vistas materializadas.

## Datos de otro proyecto

Un proyecto puede leer tablas de otro proyecto, del mismo workspace o de otro, mediante un **data share**, sin volver a extraerlas del origen. Lo crea un admin del proyecto que comparte. Ver [Compartir Datos](/es/product/use-the-app/data-shares/).

## Sistemas que no están en la lista

La arquitectura de conectores está pensada para sumar sistemas nuevos con facilidad. Si el sistema que necesita no aparece en la lista, consúltenos.

Mientras tanto, cualquier sistema que pueda exportar sus datos a una base de datos, a un bucket de S3 o a archivos se puede incorporar con los conectores existentes.
