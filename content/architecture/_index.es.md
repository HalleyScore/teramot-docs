---
title: "Arquitectura técnica de Teramot"
linkTitle: "Visión general"
weight: 20
cascade:
  type: docs
# The Getting Started section was removed; its URLs redirect here.
aliases:
  - /getting-started/
  - /getting-started/getting-started/
  - /getting-started/poc-guide/
  - /getting-started/model-deployment/
  - /getting-started/faq/
  - /getting-started/multi-tenant-deployment/
---

Esta sección explica cómo funciona Teramot por dentro. Cubre qué hace la plataforma, por dónde pasan los datos, qué transformaciones se aplican, dónde se guardan y quién puede acceder a ellos.

Está pensada para los equipos de IT, datos, arquitectura y seguridad que evalúan Teramot o ya lo usan, y la pueden tomar como documento de referencia.

## Qué hace Teramot

Teramot es una plataforma de ingeniería de datos asistida por IA. Resuelve un problema concreto: llevar datos dispersos en muchos sistemas (bases de datos, ERPs, data warehouses, aplicaciones SaaS y archivos) a un lugar único, limpio y consultable, sin que el cliente tenga que construir ni mantener pipelines.

En la práctica, Teramot:

1. **Se conecta** a los sistemas de origen con credenciales de solo lectura.
2. **Copia** las tablas elegidas a un almacenamiento propio del proyecto, con actualizaciones programadas.
3. **Limpia y normaliza** cada tabla con agentes de IA, y valida cada transformación antes de aplicarla.
4. **Construye tablas de resultados**: métricas, cruces y reportes definidos en lenguaje natural o en SQL.
5. **Sirve** esos datos por la aplicación web, por un asistente conversacional, por asistentes de IA externos vía MCP (Claude, ChatGPT, Copilot, entre otros) y por exportaciones.

## Conceptos básicos

| Concepto | Qué es |
|---|---|
| **Workspace** | El espacio de una organización. Agrupa proyectos, miembros y conexiones. Es el límite principal de acceso. |
| **Proyecto** | Una unidad de trabajo dentro de un workspace, por ejemplo "Ventas" o "Supply chain". Cada proyecto tiene su propio almacenamiento y su propio catálogo de tablas, aislados de los demás. |
| **Fuente** | Una conexión a un sistema de origen, como una base Oracle, un workspace de Databricks o una cuenta de Salesforce. |
| **Datos crudos** | La copia fiel de las tablas de origen, tal como llegan. |
| **Datos procesados** | Las mismas tablas, limpias y con tipos consistentes. Es la base sobre la que se trabaja. |
| **Tablas de resultados** | Análisis guardados y recalculables construidos sobre los datos procesados: una métrica, un cruce entre sistemas o un reporte. |
| **Dashboard** | Una visualización construida sobre tablas de resultados. |
| **Conocimiento del proyecto** | Documentación de negocio del proyecto (definiciones, reglas, glosario) que usan los agentes para responder con contexto. |

En la aplicación, las tablas raw, procesadas y de resultados aparecen como **Source tables**, **Cleaned & interpreted** y **Results**; ver [How your data is organized](/product/concepts/data-model/) (en inglés).

## Cómo leer esta sección

| Si necesita saber… | Vaya a |
|---|---|
| Qué componentes tiene la plataforma y dónde corren | [Arquitectura de la plataforma](/es/architecture/platform/) |
| El recorrido de un dato desde el origen hasta una respuesta | [Flujo de los datos](/es/architecture/data-flow/) |
| Qué cambios se hacen sobre los datos | [Transformaciones](/es/architecture/transformations/) |
| Dónde se guardan los datos y en qué formato | [Dónde viven los datos](/es/architecture/data-storage/) |
| Qué guardamos, qué compartimos con terceros y por cuánto tiempo | [Qué guardamos y qué compartimos](/es/architecture/data-handling/) |
| Qué hace la IA y qué información recibe | [Agentes de IA](/es/architecture/ai-agents/) |
| Cómo se consultan los datos | [Formas de consumo](/es/architecture/consumption/) |
| Autenticación, roles, cifrado y auditoría | [Seguridad y control de acceso](/es/architecture/security/) |
| Cómo conectar sistemas que están en una red privada | [Conectividad con las fuentes](/es/architecture/connectivity/) |
| Qué usuario y permisos crear en cada sistema de origen | [Prepare your sources](/product/connect-data/prepare-sources/) (en inglés) |
| Frecuencias de actualización y carga incremental | [Actualización e incremental](/es/architecture/refresh/) |
| Cuánto tiempo se guardan los datos y cómo se borran | [Retención y borrado](/es/architecture/retention/) |
| Qué sistemas se pueden conectar | [Catálogo de conectores](/es/architecture/connectors/) |

> [!NOTE]
> **Documentación relacionada**
>
> - [Referencia del servidor MCP](/product/mcp/overview/): cómo conectar asistentes de IA a Teramot.
> - [Compromisos de seguridad y confidencialidad](/compliance/Transparency/security-commitments/).
> - [Compliance](/compliance/about/): SOC 2 y políticas de seguridad.
