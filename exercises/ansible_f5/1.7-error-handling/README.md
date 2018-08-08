# Exercise 7: Using a combination of modules to perform a graceful rollback

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

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
- `gather_facts: false` disables facts gathering.  We are not using any fact variables for this playbook.

## Step 3

Next, add the `block` stanza and the first `task`. The first task will be the bigip_node as performed in exercise 1.2.

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
```

## Step 4

Next, add the second task for bigip_pool as demonstrated in [exercise 1.3](../1.3-add-pool/README.md).

```yaml
 - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
   block:
   - name: Create nodes
     bigip_node:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      host: "{{item}}"
      name: "{{item}}"
      validate_certs: "no"
     loop:
      - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
      - "{{ hostvars[groups['webservers'][1]].ansible_host }}"

   - name: CREATE POOL
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
```

## Step 5

Next, add the third task.  For the third task use the bigip_pool_member as demonstrated in [exercise 1.4](../1.4-add-pool-members/README.md).

```yaml
 - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
   block:
   - name: Create nodes
     bigip_node:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      host: "{{item}}"
      name: "{{item}}"
      validate_certs: "no"
     loop:
      - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
      - "{{ hostvars[groups['webservers'][1]].ansible_host }}"

   - name: CREATE POOL
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

## Step 6

Next, add the fourth task.  For the fourth task use the bigip_virtual_server as demonstrated in [exercise 1.5](../1.5-add-virtual-server/README.md).


```yaml
 - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
   block:
   - name: Create nodes
     bigip_node:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      host: "{{item}}"
      name: "{{item}}"
      validate_certs: "no"
     loop:
      - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
      - "{{ hostvars[groups['webservers'][1]].ansible_host }}"

   - name: CREATE POOL
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

## Step 7

Next, add the **rescue** stanza.  Re-enter all the bigip_node, bigip_pool and bigip_virtual_server tasks in reverse order.  The bigip_pool_member task does not need to re-enterered since by deleting the nodes and pool will remove all configuration.  For each task within the **rescue** stanza, use the paramter `state: absent`.  If any task within the **block** fails, the **rescue** stanza will execute in order.  The VIP, pool, and nodes will be removed gracefully.


```yaml
 - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
   block:
   - name: Create nodes
     bigip_node:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      host: "{{item}}"
      name: "{{item}}"
      validate_certs: "no"
     loop:
      - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
      - "{{ hostvars[groups['webservers'][1]].ansible_host }}"

   - name: CREATE POOL
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

    rescue:

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
       name: "{{item}}"
       state: absent
       validate_certs: "no"
      loop:
       - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
       - "{{ hostvars[groups['webservers'][1]].ansible_host }}"
```

## Step 8

Finally add the **always** to print out a debug message.


```yaml
 - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
   block:
   - name: Create nodes
     bigip_node:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      host: "{{item}}"
      name: "{{item}}"
      validate_certs: "no"
     loop:
      - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
      - "{{ hostvars[groups['webservers'][1]].ansible_host }}"

   - name: CREATE POOL
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

    rescue:

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
       name: "{{item}}"
       state: absent
       validate_certs: "no"
      loop:
       - "{{ hostvars[groups['webservers'][0]].ansible_host }}"
       - "{{ hostvars[groups['webservers'][1]].ansible_host }}"
    always:
    - debug: msg="Executed rollback playbook"
```
The above playbook will try and configure the Virtual Server, Pool and Nodes but since the snat value is provided as 'Automap1' the addition of virtual server will fail and the 'rescue' block will be run

## Step 9

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-error-handling.yml
```

# Playbook Output

```
[student1@ansible]$ ansible-playbook bigip-error-handling.yml

PLAY [BIG-IP SETUP] ************************************************************

TASK [Create nodes] ************************************************************
failed: [f5] (item=107.23.182.171) => {"changed": false, "item": "107.23.182.171", "msg": "400 Unexpected Error: Bad Request for uri: https://172.16.118.144:8443/mgmt/tm/ltm/node/\nText: u'{\"code\":400,\"message\":\"0107176c:3: Invalid Node, the IP address 107.23.182.171 already exists.\",\"errorStack\":[],\"apiError\":3}'"}
failed: [f5] (item=34.224.38.246) => {"changed": false, "item": "34.224.38.246", "msg": "400 Unexpected Error: Bad Request for uri: https://172.16.118.144:8443/mgmt/tm/ltm/node/\nText: u'{\"code\":400,\"message\":\"0107176c:3: Invalid Node, the IP address 34.224.38.246 already exists.\",\"errorStack\":[],\"apiError\":3}'"}

TASK [DELETE VIRTUAL SERVER] ***************************************************
ok: [f5]

TASK [DELETE POOL] *************************************************************
ok: [f5]

TASK [DELETE NODES] ************************************************************
ok: [f5] => (item=107.23.182.171)
ok: [f5] => (item=34.224.38.246)

TASK [debug] *******************************************************************
ok: [f5] => {
    "msg": "Executed rollback playbook"
}

PLAY RECAP *********************************************************************
f5                         : ok=4    changed=0    unreachable=0    failed=1
```
# Solution
The finished Ansible Playbook is provided here for an Answer key.  Click here: [bigip-error-handling.yml](bigip-error-handling.yml).

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
