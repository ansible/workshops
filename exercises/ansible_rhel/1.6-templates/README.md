# Workshop Exercise - Templates

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).


## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
  - [Step 1 - Introduction to Jinja2 Templating](#step-1---introduction-to-jinja2-templating)
  - [Step 2 - Crafting Your First Template](#step-2---crafting-your-first-template)
  - [Step 3 - Deploying the Template with a Playbook](#step-3---deploying-the-template-with-a-playbook)
  - [Step 4 - Executing the Playbook](#step-4---executing-the-playbook)

## Objective

Exercise 1.5 introduces Jinja2 templating within Ansible, a powerful feature for generating dynamic files from templates. You'll learn how to craft templates that incorporate host-specific data, enabling the creation of tailored configuration files for each managed host.

## Guide

### Step 1 - Introduction to Jinja2 Templating

Ansible leverages Jinja2, a widely-used templating language for Python, allowing dynamic content generation within files. This capability is particularly useful for configuring files that must differ from host to host.

### Step 2 - Crafting Your First Template

Templates end with a `.j2` extension and mix static content with dynamic placeholders enclosed in {% raw %} `{{ }}` {% endraw %}.

In the following example, let's create a template for the Message of the Day (MOTD) that includes dynamic host information.

#### Set Up the Template Directory:

Ensure a templates directory exists within your lab_inventory directory to organize your templates.

```bash
mkdir -p ~/lab_inventory/templates
```

#### Develop the MOTD Template:

Create a file named `motd.j2` in the templates directory with the following content:

{% raw %}

```jinja
Welcome to {{ ansible_hostname }}.
OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
Architecture: {{ ansible_architecture }}
```

{% endraw %}

This template dynamically displays the hostname, OS distribution, version, and architecture of each managed host.

### Step 3 - Deploying the Template with a Playbook

Utilize the `ansible.builtin.template` module in a playbook to distribute and render the template across your managed hosts.

Modify the `system_setup.yml` Playbook with the following content:

```yaml
---
- name: Basic System Setup
  hosts: all
  become: true
  tasks:
.
.
.
    - name: Update MOTD from Jinja2 Template
      ansible.builtin.template:
        src: templates/motd.j2
        dest: /etc/motd


  handlers:
    - name: Reload Firewall
      ansible.builtin.service:
        name: firewalld
        state: reloaded

```

The `ansible.builtin.template` module takes the `motd.j2` template and generates an `/etc/motd` file on each host, filling in the template's placeholders with the actual host facts.

### Step 4 - Executing the Playbook

Run the playbook to apply your custom MOTD across all managed hosts:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```


```plaintext
PLAY [Basic System Setup] ******************************************************
.
.
.

TASK [Update MOTD from Jinja2 Template] ****************************************
changed: [node1]
changed: [node2]
changed: [node3]
changed: [ansible-1]

PLAY RECAP *********************************************************************
ansible-1                  : ok=6    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Verify the changes by SSHing into the node, and you should see the message of the day:

```plaintext
[rhel@control ~]$ ssh node1
```
```
Welcome to node1.
OS: RedHat 8.7
Architecture: x86_64
Register this system with Red Hat Insights: insights-client --register
Create an account or view all your systems at https://red.ht/insights-dashboard
Last login: Mon Jan 29 16:30:31 2024 from 10.5.1.29

```

**Navigation**
<br>
[Previous Exercise](../1.5-handlers) - [Next Exercise](../1.7-collection)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
