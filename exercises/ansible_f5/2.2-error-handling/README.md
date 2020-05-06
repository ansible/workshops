# Exercise 2.2: Using a combination of modules to perform a graceful rollback

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate use of the different modules to perform a rollback of the configuration on the BIG-IP.

# Guide

## Step 1

Using your text editor of choice create a new file called `bigip-error-handling.yml`.

{% raw %}
```
[student1@ansible ~]$ nano bigip-error-handling.yml
```
{% endraw %}

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2

Enter the following play definition into `bigip-error-handling.yml`:

{% raw %}
``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

```
{% endraw %}

- The `---` at the top of the file indicates that this is a YAML file.
- The `hosts: f5`,  indicates the play is run only on the F5 BIG-IP device
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: false` disables facts gathering.  We are not using any fact variables for this playbook.

## Step 3

Add a tasks section with a set_fact for setting the provider values

{% raw %}
```
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

tasks:
    - name: Setup provider
      set_fact:
       provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"
```
{% endraw %}

## Step 4

Next, add the `block` stanza and the first `task`. The first task will be the bigip_node as performed in [Exercise 1.2 - Adding nodes to F5 BIG-IP](../1.2-add-node/README.md).

{% raw %}
``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
  - name: Setup provider
      set_fact:
       provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

  - name: Setup and graceful rollback BIG-IP configuration
    block:
      - name: CREATE NODES
        bigip_node:
         provider: "{{provider}}"
         host: "{{hostvars[item].ansible_host}}"
         name: "{{hostvars[item].inventory_hostname}}"
        loop: "{{ groups['web'] }}"
```

{% endraw %}

## Step 5

Next, add the second task for bigip_pool as demonstrated in [Exercise 1.3 - Adding a load balancing pool](../1.3-add-pool/README.md).

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
       provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"
```
{% endraw %}

## Step 6

Next, add the third task.  For the third task use the bigip_pool_member as demonstrated in [Exercise 1.4 - Adding members to a pool](../1.4-add-pool-members/README.md).

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
       provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

        - name: ADD POOL MEMBERS
          bigip_pool_member:
           provider: "{{provider}}"
           state: "present"
           name: "{{hostvars[item].inventory_hostname}}"
           host: "{{hostvars[item].ansible_host}}"
           port: "80"
           pool: "http_pool"
          loop: "{{ groups['web'] }}"
```
{% endraw %}

## Step 7

Next, add the fourth task.  For the fourth task use the bigip_virtual_server as demonstrated in [Exercise 1.5 - Adding a virtual server](../1.5-add-virtual-server/README.md).

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
       provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

        - name: ADD POOL MEMBERS
          bigip_pool_member:
           provider: "{{provider}}"
           state: "present"
           name: "{{hostvars[item].inventory_hostname}}"
           host: "{{hostvars[item].ansible_host}}"
           port: "80"
           pool: "http_pool"
          loop: "{{ groups['web'] }}"

        - name: ADD VIRTUAL SERVER
          bigip_virtual_server:
           provider: "{{provider}}"
           name: "vip"
           destination: "{{private_ip}}"
           port: "443"
           enabled_vlans: "all"
           all_profiles: ['http','clientssl','oneconnect']
           pool: "http_pool"
           snat: "Automap1"
```
{% endraw %}

## Step 7

Next, add the **rescue** stanza.  The tasks under the `rescue` stanza will be identical to [Exercise 2.1 - Deleting F5 BIG-IP Configuration](../2.1-delete-configuration/README.md).  The bigip_pool_member task does not need to re-enterered since by deleting the nodes and pool will remove all configuration. If any task within the **block** fails, the **rescue** stanza will execute in order.  The VIP, pool, and nodes will be removed gracefully.

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
       provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

        - name: ADD POOL MEMBERS
          bigip_pool_member:
            provider: "{{provider}}"
            state: "present"
            name: "{{hostvars[item].inventory_hostname}}"
            host: "{{hostvars[item].ansible_host}}"
            port: "80"
            pool: "http_pool"
          loop: "{{ groups['web'] }}"

        - name: ADD VIRTUAL SERVER
          bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            destination: "{{private_ip}}"
            port: "443"
            enabled_vlans: "all"
            all_profiles: ['http','clientssl','oneconnect']
            pool: "http_pool"
            snat: "Automap1"

      rescue:

        - name: DELETE VIRTUAL SERVER
          bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            state: absent

        - name: DELETE POOL
          bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            state: absent

        - name: DELETE NODES
          bigip_node:
            provider: "{{provider}}"
            name: "{{hostvars[item].inventory_hostname}}"
            state: absent
          loop: "{{ groups['web'] }}"
