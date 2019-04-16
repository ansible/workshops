# Exercise 1.4: Adding members to a pool on F5

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

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
      name: "{{hostvars[item].inventory_hostname}}"
      host: "{{hostvars[item].ansible_host}}"
      port: "80"
      pool: "http_pool"
      validate_certs: "no"
    loop: "{{ groups['webservers'] }}"
```


Explanation of each line within the task:
- `name: ADD POOL MEMBERS` is a user defined description that will display in the terminal output.
- `bigip_pool_member:` tells the task which module to use.

Next we have module parameters
- The `server: "{{private_ip}}"` parameter tells the module to connect to the F5 BIG-IP IP address, which is stored as a variable `private_ip` in inventory
- The `user: "{{ansible_user}}"` parameter tells the module the username to login to the F5 BIG-IP device with
- The`password: "{{ansible_ssh_pass}}"` parameter tells the module the password to login to the F5 BIG-IP device with
- The `server_port: 8443` parameter tells the module the port to connect to the F5 BIG-IP device with
- The `state: "present"` parameter tells the module we want this to be added rather than deleted.
- The `name: "{{hostvars[item].inventory_hostname}}"` parameter tells the module to use the `inventory_hostname` as the name (which will be host1 and host2).
- The `host: "{{hostvars[item].ansible_host}}"` parameter tells the module to add a web server IP address already defined in our inventory.
- The `pool: "http_pool"` parameter tells the module to put this node into a pool named http_pool
- The `validate_certs: "no"` parameter tells the module to not validate SSL certificates.  This is just used for demonstration purposes since this is a lab.
Finally there is a loop parameter which is at the task level (it is not a module parameter but a task level parameter:
- `loop:` tells the task to loop over the provided list.  The list in this case is the group webservers which includes two RHEL hosts.

## Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-pool-members.yml
```

# Playbook Output

The output will look as follows.

```yaml
[student1@ansible ~]$ ansible-playbook bigip-pool-members.yml

PLAY [BIG-IP SETUP] ************************************************************

TASK [ADD POOL MEMBERS] ********************************************************
changed: [f5] => (item=host1)
changed: [f5] => (item=host2)

PLAY RECAP *********************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```
# Output parsing

Let's use the bigip_device_facts to collect the pool members on BIG-IP. [JSON query](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#json-query-filter) is a powerful filter that can be used. Please go through before proceeding

```
[student1@ansible ~]$ nano display-pool-members.yml
```

Enter the following:
```
---
- name: "List pool members"
  hosts: lb
  gather_facts: false
  connection: local

  tasks:

  - name: Query BIG-IP facts
    bigip_device_facts:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "8443"
      validate_certs: "no"
      gather_subset:
       - ltm-pools
    register: bigip_device_facts

  - name: "View complete output"
    debug: "msg={{bigip_device_facts}}"
    
  - name: "Show members belonging to pool"
    debug: "msg={{item}}"
    loop: "{{bigip_device_facts.ltm_pools | json_query(query_string)}}"
    vars:
     query_string: "[?name=='http_pool'].members[*].name[]"
```
- `vars:` in the module is defining a variable query_string to be used within the module itself
- `query_String` will have the name of all members from pool name 'http_pool'. query_string is defined to make it easier to read the 
   entire json string

Execute the playbook
```
[student1@ansible ~]$ ansible-playbook display-pool-members.yml
```

Output

```
[student1@ansible ~]$ ansible-playbook display-pool-member.yml

PLAY [List pool members] ************************************************************************************************************************************

TASK [Query BIG-IP facts] ***********************************************************************************************************************************
changed: [f5]

TASK [Show members belonging to pool] ***********************************************************************************************************************
ok: [f5] => (item=host1:80) => {
    "msg": "host1:80"
}
ok: [f5] => (item=host2:80) => {
    "msg": "host2:80"
}

PLAY RECAP **************************************************************************************************************************************************
f5                         : ok=2    changed=1    unreachable=0    failed=0
```

# Solution
The finished Ansible Playbook is provided here for an Answer key.  Click here: [bigip-pool-members.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.4-add-pool-members/bigip-pool-members.yml).

# Verifying the Solution

Login to the F5 with your web browser to see what was configured.  Grab the IP information for the F5 load balancer from the lab_inventory/hosts file, and type it in like so: https://X.X.X.X:8443/

Login information for the BIG-IP:
- username: admin
- password: admin

The pool will now show two members (host1 and host2).  Click on Local Traffic-> then click on Pools.  Click on http_pool to get more granular information.  Click on the Members tab in the middle to list all the Members.
![f5members](poolmembers.png)


You have finished this exercise.  [Click here to return to the lab guide](../README.md)
