# Exercise 7: Using a combination of modules to perform a graceful rollback

## Table of Contents

- [Objective](#Objective)
- [Guide](#Guide)
- [Playbook Output](#Playbook_Output)
- [Solution](#Solution)

# Objective

Demonstrate use of the different modules to perform a rollback of the configuration on the BIG-IP. 
# Guide

## Step 1:

Using your text editor of choice create a new file called `bigip-error-handling.yml`.

```
[student1@ansible ~]$ nano bigip-error-handling.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format).

Enter the following play definition into `bigip-error-handling.yml`:

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false
```

- The `---` at the top of the file indicates that this is a YAML file.
- The `hosts: f5`,  indicates the play is run only on the F5 BIG-IP device
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: no` disables facts gathering.  We are not using any fact variables for this playbook.

## Step 3

Next, add the first `task`. This task will use the different modules to delete configuration on the BIG-IP

``` yaml
---
  - name: Setup and graceful rollback BIG-IP configuration
    block:
    - name: Create nodes
      bigip_node:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       host: "{{hostvars[item].ansible_host}}"
       name: "{{hostvars[item].inventory_hostname}}"
       validate_certs: "no"
      loop: "{{ groups['webservers'] }}"
    - name: Create pool
      bigip_pool:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       name: "http_pool"
       lb_method: "round-robin"
       monitors: "/Common/http"
       monitor_type: "and_list"
       validate_certs: "no"
    - name: Add Pool members
      bigip_pool_member:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       state: "present"
       port: "80"
       pool: "http_pool"
       host: "{{hostvars[item].ansible_host}}"
       name: "{{hostvars[item].inventory_hostname}}"
       validate_certs: "no"
      loop: "{{ groups['webservers'] }}"
    - name: Add Virtual Server
      bigip_virtual_server:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       name: "vip"
       destination: "{{private_ip}}"
       port: "443"
       enabled_vlans: "all"
       all_profiles: ['http','clientssl','oneconnect']
       pool: "http_pool"
       snat: "Automap1"
       validate_certs: "no"
    rescue:
    - name: Delete Virtual Server
      bigip_virtual_server:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       name: "vip"
       state: absent
       validate_certs: "no"
    - name: Delete pool
      bigip_pool:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       name: "http_pool"
       state: absent
       validate_certs: "no"
    - name: Delete nodes
      bigip_node:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       state: absent
       name: "{{hostvars[item].inventory_hostname}}"
       validate_certs: "no"
      loop: "{{ groups['webservers'] }}"
    always:
    - debug: msg="Executed rollback playbook"
```

>A play is a list of tasks. Tasks and modules have a 1:1 correlation.  Ansible modules are reusable, standalone scripts that can be used by the Ansible API, or by the ansible or ansible-playbook programs. They return information to ansible by printing a JSON string to stdout before exiting.

The above playbook will try and configure the Virtual Server, Pool and Nodes but since the snat value is provided as 'Automap1' the addition of virtual server will fail and the 'rescue' block will be run 

## Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-error-handling.yml
```

# Playbook Output
>*output to be given here

# Solution
The finished Ansible Playbook is provided here for an Answer key.

```yaml
---
- name: BIG-IP setup
  hosts: lb
  connection: local
  gather_facts: false

  tasks:

  - name: Setup and graceful rollback BIG-IP configuration
    block:
    - name: Create nodes
      bigip_node:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       host: "{{hostvars[item].ansible_host}}"
       name: "{{hostvars[item].inventory_hostname}}"
       validate_certs: "no"
      loop: "{{ groups['webservers'] }}"
    - name: Create pool
      bigip_pool:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       name: "http_pool"
       lb_method: "round-robin"
       monitors: "/Common/http"
       monitor_type: "and_list"
       validate_certs: "no"
    - name: Add Pool members
      bigip_pool_member:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       state: "present"
       port: "80"
       pool: "http_pool"
       host: "{{hostvars[item].ansible_host}}"
       name: "{{hostvars[item].inventory_hostname}}"
       validate_certs: "no"
      loop: "{{ groups['webservers'] }}"
    - name: Add Virtual Server
      bigip_virtual_server:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       name: "vip"
       destination: "{{private_ip}}"
       port: "443"
       enabled_vlans: "all"
       all_profiles: ['http','clientssl','oneconnect']
       pool: "http_pool"
       snat: "Automap1"
       validate_certs: "no"
    rescue:
    - name: Delete Virtual Server
      bigip_virtual_server:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       name: "vip"
       state: absent
       validate_certs: "no"
    - name: Delete pool
      bigip_pool:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       name: "http_pool"
       state: absent
       validate_certs: "no"
    - name: Delete nodes
      bigip_node:
       server: "{{private_ip}}"
       user: "{{ansible_user}}"
       password: "{{ansible_ssh_pass}}"
       server_port: "8443"
       state: absent
       name: "{{hostvars[item].inventory_hostname}}"
       validate_certs: "no"
      loop: "{{ groups['webservers'] }}"
    always:
    - debug: msg="Executed rollback playbook"
```

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
