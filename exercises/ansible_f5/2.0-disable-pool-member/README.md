# Exercise 2.0 - Disabling a pool member

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

For this last exercise instead of prescriptive step-by-step walkthrough a framework of objectives with hints for each step will be provided.  

Demonstrate the removal of a node from the pool.  Build a Playbook that:
  - Retrieve Facts from BIG-IP for the pool /Common/http_pool
  - Display pool member status to the terminal window
  - Store the pool members as a fact
  - Display pool member IP and port information to the terminal window
  - Forces a pool member offline

# Guide

## Step 1:
#### At this point your BIG-IP will have no configuraton if you sucessfully ran exercises 1.6 and 1.7
#### Before running this exercise please ensure that you have working pool members by running exercises 1.2, 1.3, and 1.4

Moving to the exercise:

Using your text editor of choice create a new file called `disable-pool-member.yml`.

```
[student1@ansible ~]$ nano disable-pool-member.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Enter the following play definition into `disable-pool-member.yml`:

``` yaml
---

- name:  Disabling a pool member
  hosts: f5
  connection: local
  gather_facts: false

  vars:
   pool_path: '/Common/http_pool'
   pool_member: 'we can pass this as an extra var'
```

## Step 3

Next, add a tasks section and create a task for the objective listed above:

  - Retrieve Facts from BIG-IP for the pool /Common/http_pool

HINT: <span style="background-color: #000000;a: #000000">Try using the bigip_facts module from <a href="../1.1-get-facts" style="color: #000000">Exercise 1.1</a></span>

## Step 4

Next, add a task for the objective listed above:

  - Display pool member status to the terminal window

HINT: <span style="background-color: #000000">
Remember to use the `register` keyword and the <a href="https://docs.ansible.com/ansible/latest/modules/debug_module.html" style="color: #000000">debug module</a></span>

## Step 5

Next, add a task for the objective listed above:

  - Store the pool members as a fact

HINT: <span style="background-color: #000000">
An easy way to set fact variables within a Playbook dynamically is using the <a href="https://docs.ansible.com/ansible/latest/modules/set_fact_module.html" style="color: #000000">set_fact module</a></span>

## Step 6

Next, add a task for the objective listed above:

  - Display pool member IP and port information to the terminal window

HINT: <span style="background-color: #000000">
Remember to use the `register` keyword and the <a href="https://docs.ansible.com/ansible/latest/modules/debug_module.html" style="color: #000000">debug</a></span>

## Step 7

Next, add a task for the objective listed above:

  - Display pool member IP and port information to the terminal window

HINT: <span style="background-color: #000000">
Remember the <a href="https://docs.ansible.com/ansible/latest/modules/bigip_pool_member_module.html" style="color: #000000">bigip_pool_member</a> module, can refer to <a href="../1.2-add-node" style="color: #000000">Exercise 1.2</a>.  Also remember to look at the state parameter.</span>

## Step 8
Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook disable-pool-member.yml -e "pool_member=host1"
```

# Playbook Output

The output will look as follows.

```yaml
PLAY [Get Status] **************************************************************

TASK [Query BIG-IP for Pool "/Common/http_pool" facts] *************************
ok: [f5]

TASK [Display pool member status] **********************************************
ok: [f5] => {
    "ansible_facts.pool[pool_path].monitor_instance": [
        {
            "enabled_state": 1,
            "instance": {
                "instance_definition": {
                    "address_type": "ATYPE_EXPLICIT_ADDRESS_EXPLICIT_PORT",
                    "ipport": {
                        "address": "18.208.130.134",
                        "port": 80
                    }
                },
                "template_name": "/Common/http"
            },
            "instance_state": "INSTANCE_STATE_UP"
        },
        {
            "enabled_state": 1,
            "instance": {
                "instance_definition": {
                    "address_type": "ATYPE_EXPLICIT_ADDRESS_EXPLICIT_PORT",
                    "ipport": {
                        "address": "34.224.26.74",
                        "port": 80
                    }
                },
                "template_name": "/Common/http"
            },
            "instance_state": "INSTANCE_STATE_UP"
        }
    ]
}

TASK [Get all the members for pool "/Common/http_pool" and store in a variable]
ok: [f5]

TASK [Display pool members ip:port information] ********************************
ok: [f5] => (item={u'port': 80, u'address': u'/Common/host1'}) => {
    "msg": "/Common/host1"
}
ok: [f5] => (item={u'port': 80, u'address': u'/Common/host2'}) => {
    "msg": "/Common/host2"
}

TASK [Force pool member offline] ***********************************************
changed: [f5] => (item={u'port': 80, u'address': u'/Common/host1'})
skipping: [f5] => (item={u'port': 80, u'address': u'/Common/host2'})

PLAY RECAP *********************************************************************
f5                         : ok=5    changed=1    unreachable=0    failed=0
```

# Solution
The solution will be provided by the instructor if you are stuck.  The GUI should show something similar to the following with a black diamond indicating the specified node was forced offline.

![f5bigip-gui](f5bigip-gui.png)

--
You have finished this exercise.  [Click here to return to the lab guide](../README.md)
