---
title: "Teramot — Compliance & Security"
weight: 10
---

<div style="text-align: center; margin: 1rem 0">
  <img class="tm-only-light" src="/img/compliance/LogoNegroTeramotHorizontal.png" alt="Teramot Logo" width="200">
  <img class="tm-only-dark" src="/img/compliance/LogoBlancoTeramotHorizontal.png" alt="Teramot Logo" width="200">
</div>

---

### Executive Summary

- **SOC 2 Type I audit** – *Successfully completed* with a U.S. auditing firm. Teramot has obtained its first SOC 2 report, covering the Security criteria. December 2025.

<div style="text-align: center; margin: 1rem 0">
  <img src="/img/compliance/soc2-new.png" alt="SOC 2" height="90" style="object-fit: contain" />
</div>

- **SOC 2 Type II audit** – *Observation period in progress* as part of the path to our SOC 2 Type II report.  
- **ISO 27001 documentation & evidence** – currently underway (*Vanta sync in progress*).  
- **Compliance monitoring** – supported by **Vanta**, our continuous compliance facilitator. Vanta continuously monitors our **attack surface**, **infrastructure posture**, and **vulnerabilities**, enabling timely remediation and patching.  
- **Recent Pentest** – performed by **Faraday Sec (Argentina)**. **15 vulnerabilities** were identified and **fully remediated**. 


### Security & Development Tools

<div style="text-align: center; margin: 24px 0">
  <!-- First row - Core Security Tools -->
  <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 20px; margin-bottom: 16px">
    <img class="tm-only-light" src="/img/compliance/faraday-logo-light.png" alt="Faraday Sec" height="70" style="border-radius: 6px; padding: 8px; background: var(--tm-rule)">
    <img class="tm-only-dark" src="/img/compliance/faraday-logo-light.png" alt="Faraday Sec" height="70" style="border-radius: 6px; padding: 8px; background: var(--tm-rule)">
    <img src="/img/compliance/soc2-logo.png" alt="SOC 2" height="90" style="object-fit: contain; margin-left: 10px; margin-right: 10px" />
    <img src="/img/compliance/vanta-logo.svg" alt="Vanta" height="70" style="object-fit: contain; border-radius: 6px; padding: 8px; background: var(--tm-rule)" />
    <img src="/img/compliance/bitdefender.png" alt="Bitdefender" height="70" style="object-fit: contain" />
  </div>
  
  <!-- Second row - Infrastructure & Development Tools -->
  <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 20px">
    <img src="/img/compliance/aws-waf.png" alt="AWS WAF" height="70" style="object-fit: contain" />
    <img src="/img/compliance/guardduty.png" alt="AWS GuardDuty" height="70" style="object-fit: contain" />
    <img src="/img/compliance/cloudwatch.png" alt="CloudWatch" height="70" style="object-fit: contain" />
    <img
      src="/img/compliance/terraform.png"
      alt="Terraform"
      height="70"
      style="object-fit: contain; border-radius: 6px; padding: 8px; background: var(--tm-rule)"
    />    
    <img
      src="/img/compliance/bitwarden.png"
      alt="Bitwarden"
      height="70"
      style="object-fit: contain"
    />
    <img src="/img/compliance/dependabot.png" alt="Dependabot" height="70" style="object-fit: contain" />
  </div>
</div>

---

# 1 Company & Governance Snapshot

| Item | Detail |
| --- | --- |
| **Legal Name** | Halley LLC |
| **Headquarters** | Rosario, Argentina |
| **U.S. Entity** | Registered in Delaware |
| **HQ Address** | 16192 Coastal Highway, City of Lewes, Country of Sussex, DE 19958 |
| **Countries Served** | Argentina · United States |
| **Information Security Committee** | Bruno Ruyu · Lucas Uzal · Leandro Ruspini · Ezequiel Alejandro Mora · Valentín Torassa Colombero |
| **Policy Approval** | Approved by Valentín Torassa Colombero – Cybersecurity Analyst |

---

# 2 Compliance Posture Overview

| Framework / Report | Status | Auditor | Period | Next Review |
| --- | --- | --- | --- | --- |
| **SOC 2 Type I** | Completed | U.S. Audit Firm | Completed audit period | Report available under NDA upon request |
| **SOC 2 Type II** | Observation period in progress | U.S. Audit Firm | Observation period | Report expected after observation period completion |
| **ISO 27001** | Documentation & evidence in progress | — | Continuous | Target 2026 |
| **Local Privacy Laws** | Law 25.326 (Argentina), SOC 2 Privacy Criteria | — | Ongoing | Annual Review Q1 2026 |

---

# 3 Information Security Management System (ISMS) Highlights

> For complete policy documentation, visit the policies section

| Domain | Key Control | Implementation |
| --- | --- | --- |
| **Identity & Access Management** | MFA enabled across AWS, GitHub & Vanta accounts | Active |
| **Cloud Security** | GuardDuty, CloudTrail, WAF, and CloudWatch alerts | Continuous |
| **Endpoint Protection** | Bitdefender GravityZone | Active |
| **Secrets & Passwords** | Bitwarden vaults with MFA & org-scoped policies | Enforced |
| **Encryption** | All data encrypted *at rest* and *in transit* | AES-256 / TLS 1.3 |
| **Vulnerability & Patch Mgmt** | Continuous monitoring + remediation validated via pentests | Active |
| **Compliance Monitoring** | Vanta agent with AWS integration | Continuous |
| **Secure Development** | CI/CD with tests, Dependabot, Terraform validation, and peer review | Active |

---

# 4 Secure Software Development Life-Cycle (SSDLC)

1. Feature branches with **Pull Requests**.  
2. **Automated tests** and **CI/CD pipelines** (GitHub Actions) validate each change.  
3. Progressive deployments to **dev**, **stg**, and **prd** on **AWS ECS**.  
4. Infrastructure is defined and deployed with **Terraform**.  
5. **Dependabot** manages security/dependency updates.  
6. Access protected with **MFA** and **least-privilege IAM**.

---

# 6 Data Privacy & Residency

| Domain | Detail |
| --- | --- |
| **Hosting Region** | AWS (us-east-1) |
| **Processing Model** | 100% cloud; no on-premises processing |
| **Compliance** | Law 25.326 (Argentina) and SOC 2 Privacy Criteria |
| **Encryption** | AES-256 at rest, TLS 1.3 in transit |
| **Retention & Deletion** | According to contractual and regulatory requirements |

---

# 7 Incident Response & Monitoring

| Component | Description |
| --- | --- |
| **Detection Tools** | AWS GuardDuty, CloudWatch Alarms, Bitdefender, AWS WAF |
| **Response Team** | Managed internally by Cybersecurity and DevOps |
| **Notification** | Customers are informed promptly upon validation of any security event |
| **Root Cause Analysis** | Documented internally and shared under NDA upon request |

---

# 8 Third-Party Risk & Pentest Results

- **Independent Security Testing** by **Faraday Sec (Argentina)**, validating **15 vulnerabilities** — all **resolved**. Reports and remediation tracking documented with continuous follow-up.


---

# 9 Revision History

| Date | Author | Role | Notes |
| --- | --- | --- | --- |
| Oct 2025 | Valentín Torassa Colombero | Cybersecurity & Compliance Analyst | Initial release of the Teramot Compliance & Security Pack |

---

### SOC 2 Report Access

If your organization needs access to Teramot’s final SOC 2 report, you can request it by emailing **security@teramot.com** (subject to NDA).

---

<p align="center"><b>Teramot – Halley LLC • Rosario / Miami • October 2025 — Version 1.0</b></p>
