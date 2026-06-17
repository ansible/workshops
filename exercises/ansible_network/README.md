# Ansible Network Automation Workshop

**Read this in other languages**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md), ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md), ![Français](https://github.com/ansible/workshops/raw/devel/images/fr.png) [Français](README.fr.md).

**This is documentation for Ansible Automation Platform 2**

The Ansible Network Automation workshop is a comprehensive beginners guide to automating popular network data center devices from Arista, Cisco and Juniper via Ansible playbooks. You'll learn how to pull facts from devices, build templated network configurations, and apply these concepts at scale with Ansible automation controller. You'll put it all together by exploring the controller's job templates, surveys, access controls and more.

> **NOTE:** This content has been updated to reflect the latest changes from the Ansible Automation Platform 2.0 release. [Learn more about how the 2.0 release impacts this workshop](https://docs.google.com/presentation/d/1VK8rF2jB6jqlcjgUzONBEGm8seqL6bfzFeyOwohICH4/edit?usp=sharing) or watch the [video walkthrough](https://www.youtube.com/watch?v=Oe1AbAvn9gg).

## Workshop Resources

| Resource | Link |
|---|---|
| Workshop content and exercises | [labs.demoredhat.com/exercises/ansible_network](https://labs.demoredhat.com/exercises/ansible_network/) |
| Follow-up handouts/assets | [Follow-up handouts/assets](https://redhat.dam.aprimo.com/Assets/Collections/~3bba623d9bf24b7bbc59acc9010b799d?state=5dcc589990f94524877315f4788b21d2) |
| Post-event survey | [Post-event survey](https://docs.google.com/document/d/1g4Q6IsV5--6H9ETARe-IL-FcUSmbO2Rv0TDXty1qwLk/edit) |
| Certain registration page & promotional email copy | [Registration page & promotional email copy](https://docs.google.com/document/d/1f2pLYP2bU_e0ksR3bhe-Yg4jXh8ymltsFoWE4tennsA/edit?usp=sharing) |
| Presenter instructions and guide | [Presenter instructions and guide](https://labs.demoredhat.com/exercises/ansible_network/) |
| Certain event banners | [Event banners (Google Drive)](https://drive.google.com/drive/folders/1QSGJltjVWGuLCt_CavddVMYSCKMzOTuj?usp=sharing) |

## Who is this workshop best for?

This workshop is intended as an introductory course for Ansible Network Automation. For more in-depth training please refer to [Red Hat Training Ansible for Network Automation](https://www.redhat.com/en/services/training/do457-ansible-network-automation). The intended audience is someone who has limited or no exposure to writing Ansible Playbooks or using Ansible Automation. This workshop will cover common network scenarios and topics and is best suited for network engineers or folks interested in network automation.

## Target audience

This workshop is geared toward network operators, network engineers, cloud administrators, DevOps engineers, security professionals and anyone interested in network automation.

## Attendee Prerequisites

* A basic understanding of working with Linux systems
* Attendees should have working knowledge of at least one Linux text editor (nano, pico, vi/vim, zile, emacs) with which to write Ansible playbooks
* Attendees must bring/use a laptop with ADMIN rights and the ability to SSH to a lab environment hosted in a public cloud
* Must bring/use a laptop with Chrome 73+, Firefox 60+, Edge 40+, or Safari 12+ installed
* Attendees should have working knowledge of using SSH and command line shell (BASH) as well as a conceptual understanding of linux system administration

There is no student prep work required prior to the workshop.

## Lab provisioner

[RHPDS](https://rhpds.redhat.com/) — Internal Red Hat Product Demo System. [AWS Lab Provisioner](https://github.com/ansible/workshops) — playbook that spins up instances on AWS for students to perform the provided exercises.

## Demos

See the [workshops repository](https://github.com/ansible/workshops) for demo content.

# Learning Resources

- [Red Hat Ansible Automation Platform - Training + Certification slides](https://docs.google.com/presentation/d/16pkh6Js89q7gR5VUILEQEU0mYRi6Ti98c9aRTcPOBVs/edit?usp=sharing)
- [How to contribute](https://github.com/ansible/workshops)
- [How to use the AWS Lab Provisioner](https://github.com/ansible/workshops)
- [FAQ](https://github.com/ansible/workshops)

## Presentation

Want the Presentation Deck?  Its right here:
- [Ansible Network Automation Workshop Deck](https://ansible.github.io/workshops/decks/ansible_network.pdf) PDF
- [Google Source](https://docs.google.com/presentation/d/1PIT-kGAGMVEEK8PsuZCoyzFC5CIzLBwdnftnUsdUNWQ/edit?usp=sharing) for Red Hat employees

## Ansible Network Automation Exercises

* [Exercise 1 - Exploring the lab environment](./1-explore/)
* [Exercise 2 - Execute your first network automation playbook](./2-first-playbook/)
* [Exercise 3 - Use Ansible facts on network devices](./3-facts/)
* [Exercise 4 - Ansible Network Resource Modules](./4-resource-module/)
* [Exercise 5 - Explore the Automation controller environment](./5-explore-controller/)
* [Exercise 6 - Create an Automation controller job template](./6-controller-job-template/)
* [Exercise 7 - Create an Automation controller Survey](./7-controller-survey/)
* [Exercise 8 - Using the Role Based Access Control (RBAC) feature](./8-controller-rbac/)
* [Exercise 9 - Create an Automation controller Workflow](./9-controller-workflow)

There are additional supplemental exercises that are [located here](supplemental/).

## Network Diagram

![Red Hat Ansible Automation](https://github.com/ansible/workshops/blob/devel/images/ansible_network_diagram.png?raw=true)

---
![Red Hat Ansible Automation](https://github.com/ansible/workshops/blob/devel/images/rh-ansible-automation-platform.png?raw=true)
