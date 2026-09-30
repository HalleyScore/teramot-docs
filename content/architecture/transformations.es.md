---
title: "Transformaciones"
weight: 40
---

Los datos pasan por tres capas. Cada una tiene un propósito distinto y un nivel de intervención distinto.

| Capa | Propósito | Quién la define |
|---|---|---|
| **Datos crudos** | Copia fiel del origen | Automático (conector) |
| **Datos procesados** | Datos limpios y con tipos consistentes | Agente de IA, validado; el usuario puede corregirlo |
| **Tablas de resultados** | Métricas, cruces y reportes | El usuario, en lenguaje natural o SQL |

## Datos crudos

La capa cruda busca **conservar el origen**. Los únicos cambios que se aplican son los necesarios para guardar los datos en un formato abierto y consultable con SQL:

- **Nombres de columna normalizados**: minúsculas, sin acentos, y los caracteres especiales se reemplazan por `_`. Si dos columnas quedan con el mismo nombre, se les agrega un sufijo para distinguirlas.
- **Fechas y horas en UTC** con precisión de microsegundos. Una fecha-hora sin zona horaria se interpreta como UTC.
- **Tipos sin equivalente directo**, como horas sueltas, duraciones y enteros muy grandes, se guardan como texto para no perder precisión.
- **Estructuras anidadas** de las APIs (JSON) se guardan como texto JSON.
- **Columnas de partición por fecha** para acelerar las consultas.

Los tipos declarados en el origen, y sus claves primarias y foráneas, se conservan como metadatos.

### Cambios de esquema

- Una **columna nueva** en el origen se agrega a la tabla sin reconstruirla.
- Un **cambio incompatible** (por ejemplo, un cambio de tipo) en una carga completa recrea la tabla con el esquema nuevo.
- Cada cambio de esquema queda registrado por ejecución: tablas o columnas agregadas, eliminadas y cambios de tipo.

### Protecciones en la escritura

Cada escritura es una **transacción atómica** de Iceberg: la tabla se ve completa antes o completa después, nunca a medias. Además, en las cargas completas:

- Una extracción **vacía** nunca reemplaza una tabla con datos.
- Si la cantidad de filas **cae de forma abrupta** respecto de la carga anterior, la carga se descarta y se conserva la versión previa.
- Si la carga **falla a mitad de camino**, se revierte.

## Datos procesados

La capa procesada es donde se **limpian** los datos. Para cada tabla, un agente de IA escribe una consulta `SELECT` que produce la versión limpia. El resultado es SQL estándar, visible y auditable.

### Qué tipo de limpieza se aplica

- Recortar espacios sobrantes.
- Convertir valores vacíos o marcadores de "sin dato" en `NULL`.
- Convertir texto a número o fecha cuando el contenido lo permite, con conversiones seguras que no fallan ante valores inválidos.
- Normalizar formatos de fecha.
- Mantener los identificadores con su tipo original, para no perder ceros a la izquierda ni formatos de código.

### Cómo se valida una transformación

Ninguna consulta propuesta por la IA se aplica sin pasar controles automáticos. Cada propuesta:

1. **Se ejecuta** contra los datos reales antes de aceptarla.
2. **No puede perder filas.** Se rechazan filtros, agregaciones, deduplicaciones y límites que reduzcan la tabla.
3. **No puede perder columnas.** Todas las columnas del origen tienen que estar presentes.
4. **No puede dejar vacía una columna** que en el origen tenía datos.
5. **Solo puede usar conversiones de tipo compatibles** con el formato de almacenamiento.

Si una propuesta no pasa los controles, el agente tiene un número limitado de intentos para corregirla. Si no lo logra, la tabla procesada queda como **copia sin cambios de la tabla cruda**. Nunca se publica una transformación que no haya pasado la validación.

### Transparencia y control

- **Reporte de cambios por columna**: cada columna modificada muestra qué se cambió y por qué.
- **Historial de versiones**: cada consulta aceptada se guarda versionada, con su origen: generada por la IA o corregida por un usuario.
- **Corrección manual**: un usuario con permisos puede reemplazar la consulta de limpieza de una tabla. La nueva consulta pasa por la misma validación, y el sistema informa qué tablas de resultados se verían afectadas antes de aplicarla.
- **Reconciliación entre tablas**: las columnas que sirven para cruzar tablas se alinean al mismo tipo, para que los cruces funcionen.

### Hallazgos de calidad

Durante el perfilado se detectan y se informan:

- Valores atípicos.
- Inconsistencias de mayúsculas y minúsculas.
- Duplicados.
- Claves candidatas.
- Relaciones probables entre tablas, con su porcentaje de registros huérfanos.

Los hallazgos se muestran junto a cada tabla. No modifican los datos por sí solos.

## Tablas de resultados

Las tablas de resultados son **análisis guardados**: una métrica, un cruce entre sistemas, un reporte. Se construyen sobre los datos procesados, y también sobre otras tablas de resultados.

Una tabla de resultados se puede crear de dos maneras:

- **En lenguaje natural**: el usuario describe qué necesita y un agente de IA escribe la consulta SQL.
- **Con SQL propio**: el usuario, o su asistente de IA vía MCP, entrega la consulta. Teramot la valida y la puede probar sin crear nada.

En ambos casos:

- La consulta queda **visible y editable**.
- Solo puede leer tablas del mismo proyecto, o tablas compartidas explícitamente desde otro proyecto.
- La tabla se **materializa** en el data lake. Consultarla es rápido y siempre devuelve el mismo resultado hasta la próxima actualización.
- Se **recalcula automáticamente** cuando se actualizan los datos procesados de los que depende.
- Su **linaje** (de qué tablas depende) se puede ver en la aplicación.

Si una tabla de origen se elimina, las tablas de resultados que dependían de ella se marcan como **desactualizadas**. Si un cambio de esquema rompe una tabla de resultados, la reparación queda pendiente de confirmación del usuario en lugar de reintentarse indefinidamente.
