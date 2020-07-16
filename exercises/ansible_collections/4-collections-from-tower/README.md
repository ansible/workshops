# Exercise 3 - How to use Collections on Red Hat Ansible Tower

## Table of Contents

<!-- TOC -->

- [Exercise 3 - How to use Collections on Red Hat Ansible Tower](#exercise-3---how-to-use-collections-on-red-hat-ansible-tower)
    - [Table of Contents](#table-of-contents)
- [Guide](#guide)
    - [Step 1 - Write requirements.yml](#step-1---write-requirementsyml)
    - [Step 2 - Create Job Template](#step-2---create-job-template)
    - [Troubleshooting](#troubleshooting)

<!-- /TOC -->

# Guide

Red Hat Ansible Tower supports Ansible Collections starting with version 3.5 - earlier version will not automatically install and configure them for you. To make sure Ansible Collections are recognized by Red Hat Ansible Tower a requirements file is needed and has to be stored in the proper directory.

## Step 1 - Write requirements.yml

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

## Troubleshooting

Since Red Hat Ansible Tower does only check for updates in the the repository in which you stored your Playbook, it might not do a refresh if there was a change in the Ansible Collection used by your Playbook.

In this case you should check the option **