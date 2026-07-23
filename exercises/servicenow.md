# Getting Started with ServiceNow Automation

The Getting Started with ServiceNow Automation Workshop is an engaging, 90-minute, hands-on session designed to introduce participants to the world of IT Service Management (ITSM) automation, emphasizing the integration of Ansible with ServiceNow. Throughout the workshop, attendees will gain practical experience and insights into automating tasks and processes with Ansible Automation Platform and ServiceNow. This course is ideal for individuals looking to enhance their ITSM skills and understand the integrations and use-cases between Ansible and ServiceNow in a dynamic, interactive learning environment.

The ServiceNow integration for Ansible Automation Platform is made possible through a certified content collection called `servicenow.itsm`. This collection is made available on Automation Hub on [console.redhat.com](https://console.redhat.com/ansible/automation-hub/repo/published/servicenow/itsm). The environment that is being created for you includes this collection in an execution environment that allows Ansible Automation Platform to execute tasks against a ServiceNow instance.

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
<td><a target="_blank" href="https://labs.demoredhat.com/webpages/servicenow">labs.demoredhat.com/webpages/servicenow</a></td>
</tr>
<tr>
<td>Follow-up assets</td>
<td><a target="_blank" href="https://docs.google.com/spreadsheets/d/1K09dmr1BAupgECzSUJd6jiRxeClmFVe4oEUTmzJn_fI/edit?usp=sharing">Follow-up assets spreadsheet</a></td>
</tr>
<tr>
<td>Post-event survey</td>
<td><a target="_blank" href="https://docs.google.com/document/d/12co-AdFYWWtHiErX041YvGbqcHmBprrA18dIdC3lrI0/edit?usp=sharing">Post-event survey</a></td>
</tr>
<tr>
<td>Certain registration page &amp; promotional email copy</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1ywFKQ4mm1ODxL5PZ9FVzmkiGHOX06-oECqDjAs5-uOY/edit?usp=sharing">Registration page &amp; promotional email copy</a></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><a target="_blank" href="https://labs.demoredhat.com/webpages/servicenow">Presenter instructions and guide</a></td>
</tr>
<tr>
<td>Certain event banners</td>
<td><a target="_blank" href="https://drive.google.com/drive/folders/1LCluPvSQaEFWpT0NmFMGwgJrCcyuaHld?usp=sharing">Event banners (Google Drive)</a></td>
</tr>
</tbody>
</table>

## Who is this workshop best for?

This workshop is intended as an introductory course for using Red Hat Ansible Automation Platform in conjunction with an IT Service Management (ITSM) tool, specifically showcasing ServiceNow. The intended audience is someone who has limited or no exposure to writing Ansible Playbooks or using Ansible Automation Platform. This workshop will cover common scenarios and topics and is best suited for IT infrastructure engineers or IT managers looking to integrate their existing ITSM workflows into automated processes that can help them reduce their mean time to resolution (MTTR).

## Target audience

Automation engineers, DevOps engineers, and operations teams looking to automate ServiceNow workflows.

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* A basic understanding of [Visual Studio Code](https://code.visualstudio.com/). [Available for MacOS, Windows and Linux]
* Attendees must bring/use a laptop with ADMIN rights and the ability to SSH to a lab environment hosted in a public cloud.
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed.

There is no student prep work required prior to the workshop. Students would greatly benefit from watching the free training course [Ansible Basics: Automation Technical Overview](https://www.redhat.com/en/services/training/do007-ansible-essentials-simplicity-automation-technical-overview).

## Presentation Deck

- [Google Slides](https://docs.google.com/presentation/d/1sE8nZJjQw74QyWccufUVNwEtIepxPYTbsn5YfjN3oU8/edit?usp=sharing) - For Red Hat employees

## Lab provisioner

This lab environment is available via the [Red Hat Demo Platform](https://catalog.demo.redhat.com/catalog) under the [Getting Started with ServiceNow Automation](https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-servicenow.prod) catalog item.

This lab is also available as a [🔬 Public Lab](https://zero.rhdp.net/lab/zt-ansiblebu.zt-ans-bu-serviceNow.prod) — publicly available, free Red Hat account required.

## Lab Index (Estimate total time ⏱️ 90 minutes)

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
<td><a target="_blank" href="https://docs.google.com/presentation/d/1sE8nZJjQw74QyWccufUVNwEtIepxPYTbsn5YfjN3oU8/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 30 minutes</td>
</tr>
<tr>
<td>Module 1: Creating Incidents</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-serviceNow/modules/module-01.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 2: Problem Management</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-serviceNow/modules/module-02.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 3: Change Management</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-serviceNow/modules/module-03.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 4: CMDB Management</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-serviceNow/modules/module-04.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 5: Record Cleanup</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-serviceNow/modules/module-05.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 6: ServiceNow Inventory</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-serviceNow/modules/module-06.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
</tbody>
</table>

## Demos

Any of the individual labs (that make up the workshop) can be used as a standalone demo. The platform is available for Red Hat employees, partners and customers 24/7/365 on [https://red.ht/ansible-labs](https://red.ht/ansible-labs).

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)

## Documentation

- [https://github.com/ansible/workshops](https://github.com/ansible/workshops)
- Blogs: 
  - [Introducing the Ansible API for ServiceNow ITSM](https://www.ansible.com/blog/introducing-the-ansible-api-for-servicenow-itsm)
  - [Enabling modern IT service management actions for ServiceNow with Red Hat Ansible Automation Platform](https://www.redhat.com/en/blog/enabling-modern-it-service-management-actions-servicenow-red-hat-ansible-automation-platform)
  - [Automating ServiceNow with Red Hat Ansible Automation Platform](https://www.ansible.com/blog/certified-collection-servicenow)
  - [Inside the newest features in the Red Hat Ansible Certified Content Collection for ServiceNow ITSM](https://www.ansible.com/blog/inside-the-newest-features-in-the-red-hat-ansible-certified-content-collection-for-servicenow-itsm)
- Overview: [Ansible Certified Content Collection for ServiceNow](https://www.redhat.com/en/resources/ansible-certified-content-collection-for-servicenow-overview)
- YouTube: [Automate ServiceNow ITSM](https://www.youtube.com/playlist?list=PLdu06OJoEf2b2O-R635ZqZERrh8Xg5e-3)
- Webinar: [Ansible certified Content Collection for ServiceNow](https://www.ansible.com/resources/webinars-training/red-hat-ansible-certified-content-collection-for-servicenow-ondemand?sc_cid=7013a000002vvHjAAI)
- Website: [Ansible Automation Platform: ServiceNow Integration](https://www.ansible.com/integrations/it-service-management/servicenow?hsLang=en-us)

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an [issues on Github](https://github.com/ansible/workshops/issues/new?title=New+servicenow+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
