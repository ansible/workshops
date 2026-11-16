# Introduction to the Ansible Automation Orchestrator

In this 90-minute hands-on workshop, you take on the role of a Platform Engineer evaluating the Ansible Automation Orchestrator (AO) for modernizing your company's IT operations — moving from reactive, manual processes to intelligent, automated workflows that unify task-based, event-driven, and AI-driven automation in a single governed experience.

**Your assignment:** build, execute, and monitor a multi-step automation workflow on the AO visual canvas that combines Ansible Automation Platform (AAP) job templates, AI-powered task nodes, and human approval gates.

**The objective:** demonstrate that one AO workflow can detect a real-world event, generate an AI-driven remediation recommendation, post enrichment messages to a Mattermost channel using Model Context Protocol (MCP) tools, route through a conditional decision, receive human approval, and trigger the correct AAP job template — all within a governed, reproducible process.

By the end of the workshop you will be able to:

* Navigate the AO interface — Workflows, Executions, Approvals, and Configuration
* Create integrations and credentials that securely connect AO to Mattermost via MCP, an AI language model, and AAP
* Build a complete workflow on the visual canvas with triggers, AI task agents, approval gates, switch routing, and AAP job template nodes
* Execute a workflow end to end — triggering it by webhook, watching node-level execution in real time, and inspecting results
* Handle approval requests and troubleshoot workflow execution

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
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/index.html">rhpds.github.io/intro-ao-workshop</a></td>
</tr>
<tr>
<td>Follow-up assets</td>
<td><a target="_blank" href="http://red.ht/ansible_trial">Start your free trial (red.ht/ansible_trial)</a> · <a target="_blank" href="https://www.redhat.com/en/technologies/management/ansible">Learn more at redhat.com/ansible</a></td>
</tr>
<tr>
<td>Post-event survey</td>
<td>TBD — post-event survey</td>
</tr>
<tr>
<td>Registration page &amp; promotional email copy</td>
<td>TBD — registration page &amp; promotional email copy</td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td>TBD — permanent lab guide</td>
</tr>
</tbody>
</table>

## Target audience

IT Operations Engineers, DevOps practitioners, Platform Engineers, and Solutions Architects evaluating AO for governed, AI-assisted automation. Experience level: beginner to intermediate.

## Attendee Prerequisites

* Familiarity with Ansible Automation Platform core concepts: inventories, job templates, and credentials
* Conceptual understanding of Ansible Playbooks and roles
* Comfort reading YAML — you will not write any from scratch
* No AI or machine learning experience required
* A modern web browser; no local installation needed

## Presentation Deck

- [Google Slides](https://docs.google.com/presentation/d/1KM5ccHj8--u6PnLsKwkWVtzvRIBqSt7L1ppk0bplUgs/edit?usp=sharing) - For Red Hat employees (Introduction to the Ansible Automation Orchestrator)

## Lab provisioner

* Lab documentation: [https://rhpds.github.io/intro-ao-workshop/](https://rhpds.github.io/intro-ao-workshop/)
* Demo Platform (RHDP) [direct link](https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/published.intro-ao-workshop.prod&utm_source=webapp&utm_medium=share-link)

**List of Proctors:** TBD

If you are an SA, SSP, or TMM you will have no problem proctoring this lab. If you have any questions around proctoring this lab, reach out to the Ansible TMM team.

## Lab Index (Estimate total time ⏱️ 90 minutes)

This hands-on workshop builds one complete AO workflow end to end. Complete the modules in order — each one builds on the previous.

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
<td><a target="_blank" href="https://docs.google.com/presentation/d/1KM5ccHj8--u6PnLsKwkWVtzvRIBqSt7L1ppk0bplUgs/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Module 1 — Overview and interface tour</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/03-module-01-overview-interface.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 2 — Set up integrations and credentials</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/04-module-02-integrations-credentials.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 3 — Build the workflow</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/05-module-03-build-workflow.html">🚀 Launch Exercise</a></td>
<td>⏱️ 30 minutes</td>
</tr>
<tr>
<td>Module 4 — Run and monitor</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/06-module-04-run-monitor.html">🚀 Launch Exercise</a></td>
<td>⏱️ 10 minutes</td>
</tr>
<tr>
<td>Module 5 — Review and best practices</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/99-conclusion.html">🚀 Launch Exercise</a></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Summary &amp; Call to Actions</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1KM5ccHj8--u6PnLsKwkWVtzvRIBqSt7L1ppk0bplUgs/edit?usp=sharing">🖥️ Summary</a></td>
<td>⏱️ 10 minutes</td>
</tr>
</tbody>
</table>

# Learning Resources

- [Workshop exercises (GitHub)](https://github.com/rhpds/intro-ao-workshop)
- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)
- YouTube playlist — [AI+Ansible](https://www.youtube.com/playlist?list=PLdu06OJoEf2Y9-d7vPaKSh6ED_rO6AQFF)
- [What is AIOps?](https://www.redhat.com/en/topics/automation/what-is-aiops)

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an [issues on Github](https://github.com/ansible/workshops/issues/new?title=New+intro+ao+lab+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
