# Workshop Exercise - Writing Your First Playbook

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

- [Workshop Exercise - Writing Your First Playbook](#workshop-exercise---writing-your-first-playbook)
  - [Objective](#objective)
  - [Guide](#guide)
    - [Step 1 - Playbook Basics](#step-1---playbook-basics)
    - [Step 2 - Creating Your Playbook](#step-2---creating-your-playbook)
    - [Step 3 - Running the Playbook](#step-3---running-the-playbook)
    - [Step 4 - Checking the Playbook](#step-4---checking-the-playbook)


## Objective

In this exercise, you'll use Ansible to conduct basic system setup tasks on a
Red Hat Enterprise Linux server. You will become familiar with fundamental
Ansible modules like `dnf` and `user`, and learn how to create and run
playbooks.

## Guide

Playbooks in Ansible are essentially scripts written in YAML format. They are
used to define the tasks and configurations that Ansible will apply to your
servers.

### Step 1 - Playbook Basics
First, create a text file in YAML format for your playbook. Remember:
- Start with three dashes (`---`).
- Use spaces, not tabs, for indentation.

Key Concepts:
- `hosts`: Specifies the target servers or devices for your playbook to run against.
- `tasks`: The actions Ansible will perform.
- `become`: Allows privilege escalation (running tasks with elevated privileges).

> NOTE: An Ansible playbook is designed to be idempotent, meaning if you run it multiple times on the same hosts, it ensures the desired state without making redundant changes.

### Step 2 - Creating Your Playbook
Before creating your first playbook, ensure you are in the correct directory by changing to `~/lab_inventory`:

```bash
cd ~/lab_inventory
```

Now create a playbook named `system_setup.yml` to perform basic system setup:
- Update all security related packages.
- Create a new user named ‘myuser’.

The basic structure looks as follows:

```yaml
---
- name: Basic System Setup
  hosts: node1
  become: true
  tasks:
    - name: Update all security-related packages
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true
   
    - name: Create a new user
      ansible.builtin.user:
        name: myuser
        state: present
        create_home: true
```

> NOTE: Updating the packages may take a few minutes prior to the Ansible playbook completing.

* About the `dnf` module: This module is used for package management with DNF (Dandified YUM) on RHEL and other Fedora-based systems.

* About the `user` module: This module is used to manage user accounts.

### Step 3 - Running the Playbook

Execute your playbook using the `ansible-navigator` command:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

Review the output to ensure each task is completed successfully.

### Step 4 - Checking the Playbook
Now, let’s create a second playbook for post-configuration checks, named `system_checks.yml`:

```yaml
---
- name: System Configuration Checks
  hosts: node1
  become: true
  tasks:
    - name: Check user existence
      ansible.builtin.command:
        cmd: id myuser
      register: user_check
 
    - name: Report user status
      ansible.builtin.debug:
        msg: "User 'myuser' exists."
      when: user_check.rc == 0
```

Run the checks playbook:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

Review the output to ensure the user creation was successful.

