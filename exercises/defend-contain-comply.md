# Technical Workshop — In-person or virtual (2 hr): Defend, Contain, Comply — Vulnerability Lifecycle Automation with Ansible Automation Platform

This workshop provides hands-on experience managing a complete vulnerability lifecycle — from CVE detection through automated containment to compliant container delivery — using Red Hat Ansible Automation Platform. Participants respond to a critical CVE alert on a production RHEL application server, using AAP Controller, Event-Driven Ansible (EDA), and integrations with Splunk (SIEM) and Open Policy Agent (OPA) to defend, patch, and prove compliance without manual intervention.

* **Module 1 — DEFEND**: Detect a critical CVE and automate containment when no patch exists
* **Module 2 — CONTAIN**: Apply a policy-gated patching workflow once an errata is published
* **Module 3 — COMPLY**: Validate compliance, apply CIS hardening, generate evidence, and deliver a hardened container

> **NOTE**
>
> Complete the modules in order — each builds on the previous one.

## Workshop Resources

<table>
<thead>
<tr>
<th>Resource</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>Workshop content and exercises</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-defend-contain-comply/modules/index.html">rhpds.github.io/zt-ans-defend-contain-comply</a></td>
</tr>
<tr>
<td>Follow-up assets</td>
<td><b>TO DO</b></td>
</tr>
<tr>
<td>Post-event survey</td>
<td><b>TO DO</b></td>
</tr>
<tr>
<td>Certain registration page &amp; promotional email copy</td>
<td><b>TO DO</b></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><b>TO DO</b></td>
</tr>
<tr>
<td>Certain event banners</td>
<td><b>TO DO</b></td>
</tr>
</tbody>
</table>

## Key themes

* Event-Driven Ansible for automated incident response
* Policy-as-Code with OPA for gated patching decisions
* Workflow orchestration with approval gates and compliance verification
* Secure supply chain delivery with Podman containerization and image scanning
* End-to-end audit trail from detection to remediation

## Who is this workshop best for?

This workshop is intended for security and operations teams who need to automate vulnerability response, policy-gated remediation, and compliance hardening with Ansible Automation Platform. Attendees will work with Event-Driven Ansible, Open Policy Agent (OPA), Splunk, and Ansible Automation Platform workflows in a realistic CVE management scenario.

## Target audience

* Platform engineers managing RHEL infrastructure at scale
* Security operations teams evaluating AAP for vulnerability response
* DevOps practitioners interested in policy-as-code for patching
* SysAdmins and IT Operations
* Anyone interested in Event-Driven Ansible for security automation

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* Familiarity with Ansible concepts such as playbooks, inventories, and job templates
* Attendees must bring/use a laptop with ADMIN rights and the ability to SSH to a lab environment hosted in a public cloud.
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed.

There is no student prep work required prior to the workshop. It is recommended to complete the free Red Hat training course [Ansible Basics: Automation Technical Overview](https://www.redhat.com/en/services/training/do007-ansible-essentials-simplicity-automation-technical-overview).

## Presentation Deck

- **TO DO** — Google Slides link for Red Hat employees

## Lab provisioner

Labs are available via the [Red Hat Demo Platform](https://catalog.demo.redhat.com/catalog) under the [Defend, Contain, Comply](https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-defend-contain-comply.prod) catalog item.

## Lab Index (Estimate total time ⏱️ 120-150 minutes)

<table>
<thead>
<tr>
<th>Activity</th>
<th>Link</th>
<th>Estimated Time</th>
</tr>
</thead>
<tbody>
<tr>
<td>Workshop Overview</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-defend-contain-comply/modules/01-overview.html">📖 View Overview</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Introduction + Workshop Brief</td>
<td><b>TO DO</b></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 1: DEFEND — Detect and Contain</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-defend-contain-comply/modules/03-module-01-defend.html">🚀 Launch Exercise</a></td>
<td>⏱️ 40 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Brief for Module 2</td>
<td><b>TO DO</b></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td>Module 2: CONTAIN — Policy-Gated Remediation</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-defend-contain-comply/modules/04-module-02-contain.html">🚀 Launch Exercise</a></td>
<td>⏱️ 40 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Brief for Module 3</td>
<td><b>TO DO</b></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td>Module 3: COMPLY — Audit, Harden, Deliver</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-defend-contain-comply/modules/05-module-03-comply.html">🚀 Launch Exercise</a></td>
<td>⏱️ 40 minutes</td>
</tr>
<tr>
<td>Conclusion</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-defend-contain-comply/modules/99-conclusion.html">📖 View Conclusion</a></td>
<td>⏱️ 10 minutes</td>
</tr>
</tbody>
</table>

## Demos

Individual modules from this workshop can be used as standalone demos for vulnerability detection and containment, policy-gated patching, or compliance hardening scenarios.

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)

## Documentation

- [https://github.com/rhpds/zt-ans-defend-contain-comply](https://github.com/rhpds/zt-ans-defend-contain-comply)
- [https://github.com/ansible/workshops](https://github.com/ansible/workshops)

# Going Further

Additional collateral for security automation:

<table>
<thead>
<tr>
<th>Title</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>Implementing Zero Trust with Ansible Automation Platform</td>
<td><a href="zero-trust">Zero Trust workshop</a></td>
</tr>
<tr>
<td>Security automation collateral</td>
<td><b>TO DO</b></td>
</tr>
</tbody>
</table>

<br>

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.
Please open an [issues on Github](https://github.com/ansible/workshops/issues/new?title=New+defend+contain+comply+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
