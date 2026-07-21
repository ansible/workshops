# Ansible for Red Hat Enterprise Linux Technical Workshop

> **IMPORTANT TO NOTE**
>
> This is the 90 minute version of this workshop. For the longer extended session please [🔬 click here](rhel)
>

This condensed workshop provides a quick introduction to Ansible Automation, starting with command-line fundamentals and progressing to Ansible Automation Platform. You'll write playbooks, use variables, create projects and job templates, work with surveys, configure role-based access control, and explore RHEL System Roles — all in 90 minutes.

> **IMPORTANT TO NOTE:** This is NOT a deep dive, in the weeds, advanced workshop — it's an introduction.

**This is documentation for Ansible Automation Platform 2.6**

> **NOTE:** This content has been updated to reflect the latest changes from the Ansible Automation Platform 2.0 release. [Learn more about how the 2.0 release impacts this workshop](https://docs.google.com/presentation/d/1VK8rF2jB6jqlcjgUzONBEGm8seqL6bfzFeyOwohICH4/edit?usp=sharing) or watch the [video walkthrough](https://www.youtube.com/watch?v=Oe1AbAvn9gg).

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
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/index.html">rhpds.github.io/zt-ans-bu-rhel</a></td>
</tr>
<tr>
<td>Follow-up handouts/assets</td>
<td><a target="_blank" href="https://redhat.dam.aprimo.com/Assets/Collections/~3bba623d9bf24b7bbc59acc9010b799d?state=5dcc589990f94524877315f4788b21d2">Follow-up handouts/assets</a></td>
</tr>
<tr>
<td>Post-event survey</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1g4Q6IsV5--6H9ETARe-IL-FcUSmbO2Rv0TDXty1qwLk/edit">Post-event survey</a></td>
</tr>
<tr>
<td>Certain registration page &amp; promotional email copy</td>
<td><a target="_blank" href="https://docs.google.com/document/d/10qE8mI00Lonf5CTDVMuaEsnoIeGkUTHpZry4_pXd9Ok/edit?usp=sharing">Registration page &amp; promotional email copy</a></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/index.html">Presenter instructions and guide</a></td>
</tr>
<tr>
<td>Certain event banners</td>
<td><a target="_blank" href="https://drive.google.com/drive/folders/1QSGJltjVWGuLCt_CavddVMYSCKMzOTuj?usp=sharing">Event banners (Google Drive)</a></td>
</tr>
</tbody>
</table>

## Who is this workshop best for?

This workshop is intended for people who want to learn the basics of Ansible Automation in a shorter timeframe. They want to understand how Ansible Automation Platform works and how it can be used to automate basic tasks. The instructor will provide information on the differentiation between the upstream project and the product offering from Red Hat. Join if you never tried Red Hat Ansible Automation.

## Target audience

DevOps engineers, operations engineers, systems engineers, release engineers, system administrators, developers, operations staff, network engineers, security professionals, and anyone interested in IT automation.

Given the current resources within the Ansible Business Unit for supporting Ansible Automation Workshops, we are restricting lab size to 49 seats (48 student workbench + 1 instructor workbench) to improve supportability and resiliency of workshops ordered through the RHPDS platform. If you need more than 49 seats, you may order multiple quantities of the workshop.

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* Attendees must bring/use a laptop with ADMIN rights and the ability to SSH to a lab environment hosted in a public cloud
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed

There is no student prep work required prior to the workshop.

## Presentation Deck

- [PDF](../decks/ansible_rhel_90.pdf) - For everyone
- [Google Slides](https://docs.google.com/presentation/d/10rltay3pr3ZLzFMGTPnc6CAtsm0AwQ3L_XbwmmMNMdc/edit?usp=sharing) - For Red Hat employees

## Lab provisioner

This lab environment is available via the [Red Hat Demo Platform](https://catalog.demo.redhat.com/catalog) under the [Ansible for Red Hat Enterprise Linux Workshop (90min)](https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-rhel-90.prod&utm_source=webapp&utm_medium=share-link) catalog item.

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
<td><a target="_blank" href="https://docs.google.com/presentation/d/10rltay3pr3ZLzFMGTPnc6CAtsm0AwQ3L_XbwmmMNMdc/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 1 — Writing Your First Playbook</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/module-01.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Exercise 2 — Using Variables</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/module-02.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 3 — Projects &amp; Job Templates</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/module-10.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 4 — Surveys</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/module-11.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 5 — Role-based Access Control</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/module-12.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 6 — RHEL System Roles</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/module-14.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 7 — Wrap-Up</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-rhel/modules/module-15.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Close Out &amp; Q&amp;A</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/10rltay3pr3ZLzFMGTPnc6CAtsm0AwQ3L_XbwmmMNMdc/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 5 minutes</td>
</tr>
</tbody>
</table>

## Demos

Demos are intended for effectively demonstrating Ansible capabilities with prescriptive guides on the Ansible Automation Workshop infrastructure. See the [workshops repository](https://github.com/ansible/workshops) for demo content.

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)

## Documentation

- [How to contribute](https://github.com/ansible/workshops)
- [FAQ](https://github.com/ansible/workshops)

# Going Further

Additional material for Ansible and RHEL Automation

<table>
<thead>
<tr>
<th>Title</th>
<th>Type</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>Ansible Automation Platform Self-Paced Labs</td>
<td>Interactive labs</td>
<td><a target="_blank" href="https://red.ht/ansible-labs">🔬 Self-Paced Labs</a></td>
</tr>
<tr>
<td>Red Hat Training and Certification for AAP</td>
<td>Training</td>
<td><a target="_blank" href="https://red.ht/aap_training">📖 Training Catalog</a></td>
</tr>
<tr>
<td>Get a Trial Subscription for AAP</td>
<td>Trial</td>
<td><a target="_blank" href="http://red.ht/try_ansible">🧪 Start Trial</a></td>
</tr>
</tbody>
</table>

<br>

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an [issues on Github](https://github.com/ansible/workshops/issues/new?title=New+rhel+90min+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
