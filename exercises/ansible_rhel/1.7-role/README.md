# Workshop Exercise - Roles: Making your playbooks reusable

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
  - [Step 1 - Role Basics](#step-1---role-basics)
  - [Step 2 - Cleaning up the Environment](#step-2---cleaning-up-the-environment)
  - [Step 3 - Building the Apache Role](#step-3---building-the-apache-role)
  - [Step 4 - Role Integration in a Playbook](#step-4---role-integration-in-a-playbook)
  - [Step 4 - Role Execution and Validation](#step-4---role-execution-and-validation)
  - [Step 5 - Verify the Apache is Running](#step-5---verify-the-apache-is-running)

## Objective

This exercise builds upon the previous exercises and advances your Ansible skills by guiding you through the creation of a role that configures Apache (httpd). You'll take the knowledge you learned to now integrate variables, handlers, and a template for a custom index.html. This role demonstrates how to encapsulate tasks, variables, templates, and handlers into a reusable structure for efficient automation.

## Guide

### Step 1 - Role Basics

Roles in Ansible organize related automation tasks and resources, such as variables, templates, and handlers, into a structured directory. This exercise focuses on creating an Apache configuration role, emphasizing reusability and modularity.

### Step 2 - Cleaning up the Environment

Building on our previous work with Apache configuration, let's craft an Ansible playbook dedicated to tidying up our environment. This step paves the way for us to introduce a new Apache role, providing a clear view of the adjustments made. Through this process, we'll gain deeper insights into the versatility and reusability afforded by Ansible Roles.

Run the following Ansible playbook to clean the environment:

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
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: absent
      when: inventory_hostname in groups['web']

    - name: Remove firewalld
      ansible.builtin.dnf:
        name: firewalld
        state: absent

    - name: Delete created users
      ansible.builtin.user:
        name: "{{ item }}"
        state: absent
        remove: true  # Use 'remove: true’ to delete home directories
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

### Step 3 - Building the Apache Role

We'll develop a role named `apache` to install, configure, and manage Apache.

1. Generate Role Structure:

Create the role using ansible-galaxy, specifying the roles directory for output.

```bash
[student@ansible-1 lab_inventory]$ mkdir roles
[student@ansible-1 lab_inventory]$ ansible-galaxy init --offline roles/apache
```

2. Define Role Variables:

Populate `/home/student/lab_inventory/roles/apache/vars/main.yml` with Apache-specific variables:

```yaml
---
# vars file for roles/apache
apache_package_name: httpd
apache_service_name: httpd
```

3. Configure Role Tasks:

Adjust `/home/student/lab_inventory/roles/apache/tasks/main.yml` to include tasks for Apache installation and service management:

{% raw %}

```yaml
---
# tasks file for ansible-files/roles/apache
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
  ansible.builtin.dnf:
    name: firewalld
    state: present

- name: Ensure firewalld is running
  ansible.builtin.service:
    name: firewalld
    state: started
    enabled: true

- name: Allow HTTPS traffic on web servers
  ansible.posix.firewalld:
    service: https
    permanent: true
    state: enabled
  when: inventory_hostname in groups['web']
  notify: Reload Firewall
```

4. Implement Handlers:

In `/home/student/lab_inventory/roles/apache/handlers/main.yml`, create a handler to restart firewalld if its configuration changes:

{% raw %}
```yaml
---
# handlers file for ansible-files/roles/apache
- name: Reload Firewall
  ansible.builtin.service:
    name: firewalld
    state: reloaded
```
{% endraw %}

5. Create and Deploy Template:

Use a Jinja2 template for a custom `index.html`. Store the template in `templates/index.html.j2`:

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

6. Update `tasks/main.yml` to deploy this `index.html` template:

```yaml
- name: Deploy custom index.html
  ansible.builtin.template:
    src: index.html.j2
    dest: /var/www/html/index.html
```

### Step 4 - Role Integration in a Playbook

Embed the `apache` role in a playbook named `deploy_apache.yml` within `/home/student/lab_inventory` to apply it to your 'web' group hosts (node1, node2, node3).

```yaml
- name: Setup Apache Web Servers
  hosts: web
  become: true
  roles:
    - apache
```

### Step 4 - Role Execution and Validation

Launch your playbook to configure Apache across the designated web servers:

```bash
ansible-navigator run deploy_apache.yml -m stdout
```

#### Output:

```plaintext
PLAY [Setup Apache Web Servers] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [node2]
ok: [node1]
ok: [node3]

TASK [apache : Install Apache web server] **************************************
changed: [node1]
changed: [node2]
changed: [node3]

TASK [apache : Ensure Apache is running and enabled] ***************************
changed: [node2]
changed: [node1]
changed: [node3]

TASK [apache : Deploy custom index.html] ***************************************
changed: [node1]
changed: [node2]
changed: [node3]

RUNNING HANDLER [apache : Reload Firewall] *************************************
ok: [node2]
ok: [node1]
ok: [node3]

PLAY RECAP *********************************************************************
node1                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node2                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node3                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Step 5 - Verify the Apache is Running

Once the playbook has completed, verify that `httpd` is indeed running on all the web nodes.

```bash
[rhel@control ~]$ ssh node1 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 46s ago
```

```bash
[rhel@control ~]$ ssh node2 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 58s ago
```

Once `httpd` has been verified it is running, check to see if the Apache webserver is serving the appropriate `index.html` file:

```bash
[student@ansible-1 lab_inventory]$ curl http://node1
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
