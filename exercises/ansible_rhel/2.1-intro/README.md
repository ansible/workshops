# Workshop Exercise - Introduction to Ansible Tower

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table Contents

* [Objective](#objective)
* [Guide](#guide)
* [Why Ansible Tower?](#why-ansible-tower)
* [Your Ansible Tower Lab Environment](#your-ansible-tower-lab-environment)
* [Dashboard](#dashboard)
* [Concepts](#concepts)

# Objective

This exercise will provide an Ansible Tower overview including going through features that are provided by the Red Hat Ansible Automation Platform.  This will cover Ansible Tower fundamentals such as:

  - Job Templates
  - Projects
  - Inventories
  - Credentials
  - Workflows

# Guide

## Why Ansible Tower?

Ansible Tower is a web-based UI that provides an enterprise solution for IT automation. It

  - has a user-friendly dashboard

  - complements Ansible, adding automation, visual management, and monitoring capabilities.

  - provides user access control to administrators.

  - graphically manages or synchronizes inventories with a wide variety of sources.

  - has a RESTful API

  - And much more...

## Your Ansible Tower Lab Environment

In this lab you work in a pre-configured lab environment. You will have access to the following hosts:

| Role                         | Inventory name |
| -----------------------------| ---------------|
| Ansible Control Host & Tower | ansible        |
| Managed Host 1               | node1          |
| Managed Host 2               | node2          |
| Managed Host 2               | node3          |

The Ansible Tower provided in this lab is individually setup for you. Make sure to access the right machine whenever you work with it. Ansible Tower has already been installed and licensed for you, the web UI will be reachable over HTTP/HTTPS.

## Dashboard

Let's have a first look at the Tower: Point your browser to the URL you were given, similar to `https://student<X>.workshopname.rhdemo.io` (replace `<X>` with your student number and `workshopname` with the name of your current workshop) and log in as `admin`. The password will be provided by the instructor.

The web UI of Ansible Tower greets you with a dashboard with a graph showing:

  - recent job activity

  - the number of managed hosts

  - quick pointers to lists of hosts with problems.

The dashboard also displays real time data about the execution of tasks completed in playbooks.

![Ansible Tower Dashboard](images/dashboard.png)

## Concepts

Before we dive further into using Ansible Tower for your automation, you should get familiar with some concepts and naming conventions.

**Projects**

Projects are logical collections of Ansible playbooks in Ansible Tower. These playbooks either reside on the Ansible Tower instance, or in a source code version control system supported by Tower.

**Inventories**

An Inventory is a collection of hosts against which jobs may be launched, the same as an Ansible inventory file. Inventories are divided into groups and these groups contain the actual hosts. Groups may be populated manually, by entering host names into Tower, from one of Ansible Tower’s supported cloud providers or through dynamic inventory scripts.

**Credentials**

Credentials are utilized by Tower for authentication when launching Jobs against machines, synchronizing with inventory sources, and importing project content from a version control system. Credential configuration can be found in the Settings.

Tower credentials are imported and stored encrypted in Tower, and are not retrievable in plain text on the command line by any user. You can grant users and teams the ability to use these credentials, without actually exposing the credential to the user.

**Templates**

A job template is a definition and set of parameters for running an Ansible job. Job templates are useful to execute the same job many times. Job templates also encourage the reuse of Ansible playbook content and collaboration between teams. To execute a job, Tower requires that you first create a job template.

**Jobs**

A job is basically an instance of Tower launching an Ansible playbook against an inventory of hosts.

----
**Navigation**
<br>
[Previous Exercise](../1.7-role) - [Next Exercise](../2.2-cred)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
