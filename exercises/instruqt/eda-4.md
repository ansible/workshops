# Event-Driven Ansible & ServiceNow Technical Workshop

> **IMPORTANT TO NOTE** 
> 
> This is the 4 hour version of this workshop.  For the shorter 90 minute session please [🔬 click here](eda)
>

As a part of Red Hat® Ansible® Automation Platform, Event-Driven Ansible can process events containing discrete intelligence about conditions in the IT environment, determine the appropriate response to the event, then execute automated actions to address or remediate the event. This workshop will demonstrate Event-Driven Ansible and how it provides the event-handling capability needed to automate time-consuming tasks and respond to changing conditions in any IT domain.

During this workshop, we will walk through the basics of EDA (Event-Driven Ansible) covering fundamentals such as sources, rules, and actions and the corresponding technology and implementation through Ansible Rulebook CLI, rulebooks, source plugins, and EDA content collections. This workshop requires students to have beginner-level knowledge of command-line Ansible, Visual Studio Code, and Git.

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
<td><a target="_blank" href="https://labs.demoredhat.com/webpages/eda-4">labs.demoredhat.com/webpages/eda-4</a></td>
</tr>
<tr>
<td>Follow-up assets</td>
<td><a target="_blank" href="https://docs.google.com/spreadsheets/d/1wW8r4xcbwKQ2K1H5E1l3XlQZ_A317i8EJdEyrKMoCqI/edit?usp=sharing">Follow-up assets spreadsheet</a></td>
</tr>
<tr>
<td>Post-event survey</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1OL6G5B3_zjmW2NP5erqhj30nFdeBvldx1hpWIlpT--Y/edit?usp=sharing">Post-event survey</a></td>
</tr>
<tr>
<td>Certain registration page &amp; promotional email copy</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1zJnh_NN4EQo_XHZ2CQhlk0beGDMvUKxre6KGo9-XNzs/edit?usp=sharing">Registration page &amp; promotional email copy</a></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><a target="_blank" href="https://labs.demoredhat.com/webpages/eda-4">Presenter instructions and guide</a></td>
</tr>
<tr>
<td>Certain event banners</td>
<td><a target="_blank" href="https://drive.google.com/drive/folders/1th8ZXbHfebvaeqQWpCyLOUd9qZmBWg6G?usp=sharing">Event banners (Google Drive)</a></td>
</tr>
</tbody>
</table>

## Who is this workshop best for?

This workshop is intended as an introductory course for using Red Hat Ansible Automation Platform in conjunction with an IT Service Management (ITSM) tool, specifically showcasing ServiceNow, as well as Event-Driven Ansible fundamentals and advanced use cases.

## Target audience

