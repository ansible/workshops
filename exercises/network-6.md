# Ansible Network Automation Workshop

> **IMPORTANT TO NOTE**
>
> This is the extended version of this workshop (~6 hours). For the shorter 90 minute session please [🔬 click here](network)
>

This comprehensive, full-day workshop covers Ansible Automation with respect to routers and switches. In the first half, attendees will learn command-line Ansible for network automation — exploring the lab environment, writing playbooks, gathering facts, and using resource modules. In the second half, attendees will apply what they've learned to Ansible Automation Platform — exploring automation controller, creating job templates, surveys, role-based access control, and workflows.

After finishing this lab you are ready to start using Ansible for your network automation requirements.

> **NOTE**
>
> In this workshop, attendees will be managing network devices, specifically a Cisco IOS-XE router.

> **IMPORTANT TO NOTE:** This is NOT a deep dive, in the weeds, advanced workshop — it's an introduction.

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
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/index.html">rhpds.github.io/zt-network-automation-workshop</a></td>
</tr>
<tr>
<td>Follow-up assets</td>
<td><a target="_blank" href="https://docs.google.com/spreadsheets/d/1zZk8Cqs0gXAKfrEE_OMn_edYHXsv6rPtMMO4rG0KVpk/edit?usp=sharing">Follow-up assets spreadsheet</a></td>
</tr>
<tr>
<td>Post-event survey</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1Wph4-abRIClCC8y1M91xZMntl0pzs6Br10fNXQW4rIQ/edit?usp=sharing">Post-event survey</a></td>
</tr>
<tr>
<td>Certain registration page &amp; promotional email copy</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1AntZfBybq_yOKJKb0khrRY63XI3_-CIT20SYrF2_Aqg/edit?usp=sharing">Registration page &amp; promotional email copy</a></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/index.html">Presenter instructions and guide</a></td>
</tr>
<tr>
<td>Certain event banners</td>
<td><a target="_blank" href="https://drive.google.com/drive/folders/1NPKWa3IUqURjAS2c38LM_LgpqXO0AeKL?usp=sharing">Event banners (Google Drive)</a></td>
</tr>
</tbody>
</table>

## Who is this workshop best for?

