# Security Incident Response Policy
**Northlane Systems — IT & Security**
**Effective Date:** November 1, 2025
**Document ID:** IT-SEC-009

## Purpose
This policy defines how Northlane Systems detects, reports, and responds to security incidents, including data breaches, malware infections, and unauthorized access attempts.

## Incident Classification
Incidents are classified into three severity tiers:

- **SEV-1 (Critical):** Active data breach, ransomware, or compromise of production customer data. Requires immediate escalation to the CISO and executive team.
- **SEV-2 (High):** Suspected unauthorized access, compromised credentials, or malware on a single endpoint without evidence of lateral movement.
- **SEV-3 (Low):** Phishing attempts, policy violations, or suspicious activity with no confirmed compromise.

## Reporting an Incident
Any employee who suspects a security incident must report it immediately via:
1. The #security-incidents Slack channel (monitored 24/7)
2. Email to security-incidents@northlane.example
3. The Incident Hotline for after-hours SEV-1 events

Employees should never attempt to independently investigate or remediate a suspected breach; doing so can destroy forensic evidence.

## Response Timeline
- SEV-1 incidents: acknowledgment within 15 minutes, containment plan within 1 hour
- SEV-2 incidents: acknowledgment within 1 hour, containment plan within 4 hours
- SEV-3 incidents: acknowledgment within 1 business day

## Containment and Eradication
The Security team leads containment efforts, which may include isolating affected devices from the network, disabling compromised accounts, and rotating affected credentials. Engineering teams must comply with Security team directives during an active incident, including emergency deployment freezes if requested.

## Customer and Regulatory Notification
For incidents involving customer data, Legal and Security jointly determine notification obligations under applicable regulations (e.g., GDPR, CCPA) and contractual commitments. Notifications are typically issued within 72 hours of confirming a reportable breach, consistent with regulatory requirements.

## Post-Incident Review
Within 5 business days of resolution, the Security team conducts a blameless post-incident review, documenting root cause, timeline, and remediation actions. Findings are shared with relevant engineering leads to prevent recurrence.

## Policy Owner
Chief Information Security Officer (CISO), Northlane Systems
