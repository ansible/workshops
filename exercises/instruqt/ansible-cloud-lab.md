# Introduction to cloud automation

This self-paced lab will demonstrate how Ansible Automation Platform can help you orchestrate, operationalize and govern your hybrid cloud environments. Use-cases will include infrastructure visibility, compliance and infrastructure optimization. Learn how Ansible can start helping you tame your hybrid cloud deployments today. This self-paced lab requires students to have beginner level knowledge of common public cloud terminology and limited to no knowledge of Ansible.

> **NOTE** 
> 
> You will have the option to use **Microsoft Azure** or **Amazon Web Services (AWS)** for each exercise.

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
<td><a target="_blank" href="https://labs.demoredhat.com/webpages/ansible-cloud-lab">labs.demoredhat.com/webpages/ansible-cloud-lab</a></td>
</tr>
<tr>
<td>Certain registration page &amp; promotional email copy</td>
<td><a target="_blank" href="https://docs.google.com/document/d/1kX_pI-Ono1_ob9R3zXQ-HSI-kqTJErYMBaKzXCyVosw/edit?usp=sharing">Registration page &amp; promotional email copy</a></td>
</tr>
<tr>
<td>Presenter instructions and guide</td>
<td><a target="_blank" href="https://labs.demoredhat.com/webpages/ansible-cloud-lab">Presenter instructions and guide</a></td>
</tr>
<tr>
<td>Certain event banners</td>
<td><a target="_blank" href="https://drive.google.com/drive/folders/17P9yNwk74yzkH_59Fpv0fRRMLezwm8xO?usp=sharing">Event banners (Google Drive)</a></td>
</tr>
</tbody>
</table>

## Who is this workshop best for?

