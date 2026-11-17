# Introduction to Ansible Development Tools

> **IMPORTANT TO NOTE**
>
> This is the extended version of this workshop (~3 hours). For the shorter 2 hour session please [🔬 click here](dev-tools)
>

This comprehensive workshop covers the full Ansible content development lifecycle — from scaffolding a collection in VS Code, through writing and testing custom modules with Molecule, pytest-ansible, and tox-ansible, to building execution environments with ansible-builder and signing content with ansible-sign. The lab uses Red Hat OpenShift Dev Spaces as the development environment.

After finishing this lab you are ready to start creating, testing, and distributing production-quality Ansible content.

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
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/index.html">rhpds.github.io/ansible-dev-tools-showroom</a></td>
</tr>
<tr>
<td>Lab source repository</td>
<td><a target="_blank" href="https://github.com/rhpds/ansible-dev-tools-showroom">github.com/rhpds/ansible-dev-tools-showroom</a></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/index.html">Presenter instructions and guide</a></td>
</tr>
</tbody>
</table>

## Who is this workshop best for?

This workshop is the comprehensive version of the Ansible Development Tools workshop. For the condensed 2-hour introduction, see [Getting Started with Ansible Development Tools in VS Code](dev-tools). The intended audience is anyone who writes Ansible automation and wants to learn the full content development lifecycle — from scaffolding through testing, packaging, and signing. This workshop includes additional exercises on tox-ansible test orchestration that are not in the shorter version.

## Target audience

Ansible developers, automation engineers, DevOps engineers, platform engineers, systems administrators, and anyone interested in building and testing Ansible content.

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* A basic understanding of Ansible (playbooks, modules, roles)
* A basic understanding of [Visual Studio Code](https://code.visualstudio.com/). [Available for MacOS, Windows and Linux]
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed

There is no student prep work required prior to the workshop. It is recommended to complete the free Red Hat training course [Ansible Basics: Automation Technical Overview](https://www.redhat.com/en/services/training/do007-ansible-essentials-simplicity-automation-technical-overview).

## Presentation Deck

- [Google Slides](https://docs.google.com/presentation/d/1OLc0hNX_2EpfIkbeWaP_aH5dOAcA1YygXofJ0LPPxOE/edit?usp=sharing) - For Red Hat employees

## Lab provisioner

This lab environment is available via the [Red Hat Demo Platform](https://catalog.demo.redhat.com/catalog) under the [Introduction to Ansible Development Tools](https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/published.ansible-dev-tools.prod) catalog item.

## Lab Index (Estimate total time ⏱️ 3 hours)

### Introduction

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
<td><a target="_blank" href="https://docs.google.com/presentation/d/1OLc0hNX_2EpfIkbeWaP_aH5dOAcA1YygXofJ0LPPxOE/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 0 — Introduction and environment setup</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/00-introduction.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
</tbody>
</table>

### Module 1 — Create

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
<td>Exercise 1.1 — Creating a collection with the Ansible extension for VS Code</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/11-vscode-collection.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 1.2 — Using the Ansible development environment tool (ade)</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/12-ade.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Exercise 1.3 — Adding a module to a collection</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/13-module.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
</tbody>
</table>

☕ **Break** — ⏱️ 15 minutes

### Module 2 — Test

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
<td>Exercise 2.1 — Testing a collection with Ansible Molecule</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/21-molecule.html">🚀 Launch Exercise</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>Exercise 2.2 — Functional testing with pytest-ansible</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/22-pytest-ansible.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Exercise 2.3 — Orchestrating tests with tox-ansible</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/23-tox-ansible.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
</tbody>
</table>

☕ **Break** — ⏱️ 15 minutes

### Module 3 — Deploy

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
<td>Exercise 3.1 — Creating an Execution Environment with ansible-builder</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/31-ansible-builder.html">🚀 Launch Exercise</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>Exercise 3.2 — Introducing supply chain security with ansible-sign</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/32-ansible-sign.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise — Workshop conclusion: What's next?</td>
<td><a target="_blank" href="https://rhpds.github.io/ansible-dev-tools-showroom/modules/99-conclusion.html">🚀 Launch Exercise</a></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Close Out &amp; Q&amp;A</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1OLc0hNX_2EpfIkbeWaP_aH5dOAcA1YygXofJ0LPPxOE/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 5 minutes</td>
</tr>
</tbody>
</table>

## Demos

Any of the individual labs (that make up the workshop) can be used as a standalone demo.

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)

## Documentation

- [How to contribute](https://github.com/ansible/workshops)
- [FAQ](https://github.com/ansible/workshops)

# Going Further

Additional material for Ansible Development Tools

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
Please open an [issues on Github](https://github.com/ansible/workshops/issues/new?title=New+dev-tools+extended+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