Automation engineers, DevOps engineers, and operations teams looking to automate ServiceNow workflows and adopt Event-Driven Ansible.

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* A basic understanding of [Visual Studio Code](https://code.visualstudio.com/). [Available for MacOS, Windows and Linux]
* Experience with building Ansible Playbooks and working with Ansible Automation Platform
* Basic understanding of Git and source control
* Attendees must bring/use a laptop with ADMIN rights and the ability to SSH to a lab environment hosted in a public cloud
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed

If the student has no Ansible experience, it is recommended, as a prerequisite, to try the free on-demand lab [Introduction to automation controller](https://play.instruqt.com/embed/redhat/tracks/controller-101?token=em_mUfT4xw1TXybXnBr&show_challenges=true). Students would greatly benefit from watching the free training course [Ansible Basics: Automation Technical Overview](https://www.redhat.com/en/services/training/do007-ansible-essentials-simplicity-automation-technical-overview).

## Presentation Deck

- [PDF](decks/lab-eda-gitops.pdf) - For everyone
- [Google Slides (EDA)](https://docs.google.com/presentation/d/1wrJ90OEvkais6wcyinMq42uv1_VJJQlzrxHy8UgC220/edit?usp=sharing) - For Red Hat employees
- [Google Slides (ServiceNow)](https://docs.google.com/presentation/d/1sE8nZJjQw74QyWccufUVNwEtIepxPYTbsn5YfjN3oU8/edit?usp=sharing) - For Red Hat employees

## Lab provisioner

This workshop uses the [Instruqt](https://play.instruqt.com/redhat) platform to load the labs inside your browser. If you have a large number of users and want to increase the amount of hot-standbys please email: ansible-tmm@redhat.com.

## Lab Index (Estimate total time ⏱️ 4 hours)

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
<td><a target="_blank" href="https://docs.google.com/presentation/d/1wrJ90OEvkais6wcyinMq42uv1_VJJQlzrxHy8UgC220/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 15 minutes</td>
</tr>
<tr>
<td>Lab 1: Getting Started with Event-Driven Ansible</td>
<td><a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/eda--ansible-rulebook?token=em_kn8hibVNgt0X03wZ">🚀 Launch Lab</a></td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Lab Brief for Lab 2</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1wrJ90OEvkais6wcyinMq42uv1_VJJQlzrxHy8UgC220/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td>Lab 2: Getting Started with EDA Controller</td>
<td><a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/getting-started-eda-controller?token=em_pnJ8mV75JMc0MhZN">🚀 Launch Lab</a></td>
<td>⏱️ 35 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Lab Brief for Lab 3</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1wrJ90OEvkais6wcyinMq42uv1_VJJQlzrxHy8UgC220/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td>Lab 3: Advanced EDA — GitOps with Event-Driven Ansible</td>
<td><a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/eda-gitops?token=em__C74PAmX2rePq7Kk">🚀 Launch Lab</a></td>
<td>⏱️ 35 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Lab Brief for Lab 4</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1wrJ90OEvkais6wcyinMq42uv1_VJJQlzrxHy8UgC220/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 5 minutes</td>
</tr>
<tr>
<td>Lab 4: Advanced EDA — Event-Driven Ansible and NetOps</td>
<td><a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/event-driven-netops?token=em_W0qtY5GifN13CZ1a">🚀 Launch Lab</a></td>
<td>⏱️ 30 minutes</td>
</tr>
<tr>
<td><b>Slides</b>: Introduction to ServiceNow and Lab Brief</td>
<td><a target="_blank" href="https://docs.google.com/presentation/d/1sE8nZJjQw74QyWccufUVNwEtIepxPYTbsn5YfjN3oU8/edit?usp=sharing">🖥️ Google Slides</a></td>
<td>⏱️ 25 minutes</td>
</tr>
<tr>
<td>Lab 5: Get started with ServiceNow automation</td>
<td><a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/getting-started-servicenow-automation?token=em_5ktpLJWtzpbqcDyM">🚀 Launch Lab</a></td>
<td>⏱️ 60 minutes</td>
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
<th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td>Event-driven Ansible with OpenShift Demo</td>
<td>Use Red Hat OpenShift events as a trigger showcasing the adaptability and effectiveness of Event-Driven Ansible</td>
<td><a target="_blank" href="https://demo.redhat.com/catalog/babylon-catalog-prod/order/enterprise.event-driven-ansible.prod">🚀 Launch Lab</a></td>
<td>⏱️ 40 minutes</td>
<td><table class="important"><tr><td><div class="infobutton"><i class="icon-info-sign"></i></div>Important</td></tr><tr><td>This runs on demo.redhat.com and is only available to Red Hat employees</td></tr></table></td>
</tr>
</tbody>
</table>

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
<td>Automate IT response with Event-Driven Ansible</td>
<td>E-Book</td>
<td><a target="_blank" href="https://www.redhat.com/en/engage/build-innovation-automation-20230414">📖 Download E-Book</a></td>
</tr>
<tr>
<td>The impact of event-driven automation on IT operations</td>
<td>Analyst material</td>
<td><a target="_blank" href="https://www.redhat.com/en/resources/event-driven-impact-on-it-operations-analyst-material">📒 Download Analyst Material</a></td>
</tr>
<tr>
<td>Work smarter using event-driven automation across IT operations</td>
<td>Webinar</td>
<td><a target="_blank" href="https://www.redhat.com/en/events/webinar/work-smarter-using-event-driven-automation-across-IT-operations">🎥 Watch recording from June 20, 2023</a></td>
</tr>
</tbody>
</table>

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an [issues on Github](https://github.com/ansible/instruqt/issues/new?title=New+eda+4hour+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