This workshop is intended for people who want to learn the basics of cloud automation. This workshop will demonstrate how Ansible Automation Platform can help you orchestrate, operationalize and govern your hybrid cloud environments. This workshop is a first step before the [Red Hat Ansible Automation Platform on AWS workshop](https://source.redhat.com/departments/marketing/globalcampaignsteamgtc/automation/automation_wiki/it_automation_technical_workshop__red_hat_ansible_automation_platform_on_aws).

## Target audience

Cloud Operators, SREs, System Administrators.

If you need help with understanding cloud personas please refer to the [How to have a hybrid cloud automation discussion](https://docs.google.com/presentation/d/1HhvqXkHwqYRwNhaznUhAZ-4J4f7TJ4PMD-M43vIEW2U/edit?usp=sharing) presentation.

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed

There is no student prep work required prior to the workshop.

## Presentation Deck

- [Google Slides](https://docs.google.com/presentation/d/1LNzCv16dZ9nNDrfEY-wOMd1jYAZMZlIcla_fUJLsq0U/edit?usp=sharing) - For Red Hat employees
- [PDF](decks/lab-introduction-to-cloud-automation.pdf) - For everyone

Optional module **Terraforming Clouds with Ansible** deck:
- [Google Slides](https://docs.google.com/presentation/d/1LNzCv16dZ9nNDrfEY-wOMd1jYAZMZlIcla_fUJLsq0U/edit?usp=sharing) - For Red Hat employees
- [PDF](decks/lab-terraforming-clouds-with-ansible.pdf) - For everyone

## Lab Agenda (Estimate total time ⏱️ 90 minutes)

<ul>
<li><b>Slides: Introduction + Workshop Brief (slides 1–16)</b> [Estimated Time ⏱️ 15 minutes]<br>
<a target="_blank" href="https://docs.google.com/presentation/d/1LNzCv16dZ9nNDrfEY-wOMd1jYAZMZlIcla_fUJLsq0U/edit?usp=sharing">[ 🖥️ Slides ]</a>
</li><br>
<li><b>Lab: Infrastructure visibility</b> [Estimated Time ⏱️ 20 minutes]<br>
In this lab we will illustrate how we can retrieve Ansible facts (key, value pairs), also known as structured data, from public clouds and how we can use this data to provide us awareness of our cloud footprint easily.<br>
<a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/cloud-visibility?token=em_IYvE6P3BoPg-Fo50">[ 🚀 Start Exercise on AWS ]</a> |
<a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/ansible-for-azure-infrastructure-visibility?token=em_b_TKcpWZfvC6Jbwe">[ 🚀 Start Exercise on Azure ]</a>
</li><br>
<li><b>Slides: Lab Brief (slides 17–23)</b> [Estimated Time ⏱️ 6 minutes]<br>
<a target="_blank" href="https://docs.google.com/presentation/d/1LNzCv16dZ9nNDrfEY-wOMd1jYAZMZlIcla_fUJLsq0U/edit?usp=sharing">[ 🖥️ Slides ]</a>
</li><br>
<li><b>Lab: Cloud Operations</b> [Estimated Time ⏱️ 20 minutes]<br>
This lab will illustrate how Ansible Automation Platform can help you automate common day-2 cloud operations tasks across your public cloud. Our focus here will be on AWS, but the use cases here are ones you can extend across the hybrid cloud.<br>
<a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/cloud-operations?token=em_785MP3rpLI7oAW1Y">[ 🚀 Start Exercise on AWS ]</a> |
<a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/ansible-for-azure-cloud-operations?token=em_Iea3nZSewDSNZBW7">[ 🚀 Start Exercise on Azure ]</a>
</li><br>
<li><b>Slides: Lab Brief (slides 24–31)</b> [Estimated Time ⏱️ 6 minutes]<br>
<a target="_blank" href="https://docs.google.com/presentation/d/1LNzCv16dZ9nNDrfEY-wOMd1jYAZMZlIcla_fUJLsq0U/edit?usp=sharing">[ 🖥️ Slides ]</a>
</li><br>
<li><b>Lab: Infrastructure optimization</b> [Estimated Time ⏱️ 20 minutes]<br>
In this lab we will guide you in understanding some basic optimization exercises that can help you tame your public clouds.<br>
<a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/cloud-optimization?token=em_0h2ed0VTvBXyHNA6">[ 🚀 Start Exercise on AWS ]</a> |
<a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/ansible-for-azure-infrastructure-optimization?token=em_habXtbTR9H2f9QWd">[ 🚀 Start Exercise on Azure ]</a>
</li><br>
<li><b>Slides: Close Out (slides 32–34)</b> [Estimated Time ⏱️ 3 minutes]<br>
<a target="_blank" href="https://docs.google.com/presentation/d/1LNzCv16dZ9nNDrfEY-wOMd1jYAZMZlIcla_fUJLsq0U/edit?usp=sharing">[ 🖥️ Slides ]</a>
</li>
</ul>

## Optional Lab

<ul>
<li><b>Terraforming Clouds with Ansible</b> [Estimated Time ⏱️ 60 minutes]<br>
In this lab we explore the basics of Terraform and how we can use it to deploy infrastructure. We then take it up a level by introducing Ansible's Automation controller and simplify the creation of this infrastructure as well as bring the all important post-provisioning tasks which we all need to do when infrastructure is being configured.<br>
<a target="_blank" href="https://play.instruqt.com/embed/redhat/tracks/terraform-ansible?token=em_9xhy_e8tyoPKFdab">[ 🚀 Start Exercise ]</a>
</li>
</ul>

## Lab Diagram AWS

<img src="https://github.com/IPvSean/pictures_for_github/blob/master/aws-diagram.png?raw=true" width="600px">

## Lab Diagram Azure

<img src="https://ipvsean.github.io/instruqt/webpages/img/azure_diagram.png" width="600px">

## Lab provisioner

There is no RHPDS lab provisioner associated with this workshop. This simply uses the Instruqt platform to load the labs inside your browser. If you have a large number of users and want to increase the amount of hot-standbys please email: ansible-tmm@redhat.com. There will be a cost charged back to the event.

## Demos

Any of the individual labs (that make up the workshop) can be used as a standalone demo.

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)
- [Hybrid Cloud Automation slides](https://ansible.github.io/slides/#hybrid-cloud-automation)

## Documentation

- [https://labs.demoredhat.com/webpages/ansible-cloud-lab](https://labs.demoredhat.com/webpages/ansible-cloud-lab)
- [https://github.com/ansible/instruqt](https://github.com/ansible/instruqt)

# Free e-books

- [Automate your hybrid cloud at scale](https://www.redhat.com/en/engage/automate-hybrid-cloud-20221006)
- [Connect your hybrid cloud environment with IT automation](https://www.redhat.com/en/engage/hybrid-cloud-environment-20220412)
- [Using automation to get the most from your public cloud](https://www.redhat.com/en/engage/automation-public-cloud-20221014)

# Ansible Workshop

This is an official Ansible Workshop

This workshop is maintained by the Red Hat Ansible Technical Marketing Team.  
Please open an [issues on Github](https://github.com/ansible/instruqt/issues/new?title=New+cloud+workshop+issue&body=)


![ansible workshop logo](https://github.com/ansible/workshops/blob/devel/images/Ansible-Workshop-Logo.png?raw=true)
