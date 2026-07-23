# Getting Started with Ansible Development Tools in VS Code

> **IMPORTANT TO NOTE**
>
> This is the shorter version of this workshop (~2 hours). For the extended session please [🔬 click here](dev-tools-extended)
>

This hands-on workshop teaches you to create, test, and package Ansible content using the full suite of Ansible development tools inside Visual Studio Code. You'll scaffold a collection, write a custom module, lint and test your automation with Molecule and pytest-ansible, build an execution environment, and sign your content for supply-chain security.

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
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/index.html">rhpds.github.io/zt-ans-bu-dev-tools</a></td>
</tr>
<tr>
<td>Lab source repository</td>
<td><a target="_blank" href="https://github.com/rhpds/zt-ans-bu-dev-tools/tree/v0.0.2">github.com/rhpds/zt-ans-bu-dev-tools</a></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/index.html">Presenter instructions and guide</a></td>
</tr>
</tbody>
</table>

## Who is this workshop best for?

This workshop is intended for people who want to learn how to create, test, and distribute Ansible content using the latest development tools. Whether you're building your first collection or looking to adopt modern testing and packaging workflows, this workshop will walk you through the developer experience end-to-end. The intended audience is anyone who writes Ansible automation and wants to adopt best practices for content development.

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

This lab environment is available via the [Red Hat Demo Platform](https://catalog.demo.redhat.com/catalog) under the [Getting Started with Ansible Development Tools](https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-dev-tools.prod) catalog item.

## Lab Index (Estimate total time ⏱️ 2 hours)

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
<td>Exercise 1 — Workshop tips</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-01.html">🚀 Launch Exercise</a></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td>Exercise 2 — Creating a collection with the Ansible extension for VS Code</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-02-collection.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 3 — Using Ansible development environment</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-03-ade.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 4 — Adding a module to our collection</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-04-module.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 5 — Testing our collection with Molecule</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-05-molecule.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Exercise 6 — Functional testing with pytest-ansible</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-06-pytest.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 7 — Creating an Execution Environment with ansible-builder</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-08-builder.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Exercise 8 — Introducing supply chain security with ansible-sign</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-09-sign.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Exercise 9 — What's next?</td>
<td><a target="_blank" href="https://rhpds.github.io/zt-ans-bu-dev-tools/modules/module-10.html">🚀 Launch Exercise</a></td>
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
Please open an [issues on Github](https://github.com/ansible/workshops/issues/new?title=New+dev-tools+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
