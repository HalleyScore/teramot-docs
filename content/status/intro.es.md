---
title: "Estado del sistema"
weight: 10
---

Manténgase al tanto del estado en tiempo real de todos los servicios y la infraestructura de Teramot.

El estado de los servicios en vivo, los mantenimientos programados y el historial de incidentes se publican en **[status.teramot.com](https://status.teramot.com)**.

{{< cards >}}
  {{< card link="https://status.teramot.com" title="Abrir status.teramot.com" icon="server" >}}
{{< /cards >}}

## Objetivo de disponibilidad

Teramot tiene como objetivo una **disponibilidad mensual del 99%**, medida en [status.teramot.com](https://status.teramot.com):

- **Qué se mide**: los seis servicios de la página de estado: la aplicación web, la API, el conector MCP, el inicio de sesión, este sitio de documentación y el sitio web.
- **Cómo se mide**: cada servicio se verifica cada minuto. Una caída va desde el primer chequeo fallido hasta el siguiente sano. La disponibilidad mensual es el tiempo sin caídas dividido por el tiempo monitoreado, por mes calendario (UTC).
- **Exclusiones**: los mantenimientos programados anunciados en la página de estado.

La página de estado publica la cifra de cada mes y cada caída que detectan sus chequeos.

El objetivo del 99% aplica a todos los planes. Es un objetivo, no una garantía. Los planes Enterprise pueden sumar un compromiso contractual de disponibilidad de hasta el 99,9% con créditos de servicio, establecido en la orden de compra.

## Soporte

Si tiene problemas con el servicio, contacte a nuestro equipo de soporte en [support@teramot.com](mailto:support@teramot.com).
