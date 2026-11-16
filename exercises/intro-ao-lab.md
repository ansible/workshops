# Introduction to Automation Orchestrator

Automation orchestrator is an add-on to Red Hat Ansible Automation Platform: a composable canvas for designing, deploying, and governing complex IT operations workflows. In this 90-minute hands-on lab you build workflows on that canvas from an empty page and watch them run against real systems.

A workflow is a sequence of connected steps. A trigger starts it, steps do the work, and logic steps decide which step comes next. The trigger is part of the workflow itself: manual, webhook, and Event-Driven Ansible triggers are steps you place on the canvas, so the automation and the thing that starts it stay a single artifact. Switch steps route on values produced earlier in the run, which lets one workflow carry several possible paths. AI-powered task agent steps handle the input you could not predict, such as an incident ticket, a log excerpt, or an alert description that no rule written in advance would cover: the agent reads it, classifies it, and recommends what to run.

Every Ansible job template you have already created becomes a reusable workflow step immediately, without modification. AI recommends the action while AAP remains your trusted execution layer, and approval steps let you decide when a person should review an action before it runs.

Across six modules you connect automation orchestrator to the tools you already use and build four complete workflows:

* Your own integrations and credentials, connecting automation orchestrator to AAP and to an AI model
* A **message of the day** workflow on an empty canvas: a trigger, a task agent, and an AAP job template that writes the agent's wording into the login banner on a real RHEL host
* A **disk utilization** workflow that branches on how full a filesystem is and hands the fix to AAP
* A **ticket enrichment** workflow where a task agent reads a live OpenFlake incident and routes it to auto-remediation, an approval gate, or back to a human
* A **CVE auto-remediation** workflow that patches development hosts automatically while requiring approval before production, routing on findings from Red Hat Lightspeed

Every module ends in a live run you can watch step by step. If one of your workflows does not work, a solutions project in automation orchestrator holds a complete, published copy of every workflow in the lab to compare against.

**Red Hat products included:** Ansible Automation Platform, OpenShift Container Platform, Red Hat Enterprise Linux, and Red Hat Lightspeed. Supporting applications in the environment: OpenFlake (the ITSM system holding the incident tickets), Gitea (the Git service the CVE remediation playbook is committed to), and Mattermost (where your workflows post notifications).

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
<td>TBD: post-event survey</td>
</tr>
<tr>
<td>Registration page &amp; promotional email copy</td>
<td>TBD: registration page &amp; promotional email copy</td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td>TBD: permanent lab guide</td>
</tr>
</tbody>
</table>

## Target audience

You will get the most out of this lab if you are:

* An automation engineer or platform team member interested in using automation orchestrator alongside your existing Ansible Automation Platform environment
* Working with alerts, tickets, or logs that require someone to interpret the information before deciding which automation to run
* Curious about how AI-powered task agents can recommend actions while keeping humans in the loop when approvals are needed
* Evaluating automation orchestrator and would rather build and run real workflows than watch a demo

## Attendee Prerequisites

* Familiarity with the basics of Ansible Playbooks and AAP job templates
* No prior automation orchestrator experience required
* No playbook writing required, you will not write a single one to complete the modules
* Everything runs in the browser, there is nothing to install

## Presentation Deck

- <a target="_blank" href="https://docs.google.com/presentation/d/1KM5ccHj8--u6PnLsKwkWVtzvRIBqSt7L1ppk0bplUgs/edit?usp=sharing">Google Slides</a> - For Red Hat employees (Introduction to Automation Orchestrator)

## Lab provisioner

* Lab documentation: <a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/">https://rhpds.github.io/intro-ao-workshop/</a>
* Demo Platform (RHDP) <a target="_blank" href="https://catalog.demo.redhat.com/catalog/babylon-catalog-prod?item=babylon-catalog-prod/published.intro-ao-workshop.prod&utm_source=webapp&utm_medium=share-link">direct link</a>

**List of Proctors:** TBD

If you are an SA, SSP, or TMM you will have no problem proctoring this lab. If you have any questions around proctoring this lab, reach out to the Ansible TMM team.

## Lab Index (Estimate total time ⏱️ 90 minutes)

Complete the modules in order. Each one builds on the integrations and concepts from the last. Add roughly 15 minutes if you are presenting the introduction and summary slides alongside the lab.

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
<td>Module 1: Lab overview</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/index.html">🚀 Launch Exercise</a></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td>Module 2: Getting started, integrations and credentials</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/module-02-integrations-and-credentials.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Module 3: Your first workflow, message of the day</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/module-03-your-first-workflow-motd.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Module 4: Disk utilization remediation</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/module-04-disk-utilization.html">🚀 Launch Exercise</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Module 5: Ticket enrichment workflow</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/module-05-ticket-enrichment.html">🚀 Launch Exercise</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td>Module 6: CVE auto-remediation workflow</td>
<td><a target="_blank" href="https://rhpds.github.io/intro-ao-workshop/modules/module-06-cve-remediation.html">🚀 Launch Exercise</a></td>
<td>⏱️ 20 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Introduction &amp; Summary (optional)</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1KM5ccHj8--u6PnLsKwkWVtzvRIBqSt7L1ppk0bplUgs/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 15 minutes</td>
</tr>
</tbody>
</table>

# Learning Resources

- <a target="_blank" href="https://github.com/rhpds/intro-ao-workshop">Workshop exercises (GitHub)</a>
- <a target="_blank" href="https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing">Red Hat Ansible Automation Platform - Training + Certification slides</a>
- YouTube playlist: <a target="_blank" href="https://www.youtube.com/playlist?list=PLdu06OJoEf2Y9-d7vPaKSh6ED_rO6AQFF">AI+Ansible</a>
- <a target="_blank" href="https://www.redhat.com/en/topics/automation/what-is-aiops">What is AIOps?</a>

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an <a target="_blank" href="https://github.com/ansible/workshops/issues/new?title=New+intro+ao+lab+workshop+issue&body=">issues on Github</a>


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
