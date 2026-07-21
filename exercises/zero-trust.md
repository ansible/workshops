# Implementing Zero Trust with Ansible Automation Platform

In traditional network models, a firewall protects the edge, and anything "inside" is implicitly trusted — a system that critically fails when attackers breach the perimeter, insiders go rogue, or workloads span distributed clouds. Zero Trust flips this model, dictating that every single request — whether from a person, an application, or an automation job — must prove it should be allowed through strong identity management, explicit policy enforcement, and continuous verification.

This workshop provides hands-on experience building a NIST SP 800-207 compliant environment where Red Hat Ansible Automation Platform sits at the center of the architecture. By integrating various infrastructure and security tools — such as Open Policy Agent (OPA) for policy decisions, HashiCorp Vault for secrets, and Splunk for threat signaling — Ansible Automation Platform acts as the unified gateway, ensuring that every operational change passes through identity checks, policy gates, and audit trails.

**Key themes explored in the workshop:**

- **Ansible Automation Platform as the Policy Enforcement Point**: By acting as the Policy Enforcement Point (PEP) specified in this NIST standard, Ansible Automation Platform prevents tangles of one-off tool integrations. It ties identity providers, policy engines, secret managers, and SIEMs into a single cohesive platform.
- **Policy as Code**: Utilizing OPA as the Policy Decision Point (PDP) from NIST, every job is gated at the platform level. This ensures strict adherence to principles like "deny by default" and "least privilege," stopping unauthorized actions before a playbook even begins.
- **Security Posture as Playbooks**: The workshop instills the discipline that configurations in a Zero Trust Architecture must be repeatable, auditable, and version-controlled. Every integration is defined as an Ansible Playbook, meaning the playbooks themselves are the verifiable security posture.
- **Automated Containment & Dynamic Credentials**: Emphasizes "no passwords on disk" approach using short-lived credentials from HashiCorp Vault, alongside Ansible Automation Platform's Event-Driven Ansible (EDA), which automatically closes the detection-to-containment loop in seconds when threats are detected.

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
<td><a target="_blank" href="https://docs.google.com/presentation/d/1K08HLtn03tzT7RqmYn6xEeec6D3ONRXn8Y7LHc6dzf4/edit?slide=id.g3d680270401_0_0#slide=id.g3d680270401_0_0">🖥️ Google Slides</a></td>
</tr>
<tr>
<td>Post-event survey</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1tA8-qFOjrGnFXB9oTOQucri0UGwF4qRs8xjgFqHBxs4/edit?tab=t.0">📋 Post-event survey</a></td>
</tr>
<tr>
<td>Registration page & promotional email copy</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1u__keNCmzp4hEOktAxNVXcIVqgQgZdJcPhUySw7zFH8/edit?tab=t.0">📝 Registration page & promotional email copy</a></td>
</tr>
<tr>
<td>Event banners</td>
<td><a target="_blank" href="https://new.express.adobe.com/id/urn:aaid:sc:VA6C2:18999ac4-dc21-41dd-8448-34e0609691ed?category=search">🎨 Adobe Express banners</a></td>
</tr>
</tbody>
</table>

## Target Audience

- Security operations, engineers, and architects
- SysAdmins and ITOps
- Network Architects and operations
- Cloud Architects and operations
- IT Architects
- Platform Engineers

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* A basic understanding of [Visual Studio Code](https://code.visualstudio.com/). [Available for MacOS, Windows and Linux]
* Student has one (1) of the following:
  * Student has completed the Ansible Red Hat Enterprise Linux Workshop
  * Student has completed the Write your first playbook interactive lab
  * Student has completed the Red Hat training course [Ansible Basics: Automation Technical Overview](https://www.redhat.com/en/services/training/au094-ansible-essentials-simplicity-automation-technical-overview)
* Attendees must bring/use a laptop with ADMIN rights and the ability to SSH to a lab environment hosted in a public cloud.
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed.

## Presentation Deck

- [Google Slides](https://docs.google.com/presentation/d/1K08HLtn03tzT7RqmYn6xEeec6D3ONRXn8Y7LHc6dzf4/edit?slide=id.g3d680270401_0_0#slide=id.g3d680270401_0_0) - For Red Hat employees

## Lab Options

<table>
<thead>
<tr>
<th>Option</th>
<th>Link</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>Launch on RHDP</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-zta-aap.prod&utm_source=webapp&utm_medium=share-link">🚀 Launch Lab</a></td>
<td>Provision a full lab environment on the Red Hat Demo Platform</td>
</tr>
<tr>
<td>View Instructions</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-zta-aap/modules/index.html">📖 View Showroom</a></td>
<td>Browse the lab instructions and exercises</td>
</tr>
</tbody>
</table>

## Lab provisioner

This lab environment is available via the [Red Hat Demo Platform](https://catalog.demo.redhat.com/catalog) under the [Implementing Zero Trust with Ansible Automation Platform](https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-zta-aap.prod&utm_source=webapp&utm_medium=share-link) catalog item.

## Exercises

<table>
<thead>
<tr>
<th>Activity</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>Slides</b>: Introduction + Workshop Brief</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1K08HLtn03tzT7RqmYn6xEeec6D3ONRXn8Y7LHc6dzf4/edit?slide=id.g3d680270401_0_0#slide=id.g3d680270401_0_0">🖥️ Google Slides</a></td>
</tr>
<tr>
<td>Exercise 1 — Verify ZTA Components and AAP Integration</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-zta-aap/modules/module-01.html">🚀 Launch Exercise</a></td>
</tr>
<tr>
<td>Exercise 2 — Deploy application with short-lived credentials</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-zta-aap/modules/module-02.html">🚀 Launch Exercise</a></td>
</tr>
<tr>
<td>Exercise 3 — AAP Policy as Code: platform-gated patching</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-zta-aap/modules/module-03.html">🚀 Launch Exercise</a></td>
</tr>
<tr>
<td>Exercise 4 — SPIFFE-verified network VLAN management</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-zta-aap/modules/module-04.html">🚀 Launch Exercise</a></td>
</tr>
<tr>
<td>Exercise 5 — Automated incident response with Splunk and EDA</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-zta-aap/modules/module-05.html">🚀 Launch Exercise</a></td>
</tr>
<tr>
<td colspan="2"><b>*Extended security workshop option</b></td>
</tr>
<tr>
<td>Exercise 6 — SSH lockdown and break-glass</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-zta-aap/modules/module-06.html">🚀 Launch Exercise</a></td>
</tr>
<tr>
<td>Exercise 7 — Wazuh SIEM (optional)</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-zta-aap/modules/module-07.html">🚀 Launch Exercise</a></td>
</tr>
</tbody>
</table>

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.
Please open an [issues on Github](https://github.com/ansible/workshops/issues/new?title=New+zero+trust+workshop+issue&body=)

![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
