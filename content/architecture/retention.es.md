---
title: "Retención y borrado"
weight: 130
---

## Cuánto tiempo se guardan los datos

| Información | Retención |
|---|---|
| Datos crudos, procesados y tablas de resultados | Mientras exista la fuente o el proyecto, durante la vigencia del contrato |
| Versiones anteriores de cada tabla (snapshots) | 3 días; siempre se conserva la versión actual |
| Copias de seguridad de las bases de metadatos | 7 días |
| Trazas de los agentes de IA | 14 días |
| Registro de actividad del proyecto | Consultable en la aplicación para los últimos 90 días |
| Logs técnicos de infraestructura y red | 365 días |

Teramot guarda **la versión más reciente** de cada tabla, más un historial corto que permite revertir una carga fallida. No es un archivo histórico del origen. Si el cliente necesita conservar la historia de los cambios, puede construir tablas de resultados que la acumulen.

## Qué pasa al borrar

### Una fuente

1. Se cancelan las ejecuciones en curso de esa fuente.
2. Se eliminan sus tablas crudas y procesadas, junto con sus archivos en el almacenamiento.
3. Las tablas de resultados que dependían de ella se marcan como **desactualizadas**, para que el usuario las revise.

Si el borrado falla a mitad de camino, la fuente queda marcada como eliminada y el borrado se puede reintentar.

### Un proyecto

Se eliminan sus tablas de resultados, sus fuentes, sus data shares, **todo su espacio en el almacenamiento**, su base de datos en el catálogo y su programación.

### Un workspace

El borrado se propaga a todos sus proyectos. Si el workspace tiene conexiones privadas IPsec activas, hay que eliminarlas antes.

## Fin del contrato

Al terminar el contrato, Teramot ejecuta un **procedimiento documentado de borrado**. Cubre el almacenamiento de objetos, el catálogo de datos, los metadatos de la aplicación, los registros de uso y las trazas, y termina con una **confirmación escrita de destrucción**. Ver [Compromisos de seguridad y confidencialidad](/compliance/Transparency/security-commitments/).

Mientras el contrato esté vigente, el cliente puede exportar sus tablas de resultados en CSV desde la aplicación o vía MCP.
