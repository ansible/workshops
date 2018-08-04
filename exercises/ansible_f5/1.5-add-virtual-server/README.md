# Exercise 5: Using the bigip_virtual_server module

## Table of Contents

- [Objective](#Objective)
- [Guide](#Guide)
- [Playbook Output](#Playbook_Output)
- [Solution](#Solution)

# Objective

Demonstrate use of the [BIG-IP virtual server module](https://docs.ansible.com/ansible/latest/modules/bigip_virtual_server_module.html) to configure a virtual server on the BIG-IP. Virtual server is a combination of IP:Port.

# Guide

## Step 1:

Using your text editor of choice create a new file called `bigip-virtual-server.yml`.

```
[student1@ansible ~]$ nano bigip-virtual-server.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format).

Enter the following play definition into `bigip-virtual-server.yml`:

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

Next, add the first `task`. This task will use the `bigip-virtual-server` to configure a virtual server on the BIG-IP

``` yaml
---
- name: ADD VIRTUAL SERVER
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
      snat: "Automap"
      validate_certs: "no"
```

>A play is a list of tasks. Tasks and modules have a 1:1 correlation.  Ansible modules are reusable, standalone scripts that can be used by the Ansible API, or by the ansible or ansible-playbook programs. They return information to ansible by printing a JSON string to stdout before exiting.

- `name: ADD VIRTUAL SERVER` is a user defined description that will display in the terminal output.
- `bigip_virtual_server:` tells the task which module to use.
- The `server: "{{private_ip}}"` parameter tells the module to connect to the F5 BIG-IP IP address, which is stored as a variable `private_ip` in inventory
- The `user: "{{ansible_user}}"` parameter tells the module the username to login to the F5 BIG-IP device with
- The`password: "{{ansible_ssh_pass}}"` parameter tells the module the password to login to the F5 BIG-IP device with
- The `server_port: 8443` parameter tells the module the port to connect to the F5 BIG-IP device with
- The `name: "vip"` parameter tells the module to create a virtual server named vip
- The `destination"` parameter tells the module which IP address to assign for the virtual server
- The `port` paramter tells the module which Port the virtual server will be listening on
- The `enabled_vlans` parameter tells the module which all vlans the virtual server is enbaled for
- The `all_profiles` paramter tells the module which all profiles are assigned to the virtuals server 
- The `pool` parameter tells the module which pool is assigned to the virtual server
- The `snat` paramter tells the module what the Source network address address should be. In this module we are assigning it to be Automap which means the source address on the request that goes to the backend server will be the self-ip address of the BIG-IP
- The `validate_certs: "no"` parameter tells the module to not validate SSL certificates.  This is just used for demonstration purposes since this is a lab.

## Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-virtual-server.yml
```

# Playbook Output
>*output to be given here

# Solution
The finished Ansible Playbook is provided here for an Answer key.

```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:

  - name: ADD VIRTUAL SERVER
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
      snat: "Automap"
      validate_certs: "no"
```

# Verifying the Solution

Login to the F5 with your web browser to see what was configured.  Grab the IP information for the F5 load balancer from the lab_inventory/hosts file, and type it in like so: https://X.X.X.X:8443/

The load balancer virtual server can be found by navigating the menu on the left.  Click on Local Traffic-> then click on Virtual Server.
>*Image to be inserted

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
