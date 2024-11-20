# Workshop Exercise - Collections: Making Your Playbooks Modular and Scalable

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
  - [Step 1 - Understanding Ansible Collections](#step-1---understanding-ansible-collections)
  - [Step 2 - Cleaning up the Environment](#step-2---cleaning-up-the-environment)
  - [Step 3 - Building an Apache Collection](#step-3---building-an-apache-collection)
  - [Step 4 - Using the Collection in a Playbook](#step-4---using-the-collection-in-a-playbook)
  - [Step 5 - Collection Execution and Validation](#step-5---collection-execution-and-validation)
  - [Step 6 - Verify Apache is Running](#step-6---verify-apache-is-running)

## Objective

This exercise builds on your previous experience with Ansible by focusing on **collections**. Collections offer an efficient way to package and distribute automation content, including roles, modules, plugins, and playbooks, all within a single unit. In this exercise, we’ll develop a collection that installs and configures Apache (httpd), demonstrating how to structure content for modular and reusable automation.

## Guide

### Step 1 - Understanding Ansible Collections

**Ansible collections** are the preferred way to **organize, distribute, and reuse automation content**. They group together various components—like roles, modules, and plugins—so developers can manage and share automation resources more efficiently. Collections allow you to store related content in one place and distribute it via **Ansible Galaxy**, **Automation Hub**, or **private Automation Hub** within your organization.

Each **collection** can include the following components:

#### Modules  
Small programs that perform specific automation tasks on **local machines, APIs, or remote hosts**. Modules are usually written in **Python** and include metadata defining **how, when, and by whom** the task can be executed. Modules can be used across various use cases like **cloud management, networking, and configuration management**.  

**Example modules:**  
- **package**: Installs or removes packages with the systems package manager.  
- **service**: Manages system services (start, stop, restart).  
- **command**: Executes commands on a target system.  

#### Roles  
**Roles** are modular bundles of tasks, variables, templates, and handlers. They simplify automation workflows by breaking them into **reusable components**. Roles can be imported into **playbooks** and used across multiple automation scenarios, reducing duplication and improving manageability.

#### Plugins  
**Plugins** extend Ansible’s core functionality by adding **custom connection types, callbacks, or lookup functions**. Unlike modules, which execute actions on managed nodes, plugins **typically run on the control node** to enhance how Ansible operates during execution.

#### Playbooks  
**Playbooks** are **YAML files** that describe **automation workflows**. They contain a series of **plays**—which map tasks to managed hosts—and serve as the blueprint for configuring and managing systems.

### Step 2 - Cleaning up the Environment

Before we build the collection, let's clean up any previous Apache installations.

{% raw %}

```yaml
---
- name: Cleanup Environment
  hosts: all
  become: true
  vars:
    package_name: httpd
  tasks:
    - name: Remove Apache from web servers
      ansible.builtin.package:
        name: "{{ package_name }}"
        state: absent
      when: inventory_hostname in groups['web']

    - name: Remove firewalld
      ansible.builtin.package:
        name: firewalld
        state: absent

    - name: Delete created users
      ansible.builtin.user:
        name: "{{ item }}"
        state: absent
        remove: true
      loop:
        - alice
        - bob
        - carol
        - Roger

    - name: Reset MOTD to an empty message
      ansible.builtin.copy:
        dest: /etc/motd
        content: ''
```

{% endraw %}

Now run the playbook to clean the environment

```bash
ansible-navigator run cleanup.yml -m stdout
```

## Step 3 - Building an Apache Collection

1. Create the Collection Structure

Use `ansible-galaxy` to initialize the collection structure:

```bash
[student@ansible-1 lab_inventory]$ ansible-galaxy collection init webops.apache --init-path ./collections/ansible_collections
```

This creates the following structure:

```bash
.
└── collections
    └── ansible_collections
        └── webops
            └── apache
                ├── docs
                ├── galaxy.yml
                ├── meta
                │   └── runtime.yml
                ├── plugins
                │   └── README.md
                ├── README.md
                └── roles
```

2. Create the `apache` role within your `webops.apache` collection:

```bash
[student@ansible-1 lab_inventory]$ cd collections/ansible_collections/webops/apache/roles
[student@ansible-1 roles]$ ansible-galaxy role init apache
```

3. Define Role Variables:

Add Apache-specific variables in roles/apache/vars/main.yml:

```yaml
---
apache_package_name: httpd
apache_service_name: httpd
```

4. Create Role Tasks:

Add the following tasks to roles/apache/tasks/main.yml to install and configure Apache:

{% raw %}

```yaml
---
- name: Install Apache web server
  ansible.builtin.package:
    name: "{{ apache_package_name }}"
    state: present

- name: Ensure Apache is running and enabled
  ansible.builtin.service:
    name: "{{ apache_service_name }}"
    state: started
    enabled: true

- name: Install firewalld
  ansible.builtin.package:
    name: firewalld
    state: present

- name: Allow HTTP traffic on web servers
  ansible.posix.firewalld:
    service: http
    permanent: true
    state: enabled
  when: inventory_hostname in groups['web']
  notify: Reload Firewall
```
{% endraw %}

5. Add Handlers:

Create a handler to reload the firewall in roles/apache/handlers/main.yml:

{% raw %}

```yaml
---
- name: Reload Firewall
  ansible.builtin.service:
    name: firewalld
    state: reloaded
```
{% endraw %}

6. Create a Custom Webpage Template:

Add a Jinja2 template for the web page in roles/apache/templates/index.html.j2:

{% raw %}

```html
<html>
<head>
  <title>Welcome to {{ ansible_hostname }}</title>
</head>
<body>
  <h1>Hello from {{ ansible_hostname }}</h1>
</body>
</html>
```

{% endraw %}

7. Deploy the Template:

Add the template deployment task to roles/apache/tasks/main.yml:

```yaml
- name: Deploy custom index.html
  ansible.builtin.template:
    src: index.html.j2
    dest: /var/www/html/index.html
```

## Step 4 - Using the Collection in a Playbook

Create a playbook named `deploy_apache.yml` within `~/lab_inventory` directory to apply the collection to the `web` group:

```yaml
---
- name: Deploy Apache using Collection
  hosts: web
  become: true
  collections:
    - webops.apache
  roles:
    - apache
```

## Step 5 Create a `requirements.yml` file and run it

The Ansible playbook requires the `ansible.posix` collection. Create and add this requirement to your `requirements.yml` file that shall reside under `~/lab_inventory`

```bash
collections:
  - name: ansible.posix
```

```bash
ansible-galaxy collection install -r requirements.yml
```

## Step 6 - Collection Execution and Validation

Run the playbook using `ansible-navigator`:

```bash
ansible-navigator run deploy_apache.yml -m stdout
```
```text
PLAY [Deploy Apache using Collection] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node1]
ok: [node2]

TASK [webops.apache.apache : Install Apache web server] ************************
changed: [node3]
changed: [node1]
changed: [node2]

TASK [webops.apache.apache : Ensure Apache is running and enabled] *************
changed: [node3]
changed: [node1]
changed: [node2]

TASK [webops.apache.apache : Install firewalld] ********************************
changed: [node3]
changed: [node1]
changed: [node2]

TASK [webops.apache.apache : Allow HTTP traffic on web servers] ****************
ok: [node3]
ok: [node1]
ok: [node2]

TASK [webops.apache.apache : Deploy custom index.html] *************************
ok: [node3]
ok: [node2]
ok: [node1]

PLAY RECAP *********************************************************************
node1                      : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node2                      : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node3                      : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

## Step 6 - Verify Apache is Running

After the playbook runs, verify Apache is active on the web servers:

```bash
[rhel@control ~]$ ssh node1 "systemctl status httpd"
```

You should see output confirming Apache is running. Finally, confirm the web page is served:

```bash
[student@ansible-1 lab_inventory]$ curl http://node1
```
```html
<html>
<head>
  <title>Welcome to node1</title>
</head>
<body>
  <h1>Hello from node1</h1>
</body>
</html>
```
---
**Navigation**
<br>
[Previous Exercise](../1.6-templates) - [Next Exercise](../1.8-troubleshoot)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
