---
title: "Autenticación"
weight: 20
---

El servidor MCP de Teramot admite dos modos de autenticación. Los dos envían un Bearer token al
servidor; elija el que soporte su cliente.

| Modo | Para qué usarlo |
| --- | --- |
| **OAuth 2.0 + PKCE** | Claude (Code, Desktop, Browser), ChatGPT y cualquier cliente que pueda completar un flujo OAuth |
| **Clave de API estática** | Cursor, v0.dev, Antigravity y cualquier cliente que solo soporte un Bearer token estático |

Los dos modos conviven en el mismo endpoint y otorgan el mismo acceso. Los métodos de
descubrimiento `initialize` y `tools/list` no requieren ningún token (ver
[Visión general → Métodos de arranque](/es/api/intro/#métodos-de-arranque-sin-autenticación)).

> [!NOTE]
> Su conexión es **de toda la cuenta**: las mismas credenciales valen para todos los workspaces y proyectos
> de su cuenta de Teramot. No necesita un token distinto por workspace.

## OAuth 2.0 + PKCE

Es la vía recomendada para los clientes que la soportan. Solo se configuran dos valores:
la **URL de MCP** (`https://mcp.teramot.com/mcp`) y el **Client ID**
(`5nldf3wj83yz9f6zbrsjx`). El cliente abre una ventana del navegador, usted inicia sesión en Teramot y el
cliente recibe y renueva los tokens automáticamente.

Por debajo, el servidor expone los metadatos y endpoints estándar de OAuth 2.0, así que la mayoría de los clientes
MCP se configuran solos, sin datos adicionales:

- `GET /.well-known/oauth-authorization-server`: metadatos del servidor de autorización (RFC 8414)
- `GET /.well-known/oauth-protected-resource`: metadatos del recurso protegido (RFC 9728)
- `GET /authorize`: endpoint de autorización
- `POST /token`: endpoint de tokens
- `POST /register`: registro dinámico de clientes

El flujo usa PKCE (`S256`) y los scopes `openid email access offline_access`. Vea
**[Conectar su cliente](/es/api/connect-clients/)** para los pasos de cada cliente.

## Clave de API estática

Para los clientes que no pueden completar el intercambio OAuth (Cursor, v0.dev, Antigravity), genere una
clave de API estática y envíela como Bearer token.

### Generar una clave

1. Abra la aplicación de Teramot y vaya a la página **MCP**.
2. En la sección **API Keys** (claves de API), ingrese un nombre (por ejemplo, `cursor-work`) y haga clic en **Generate Key**.
3. **Copie la clave en ese momento: no se vuelve a mostrar.**

Puede crear varias claves (una por cliente o máquina) y eliminar cualquiera de ellas más tarde desde la
misma página.

### Usar la clave

Envíela en el encabezado `Authorization`:

```http
Authorization: Bearer YOUR_API_KEY
```

La mayoría de los clientes MCP aceptan un encabezado personalizado en la configuración del servidor:

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

> [!WARNING]
> Trate las claves de API como contraseñas. Dan acceso completo a los datos de su cuenta. Si una clave se filtra,
> elimínela desde la página **MCP → API Keys** y genere una nueva.

## Errores

| Situación | Resultado |
| --- | --- |
| Sin token en un método autenticado | `401 Unauthorized` |
| Token vencido o inválido | `401 Unauthorized` |
| Falta `Mcp-Session-Id` en `GET /mcp` | `401 Unauthorized` (`missing Mcp-Session-Id; re-initialize via POST`) |
