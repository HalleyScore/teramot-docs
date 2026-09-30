---
title: "Arquitectura de la plataforma"
weight: 20
---

Teramot se ofrece como servicio (SaaS) sobre **Amazon Web Services**, en la región **us-east-1** (Norte de Virginia, EE. UU.). Toda la infraestructura está definida como código y existen entornos separados de desarrollo, staging y producción, cada uno en su propia cuenta de AWS.

La plataforma se divide en cuatro bloques:

- **Plano de control**: la aplicación web, la API y el servidor MCP. Gestiona usuarios, permisos, proyectos, fuentes y programaciones.
- **Plano de datos**: extrae, transforma, guarda y consulta los datos.
- **Servicios de IA**: los agentes que limpian datos, generan tablas de resultados y responden preguntas.
- **Canales de consumo**: los puntos por los que usuarios y sistemas acceden a los datos.

## Diagrama general

![Arquitectura de Teramot: los sistemas del cliente se conectan por IPsec, SSH o TLS a los extractores; el plano de datos en subredes privadas guarda los datos en S3 con Apache Iceberg y los transforma con Amazon Athena; el plano de control expone la API, la aplicación web y el servidor MCP a usuarios y asistentes de IA.](/img/architecture/platform.svg)

## Plano de control

El plano de control es la parte de Teramot con la que interactúan las personas.

| Componente | Función |
|---|---|
| **Aplicación web** | Aplicación de una sola página servida por una CDN (Amazon CloudFront). Incluye el asistente conversacional, la gestión de fuentes, el explorador de tablas, el editor SQL, el linaje, los dashboards, las programaciones y la administración del workspace. |
| **API** | Servicio que concentra toda la lógica de negocio y **aplica los permisos**. Todo pasa por ella: la aplicación web, el servidor MCP y las integraciones. |
| **Servidor MCP** | Expone las capacidades de Teramot a asistentes de IA externos con el estándar [Model Context Protocol](https://modelcontextprotocol.io). No tiene permisos propios: cada acción se ejecuta contra la API con la identidad del usuario que la pide. |
| **Base de metadatos** | Amazon Aurora PostgreSQL. Guarda la configuración: workspaces, proyectos, miembros, definiciones de fuentes, tablas de resultados, dashboards y registros de actividad. **No guarda los datos de negocio**, que viven en el data lake. |
| **Programador** | Un servicio de programación administrado de AWS dispara las actualizaciones periódicas de cada proyecto. |
| **Identidad** | Un proveedor de identidad administrado basado en OpenID Connect. Ver [Seguridad](/es/architecture/security/). |

Los servicios del plano de control corren en contenedores sobre Amazon ECS. Se exponen al exterior solo por balanceadores con TLS.

## Plano de datos

El plano de datos es donde se mueven y transforman los datos.

| Componente | Función |
|---|---|
| **Orquestador de workflows** | Coordina cada ejecución: extraer, validar, transformar, construir resultados. Usa [Temporal](https://temporal.io), un motor de workflows durables. Si un paso falla, se reintenta sin repetir los anteriores. |
| **Extractores** | Leen las tablas de origen. Corren en funciones serverless (AWS Lambda) y, para cargas grandes, en contenedores (AWS Fargate). Trabajan en subredes privadas y procesan los datos en streaming, sin cargarlos enteros en memoria. |
| **Data lake** | Amazon S3, con las tablas en formato abierto **Apache Iceberg** sobre archivos Parquet. Ver [Dónde viven los datos](/es/architecture/data-storage/). |
| **Catálogo** | AWS Glue Data Catalog registra cada tabla y su esquema. Cada proyecto tiene su propia base de datos en el catálogo. |
| **Motor SQL** | Amazon Athena (dialecto Trino) ejecuta las transformaciones y las consultas. Las tablas procesadas y las de resultados se materializan con sentencias `CREATE TABLE AS SELECT`. |

Todas las transformaciones de Teramot son **SQL estándar sobre tablas abiertas**. No hay procesos opacos: cada tabla procesada o de resultados tiene una consulta SQL que la define, visible para el usuario.

## Servicios de IA

Los agentes de IA usan modelos de lenguaje de terceros (Anthropic y OpenAI) por API. Teramot no entrena modelos propios ni hace fine-tuning con datos de clientes. El detalle de qué hace cada agente y qué información recibe está en [Agentes de IA](/es/architecture/ai-agents/).

## Modelo de servicio

Teramot es una plataforma **multi-tenant** con aislamiento lógico por proyecto. Todos los clientes comparten la infraestructura, pero:

- Cada proyecto tiene un **prefijo de almacenamiento propio** y una **base de datos propia en el catálogo**.
- La identidad del proyecto se resuelve **en el servidor**, a partir del token del usuario. Ninguna operación de la API acepta un identificador de tenant enviado por el cliente.
- Cada consulta SQL se analiza antes de ejecutarse. Si hace referencia a una base de datos que no pertenece al proyecto, se rechaza.

La plataforma también se puede contratar a través de **AWS Marketplace**.