```
{% endraw %}

## Step 8

Finally add the **always** to save the running configuration.

{% raw %}
```yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false

  tasks:
    - name: Setup provider
      set_fact:
       provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: "8443"
        validate_certs: "no"

    - name: SETUP AND GRACEFUL ROLLBACK BIG-IP CONFIGURATION
      block:
        - name: CREATE NODES
          bigip_node:
            provider: "{{provider}}"
            host: "{{hostvars[item].ansible_host}}"
            name: "{{hostvars[item].inventory_hostname}}"
          loop: "{{ groups['web'] }}"

        - name: CREATE POOL
          bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            lb_method: "round-robin"
            monitors: "/Common/http"
            monitor_type: "and_list"

        - name: ADD POOL MEMBERS
          bigip_pool_member:
            provider: "{{provider}}"
            state: "present"
            name: "{{hostvars[item].inventory_hostname}}"
            host: "{{hostvars[item].ansible_host}}"
            port: "80"
            pool: "http_pool"
          loop: "{{ groups['web'] }}"

        - name: ADD VIRTUAL SERVER
          bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            destination: "{{private_ip}}"
            port: "443"
            enabled_vlans: "all"
            all_profiles: ['http','clientssl','oneconnect']
            pool: "http_pool"
            snat: "Automap1"

      rescue:

        - name: DELETE VIRTUAL SERVER
          bigip_virtual_server:
            provider: "{{provider}}"
            name: "vip"
            state: absent

        - name: DELETE POOL
          bigip_pool:
            provider: "{{provider}}"
            name: "http_pool"
            state: absent

        - name: DELETE NODES
          bigip_node:
            provider: "{{provider}}"
            name: "{{hostvars[item].inventory_hostname}}"
            state: absent
          loop: "{{ groups['web'] }}"
      always:
        - name: SAVE RUNNING CONFIGURATION
          bigip_config:
            provider: "{{provider}}"
            save: yes
```
{% endraw %}

The above playbook will try and configure the Virtual Server, Pool and Nodes but since the snat value is provided as 'Automap1' the addition of virtual server will fail and the 'rescue' block will be run

## Step 9

Run the playbook - exit back into the command line of the control host and execute the following:

{% raw %}
```
[student1@ansible ~]$ ansible-playbook bigip-error-handling.yml
```
{% endraw %}

# Playbook Output

{% raw %}
```
[student1@ansible ~]$ ansible-playbook bigip-error-handling.yml

[student1@ansible ~]$ ansible-playbook bigip-error-handling.yml

PLAY [BIG-IP SETUP] ****************************************************************************************************

TASK [Setup provider] **************************************************************************************************
ok: [f5]

TASK [CREATE NODES] *****************************************************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [CREATE POOL] *******************************************************************************************************
changed: [f5]

TASK [ADD POOL MEMBERS] **************************************************************************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [ADD VIRTUAL SERVER] ***************************************************************************************************************************
fatal: [f5]: FAILED! => {"changed": false, "msg": "0107163f:3: Pool (/Common/Automap1) of type (snatpool) doesn't exist."}

TASK [DELETE VIRTUAL SERVER] **************************************************************************************************************************
ok: [f5]

TASK [DELETE POOL] **************************************************************************************************************************
changed: [f5]

TASK [DELETE NODES] **************************************************************************************************************************
changed: [f5] => (item=node1)
changed: [f5] => (item=node2)

TASK [SAVE RUNNING CONFIGURATION] ***************************************************************************************************************************
changed: [f5]

PLAY RECAP *****************************************************************************************************************
f5                         : ok=8    changed=6    unreachable=0    failed=1

```
{% endraw %}
# Solution

The finished Ansible Playbook is provided here for an Answer key.  Click here: [bigip-error-handling.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/2.2-error-handling/bigip-error-handling.yml).

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
