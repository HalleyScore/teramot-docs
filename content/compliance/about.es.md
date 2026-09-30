---
title: "Teramot — Cumplimiento y seguridad"
weight: 10
---

<div style="text-align: center; margin: 1rem 0">
  <img class="tm-only-light" src="/img/compliance/LogoNegroTeramotHorizontal.png" alt="Teramot Logo" width="200">
  <img class="tm-only-dark" src="/img/compliance/LogoBlancoTeramotHorizontal.png" alt="Teramot Logo" width="200">
</div>

---

### Resumen ejecutivo

- **SOC 2 Tipo I** – *Ya aprobado* con una firma auditora de EE. UU. Teramot cuenta con su primer informe SOC 2, cubriendo el criterio de Seguridad. Diciembre 2025.  

<div style="text-align: center; margin: 1rem 0">
  <img src="/img/compliance/soc2-logo.png" alt="SOC 2" height="90" style="object-fit: contain" />
</div>

- **SOC 2 Tipo II** – Actualmente nos encontramos en el *período de observación* necesario para obtener el informe SOC 2 Tipo II.  
- **ISO 27001** – Documentación y evidencias en curso (*Vanta sync in progress*).  
- **Monitoreo de cumplimiento** – impulsado por **Vanta**, nuestro facilitador de compliance: monitoreamos de forma continua la **superficie de ataque**, la **postura de infraestructura** y **vulnerabilidades** para su remediación oportuna.  
- **Pentest reciente** – realizado por **Faraday Sec (Argentina)**. Se identificaron **15 vulnerabilidades** y ya fueron **remediadas**. 

### Herramientas de Seguridad y Desarrollo

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

# 1 Compañía & Gobernanza

| Ítem | Detalle |
| --- | --- |
| **Razón social** | Halley LLC |
| **Sede principal** | Rosario, Argentina |
| **Entidad en EE. UU.** | Registrada en Delaware |
| **Dirección HQ (EE. UU.)** | 16192 Coastal Highway, City of Lewes, Country of Sussex, DE 19958 |
| **Países atendidos** | Argentina · United States |
| **Comité de Seguridad de la Información** | Bruno Ruyu · Lucas Uzal · Leandro Ruspini · Ezequiel Alejandro Mora · Valentín Torassa Colombero |
| **Aprobación de políticas** | Aprobadas por Valentín Torassa Colombero – Analista de Ciberseguridad |

---

# 2 Panorama de Cumplimiento

| Marco / Reporte | Estado | Auditor | Período | Próxima revisión |
| --- | --- | --- | --- | --- |
| **SOC 2 Tipo I** | Completado | Firma auditora de EE. UU. | Período de auditoría completado | Informe disponible bajo NDA a solicitud |
| **SOC 2 Tipo II** | Período de observación en curso | Firma auditora de EE. UU. | Período de observación | Informe estimado tras finalizar el período de observación |
| **ISO 27001** | Documentación & evidencias en curso | — | Continuo | Objetivo 2026 |
| **Privacidad local** | Ley 25.326 (AR), Criterios de Privacidad SOC 2 | — | Continuo | Revisión anual Q1 2026 |

---

# 3 SGSI — Destacados

> La documentación completa de políticas está disponible en la sección de políticas

| Dominio | Control clave | Implementación |
| --- | --- | --- |
| **Identidades & accesos** | MFA en AWS, GitHub y Vanta | Activo |
| **Seguridad en la nube** | GuardDuty, CloudTrail, WAF y alertas de CloudWatch | Continuo |
| **Protección de endpoints** | Bitdefender GravityZone | Activo |
| **Secretos & contraseñas** | Bitwarden con MFA y políticas organizacionales | Aplicado |
| **Encriptación** | Datos *en reposo* y *en tránsito* | AES-256 / TLS 1.3 |
| **Vulnerabilidades & parcheo** | Monitoreo continuo + remediación validada vía pentests | Activo |
| **Monitoreo de compliance** | Agente Vanta e integración con AWS | Continuo |
| **Desarrollo seguro** | CI/CD con pruebas, Dependabot, validación de Terraform y peer review | Activo |

---

# 4 Ciclo de Vida de Desarrollo Seguro (SSDLC)

1. Desarrollo por ramas de **feature** y **Pull Requests**.  
2. **Pruebas automatizadas** y **pipelines CI/CD** (GitHub Actions) validan cada cambio.  
3. Despliegue progresivo a **dev**, **stg** y **prd** sobre **AWS ECS**.  
4. Infraestructura definida y desplegada con **Terraform**.  
5. **Dependabot** asiste con actualizaciones de seguridad/dependencias.  
6. Accesos protegidos con **MFA** y **roles IAM de mínimo privilegio**.

---

# 6 Privacidad y Residencia de Datos

| Dominio | Detalle |
| --- | --- |
| **Región de hosting** | AWS (us-east-1) |
| **Modelo de procesamiento** | 100 % en la nube; sin on-premises |
| **Cumplimiento** | Ley 25.326 (Argentina) y Criterios de Privacidad SOC 2 |
| **Encriptación** | AES-256 en reposo, TLS 1.3 en tránsito |
| **Retención & eliminación** | Según requisitos contractuales y regulatorios |

---

# 7 Respuesta a Incidentes & Monitoreo

| Componente | Descripción |
| --- | --- |
| **Herramientas de detección** | AWS GuardDuty, CloudWatch Alarms, Bitdefender, AWS WAF |
| **Equipo de respuesta** | Gestionado internamente por Ciberseguridad y DevOps |
| **Notificación** | Los clientes son informados oportunamente una vez validado cualquier evento |
| **Análisis de causa raíz** | Documentado internamente y compartido bajo NDA si se solicita |

---

# 8 Riesgo de Terceros & Resultados de Pentest

- **Pruebas de seguridad independientes** realizadas por **Faraday Sec (Argentina)**, validando **15 vulnerabilidades** — todas **resueltas**. Reportes y remediaciones documentados, con seguimiento continuo.


---

# 9 Historial de revisiones

| Fecha | Autor | Rol | Notas |
| --- | --- | --- | --- |
| Oct 2025 | Valentín Torassa Colombero | Analista de Ciberseguridad & Cumplimiento | Publicación inicial del Paquete de Cumplimiento y Seguridad de Teramot |

---

### Acceso al informe SOC 2

Si tu organización cliente necesita acceder al informe final de SOC 2 de Teramot, podés solicitarlo escribiendo a **security@teramot.com** (sujeto a NDA).

---

<p align="center"><b>Teramot – Halley LLC • Rosario / Miami • Octubre 2025 — Versión 1.0</b></p>
