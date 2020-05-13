# Workshop Exercise - Templates

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
* [Step 1 - Using Templates in Playbooks](#step-1---using-templates-in-playbooks)
* [Step 2 - Challenge Lab](#step-2---challenge-lab)

# Objective

This exercise will cover Jinja2 templating. Ansible uses Jinja2 templating to modify files before they are distributed to managed hosts. Jinja2 is one of the most used template engines for Python (<http://jinja.pocoo.org/>).  

# Guide

## Step 1 - Using Templates in Playbooks

When a template for a file has been created, it can be deployed to the managed hosts using the `template` module, which supports the transfer of a local file from the control node to the managed hosts.

As an example of using templates you will change the motd file to contain host-specific data.

First create the directory `templates` to hold template resources in `~/ansible-files/`:

```bash
[student<X>@ansible ansible-files]$ mkdir templates
```

Then in the `~/ansible-files/templates/` directory create the template file `motd-facts.j2`:

<!-- {% raw %} -->
```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture.
```
<!-- {% endraw %} -->

The template file contains the basic text that will later be copied over. It also contains variables which will be replaced on the target machines individually.

Next we need a playbook to use this template. In the `~/ansible-files/` directory create the Playbook `motd-facts.yml`:

```yaml
---
- name: Fill motd file with host data
  hosts: node1
  become: true
  tasks:
    - template:
        src: motd-facts.j2
        dest: /etc/motd
        owner: root
        group: root
        mode: 0644
```

You have done this a couple of times by now:

  - Understand what the Playbook does.

  - Execute the Playbook `motd-facts.yml`.

  - Login to node1 via SSH and check the message of the day content.

  - Log out of node1.

You should see how Ansible replaces the variables with the facts it discovered from the system.

## Step 2 - Challenge Lab

Add a line to the template to list the current kernel of the managed node.

  - Find a fact that contains the kernel version using the commands you learned in the "Ansible Facts" chapter.

> **Tip**
>
> Do a `grep -i` for kernel

  - Change the template to use the fact you found.

  - Run the Playbook again.

  - Check motd by logging in to node1

> **Warning**
>
> **Solution below\!**


  - Find the fact:
```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep -i kernel
       "ansible_kernel": "3.10.0-693.el7.x86_64",
```

  - Modify the template `motd-facts.j2`:
<!-- {% raw %} -->
```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture
running kernel {{ ansible_kernel }}.
```
<!-- {% endraw %} -->

  - Run the playbook.
```
[student1@ansible ~]$ ansible-playbook motd-facts.yml
```

  - Verify the new message via SSH login to `node1`.
```
[student1@ansible ~]$ ssh node1
Welcome to node1.
RedHat 8.1
deployed on x86_64 architecture
running kernel 4.18.0-147.8.1.el8_1.x86_64.
```

----
**Navigation**
<br>
[Previous Exercise](../1.5-handlers) - [Next Exercise](../1.7-role)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
