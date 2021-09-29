# Exercise 4 - How to use Collections on Red Hat Ansible Tower

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
    - [Step 1 - Write a requirements.yml](#step-1---write-a-requirementsyml)
    - [Step 2 - Create Job Template](#step-2---create-job-template)
- [Troubleshooting](#troubleshooting)

# Objective

Red Hat Ansible Tower supports Ansible Collections starting with version 3.5 - earlier version will not automatically install and configure them for you. To make sure Ansible Collections are recognized by Red Hat Ansible Tower a requirements file is needed and has to be stored in the proper directory.

Ansible Galaxy is already configured by default, however if you want your Red Hat Ansible Tower to prefer and fetch content from the Red Hat Automation Hub, additional configuration changes are required. They are addressed in a the chapter [Use Automation Hub](../7-use-automation-hub/) in this lab.

# Guide

In this exercise you will learn how to define an Ansible Collection as a requirement in a format recognized by Red Hat Ansible Tower.

## Step 1 - Write a requirements.yml

Red Hat Ansible Tower can download and install Ansible Collections automatically before executing a Job Template. If a `collections/requirements.yml` exists, it will be parsed and Ansible Collections specified in this file will be automatically installed.

> **NOTE**: Starting with Red Hat Ansible Tower 3.6 the working directory for the Job Template is in `/tmp`. Since the Ansible Collection is downloaded into this directory before the Job Template is executed, you will not find temporary files of your Ansible Collection in `/var/lib/awx/projects/`.

The format of the `requirements.yml` for Ansible Collections is very similar to the one for roles, however it is very important to store in the folder `collections`.

Here is an example to set the `ansible.posix` Ansible Collection as a requirement:

```yaml
---
collections:
- ansible.posix
```

## Step 2 - Create Job Template

When using Ansible Collections in your Playbook, there are no additional options to set in your Red Hat Ansible Tower Job Template. You specify the repository in which your Playbook is stored, inventory, credentials and other parameters, and execute it by clicking on the **Launch** button.

# Troubleshooting

Since Red Hat Ansible Tower does only check for updates in the repository in which you stored your Playbook, it might not do a refresh if there was a change in the Ansible Collection used by your Playbook. This happens particularly if you also combine Roles and Collections.

In this case you should check the option **Delete on Update** which will delete the entire local directory during a refresh.

If there is a problem while parsing your `requirements.yml` it worth testing it with the `ansible-galaxy` command. As a reminder, Red Hat Ansible Tower basically also just runs the command for you with the appropriate parameters, so testing this works manually makes a lot of sense.

```bash
ansible-galaxy collections install -r collections/requirements.yml -f
```

> **NOTE**: The `-f` switch will forces a fresh installation of the specified Ansible Collections, otherwise `ansible-galaxy` will only install it, if it wasn't already installed. You can also use the `--force-with-deps` switch to make sure Ansible Collections which have dependencies to others are refreshed as well.

----
**Navigation**
<br>
[Previous Exercise](../3-collections-from-roles/) - [Next Exercise](../5-use-automation-hub)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
