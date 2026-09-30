---
title: "🔐 Security & Confidentiality Commitments"
linkTitle: "Security & Confidentiality Commitments"
weight: 40
---

These are the commitments Teramot makes to its customers regarding the security and confidentiality of the Teramot Data Engineering Platform, together with the requirements we set for ourselves to meet them. They supplement the [Terms of Service](/compliance/Transparency/terms-of-service/) and the [Privacy Policy](/compliance/transparency/privacy-policy/), and they are the objectives against which our controls are examined in our SOC 2 report.

**Effective date:** 13 August 2026 · **Applies to:** the Teramot Data Engineering Platform, hosted in AWS `us-east-1`.

---

## Security

### S1 · Your data is not accessible to other customers

Every project is assigned a unique use case identifier that segments its resources: its own data catalog database and its own dedicated storage prefix. Access tokens are resolved to exactly one use case **on our servers** — the client never supplies a tenant identifier, and no API operation accepts one — so a token cannot be made to address another customer's data. Customers using direct query access receive credentials whose permissions enumerate only their own databases and storage prefixes.

### S2 · Your data is encrypted at rest and in transit

**At rest:** AES-256 across our production database clusters, object storage, key-value stores, block volumes and infrastructure state. Credentials you provide for your source systems are additionally encrypted with AES-256-GCM at the field level, decrypted only at the moment of use, never written to logs, and never propagated to other services.

**In transit:** TLS 1.2 minimum, TLS 1.3 supported, on all public endpoints, with HTTP redirected to HTTPS. Internal service-to-service traffic uses mutual TLS. Administrative access runs over a dedicated VPN.

### S3 · Access to your data is restricted and reviewed

Access to production is granted on a least-privilege basis through federated single sign-on with multi-factor authentication enforced at the identity provider. Our personnel hold no standing database passwords. All administrative access requires the VPN. **Access rights are reviewed at least quarterly**, and changes are tracked to completion. Personnel access is revoked within three business days of termination.

Teramot personnel do not access customer business data in the ordinary course of operating the platform. Where access is technically necessary to operate or support the service, it is limited to authorized administrators and recorded in our audit logs.

### S4 · Unauthorized and anomalous activity is detected

Continuous threat detection across our cloud control plane, DNS, network flow, object storage and runtime layers, with findings routed to our security on-call. Every cloud API call is recorded in an immutable audit trail with log file validation enabled. Network flow logs are retained 365 days. Application write actions are recorded with actor, endpoint and timestamp. Automated alarms cover error rates, latency, host health and database resource thresholds.

### S5 · Vulnerabilities are identified and remediated

Vulnerability scanning runs at least quarterly across external-facing systems. Dependency and code scanning run continuously on every repository. **An independent penetration test is performed at least annually**, and findings are tracked to closure on our security board with critical and high severity prioritized.

### S6 · Changes are authorized, tested and traceable

All infrastructure is defined as code. Every application change requires peer review before merge. Deployments run through federated CI with no static credentials, and promote through development and staging before production.

### S7 · Security incidents are contained, investigated and communicated

We maintain a documented incident response plan, tested at least annually. Where an incident affects your data, **we notify you within 72 hours of confirmed identification**, and provide a written post-incident report including root cause and corrective action.

---

## Confidentiality

### C1 · Your data is used only to serve you

We do not train models of our own. We procure third-party model inference under terms that exclude API traffic from provider training. Code and analyses generated within your project stay within your project and are not exposed to any other customer. We perform no fine-tuning on customer data.

### C2 · Data is classified and handled by sensitivity

We maintain a data classification policy under which customer data receives the strictest handling requirements, with documented retention and disposal procedures.

### C3 · Your data is retained only while you are a customer

Business data is retained for the life of the agreement. On termination we execute a documented deletion procedure covering object storage, the data catalog, application metadata, usage records and tracing data, and issue written confirmation of destruction on completion.

### C4 · Confidentiality extends to our people and our suppliers

All personnel sign confidentiality agreements at onboarding. Written agreements with our vendors and subprocessors carry confidentiality commitments. No subcontractor has access to our production environment.

---

## Independent assurance

Our controls over these commitments are examined by an independent service auditor under **SOC 2**. Our report is available under NDA — see [SOC 2 Report Access](/compliance/about/#soc-2-report-access).

We rely on the following subservice organizations, whose own controls are necessary alongside ours: **Amazon Web Services** for cloud infrastructure, and **Anthropic** and **OpenAI** for model inference.

## Your responsibilities

Some of these commitments depend on controls at your end — protecting the access tokens and credentials we issue you, scoping the source-system credentials you provide us, and notifying us of personnel changes. These are set out in full as complementary user entity controls in our SOC 2 report.

## Contact

Security questions, vulnerability reports and incident notifications: **[security@teramot.com](mailto:security@teramot.com)**