This workshop is intended as a comprehensive course for Ansible Network Automation. For the condensed 90-minute introduction, see [Getting Started with Network Automation](network). For more in-depth training please refer to [Red Hat Training Ansible for Network Automation](https://www.redhat.com/en/services/training/do457-ansible-network-automation). The intended audience is someone who has limited or no exposure to writing Ansible Playbooks or using Ansible Automation Platform. This workshop will cover common network scenarios and topics and is best suited for network engineers or folks interested in network automation.

## Target audience

This workshop is geared toward network operators, network engineers, cloud administrators, DevOps engineers, security professionals and anyone interested in network automation.

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* A basic understanding of [Visual Studio Code](https://code.visualstudio.com/). [Available for MacOS, Windows and Linux]
* Attendees must bring/use a laptop with ADMIN rights and the ability to SSH to a lab environment hosted in a public cloud.
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed.

There is no student prep work required prior to the workshop. It is recommended to complete the free Red Hat training course [Ansible Basics: Automation Technical Overview](https://www.redhat.com/en/services/training/do007-ansible-essentials-simplicity-automation-technical-overview).

## Presentation Deck

- [Google Slides](https://docs.google.com/presentation/d/1TVeHwv-4dtOmh8FMJa2Kd0Md8aqWGI0vHIwBpFih6_0/edit?usp=sharing) - For Red Hat employees

## Lab provisioner

Labs are available via the [Red Hat Demo Platform](https://catalog.demo.redhat.com/catalog) under the [Introduction to Ansible Network Automation Workshop](https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/zt-ansiblebu.ansible-network-automation-workshop.prod) catalog item. For large events, use the lab hotstarter: [https://red.ht/lab-hotstarter](https://red.ht/lab-hotstarter)

## Lab Index (Estimate total time ⏱️ 6 hours)

### Section 1 — Network Basics

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
<td><b>Slides</b>: Introduction + Workshop Brief</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1TVeHwv-4dtOmh8FMJa2Kd0Md8aqWGI0vHIwBpFih6_0/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>Exercise 1-1 — Explore the lab environment</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/03-module-01-explore-lab.html">🚀 Launch Exercise</a></td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td>Exercise 1-2 — First Ansible Playbook</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/04-module-02-first-playbook.html">🚀 Launch Exercise</a></td>
<td>⏱️ 30 minutes</td>
</tr>
<tr>
<td>Exercise 1-3 — Ansible facts</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/05-module-03-facts.html">🚀 Launch Exercise</a></td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td>Exercise 1-4 — Resource modules</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/06-module-04-resource-modules.html">🚀 Launch Exercise</a></td>
<td>⏱️ 30 minutes</td>
</tr>
</tbody>
</table>

☕ **Break** — ⏱️ 15 minutes

### Section 2 — Intro to Ansible Automation Platform

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
<td><b>Slides</b>: Ansible Automation Platform Introduction</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1TVeHwv-4dtOmh8FMJa2Kd0Md8aqWGI0vHIwBpFih6_0/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Exercise 2-1 — Explore Ansible Automation Platform</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/07-module-05-explore-controller.html">🚀 Launch Exercise</a></td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td>Exercise 2-2 — Job templates</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/08-module-06-job-template.html">🚀 Launch Exercise</a></td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td>Exercise 2-3 — Surveys</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/09-module-07-survey.html">🚀 Launch Exercise</a></td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td>☕ <b>Break</b></td>
<td></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Exercise 2-4 — RBAC</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/10-module-08-rbac.html">🚀 Launch Exercise</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>Exercise 2-5 — Workflows</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-network-automation-workshop/modules/11-module-09-workflow.html">🚀 Launch Exercise</a></td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Close Out &amp; Q&amp;A</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1TVeHwv-4dtOmh8FMJa2Kd0Md8aqWGI0vHIwBpFih6_0/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 10 minutes</td>
</tr>
</tbody>
</table>

## Supplemental Labs

<table>
<thead>
<tr>
<th>Lab Title</th>
<th>Description</th>
<th>Link</th>
<th>Estimated Time</th>
</tr>
</thead>
<tbody>
<tr>
<td>Network automation basics: Resource modules</td>
<td>Learn Red Hat Ansible Automation Platform playbook basics for network automation.</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=resource+module&item=zt-ansiblebu.ansible-network-automation-basics-lab-3.prod">🚀 Launch Lab</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>Network automation basics: Facts</td>
<td>Learn about retrieving facts from a Cisco IOS-XE device.</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=facts&item=zt-ansiblebu.ansible-network-automation-basics-lab-2.prod">🚀 Launch Lab</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>Network automation basics: Infrastructure visibility and awareness</td>
<td>Learn how to use Red Hat Ansible Automation Platform to retrieve facts from network infrastructure and create dynamic documentation.</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=network+automation+-+infra&item=zt-ansiblebu.zt-ans-bu-network-lab-2.prod">🚀 Launch Lab</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>Network automation basics: Surveys</td>
<td>Learn how to create an automation controller survey to configure a Cisco IOS network device.</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=network+automation+basics+-&item=babylon-catalog-prod%2Fzt-ansiblebu.ansible-network-automation-basics-lab-4.prod">🚀 Launch Lab</a></td>
<td>⏱️ 20 minutes</td>
</tr>
</tbody>
</table>

## Demos

Any of the individual labs (that make up the workshop) can be used as a standalone demo.

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)

## Documentation

- [https://github.com/ansible/instruqt](https://github.com/ansible/instruqt)
- [https://red.ht/lab-hotstarter](https://red.ht/lab-hotstarter)

# Going Further

Additional collateral for network automation:

<table>
<thead>
<tr>
<th>ebook title</th>
<th>external link</th>
<th>RHCC Link (employees and partners)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Network automation for everyone</td>
<td><a target="_blank" href="https://www.redhat.com/en/engage/network-automation-everyone-s-202101221234">on redhat.com</a></td>
<td><a target="_blank" href="https://content.redhat.com/content/rhcc/us/en/assets/display.html?id=026234ee-52b2-4cb4-84b8-66489678236a">Content Center</a></td>
</tr>
<tr>
<td>Network automation guide: Expand automation across multivendor networks</td>
<td><a target="_blank" href="https://www.redhat.com/en/engage/network-automation-guide-20221202">on redhat.com</a></td>
<td><a target="_blank" href="https://content.redhat.com/content/rhcc/us/en/assets/display.html?id=5c47feab-360d-42c4-8335-d7199cee4985">Content Center</a></td>
</tr>
<tr>
<td>Connect and communicate with reliable, security-focused network</td>
<td><a target="_blank" href="https://www.redhat.com/en/resources/connect-and-communicate-network-ecosystem-ebook">on redhat.com</a></td>
<td><a target="_blank" href="https://content.redhat.com/content/rhcc/us/en/assets/display.html?id=e0506582-97d4-4b47-bb13-c63df3c694cf">Content Center</a></td>
</tr>
<tr>
<td>Automate your network with Red Hat</td>
<td><a target="_blank" href="https://www.redhat.com/en/resources/network-automation-technical-e-book">on redhat.com</a></td>
<td><a target="_blank" href="https://content.redhat.com/content/rhcc/us/en/assets/display.html?id=363c136c-0c30-4d74-a3d0-59f3d1eea97a">Content Center</a></td>
</tr>
</tbody>
</table>

<br>

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an [issues on Github](https://github.com/ansible/instruqt/issues/new?title=New+network+automation+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
