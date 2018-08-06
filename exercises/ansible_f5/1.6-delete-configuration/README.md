# Exercise 6: Using a combination of modules to delete configuration on the BIG-IP

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate use of the different modules to delete the configuration (Nodes/Pool/Virtual Server) on the BIG-IP.
# Guide

## Step 1:

Using your text editor of choice create a new file called `bigip-delete-configuration.yml`.

```
[student1@ansible ~]$ nano bigip-delete-configuration.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format).

Enter the following play definition into `bigip-delete-configuration.yml`:

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
      name: "{{hostvars[item].inventory_hostname}}"
      state: absent
      validate_certs: "no"
    loop: "{{ groups['webservers'] }}"
```

>A play is a list of tasks. Tasks and modules have a 1:1 correlation.  Ansible modules are reusable, standalone scripts that can be used by the Ansible API, or by the ansible or ansible-playbook programs. They return information to ansible by printing a JSON string to stdout before exiting.

- `state: absent` iis a paremeter that tells the module to delete the configuration

The above playbook will delete the virtual server, then the pool and then the nodes configured

## Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-delete-configuration.yml
```

# Playbook Output
>output to be given here

# Solution
The finished Ansible Playbook is provided here for an Answer key. Click here: [bigip-delete-configuration.yml](bigip-delete-configuration.yml) or see below:

```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:

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
      name: "{{hostvars[item].inventory_hostname}}"
      state: absent
      validate_certs: "no"
    loop: "{{ groups['webservers'] }}"
```

# Verifying the Solution

Login to the F5 with your web browser to see what was configured.  Grab the IP information for the F5 load balancer from the lab_inventory/hosts file, and type it in like so: https://X.X.X.X:8443/

Navigate the menu on the left and view that the configuration has been deleted
* Local Traffic Manager -> Virtual Server
* Local Traffic Manager -> Pool
* Local Traffic Manager -> Node

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
