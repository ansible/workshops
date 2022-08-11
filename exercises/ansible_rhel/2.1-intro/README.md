# Workshop Exercise - Introduction to Ansible automation controller

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table Contents

* [What's New in Ansible automation controller 4.0](#whats-new-in-ansible-automation-controller-40)
* [Why was Ansible Tower renamed to automation controller?](#why-was-ansible-tower-renamed-to-automation-controller)
* [Who is automation controller for?](#who-is-automation-controller-for)
* [Objective](#objective)
* [Guide](#guide)
* [Why Ansible automation controller?](#why-ansible-automation-controller)
* [Your Ansible automation controller lab environment](#your-ansible-automation-controller-lab-environment)
* [Dashboard](#dashboard)
* [Concepts](#concepts)

## What's New in Ansible automation controller 4.0

Ansible Automation Platform 2 is the next evolution in automation from Red Hat’s trusted enterprise technology experts. The Ansible Automation Platform 2 release includes automation controller 4.0, the improved and renamed Ansible Tower.

Controller continues to provide a standardized way to define, operate, and delegate automation across the enterprise. It introduces new technologies and an enhanced architecture that enables automation teams to scale and deliver automation rapidly.

### Why was Ansible Tower renamed to automation controller?

As Ansible Automation Platform 2 continues to evolve, certain functionality has been decoupled (and will continue to be decoupled in future releases) from what was formerly known as Ansible Tower. It made sense to introduce the naming change that better reflects these enhancements and the overall position within the Ansible Automation Platform suite.

### Who is automation controller for?
All automation team members interact with or rely on automation controller, either directly or indirectly.

* Automation creators develop Ansible playbooks, roles, and modules.
* Automation architects elevate automation across teams to align with IT processes and streamline adoption.
* Automation operators ensure the automation platform and framework are operational.

These roles are not necessarily dedicated to a person or team. Many organizations assign multiple roles to people or outsource specific automation tasks based on their needs.

Automation operators are typically the primary individuals who interact directly with the automation controller, based on their responsibilities.

{% include mesh.md %}

## Objective

The following exercise will provide an Ansible automation controller overview including going through features that are provided by the Red Hat Ansible Automation Platform.  This will cover automation controller fundamentals such as:

* Job Templates
* Projects
* Inventories
* Credentials
* Workflows

## Guide

### Why Ansible automation controller?

Automation controller is a web-based UI that provides an enterprise solution for IT automation. It

* has a user-friendly dashboard.
* complements Ansible, adding automation, visual management, and monitoring capabilities.
* provides user access control to administrators.
* provides distinct _view_ and _edit_ perspectives for automation controller objects and components.
* graphically manages or synchronizes inventories with a wide variety of sources.
* has a RESTful API.
* And much more...

### Your Ansible automation controller lab environment

In this lab you work in a pre-configured lab environment. You will have access to the following hosts:

| Role                                          | Inventory name |
| --------------------------------------------- | ---------------|
| Ansible control host & automation controller  | ansible-1      |
| Managed Host 1                                | node1          |
| Managed Host 2                                | node2          |
| Managed Host 2                                | node3          |

The Ansible automation controller provided in this lab is individually setup for you. Make sure to access the right machine whenever you work with it. Automation controller has already been installed and licensed for you, the web UI will be reachable over HTTP/HTTPS.

### Dashboard

Let's have a first look at the automation controller: Point your browser to the URL you were given, similar to `https://student<X>.<workshopname>.demoredhat.com` (replace `<X>` with your student number and `workshopname` with the name of your current workshop) and log in as `admin`. The password will be provided by the instructor.

The web UI of automation controller greets you with a dashboard with a graph showing:

* recent job activity
* the number of managed hosts
* quick pointers to lists of hosts with problems.

The dashboard also displays real time data about the execution of tasks completed in playbooks.

![Ansible automation controller dashboard](images/controller_dashboard.jpg)

### Concepts

Before we dive further into using Ansible automation controller, you should get familiar with some concepts and naming conventions.

#### Projects

Projects are logical collections of Ansible playbooks in Ansible automation controller. These playbooks either reside on the Ansible automation controller instance, or in a source code version control system supported by automation controller.

#### Inventories

An Inventory is a collection of hosts against which jobs may be launched, the same as an Ansible inventory file. Inventories are divided into groups and these groups contain the actual hosts. Groups may be populated manually, by entering host names into automation controller, from one of Ansible Automation controller’s supported cloud providers or through dynamic inventory scripts.

#### Credentials

Credentials are utilized by automation controller for authentication when launching Jobs against machines, synchronizing with inventory sources, and importing project content from a version control system. Credential configuration can be found in the Settings.

automation controller credentials are imported and stored encrypted in automation controller, and are not retrievable in plain text on the command line by any user. You can grant users and teams the ability to use these credentials, without actually exposing the credential to the user.

#### Templates

A job template is a definition and set of parameters for running an Ansible job. Job templates are useful to execute the same job many times. Job templates also encourage the reuse of Ansible playbook content and collaboration between teams. To execute a job, automation Controller requires that you first create a job template.

#### Jobs

A job is basically an instance of automation controller launching an Ansible playbook against an inventory of hosts.

---
**Navigation**
<br>
[Previous Exercise](../1.7-role) - [Next Exercise](../2.2-cred)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
