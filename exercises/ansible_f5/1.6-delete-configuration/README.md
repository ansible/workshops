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

Next, add the first `task` using the [bigip_virtual_server](https://docs.ansible.com/ansible/latest/modules/bigip_virtual_server_module.html).  This task will be identical to [Exercise 1.5 - Adding a virtual server](../1.5-add-virtual-server/README.md) with an additional **state** parameter.  The `state: absent` will remove the configuration from the F5 BIG-IP load balancer.

{% raw %}

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  - name: DELETE VIRTUAL SERVER
    bigip_virtual_server:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      name: "vip"
      state: absent
      validate_certs: "no"
```

{% endraw %}

- `state: absent` is a parameter that tells the module to delete the configuration

## Step 4

Next, add the second `task` using the [bigip_pool](https://docs.ansible.com/ansible/latest/modules/bigip_pool_module.html).  This task will be identical to [Exercise 1.3 - Adding a load balancing pool](../1.3-add-pool/README.md) with an additional **state** parameter set to `absent`.


{% raw %}

```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:

  - name: DELETE VIRTUAL SERVER
    bigip_virtual_server:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      name: "vip"
      state: absent
      validate_certs: "no"

  - name: DELETE POOL
    bigip_pool:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      name: "http_pool"
      state: absent
      validate_certs: "no"
```
{% endraw %}

## Step 5

Finally, add the last `task` using the [bigip_node](https://docs.ansible.com/ansible/latest/modules/bigip_node_module.html).  This task will be identical to [Exercise 1.2 - Adding nodes to F5 BIG-IP](1.2-add-node) with an additional **state** parameter set to `absent`.


{% raw %}

```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:

  - name: DELETE VIRTUAL SERVER
    bigip_virtual_server:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      name: "vip"
      state: absent
      validate_certs: "no"

  - name: DELETE POOL
    bigip_pool:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      name: "http_pool"
      state: absent
      validate_certs: "no"

  - name: DELETE NODES
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
{% endraw %}

The above playbook will delete the virtual server, then the pool and then the nodes configured in previous exercises.


## Step 6

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-delete-configuration.yml
```

# Playbook Output

```
[student1@ansible]$ ansible-playbook bigip-delete-configuration.yml

PLAY [BIG-IP TEARDOWN] *********************************************************

TASK [DELETE VIRTUAL SERVER] ***************************************************
changed: [f5]

TASK [DELETE POOL] ********************************************************************************
changed: [f5]

TASK [DELETE NODES] ************************************************************
ok: [f5] => (item=107.23.182.171)
ok: [f5] => (item=34.224.38.246)

PLAY RECAP ********************************************************************************
f5                         : ok=3    changed=2    unreachable=0    failed=0
```
# Solution

The finished Ansible Playbook is provided here for an Answer key. Click here: [bigip-delete-configuration.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.6-delete-configuration/bigip-delete-configuration.yml).

# Verifying the Solution

Login to the F5 with your web browser to see what was configured.  Grab the IP information for the F5 load balancer from the lab_inventory/hosts file, and type it in like so: https://X.X.X.X:8443/

Navigate the menu on the left and view that the configuration has been deleted
* Local Traffic Manager -> Virtual Server
* Local Traffic Manager -> Pool
* Local Traffic Manager -> Node

You have finished this exercise.  

[Click here to return to the lab guide](../README.md)
