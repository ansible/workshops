# Ansible Lightspeed and Development Technical Workshop

> **IMPORTANT TO NOTE** 
> 
> This is the 90 minute version of this workshop.  For the longer 4-hour session please [🔬 click here](lightspeed-4.md)
>

This workshop is for the Ansible automation engineer or application developer.  While their experience, skills, and job roles differ, both of these personas create automation.  This includes writing Ansible Playbooks, Ansible Roles, and Ansible Content Collections and learning how to distribute these throughout the organization. This workshop will provide an opinionated experience for both of these roles.

The Ansible developer experience includes numerous capabilities to aid in the creation of Ansible automation content.  This includes an Ansible plugin for Microsoft Visual Studio Code as well as generative AI (artificial intelligence) integrations such as Red Hat Ansible Lightspeed with watsonx Code Assistant.

After finishing this lab you are ready to start taking advantage of the numerous Ansible content tools included in your Red Hat Ansible Automation Platform subscription.

> **IMPORTANT TO NOTE** 
> 
> This workshop is focused on the automation development capabilities of Ansible and is highly focused on using an IDE (Integrated Development Environment), Visual Studio Code, as well as other various CLI tools that run on Red Hat Enterprise Linux.  It is highly encouraged to attend the Ansible Red Hat Enterprise Linux Workshop before attending this workshop.
>

> **IMPORTANT TO NOTE** 
> 
> This workshop requires a Red Hat employee instructor
> 

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
<td><a target="_blank" href="https://labs.demoredhat.com/exercises/instruqt/lightspeed-4">labs.demoredhat.com/exercises/instruqt/lightspeed-4</a></td>
</tr>
<tr>
<td>Follow-up assets</td>
<td><a target="_blank" href="https://docs.google.com/spreadsheets/d/1D7FyUExIWR6aZxXevbUHZ_G4nDQsUhAbASVEGAvc2Wc/edit?usp=sharing">Follow-up assets spreadsheet</a></td>
</tr>
<tr>
<td>Post-event survey</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1wviedVHnvy49j68Bf8-6EN4c-TMzqkk6kx5xivk3aXk/edit?usp=sharing">Post-event survey</a></td>
</tr>
<tr>
<td>Certain registration page &amp; promotional email copy</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1bhJKfCyTOWMeECzA3D-xp7pQQweJOaM6khfAtAxRllw/edit?usp=sharing">Registration page &amp; promotional email copy</a></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><a target="_blank" href="https://labs.demoredhat.com/webpages/lightspeed-4">Presenter instructions and guide</a></td>
</tr>
<tr>
<td>Certain event banners</td>
<td><a target="_blank" href="https://drive.google.com/drive/folders/1D9vkg8zF3jYFCDqD4unrVZ_tuAseqyPO?usp=sharing">Event banners (Google Drive)</a></td>
</tr>
</tbody>
</table>

## Target audience

Anyone who is currently writing Ansible automation content such as Ansible Playbooks.  This includes the Ansible for Red Hat Enterprise Linux personas including DevOps engineers, operations engineers, systems engineers, release engineers, system administrators, developers, operations staff, network engineers, security professionals, and anyone interested in IT automation.

## Attendee Prerequisites

Student has one (1) of the following:

