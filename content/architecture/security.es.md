---
title: "Seguridad y control de acceso"
weight: 90
---

Esta página describe cómo se controla quién accede a qué dentro de Teramot, y cómo se protege la plataforma. Los compromisos formales de Teramot en esta materia están en [Compromisos de seguridad y confidencialidad](/compliance/Transparency/security-commitments/), y el estado de las certificaciones en [Compliance](/compliance/about/).

## Autenticación

- El inicio de sesión se delega en un **proveedor de identidad administrado** compatible con OpenID Connect, con flujo de código de autorización y PKCE.
- La API valida en cada pedido la firma, el emisor, la audiencia y el sujeto de cada token.
- Los asistentes externos se autentican con **OAuth 2.1**. Ver [Formas de consumo](/es/architecture/consumption/#asistentes-de-ia-vía-mcp).
- Las claves de API y las access keys de MCP se guardan como hash.

## Roles y permisos

Cada miembro de un workspace tiene uno de cuatro roles: **Owner**, **Admin**, **Analyst** y
**Read only**, y cada uno incluye lo que pueden hacer los de abajo. Una persona también
puede tener un rol en un solo proyecto, que tiene prioridad sobre su rol del workspace ahí;
alguien invitado solo a un proyecto ve ese proyecto y nada más del workspace. Qué puede
hacer cada rol, acción por acción, está en
[Roles y permisos](/es/product/concepts/roles-and-permissions/).

Los permisos se aplican en la API, que es el único punto de entrada a los datos. Por eso
rigen igual en la aplicación web, para un asistente de IA vía MCP y en las integraciones.

### Acceso del personal de Teramot

El personal de Teramot no accede a los datos de negocio de los clientes durante la operación normal. Cuando un acceso es técnicamente necesario para operar la plataforma o dar soporte, se limita a personal autorizado y las acciones quedan registradas.

## Registro de actividad

Cada proyecto tiene un **registro de actividad**, visible para administradores. Registra las acciones que modifican el proyecto, con autor, acción y fecha, sin importar si se hicieron desde la aplicación web, la API o un asistente vía MCP.

Las consultas de lectura no se registran en este log.

## Protección de la plataforma

| Área | Control |
|---|---|
| **Red** | Los servicios de procesamiento y las bases de datos corren en subredes privadas, sin acceso directo desde Internet. Solo los balanceadores y la CDN reciben tráfico público. |
| **Cifrado en tránsito** | TLS 1.2 como mínimo y TLS 1.3 disponible en los endpoints públicos; HTTP se redirige a HTTPS. TLS mutuo entre servicios internos. |
| **Cifrado en reposo** | AES-256 en almacenamiento de objetos, bases de datos y volúmenes. |
| **Credenciales de origen** | Se guardan cifradas en reposo, se usan solo al momento de conectar, no se escriben en logs y la API nunca las devuelve. |
| **Aplicación web** | Política de seguridad de contenido (CSP) estricta, HSTS y protección contra embebido en otros sitios. |
| **Detección de amenazas** | Detección continua sobre la cuenta de nube, la red, el almacenamiento y los servicios, con alertas al equipo de seguridad. |
| **Auditoría de infraestructura** | Cada llamada a la API de la nube se registra en un log inmutable con validación de integridad. Los logs de red y de servicios se conservan 365 días. |
| **Cambios** | Toda la infraestructura está definida como código. Cada cambio pasa por revisión y se despliega primero en desarrollo y staging. |
| **Continuidad** | Bases de datos con copias de seguridad diarias, réplica en una segunda zona de disponibilidad y protección contra borrado. |

## Proveedores que procesan datos

| Proveedor | Función | Qué datos recibe |
|---|---|---|
| **Amazon Web Services** | Infraestructura, almacenamiento, procesamiento e inferencia (Amazon Bedrock) | Todos los datos del servicio |
| **Anthropic** | Modelos de lenguaje | Lo descrito en [Agentes de IA](/es/architecture/ai-agents/) |
| **OpenAI** | Modelos de lenguaje | Lo descrito en [Agentes de IA](/es/architecture/ai-agents/) |
| **LangSmith** | Observabilidad de IA | Trazas de los agentes |
| **Langfuse** | Observabilidad de IA | Trazas de las herramientas MCP |
| **Temporal Cloud** | Orquestación de workflows | Metadatos de ejecución |
| **Proveedor de identidad (Logto)** | Autenticación | Datos de cuenta de los usuarios |
| **Sentry** | Monitoreo de errores | Información técnica de errores |
| **Stripe** | Facturación | Datos de facturación |
| **Microsoft Clarity** | Analítica de uso de la aplicación web | Datos de navegación en la aplicación |
