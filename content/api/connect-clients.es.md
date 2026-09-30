---
title: "Conectar su cliente"
weight: 30
---

Use estos valores para conectar su cliente MCP al servidor MCP de Teramot.

| | |
| --- | --- |
| **URL de MCP** | `https://mcp.teramot.com/mcp` |
| **Client ID** | `5nldf3wj83yz9f6zbrsjx` |

> [!NOTE]
> **Claude** y **ChatGPT** se autentican con OAuth: solo necesitan la URL de MCP (y el Client ID
> si lo piden). **Cursor**, **v0.dev** y **Antigravity** usan una clave de API estática: genérela
> primero en la página **MCP → API Keys** (ver [Autenticación](/es/api/authentication/#clave-de-api-estática)).

{{< tabs >}}

{{< tab name="Claude Code" >}}

Ejecute este comando en su terminal:

```bash
claude mcp add --transport http --client-id 5nldf3wj83yz9f6zbrsjx --callback-port 8090 teramot https://mcp.teramot.com/mcp
```

Se abre una ventana del navegador para que autorice el acceso con Teramot. Después, las herramientas de `teramot`
quedan disponibles en Claude Code.

{{< /tab >}}

{{< tab name="Claude Desktop / Browser" >}}

1. Abra **Settings → Developer → MCP Servers** (o **Edit Config**).
2. Agregue un servidor nuevo con estos valores:
   - **Name:** `teramot`
   - **Transport:** `HTTP`
   - **URL:** `https://mcp.teramot.com/mcp`
   - **Client ID:** `5nldf3wj83yz9f6zbrsjx`
3. Guarde y reinicie Claude Desktop.
4. Abra un chat nuevo y active el conector **teramot**.

{{< /tab >}}

{{< tab name="ChatGPT" >}}

En ChatGPT, abra **Settings → Apps** (o **Apps & Connectors**), agregue una app MCP personalizada y use
estos valores:

- **Server URL:** `https://mcp.teramot.com/mcp`
- **Client ID:** `5nldf3wj83yz9f6zbrsjx`

Paso a paso en ChatGPT Desktop / Browser:

1. Abra ChatGPT y vaya a **Settings**.
2. Abra **Apps** (o **Apps & Connectors**) y cree o importe una app MCP personalizada.
3. Configure la app con estos valores:
   - **Name:** `teramot`
   - **Transport:** `HTTP`
   - **URL:** `https://mcp.teramot.com/mcp`
   - **Client ID:** `5nldf3wj83yz9f6zbrsjx`
4. Guarde la configuración y complete la autorización si se la piden.
5. Abra un chat nuevo y habilite la app **teramot**.

{{< /tab >}}

{{< tab name="Cursor" >}}

Cursor usa una **clave de API estática**. Primero genere una en la página **MCP → API Keys**
(ver [Autenticación](/es/api/authentication/#clave-de-api-estática)) y después agregue el servidor a su configuración
de MCP (Settings → MCP, o `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "teramot": {
      "url": "https://mcp.teramot.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

{{< /tab >}}

{{< tab name="v0.dev" >}}

v0.dev usa una **clave de API estática**. Genere una en la página **MCP → API Keys**
(ver [Autenticación](/es/api/authentication/#clave-de-api-estática)) y agregue el servidor con el
encabezado `Authorization: Bearer`:

```json
{
  "mcpServers": {
    "teramot": {
      "url": "https://mcp.teramot.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

{{< /tab >}}

{{< tab name="Antigravity" >}}

Antigravity usa una **clave de API estática**. Genere una en la página **MCP → API Keys**
(ver [Autenticación](/es/api/authentication/#clave-de-api-estática)) y configure el servidor MCP con
el encabezado `Authorization: Bearer`:

```json
{
  "mcpServers": {
    "teramot": {
      "url": "https://mcp.teramot.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

{{< /tab >}}

{{< /tabs >}}

## Verificar la conexión

Una vez conectado, pídale a su cliente que **liste sus workspaces**: debería llamar a `list_workspaces`
y devolverlos. A partir de ahí puede explorar proyectos, ver vistas previas de tablas y construir tablas de resultados.
Vea la **[Referencia de herramientas](/es/api/tools-reference/)** completa.
