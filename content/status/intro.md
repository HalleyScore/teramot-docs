---
title: "System Status"
weight: 10
---

Stay informed on the real-time status of all Teramot services and infrastructure.

Live service status, scheduled maintenance and incident history are published at **[status.teramot.com](https://status.teramot.com)**.

{{< cards >}}
  {{< card link="https://status.teramot.com" title="Open status.teramot.com" icon="server" >}}
{{< /cards >}}

## Availability target

Teramot targets **99% monthly availability**, measured on [status.teramot.com](https://status.teramot.com):

- **What is measured**: the six services listed on the status page: the web app, the API, the MCP connector, sign-in, this documentation site and the website.
- **How it is measured**: each service is checked every minute. Downtime runs from the first failed check to the next healthy one. Monthly availability is the time without downtime divided by the time monitored, per calendar month (UTC).
- **Exclusions**: scheduled maintenance announced on the status page.

The status page publishes each month's figure and every outage its checks detect.

The 99% target applies to every plan. It is an objective, not a guarantee. Enterprise plans can add a contractual availability commitment of up to 99.9% with service credits, set out in the order form.

## Support

If you experience service issues, contact our support team at [support@teramot.com](mailto:support@teramot.com).
