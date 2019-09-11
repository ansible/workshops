# Exercise 3.2 - Deleting a Web Application

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate deleting a Web Application with AS3 and the uri module.

# Guide

## Step 1:

Using your text editor of choice create a new file called `delete.yml`:

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Enter the following play definition into `delete.yml`:

{% raw %}
``` yaml
---
- name: LINKLIGHT AS3
  hosts: lb
  connection: local
  gather_facts: false

```
{% endraw %}

- The `---` at the top of the file indicates that this is a YAML file.
- The `hosts: lb`,  indicates the play is run only on the lb group.  Technically there only one F5 device but if there were multiple they would be configured simultaneously.
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: false` disables facts gathering.  We are not using any fact variables for this playbook.

## Step 3

**Append** the following to the delete.yml Playbook.  
{% raw %}
```
  tasks:

  - name: PUSH AS3
    uri:
      url: "https://{{ ansible_host }}:8443/mgmt/shared/appsvcs/declare/WorkshopExample"
      method: DELETE
      status_code: 200
      timeout: 300
      body_format: json
      force_basic_auth: yes
      user: "{{ ansible_user }}"
      password: "{{ ansible_ssh_pass }}"
      validate_certs: no
    delegate_to: localhost
```
{% endraw %}

There is only three parameters that have changed from the previous exercise.
- `url` has changed.  Instead of ending with `declare` it now ends with the tenant name, which is `WorkshopExample`.
- `method` has changed from POST to DELETE.
- `body` has been removed.  It is not required since we simply deleting this entire tenant.

## Step 4
Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook delete.yml
```

# Playbook Output

The output will look as follows.

{% raw %}
```yaml
[student1@ansible ~]$ ansible-playbook delete.yml

PLAY [LINKLIGHT AS3] ***********************************************************

TASK [PUSH AS3] ********************************************************************************
ok: [f5 -> localhost]

PLAY RECAP ********************************************************************************
f5                         : ok=1    changed=0    unreachable=0    failed=0
```
{% endraw %}

# Solution

The finished Ansible Playbook is provided here for an Answer key.  Click here: [delete.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/3.2-as3-delete/delete.yml).

Login to the web UI and make sure the `Partition` is removed.

--
You have finished this exercise.  [Click here to return to the lab guide](../README.md)
