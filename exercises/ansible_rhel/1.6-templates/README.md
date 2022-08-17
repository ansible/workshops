# Workshop Exercise - Templates

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
* [Step 1 - Using Templates in Playbooks](#step-1---using-templates-in-playbooks)
* [Step 2 - Challenge Lab](#step-2---challenge-lab)

## Objective

This exercise will cover Jinja2 templating. Ansible uses Jinja2 templating to modify files before they are distributed to managed hosts. Jinja2 is one of the most used template engines for Python (<http://jinja.pocoo.org/>).

## Guide

### Step 1 - Using Templates in Playbooks

When a template for a file has been created, it can be deployed to the managed hosts using the `template` module, which supports the transfer of a local file from the control node to the managed hosts.

As an example of using templates you will change the motd file to contain host-specific data.

First create the directory `templates` to hold template resources in `~/ansible-files/`:

```bash
[student@ansible-1 ansible-files]$ mkdir templates
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

* Understand what the Playbook does.
* Execute the Playbook `motd-facts.yml`.
* Login to node1 via SSH and check the message of the day content.
* Log out of node1.

You should see how Ansible replaces the variables with the facts it discovered from the system.

### Step 2 - Challenge Lab

Add a line to the template to list the current kernel of the managed node.

* Find a fact that contains the kernel version using the commands you learned in the "Ansible Facts" chapter.

> **Tip**
>
> filter for kernel

> Run the newly created playbook to find the fact name.

* Change the template to use the fact you found.

* Run the motd playbook again.

* Check motd by logging in to node1

> **Warning**
>
> **Solution below\!**

* Find the fact:

```yaml
---
- name: Capture Kernel Version
  hosts: node1

  tasks:

    - name: Collect only kernel facts
      ansible.builtin.setup:
        filter:
        - '*kernel'
      register: setup

    - debug:
        var: setup
```

With the wildcard in place, the output shows:

```bash

TASK [debug] *******************************************************************
ok: [node1] => {
    "setup": {
        "ansible_facts": {
            "ansible_kernel": "4.18.0-305.12.1.el8_4.x86_64"
        },
        "changed": false,
        "failed": false
    }
}
```

With this we can conclude the variable we are looking for is labeled `ansible_kernel`.

Then we can update the motd-facts.j2 template to include `ansible_kernel` as part of its message.

* Modify the template `motd-facts.j2`:

<!-- {% raw %} -->

```html+jinja
Welcome to {{ ansible_hostname }}.
{{ ansible_distribution }} {{ ansible_distribution_version}}
deployed on {{ ansible_architecture }} architecture
running kernel {{ ansible_kernel }}.
```

<!-- {% endraw %} -->

* Run the playbook.

```bash
[student@ansible-1 ~]$ ansible-navigator run motd-facts.yml -m stdout
```

* Verify the new message via SSH login to `node1`.

```bash
[student@ansible-1 ~]$ ssh node1
Welcome to node1.
RedHat 8.1
deployed on x86_64 architecture
running kernel 4.18.0-305.12.1.el8_4.x86_64.
```

---
**Navigation**
<br>
[Previous Exercise](../1.5-handlers) - [Next Exercise](../1.7-role)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
