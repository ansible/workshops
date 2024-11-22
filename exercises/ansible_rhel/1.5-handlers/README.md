# Workshop Exercise - Conditionals, Handlers and Loops

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

# Workshop Exercises - Using Conditionals, Handlers, and Loops

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
  - [Step 1 - Understanding Conditionals, Handlers, and Loops](#step-1---understanding-conditionals-handlers-and-loops)
  - [Step 2 - Conditionals](#step-2---conditionals)
  - [Step 3 - Handlers](#step-3---handlers)
  - [Step 4 - Loops](#step-4---loops)

## Objective

Expanding on Exercise 1.4, this exercise introduces the application of conditionals, handlers, and loops in Ansible playbooks. You'll learn to control task execution with conditionals, manage service responses with handlers, and efficiently handle repetitive tasks using loops.

## Guide

Conditionals, handlers, and loops are advanced features in Ansible that enhance control, efficiency, and flexibility in your automation playbooks.

### Step 1 - Understanding Conditionals, Handlers, and Loops

- **Conditionals**: Enable tasks to be executed based on specific conditions.
- **Handlers**: Special tasks triggered by a `notify` directive, typically used for restarting services after changes.
- **Loops**: Used to repeat a task multiple times, particularly useful when the task is similar but needs to be applied to different items.

### Step 2 - Conditionals

Conditionals in Ansible control whether a task should run based on certain conditions.
Let's add to the system_setup.yml playbook the ability to install the Apache HTTP Server (`httpd`) only on hosts that belong to the `web` group in our inventory.

> NOTE: Previous examples had hosts set to node1 but now it is set to all. This means when you run this updated Ansible playbook you will notice updates for the new systems being automated against, the user Roger created on all new systems and the Apache web server package httpd installed on all the hosts within the web group.

{% raw %}

```yaml
---
- name: Basic System Setup
  hosts: all
  become: true
  vars:
    user_name: 'Roger'
    package_name: httpd
  tasks:
    - name: Update all security-related packages
      ansible.builtin.package:
        name: '*'
        state: latest
        security: true
        update_only: true

    - name: Create a new user
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true

    - name: Install Apache on web servers
      ansible.builtin.package:
        name: "{{ package_name }}"
        state: present
      when: inventory_hostname in groups['web']
```

{% endraw %}

In this example, `inventory_hostname in groups['web']` is the conditional statement. `inventory_hostname` refers to the name of the current host that Ansible is working on in the playbook. The condition checks if this host is part of the `web` group defined in your inventory file. If true, the task will execute and install Apache on that host.

### Step 3 - Handlers

Handlers are used for tasks that should only run when notified by another task. Typically, they are used to restart services after a configuration change.

Let's say we want to ensure the firewall is configured correctly on all web servers and then reload the firewall service to apply any new settings. We'll define a handler that reloads the firewall service and is notified by a task ^that ensures the desired firewall rules are in place. Add the following tasks to the existing playbook to install firewalld and enable firewalld and reload the service with the help of handlers.


```yaml
---
- name: Basic System Setup
  hosts: all
  become: true
  .
  .
  .
    - name: Install firewalld
      ansible.builtin.package:
        name: firewalld
        state: present
      when: inventory_hostname in groups['web']

    - name: Ensure firewalld is running
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true
      when: inventory_hostname in groups['web']

    - name: Allow HTTP traffic on web servers
      ansible.posix.firewalld:
        service: http
        permanent: true
        state: enabled
      when: inventory_hostname in groups['web']
      notify: Reload Firewall

  handlers:
    - name: Reload Firewall
      ansible.builtin.service:
        name: firewalld
        state: reloaded

```

The handler Restart Apache is triggered only if the task “Allow HTTP traffic on web servers” makes any changes.

> NOTE: Notice how the name of the handler is used within the notify section of the “Reload Firewall” configuration task. This ensures that the proper handler is executed as there can be multiple handlers within an Ansible playbook.

```
PLAY [Basic System Setup] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node1]
ok: [node2]
ok: [ansible-1]

TASK [Update all security-related packages] ************************************
ok: [node1]
changed: [ansible-1]
changed: [node3]
changed: [node2]

TASK [Create a new user] *******************************************************
changed: [node3]
ok: [node1]
changed: [node2]
changed: [ansible-1]

TASK [Install Apache on web servers] *******************************************
skipping: [ansible-1]
ok: [node3]
ok: [node1]
ok: [node2]

PLAY RECAP *********************************************************************
ansible-1                  : ok=3    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
node1                      : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node2                      : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node3                      : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

### Step 4 - Loops

Loops in Ansible allow you to perform a task multiple times with different values. This feature is particularly useful for tasks like creating multiple user accounts in our given example.
In the original system_setup.yml playbook from Exercise 1.4, we had a task for creating a single user:

{% raw %}
```yaml
- name: Create a new user
  ansible.builtin.user:
    name: "{{ user_name }}"
    state: present
    create_home: true

```
{% endraw %}

Now, let's modify this task to create multiple users using a loop:

{% raw %}
```yaml
- name: Create a new user
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
    create_home: true
  loop:
    - alice
    - bob
    - carol
```
{% endraw %}

What Changed?

1. Loop Directive: The loop keyword is used to iterate over a list of items. In this case, the list contains the names of users we want to create: alice, bob, and carol.

2. User Creation with Loop: Instead of creating a single user, the modified task
now iterates over each item in the loop list. The {% raw %}`{{ item }}` {% endraw %} placeholder is dynamically replaced with each username in the list, so the ansible.builtin.user module creates each user in turn.

When you run the updated playbook, this task is executed three times, once for each user specified in the loop. It's an efficient way to handle repetitive tasks with varying input data.

Snippet of the output for creating a new user on all the nodes.

```
[student@ansible-1 ~lab_inventory]$ ansible-navigator run system_setup.yml -m stdout

PLAY [Basic System Setup] ******************************************************

.
.
.

TASK [Create a new user] *******************************************************
changed: [node3] => (item=alice)
changed: [node1] => (item=alice)
changed: [node2] => (item=alice)
changed: [ansible-1] => (item=alice)
changed: [node3] => (item=bob)
changed: [node1] => (item=bob)
changed: [node2] => (item=bob)
changed: [node3] => (item=carol)
changed: [ansible-1] => (item=bob)
changed: [node1] => (item=carol)
changed: [node2] => (item=carol)
changed: [ansible-1] => (item=carol)

.
.
.


PLAY RECAP *********************************************************************
ansible-1                  : ok=3    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
node1                      : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node2                      : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node3                      : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 

```
---
**Navigation**
<br>
[Previous Exercise](../1.4-variables) - [Next Exercise](../1.6-templates)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
