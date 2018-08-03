# Exercise 1: Using the bigip_facts module

## Table of Contents

- [Objective](#Objective)
- [Guide](#Guide)
- [Playbook Output](#Playbook_Output)
- [Solution](#Solution)

# Objective

Demonstrate use of the [BIG-IP pool member module](https://docs.ansible.com/ansible/latest/modules/bigip_pool_module.html) to tie web server nodes into the load balancing pool `http_pool` created in the previous exercises.  

# Guide

## Step 1:

Using your text editor of choice create a new file called `bigip-pool-members.yml`.

```
[student1@ansible ~]$ nano bigip-pool-members.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Enter the following play definition into `bigip-pool-members.yml`:

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false
```

- The `---` at the top of the file indicates that this is a YAML file.
- The `hosts: lb`,  indicates the play is run only on the lb group.  Technically there only one F5 device but if there were multiple they would be configured simultaneously.
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: false` disables facts gathering.  We are not using any fact variables for this playbook.

## Step 3

Next, add the first `task`. This task will use the `bigip_pool_member` module configure the two RHEL web servers as nodes on the BIG-IP F5 load balancer.

``` yaml
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:

  - name: ADD POOL MEMBERS
    bigip_pool_member:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      state: "present"
      name: "{{item}}"
      host: "{{item}}"
      port: "80"
      pool: "http_pool"
      validate_certs: "no"
    loop:
      - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
      - "{{ hostvars[groups['webservers'][1]].ansible_host }}"
```

- `name: ADD POOL MEMBERS` is a user defined description that will display in the terminal output.
- `bigip_pool_member:` tells the task which module to use.
- The `server: "{{private_ip}}"` parameter tells the module to connect to the F5 BIG-IP IP address, which is stored as a variable `private_ip` in inventory
- The `user: "{{ansible_user}}"` parameter tells the module the username to login to the F5 BIG-IP device with
- The`password: "{{ansible_ssh_pass}}"` parameter tells the module the password to login to the F5 BIG-IP device with
- The `server_port: 8443` parameter tells the module the port to connect to the F5 BIG-IP device with
- The `server_port: 8443` parameter tells the module the port to connect to the F5 BIG-IP device withg
- The `name: "http_pool"` parameter tells the module to create a pool named http_pool
- The `lb_method: "round-robin"` parameter tells the module the load balancing method will be round-robin.  A full list of methods can be found on the documentation page for bigip_pool.
- The `monitors: "/Common/http"` parameter tells the module the that the http_pool will only look at http traffic.
- The `monitor_type: "and_list"` ensures that all monitors are checked.
- The `validate_certs: "no"` parameter tells the module to not validate SSL certificates.  This is just used for demonstration purposes since this is a lab.

## Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-pool-members.yml
```

# Playbook Output

The output will look as follows.

```yaml
[student1@ansible ~]$ ansible-playbook bigip-pool-members.yml

PLAY [SIMPLE DEBUG PLAYBOOK] *******************************************************************************

TASK [DISPLAY TEST_VARIABLE] *******************************************************************************
ok: [localhost] => {
    "test_variable": "my test variable"
}

PLAY RECAP *************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0
```

# Solution
The finished Ansible Playbook is provided here for an Answer key.

```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:

  - name: ADD POOL MEMBERS
    bigip_pool_member:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      state: "present"
      name: "{{item}}"
      host: "{{item}}"
      port: "80"
      pool: "http_pool"
      validate_certs: "no"
    loop:
      - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
      - "{{ hostvars[groups['webservers'][1]].ansible_host }}"
```

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
