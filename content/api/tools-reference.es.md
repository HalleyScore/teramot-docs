---
title: "Referencia de herramientas"
weight: 40
---

El catálogo completo de herramientas que expone el servidor MCP de Teramot, agrupadas por dominio.
Se descubren en tiempo de ejecución con `tools/list` y se invocan con `tools/call`
(ver la [Visión general](/es/api/intro/#métodos-mcp)).

La mayoría de las herramientas aceptan los argumentos opcionales `workspace_name` y `project_name`. Si se omiten, el
servidor usa su contexto activo (o el único workspace o proyecto disponible). Si tiene varios
workspaces, indique el que corresponde.

## Sesión

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `switch_context` | Define el workspace (y, opcionalmente, el proyecto) por defecto para el resto de esta sesión MCP. | `workspace_name` (string); `project_name` (string) |

## Workspaces

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `list_workspaces` | Lista todos los workspaces a los que el usuario tiene acceso. | — |
| `create_workspace` | Crea un workspace nuevo. | `name` (string, obligatorio); `index_color` (int) |
| `delete_workspace` | Elimina de forma permanente un workspace por nombre. Irreversible; requiere acceso de owner. Confirmación en dos pasos. | `workspace_name` (string, obligatorio); `confirmed` (bool) |

## Proyectos

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `list_projects` | Lista los proyectos por nombre. | `workspace_name` (string) |
| `create_project` | Crea un proyecto nuevo dentro de un workspace. | `workspace_name` (string, obligatorio); `slug` (string, obligatorio) |
| `delete_project` | Elimina de forma permanente un proyecto por nombre. Irreversible; requiere acceso de owner. Confirmación en dos pasos. | `project_name` (string, obligatorio); `workspace_name` (string); `confirmed` (bool) |
| `review_project` | Revisa el estado general de un proyecto: cada fuente de ETL y sus tablas, el estado y la fecha de última actualización de cada tabla, y un resumen de salud por fuente. | `workspace_name`/`project_name` (string) |

## Conocimiento del proyecto

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `project_knowledge` | Muestra el documento de conocimiento duradero y compartido de un proyecto: claves de cruce, definiciones de negocio y advertencias sobre los datos (un documento por proyecto, compartido por el equipo). | `workspace_name`/`project_name` (string) |
| `update_project_knowledge` | Crea, edita o elimina el documento de conocimiento de un proyecto. `create` crea el documento o lo reemplaza por completo si ya existe; `str_replace` reemplaza un texto que debe coincidir exactamente una vez; `insert` agrega texto después de una línea dada; `delete` elimina el documento por completo. | `command` (string, obligatorio: create \| str_replace \| insert \| delete); `content` (string, obligatorio para create); `old_str`/`new_str` (string, para str_replace); `insert_line` (int, para insert); `insert_text` (string, para insert); `workspace_name`/`project_name` (string) |

## Tablas y datos

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `explore_tables` | Lista o inspecciona tablas del data warehouse. **Listado** (sin `table_name`): nombres físicos de las tablas, filtrables por `layer`; el listado gold incluye también las tablas de resultados que todavía se están construyendo, que fallaron o que están en borrador. **Detalle** (con `table_name`): el SQL de una tabla, su estado de construcción, su linaje, su perfil de calidad de datos y los hallazgos por columna. | `table_name` (string, obligatorio para `with_sql`, `with_quality`, `with_status`); `layer` (string: gold \| silver \| bronze); `table_name_filter` (array de string); `with_columns` (bool); `with_instructions` (bool); `with_empty` (bool); `with_sql` (bool); `with_information` (bool); `with_quality` (bool); `with_status` (bool); `with_build_context` (bool); `build_context_table_names` (array de string); `workspace_name`/`project_name` (string) |
| `preview_table` | Muestra una vista previa de las primeras 100 filas de una tabla (columnas, tipos y filas de muestra). | `table_name` (string, obligatorio); `workspace_name`/`project_name` (string) |
| `query_data` | Ejecuta una consulta SQL (dialecto TRINO) sobre una tabla. | `table_name` (string, obligatorio); `sql` (string, obligatorio); `execution_id` (string); `page` (int); `workspace_name`/`project_name` (string) |
| `revise_silver_query` | Corrige un error, identificado durante la conversación, en el SQL de transformación de una tabla de la capa Silver (datos procesados). Solo para la capa Silver. Primero valida; aplicar el cambio requiere confirmación explícita del usuario, salvo que la validación salga limpia y la confianza sea alta. | `table_name` (string, obligatorio); `new_sql` (string, obligatorio); `reasoning` (string, obligatorio); `confidence` (string, obligatorio: high \| low); `validate_only` (bool); `confirmed` (bool); `workspace_name`/`project_name` (string) |

## Tablas de resultados (gold)

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `sql_tool` | Ejecuta una consulta candidata para una tabla de resultados y muestra lo que produce (filas, tipos de columna o el error del motor) sin crear nada. Cuando el resultado es el correcto, pase el mismo SQL a `create_gold_table`. | `query` (string, obligatorio); `workspace_name`/`project_name` (string) |
| `create_gold_table` | Crea una tabla de resultados a partir de una definición SQL, usada tal cual. Si todo sale bien, envía la construcción y responde de inmediato. | `sql` (string, obligatorio); `source_tables` (string, obligatorio); `name` (string); `description` (string); `questions` (string); `knowledges` (string); `join_keys` (string); `validate_only` (bool); `workspace_name`/`project_name` (string) |
| `update_gold_table` | Actualiza una tabla de resultados existente: descripción, instrucciones, regeneración de la consulta o tablas de origen. | `analysis_spec_name` (string, obligatorio); `action` (string: update_description \| create_instruction \| update_instruction \| replace_instruction \| delete_instruction \| regenerate_query); `description` (string); `instructions` (array de `{id?, text}`); `instruction_ids` (array de string); `add_source_tables` (string); `remove_source_tables` (string); `workspace_name`/`project_name` (string) |
| `delete_gold_table` | Elimina de forma permanente una tabla de resultados y todos sus datos. Confirmación en dos pasos. | `analysis_spec_name` (string); `confirmed` (bool); `workspace_name`/`project_name` (string) |
| `duplicate_gold_table` | Duplica una tabla de resultados en un nuevo analysis spec en borrador. | `analysis_spec_name` (string, obligatorio); `dry_run` (bool); `workspace_name`/`project_name` (string) |
| `get_gold_table_download_link` | Obtiene un enlace de descarga con todos los datos de una tabla de resultados en un archivo CSV. El enlace vence poco después de emitirse. | `analysis_spec_name` (string); `visibility` (string: private \| public); `workspace_name`/`project_name` (string) |

## Dashboards

Dashboards de HTML o widgets escritos por un LLM, cada uno vinculado por slug a una o más tablas de resultados. Los dashboards
**dinámicos** combinan una plantilla con una `query`, así que los datos se actualizan en vivo; los **estáticos** no tienen
`{{expressions}}` ni query.

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `dashboard_authoring_guide` | La guía completa para escribir un dashboard: renderizado, el motor de plantillas, las reglas de las consultas, los tipos de widget, el tema, el diseño, la lista de verificación previa al guardado y un ejemplo resuelto. | — |
| `list_dashboards` | Lista los dashboards guardados del proyecto: id, título, tipo y fechas, sin el cuerpo del documento. | `workspace_name`/`project_name` (string) |
| `get_dashboard` | Obtiene un dashboard guardado completo, con su documento y su consulta. | `dashboard_id` (string, obligatorio); `workspace_name`/`project_name` (string) |
| `preview_dashboard` | Muestra una vista previa de un dashboard en el chat sin guardar nada. | `title` (string); `type` (string: html \| widget); `content` (string); `source_html` (string); `query` (string, obligatorio si `content` contiene `{{expressions}}`); `workspace_name`/`project_name` (string) |
| `save_dashboard` | Guarda un dashboard nuevo, vinculado por slug a una o más tablas de resultados. | `title` (string, obligatorio); `type` (string: html \| widget, obligatorio); `content` (string, obligatorio); `source_html` (string); `query` (string); `gold_table_slug` (string); `gold_table_slugs` (array de string, obligatorio salvo que se indique `gold_table_slug`); `min_role` (string: readonly \| member \| admin \| owner); `workspace_name`/`project_name` (string) |
| `update_dashboard` | Cambia el título, el contenido, la consulta, las fuentes o el rol mínimo para ver un dashboard guardado. Reemplaza el valor guardado por completo: envíe el contenido completo, no un fragmento. | `dashboard_id` (string, obligatorio); `title`/`content`/`source_html`/`query`/`min_role` (string, todos opcionales); `gold_table_slug` (string); `gold_table_slugs` (array de string); `workspace_name`/`project_name` (string) |
| `delete_dashboard` | Elimina un dashboard guardado. En el backend se hace un borrado lógico, pero desde esta interfaz no se puede deshacer, y todas las personas con las que se había compartido pierden el acceso. | `dashboard_id` (string, obligatorio); `workspace_name`/`project_name` (string) |

## Actualización y programación

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `refresh_tables` | Dispara una actualización de ETL (el pipeline de una tabla o el proyecto completo) para incorporar los datos nuevos de la fuente (genera una nueva revisión). | `action` (string, obligatorio: refresh_table \| refresh_all); `table_name` (string); `workspace_name`/`project_name` (string) |

## Controles

Un control es una pregunta de negocio que el equipo confirmó que se respondió correctamente; el monitor la vuelve a hacer
periódicamente e informa si la respuesta se sigue obteniendo de la misma forma.

| Herramienta | Descripción | Parámetros |
| --- | --- | --- |
| `list_controls` | Lista las preguntas que un workspace vigila mes a mes, cada una con su estado, la conversación de la que surgió y la fecha en que corresponde volver a examinarla. | `workspace_name` (string) |
| `control_index` | Lee el índice de deterioro de un mes para un workspace: el puntaje, su cobertura y los controles que no pudo evaluar (se marca como insuficiente por debajo del 50% de cobertura). | `month` (string, obligatorio, YYYY-MM); `workspace_name` (string) |
| `get_control` | Obtiene un control completo: su pregunta, su estado, quién lo confirmó y cuándo vence su próxima revisión. | `control_id` (string, obligatorio); `workspace_name` (string) |
| `add_control` | Empieza a vigilar una pregunta que el workspace ya respondió correctamente. Se crea como candidato: no se vigila hasta que se confirma. | `question` (string, obligatorio); `conversation_id` (string, obligatorio); `review_due` (string, obligatorio, YYYY-MM-DD); `workspace_name` (string) |
| `confirm_control` | Promueve un candidato a control vigilado, avalando que su respuesta era correcta. | `control_id` (string, obligatorio); `workspace_name` (string) |
| `remove_control` | Deja de vigilar una pregunta, con un motivo. Se conserva marcado como eliminado, sin borrarse, para que los meses anteriores sigan cerrando. | `control_id` (string, obligatorio); `reason` (string, obligatorio); `workspace_name` (string) |
