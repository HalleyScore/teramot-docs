---
title: "Formas de consumo"
weight: 80
---

Los datos de Teramot se pueden consumir por cuatro vías. Todas pasan por la misma API, así que en todas rigen **los mismos permisos**.

```mermaid
flowchart LR
    U1[Usuario] --> W[Aplicación web]
    U2[Asistente de IA del cliente<br/>Claude, ChatGPT, Copilot] --> M[Servidor MCP]
    U3[Integraciones] --> K[API con clave de proyecto]
    W & M & K --> API[API de Teramot<br/>autenticación y permisos]
    API --> D[(Datos del proyecto)]
    API --> E[Exportación CSV<br/>enlace temporal]
```

## Aplicación web

La aplicación web incluye:

- **Asistente conversacional**: preguntas en lenguaje natural sobre los datos del proyecto.
- **Fuentes**: alta, configuración, estado y actualización de conexiones.
- **Explorador de datos**: tablas crudas, procesadas y de resultados, con esquema, vista previa, hallazgos de calidad y linaje.
- **Editor SQL**: consultas de solo lectura sobre las tablas del proyecto.
- **Tablas de resultados**: creación, edición y actualización.
- **Dashboards**: visualizaciones construidas sobre tablas de resultados. Se sanitizan en el servidor y se muestran aislados en el navegador.
- **Conocimiento del proyecto**: definiciones de negocio que usan los agentes.
- **Programación**: frecuencia de actualización de cada proyecto.
- **Administración**: miembros, roles, data shares, registro de actividad y uso de IA.

Una conversación se puede compartir con otros miembros del workspace. Un dashboard se comparte con un enlace que solo pueden abrir las personas del workspace, y un admin puede limitar cada dashboard a un rol mínimo.

## Asistentes de IA vía MCP

Teramot publica un servidor **[Model Context Protocol](https://modelcontextprotocol.io)** para que el cliente use sus datos desde el asistente de IA que ya tiene.

| | |
|---|---|
| **Endpoint** | `https://mcp.teramot.com/mcp` |
| **Transporte** | Streamable HTTP |
| **Autenticación** | OAuth 2.1 con PKCE, o una access key para clientes que no soportan OAuth |
| **Clientes compatibles** | Claude (web, escritorio, Team, Enterprise y Claude Code), ChatGPT, GitHub Copilot en VS Code, Gemini, Cursor, v0, Antigravity y otros clientes MCP. Cómo configurar cada uno: [Connect an AI assistant](/product/mcp/connect-clients/) (en inglés) |

### Cómo funciona la identidad

1. El administrador de la herramienta de IA del cliente agrega el conector de Teramot.
2. Cuando una persona lo usa por primera vez, el asistente la redirige a iniciar sesión en Teramot.
3. Desde ese momento, **cada acción se ejecuta como esa persona**, con su rol en cada workspace y proyecto.

Que el conector esté disponible para toda la organización no le da acceso a nadie: solo pueden usarlo las personas que tienen un usuario en Teramot, y cada una ve solo lo que su rol le permite.

Las redirecciones de OAuth se aceptan solo hacia una lista cerrada de destinos: los dominios de los clientes compatibles y direcciones locales para aplicaciones de escritorio.

### Qué se puede hacer vía MCP

Un asistente puede hacer exactamente lo que permite el rol de su usuario, nada más: explorar
y consultar tablas, armar tablas de resultados y dashboards, actualizar fuentes, etc. La
[Tool reference](/product/mcp/tools-reference/) lista cada herramienta con el rol mínimo que
necesita, y [Roles and permissions](/product/concepts/roles-and-permissions/) qué cubre cada
rol (ambas en inglés).

## API

Para integraciones sistema a sistema, un usuario puede generar **claves de API de proyecto**. Cada clave:

- Queda asociada a un workspace, un proyecto y un usuario.
- Hereda **en cada uso** los permisos actuales de ese usuario: si el usuario pierde el acceso, la clave también lo pierde.
- Se guarda como hash: Teramot no conserva la clave en claro.

## Exportación

Las tablas de resultados se pueden descargar como **CSV** con un enlace temporal:

- **Enlace privado** (por defecto, y el que usa la aplicación web): funciona durante 10 minutos y solo para la cuenta que lo pidió.
- **Enlace público**: un asistente lo puede pedir cuando el archivo tiene que llegar a alguien sin cuenta en Teramot. Funciona durante 15 minutos para cualquiera que lo tenga.

Cómo descargarla: [Results tables](/product/use-the-app/results-tables/#download) (en inglés).
