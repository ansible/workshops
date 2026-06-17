# Ansible for Red Hat Enterprise Linux Technical Workshop

> **IMPORTANT TO NOTE** 
> 
> This is the 90 minute version of this workshop.  For the longer extended session please [🔬 click here](rhel.md)
>

If you're new to Ansible Automation, but want a quicker version of the original RHEL workshop, this 90-minute workshop provides you with fewer exercises, focused on cloud provisioning, converting bash/shell commands to Ansible, all the way to utilizing RHEL System Roles.

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
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90">labs.demoredhat.com/exercises/ansible_rhel_90</a></td>
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
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90">Presenter instructions and guide</a></td>
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

- [PDF](../../decks/ansible_rhel_90.pdf) - For everyone
- [Google Slides](https://docs.google.com/presentation/d/10rltay3pr3ZLzFMGTPnc6CAtsm0AwQ3L_XbwmmMNMdc/edit?usp=sharing) - For Red Hat employees

## Lab Agenda (Estimate total time ⏱️ 90 minutes)

<ul>
<li><b>Slides: Introduction + Workshop Brief</b> [Estimated Time ⏱️ 10 minutes]<br>
<a target="_blank" href="https://docs.google.com/presentation/d/10rltay3pr3ZLzFMGTPnc6CAtsm0AwQ3L_XbwmmMNMdc/edit?usp=sharing">[ 🖥️ Slides ]</a>
</li><br>
<li><b>Exercise 1: Overview of public cloud provisioning</b> [Estimated Time ⏱️ 15 minutes]<br>
<a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/1-setup">[ 🚀 Start Exercise ]</a>
</li><br>
<li><b>Exercise 2: The Ansible Basics</b> [Estimated Time ⏱️ 10 minutes]<br>
<a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/2-thebasics">[ 🚀 Start Exercise ]</a>
</li><br>
<li><b>Exercise 3: Deploying applications to linux hosts</b> [Estimated Time ⏱️ 10 minutes]<br>
<a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/3-playbook">[ 🚀 Start Exercise ]</a>
</li><br>
<li><b>Exercise 4: Retrieving information from automation hosts</b> [Estimated Time ⏱️ 10 minutes]<br>
<a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/4-variables">[ 🚀 Start Exercise ]</a>
</li><br>
<li><b>Exercise 5: Self-service IT via surveys</b> [Estimated Time ⏱️ 10 minutes]<br>
<a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/5-surveys">[ 🚀 Start Exercise ]</a>
</li><br>
<li><b>Exercise 6: Overview of system roles for RHEL</b> [Estimated Time ⏱️ 10 minutes]<br>
<a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/6-system-roles">[ 🚀 Start Exercise ]</a>
</li><br>
<li><b>Slides: Close Out &amp; Q&amp;A</b> [Estimated Time ⏱️ 5 minutes]<br>
<a target="_blank" href="https://docs.google.com/presentation/d/10rltay3pr3ZLzFMGTPnc6CAtsm0AwQ3L_XbwmmMNMdc/edit?usp=sharing">[ 🖥️ Slides ]</a>
</li>
</ul>

## Lab Index

<table>
<thead>
<tr>
<th>Exercise</th>
<th>Description</th>
<th>Link</th>
<th>Estimated Time</th>
</tr>
</thead>
<tbody>
<tr>
<td>Exercise 1 — Overview of public cloud provisioning</td>
<td>Set up your lab environment and explore cloud provisioning</td>
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/1-setup">🚀 Launch Lab</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Exercise 2 — The Ansible Basics</td>
<td>Learn fundamental Ansible concepts and ad hoc commands</td>
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/2-thebasics">🚀 Launch Lab</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 3 — Deploying applications to linux hosts</td>
<td>Create and run your first Ansible playbook</td>
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/3-playbook">🚀 Launch Lab</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 4 — Retrieving information from automation hosts</td>
<td>Learn how to use variables and facts in playbooks</td>
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/4-variables">🚀 Launch Lab</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 5 — Self-service IT via surveys</td>
<td>Add surveys to job templates for user-driven input</td>
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/5-surveys">🚀 Launch Lab</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 6 — Overview of system roles for RHEL</td>
<td>Use RHEL System Roles for configuration management</td>
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/ansible_rhel_90/6-system-roles">🚀 Launch Lab</a></td>
<td>⏱️ 10 minutes</td>
</tr>
</tbody>
</table>

## Lab provisioner

[RHPDS](https://rhpds.redhat.com/) — Internal Red Hat Product Demo System. [AWS Lab Provisioner](https://github.com/ansible/workshops) — playbook that spins up instances on AWS for students to perform the provided exercises.

## Demos

Demos are intended for effectively demonstrating Ansible capabilities with prescriptive guides on the Ansible Automation Workshop infrastructure. See the [workshops repository](https://github.com/ansible/workshops) for demo content.

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)

## Documentation

- [How to contribute](https://github.com/ansible/workshops)
- [How to use the AWS Lab Provisioner](https://github.com/ansible/workshops)
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

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an [issues on Github](https://github.com/ansible/instruqt/issues/new?title=New+rhel+90min+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