* Student has completed the Ansible Red Hat Enterprise Linux Workshop
* Student has completed the [Write your first playbook interactive lab](https://docs.google.com/document/d/1nnhVUhFs2Z-WliGae505yc2GEzNhrE74ceec8p83ntk/edit?usp=sharing)
* Student has completed the Red Hat training course [Ansible Basics: Automation Technical Overview](https://www.redhat.com/en/services/training/do007-ansible-essentials-simplicity-automation-technical-overview)

* A basic understanding of working with Linux systems
* A basic understanding of [Visual Studio Code](https://code.visualstudio.com/). [Available for MacOS, Windows and Linux]
* Attendees must bring/use a laptop with ADMIN rights and the ability to SSH to a lab environment hosted in a public cloud.
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed.

There is no student prep work required prior to the workshop.

## Presentation Deck

- [Google Slides](https://docs.google.com/presentation/d/1Px4Fn6VBfQeAZnx4_3ydUZDNEteOTrYPfXCOfFOZTsc/edit?usp=sharing) - For Red Hat employees

## Lab Agenda (Estimate total time ⏱️ 90 minutes)

Each workshop module and lab is designed to stand on its own, but may also be combined to suit your event and time constraints.  A sample 90 agenda and suggested pairings for shorter events can be found below.

<ul>
<li><b>Slides: Introduction + Workshop Brief</b> [Estimated Time ⏱️ 15 minutes]<br>
<a target="_blank" href="https://docs.google.com/presentation/d/1Px4Fn6VBfQeAZnx4_3ydUZDNEteOTrYPfXCOfFOZTsc/edit?usp=sharing">[ 🖥️ Slides ]</a>
</li><br>
<li><b>Get started with ansible-builder</b> [Estimated Time ⏱️ 30 minutes]<br>
Install ansible-builder v3 and learn how to create custom execution environments.<br>
<a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=ansible+builder&item=zt-ansiblebu.zt-ans-bu-ansible-builder.prod">[ 🚀 Start Exercise ]</a>
</li><br>
<li><b>Slides: Introduction to Ansible Lightspeed with IBM watsonx Code Assistant</b> [Estimated Time ⏱️ 15 minutes]<br>
<a target="_blank" href="https://docs.google.com/presentation/d/1Px4Fn6VBfQeAZnx4_3ydUZDNEteOTrYPfXCOfFOZTsc/edit?usp=sharing">[ 🖥️ Slides ]</a>
</li><br>
<li><b>Get started with Ansible Lightspeed with IBM watsonx Code Assistant</b> [Estimated Time ⏱️ 30 minutes]<br>
Learn how to configure, activate, and use Ansible Lightspeed to generate Ansible content.<br>
<a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=lightspeed&item=zt-ansiblebu.zt-ans-lightspeed-101.prod">[ 🚀 Start Exercise ]</a>
</li>
</ul>

## Lab Index

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
<td>Get started with ansible-builder</td>
<td>Install ansible-builder v3 and learn how to create custom execution environments.</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=ansible+builder&item=zt-ansiblebu.zt-ans-bu-ansible-builder.prod">🚀 Launch Lab</a></td>
<td>⏱️ 30 minutes</td>
</tr>
<tr>
<td>Get started with Ansible Lightspeed with IBM watsonx Code Assistant</td>
<td>Learn how to configure, activate, and use Ansible Lightspeed to generate Ansible content.</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=lightspeed&item=zt-ansiblebu.zt-ans-lightspeed-101.prod">🚀 Launch Lab</a></td>
  <!-- NOTE: This Lightspeed lab is deprecated and the commercial lab requires Red Hat supervision-->
<td>⏱️ 30 minutes</td>
</tr>
</tbody>
</table>

## Supplemental Lab

<ul>
<li><b>Sign and verify projects with Red Hat Ansible Automation Platform</b> [Estimated Time ⏱️ 45 minutes]<br>
Sign source repositories that include Ansible Playbooks and content, and validate signed content in the automation controller.<br>
<a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?search=sign+and+verify&item=zt-ansiblebu.zt-ans-bu-verify-sign.prod">[ 🚀 Start Exercise ]</a>
</li>
</ul>

## Lab provisioner

All of these labs can be provisioned on RHDP. They can be provisioned separately with the links of each individual lab above or together on the [multi-asset workshop section](https://catalog.demo.redhat.com/multi-workshop/).

## Demos

Any of the individual labs (that make up the workshop) can be used as a standalone demo.

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)

## Documentation

- [https://github.com/ansible/instruqt](https://github.com/ansible/instruqt)

# Going Further

Additional material for Event-Driven Ansible

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
<td>Learn how to set up Ansible Lightspeed with watsonx Code Assistant—from installation and configuration to content creation.
</td>
<td>Step-by-step guide</td>
<td><a target="_blank" href="https://www.redhat.com/en/blog/getting-started-red-hat-ansible-lightspeed-ibm-watsonx-code-assistant">📖 Read Guide</a></td>
</tr>
<tr>
<td>Red Hat talks to RedMonk</td>
<td>Analyst material</td>
<td><a target="_blank" href="https://redmonk.com/videos/a-redmonk-conversation-ai-and-it-automation-with-ansible">🎥 Watch Interview</a></td>
</tr>
<tr>
<td>Explore this playlist of announcements and demo</td>
<td>YouTube playlist</td>
<td><a target="_blank" href="https://www.youtube.com/playlist?list=PLdu06OJoEf2bVLR899FuKc3AiuJvbIRZU">🎥 Ansible Lightspeed with watsonx Code Assistant</a></td>
</tr>
</tbody>
</table>

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an [issues on Github](https://github.com/ansible/instruqt/issues/new?title=New+lightspeed+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
