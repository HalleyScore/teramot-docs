---
title: "Teramot MCP — Visión general"
weight: 10
---

El servidor Model Context Protocol (MCP) de Teramot permite que cualquier cliente de IA compatible con MCP
(Claude, ChatGPT, Cursor y otros) trabaje directamente con su plataforma de datos de Teramot.
Una vez conectado, el cliente puede explorar sus workspaces, proyectos y fuentes de datos,
ver vistas previas de tablas y consultarlas, y construir nuevas tablas de resultados (gold), todo en lenguaje natural.

Implementa el transporte MCP **Streamable HTTP**, con OAuth 2.0 (o un token estático)
para la autenticación.

## Datos esenciales de conexión

| | |
| --- | --- |
| **Endpoint** | `https://mcp.teramot.com/mcp` |
| **Transporte** | Streamable HTTP (`POST` para JSON-RPC, `GET` para el stream SSE) |
| **Client ID** | `5nldf3wj83yz9f6zbrsjx` |
| **Autenticación** | OAuth 2.0 + PKCE, o una clave de API estática (Bearer token) |
| **Servidor** | `teramot-mcp` `v0.1.0` |

> [!TIP]
> La mayoría de los usuarios nunca toca el protocolo directamente: vea **[Conectar su cliente](/es/api/connect-clients/)**
> para la configuración lista para copiar y pegar en Claude, ChatGPT, Cursor, v0.dev y Antigravity. Esta página documenta el
> protocolo subyacente para integraciones a medida.

## Cómo funciona la conexión

1. El cliente apunta a `https://mcp.teramot.com/mcp` y (en los clientes OAuth) al Client ID de arriba.
2. El cliente llama a `initialize` y `tools/list` para descubrir las capacidades; estos métodos **no requieren autenticación**.
3. Para cualquier trabajo real (`tools/call`), el cliente se autentica con un Bearer token, obtenido
   con el flujo automático de OAuth o con una clave de API estática. Vea **[Autenticación](/es/api/authentication/)**.

## Transporte y endpoints

Todo el tráfico va a un único endpoint, `https://mcp.teramot.com/mcp`.

### `POST /mcp`

Transporta pedidos JSON-RPC 2.0 (`initialize`, `tools/list`, `tools/call`, …). Las respuestas se
devuelven como `application/json` o, en las operaciones con streaming, como `text/event-stream`.

```http
POST /mcp HTTP/1.1
Host: mcp.teramot.com
Authorization: Bearer YOUR_TOKEN
Accept: application/json, text/event-stream
Content-Type: application/json
Mcp-Session-Id: SESSION_UUID   # echoed after initialize
```

### `GET /mcp`

Abre un stream de Server-Sent Events para los mensajes del servidor al cliente. Requiere el
encabezado `Mcp-Session-Id` que devuelve `initialize`; sin él, el servidor responde
`401 Unauthorized` (`missing Mcp-Session-Id; re-initialize via POST`).

### Métodos de arranque (sin autenticación)

Para que los clientes puedan descubrir el servidor antes de autorizarse, tres métodos no requieren autenticación:

- `initialize`
- `tools/list`
- `notifications/initialized`

Todos los demás métodos requieren un Bearer token válido.

## Gestión de sesiones

`initialize` devuelve un encabezado de respuesta `Mcp-Session-Id`. Inclúyalo en los pedidos
siguientes y en el stream de `GET /mcp`. Las sesiones se guardan en memoria y se reinician cuando
el servidor se reinicia: si se pierde una sesión, simplemente vuelva a llamar a `initialize`.

## Métodos MCP

### `initialize`

Negocia la versión del protocolo y las capacidades. **No requiere autenticación.**

{{< tabs >}}
{{< tab name="Solicitud" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "init-1",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": { "tools": {} },
    "clientInfo": { "name": "MyApp", "version": "1.0.0" }
  }
}
```

{{< /tab >}}
{{< tab name="Respuesta" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "init-1",
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": { "tools": { "listChanged": true } },
    "serverInfo": { "name": "teramot-mcp", "version": "v0.1.0" },
    "instructions": "You are connected to the Teramot data platform. Help users explore their workspaces, projects, data sources, tables, and create results tables."
  }
}
```

{{< /tab >}}
{{< /tabs >}}

La respuesta trae el encabezado `Mcp-Session-Id` para los pedidos siguientes.

### `tools/list`

Lista las herramientas disponibles. **No requiere autenticación** (es parte del flujo de arranque).
Vea el catálogo completo en la **[Referencia de herramientas](/es/api/tools-reference/)**.

{{< tabs >}}
{{< tab name="Solicitud" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "list-tools",
  "method": "tools/list"
}
```

{{< /tab >}}
{{< tab name="Respuesta" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "list-tools",
  "result": {
    "tools": [
      {
        "name": "list_workspaces",
        "description": "Lists all workspaces the user has access to.",
        "inputSchema": { "type": "object", "properties": {} }
      },
      {
        "name": "preview_table",
        "description": "Preview the first 100 rows of a data table.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "table_name": { "type": "string", "description": "Name of the table to preview" }
          },
          "required": ["table_name"]
        }
      }
    ]
  }
}
```

{{< /tab >}}
{{< /tabs >}}

### `tools/call`

Ejecuta una herramienta. **Requiere autenticación** (Bearer token).

{{< tabs >}}
{{< tab name="Solicitud" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "call-tool",
  "method": "tools/call",
  "params": {
    "name": "preview_table",
    "arguments": { "table_name": "sales" }
  }
}
```

{{< /tab >}}
{{< tab name="Respuesta" >}}

```json
{
  "jsonrpc": "2.0",
  "id": "call-tool",
  "result": {
    "content": [
      { "type": "text", "text": "{ \"columns\": [...], \"rows\": [...] }" }
    ]
  }
}
```

{{< /tab >}}
{{< /tabs >}}

## Manejo de errores

Se aplican los códigos de error estándar de JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "error": { "code": -32602, "message": "Invalid params" }
}
```

| Código | Significado |
| --- | --- |
| `-32700` | Error de parseo (JSON inválido) |
| `-32600` | Pedido inválido (JSON-RPC mal formado) |
| `-32601` | Método no encontrado |
| `-32602` | Parámetros inválidos |
| `-32000` | Error interno o de autenticación |

En la capa HTTP, un token ausente o vencido devuelve `401 Unauthorized`.

## Próximos pasos

- **[Autenticación](/es/api/authentication/)**: OAuth 2.0 y claves de API estáticas.
- **[Conectar su cliente](/es/api/connect-clients/)**: Claude, ChatGPT, Cursor, v0.dev, Antigravity.
- **[Referencia de herramientas](/es/api/tools-reference/)**: el catálogo completo de herramientas disponibles.
