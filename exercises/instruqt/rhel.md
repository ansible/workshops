# Ansible for Red Hat Enterprise Linux Technical Workshop

> **IMPORTANT TO NOTE** 
> 
> This is the extended version of this workshop (~6 hours).  For the shorter 90 minute session please [🔬 click here](rhel-90.md)
>

If you're new to Ansible Automation, this workshop consists of two parts: 1) starting with the basic fundamentals and 2) applying what you've learned to implement Ansible automation controller to your enterprise use cases. You'll start off by writing your first Ansible playbook, work on Jinja templates, and implement higher-level Ansible roles. Next you'll get started on automation controller, understand inventory and credential management, projects, job templates, surveys, workflows and more.

After finishing this lab you are ready to start using Ansible for your automation requirements.

**This is documentation for Ansible Automation Platform 2.6**

## Presentation Deck

- [PDF](../../decks/ansible_rhel.pdf) - For everyone
- [Google Slides](https://docs.google.com/presentation/d/1V2IbX4hux4__6nZZMZZp3HMUFgYrt0ZH9LL6r30CBhs/edit?usp=sharing) - For Red Hat employees

## Lab Agenda (Estimate total time ⏱️ 6 hours)

Recommended agenda for when there is an instructor teaching.

<table>
<thead>
<tr>
<th>Agenda Item</th>
<th>Description</th>
<th>Link</th>
<th>Estimated Time</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>Slides</b></td>
<td>Introduction + Workshop Brief</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1V2IbX4hux4__6nZZMZZp3HMUFgYrt0ZH9LL6r30CBhs/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td><b>Lab</b>: Section 1 — Command-line Ansible (Exercises 1.1–1.4)</td>
<td>Writing playbooks, variables, conditionals/handlers/loops, and templates</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-rhel.prod&utm_source=webapp&utm_medium=share-link">🚀 Launch Lab</a></td>
<td>⏱️ 80 minutes</td>
</tr>
<tr>
<td>☕ <b>Break</b></td>
<td>Suggested break</td>
<td></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td><b>Lab</b>: Section 1 — Command-line Ansible (Exercises 1.5–1.7)</td>
<td>Collections, Ansible Navigator & execution environments, debugging</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-rhel.prod&utm_source=webapp&utm_medium=share-link">🚀 Launch Lab</a></td>
<td>⏱️ 55 minutes</td>
</tr>
<tr>
<td>☕ <b>Break</b></td>
<td>Suggested break</td>
<td></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td><b>Lab</b>: Section 2 — Ansible Automation Platform (Exercises 2.1–2.4)</td>
<td>Automation controller: inventories, credentials, projects, job templates, and surveys</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-rhel.prod&utm_source=webapp&utm_medium=share-link">🚀 Launch Lab</a></td>
<td>⏱️ 70 minutes</td>
</tr>
<tr>
<td>☕ <b>Break</b></td>
<td>Suggested break</td>
<td></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td><b>Lab</b>: Section 2 — Ansible Automation Platform (Exercises 2.5–2.8)</td>
<td>RBAC, workflows, system roles, and wrap-up</td>
<td><a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/zt-ansiblebu.zt-ans-bu-rhel.prod&utm_source=webapp&utm_medium=share-link">🚀 Launch Lab</a></td>
<td>⏱️ 75 minutes</td>
</tr>
<tr>
<td><b>Slides</b></td>
<td>Close Out & Q&A</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1V2IbX4hux4__6nZZMZZp3HMUFgYrt0ZH9LL6r30CBhs/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 10 minutes</td>
</tr>
</tbody>
</table>

## Exercise Index

### Section 1 — Command-line Ansible

<table>
<thead>
<tr>
<th>Exercise</th>
<th>Description</th>
<th>Estimated Time</th>
</tr>
</thead>
<tbody>
<tr>
<td>1.1 Writing Your First Playbook</td>
<td>Create and run your first Ansible playbook</td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td>1.2 Using Variables</td>
<td>Learn how to use variables in playbooks</td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>1.3 Conditionals, Handlers and Loops</td>
<td>Implement conditionals, handlers, and loops</td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>1.4 Templates</td>
<td>Use Jinja2 templates to create dynamic configurations</td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>1.5 Collections</td>
<td>Explore and use Ansible collections</td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>1.6 Ansible Navigator & Execution Environments</td>
<td>Introduction to Ansible Navigator and execution environments</td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>1.7 Debugging and Error Handling</td>
<td>Debug playbooks and handle errors effectively</td>
<td>⏱️ 20 minutes</td>
</tr>
</tbody>
</table>

### Section 2 — Ansible Automation Platform

<table>
<thead>
<tr>
<th>Exercise</th>
<th>Description</th>
<th>Estimated Time</th>
</tr>
</thead>
<tbody>
<tr>
<td>2.1 Introduction to Automation Platform</td>
<td>Get familiar with the Ansible Automation Controller web UI</td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>2.2 Inventories and Credentials</td>
<td>Manage inventories and credentials in automation controller</td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>2.3 Projects & Job Templates</td>
<td>Create projects and job templates to run automation</td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>2.4 Surveys</td>
<td>Add surveys to job templates for user-driven input</td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>2.5 Role-based Access Control</td>
<td>Configure RBAC to manage user access and permissions</td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>2.6 Workflows</td>
<td>Build multi-step automation workflows</td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>2.7 System Roles</td>
<td>Use RHEL System Roles for firewall and timesync configuration</td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>2.8 Wrap Up</td>
<td>Capstone exercise combining inventory, templates, surveys, and RBAC</td>
<td>⏱️ 25 minutes</td>
</tr>
</tbody>
</table>

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
Please open an [issues on Github](https://github.com/ansible/instruqt/issues/new?title=New+rhel+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
