---
title: "Agentes de IA"
weight: 70
---

Teramot usa agentes de IA en puntos concretos del flujo. Esta página explica **qué hace cada agente, qué información recibe y qué controles tiene**.

## Principios

- **La IA propone y el sistema valida.** Toda transformación generada por IA se ejecuta y se controla antes de aplicarse. Ver [Transformaciones](/es/architecture/transformations/).
- **Todo resultado es SQL visible.** Los agentes no producen tablas opacas: cada tabla procesada o de resultados tiene una consulta que el usuario puede leer y corregir.
- **Los agentes actúan con los permisos del usuario.** Un agente no puede hacer nada que el usuario que lo invoca no pueda hacer.
- **Sin entrenamiento con datos de clientes.** Teramot no entrena modelos propios ni hace fine-tuning con datos de clientes. La inferencia se contrata en condiciones que excluyen el tráfico de la API del entrenamiento de los proveedores.

## Agentes y funciones

| Agente | Qué hace | Cuándo actúa | Qué recibe |
|---|---|---|---|
| **Limpieza de datos** | Escribe la consulta SQL que convierte cada tabla cruda en su versión procesada. | Al configurar una fuente, y cuando cambia el esquema de una tabla. | El esquema de la tabla, estadísticas por columna (proporción de nulos, cantidad de valores distintos, valores más frecuentes, proporción numérica), las claves declaradas y una **muestra de hasta 100 filas**. |
| **Reconciliación de tipos** | Alinea el tipo de las columnas que se usan para cruzar tablas. | Al configurar una fuente, antes de construir los datos procesados. | Esquemas y estadísticas de las columnas involucradas. |
| **Documentación** | Genera descripciones de tablas y columnas para el catálogo del proyecto. | Al final de la configuración de una fuente. | Esquemas, descripciones de columnas y consultas de limpieza. |
| **Tablas de resultados** | Traduce un pedido en lenguaje natural a una consulta SQL sobre los datos procesados. | Cuando el usuario pide una tabla de resultados nueva. | El pedido del usuario, el catálogo de tablas disponibles, sus esquemas y el conocimiento del proyecto. |
| **Asistente de la aplicación** | Conversa con el usuario, explora tablas, ejecuta consultas, crea tablas de resultados y dashboards. | Cuando el usuario escribe en el chat. | La conversación y los resultados de las herramientas que ejecuta: esquemas, filas consultadas y resultados. |

> [!WARNING]
> **Datos reales en las muestras**
>
> Para limpiar bien una tabla, el agente necesita ver ejemplos reales de sus valores. Esas muestras se envían al proveedor del modelo **sin enmascarar**. Si una tabla contiene datos personales o sensibles que no hacen falta para el análisis, lo recomendable es no incorporarla o excluir esas columnas en el origen, por ejemplo con una vista.

## El asistente de la aplicación y los asistentes externos

Hay dos maneras de conversar con los datos:

| | Asistente de la aplicación | Asistente propio vía MCP |
|---|---|---|
| **Dónde razona el modelo** | En Teramot, con los proveedores de modelos que contrata Teramot | En el asistente del cliente (Claude, ChatGPT, Copilot u otro), con el proveedor y el contrato del cliente |
| **Herramientas disponibles** | Las mismas herramientas que expone el servidor MCP | Las herramientas del servidor MCP |
| **Permisos** | Los del usuario conectado | Los del usuario conectado |
| **A dónde van los resultados** | Al proveedor de modelos de Teramot | Al proveedor de modelos del cliente |

El servidor MCP de Teramot **no usa modelos de lenguaje**. Solo ejecuta las herramientas que el asistente del cliente le pide. Ver [Formas de consumo](/es/architecture/consumption/).

El asistente de la aplicación tiene además un **filtro de tema** que puede rechazar pedidos ajenos al análisis de datos.

## Controles sobre lo que la IA puede ejecutar

- **Solo lectura en las consultas**: cualquier consulta que ejecute un agente o un usuario se analiza y solo se acepta si es una única sentencia de lectura.
- **Alcance del proyecto**: las consultas solo pueden leer tablas del proyecto activo, o tablas compartidas explícitamente.
- **Resultados paginados y con tiempo máximo**: las consultas conversacionales devuelven resultados por páginas y tienen un tiempo máximo de ejecución.
- **Permisos por rol**: crear o modificar tablas de resultados, lanzar actualizaciones o corregir transformaciones requiere el rol correspondiente. Ver [Roles](/es/architecture/security/#roles-y-permisos).
- **Registro de actividad**: los cambios que se hacen desde el asistente o vía MCP quedan en el registro de actividad del proyecto, a nombre del usuario que los pidió.

## Proveedores de modelos

| Proveedor | Uso | Modalidad |
|---|---|---|
| **Anthropic** (modelos Claude) | Agentes de datos y asistente de la aplicación | API de Anthropic y Amazon Bedrock |
| **OpenAI** (modelos GPT) | Agentes de datos, como proveedor alternativo | API de OpenAI |

Los agentes de datos tienen **conmutación automática entre proveedores**: si uno no responde, el pedido pasa a otro. El modelo concreto de cada agente puede cambiar con el tiempo, a medida que aparecen modelos mejores.

## Trazabilidad de la IA

Para depurar y mejorar la calidad de los agentes, Teramot registra las trazas de ejecución (lo que entra al modelo y lo que sale) en servicios de observabilidad de IA:

| Servicio | Qué recibe |
|---|---|
| **LangSmith** | Trazas de los agentes de datos y del asistente de la aplicación |
| **Langfuse** | Trazas de las herramientas del servidor MCP |

Las trazas pueden incluir esquemas, muestras de datos y resultados de consultas. Se guardan por 14 días y se incluyen en el procedimiento de borrado al finalizar el contrato. Ver [Retención y borrado](/es/architecture/retention/).
