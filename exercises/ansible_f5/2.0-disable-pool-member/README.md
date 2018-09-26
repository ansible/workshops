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

Using your text editor of choice create a new file called `disable-pool-member.yml`.

```
[student1@ansible ~]$ nano disable-pool-member.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Enter the following play definition into `disable-pool-member.yml`:

``` yaml
---

- name:  Get Status
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
   pool_path: '/Common/http_pool'
   pool_member: 'we can pass this as an extra var'
```

## Step 3

Next, add a tasks section and create a task for the objective listed above:

  - Retrieve Facts from BIG-IP for the pool /Common/http_pool

HINT: <span style="background-color: #000000">Try using the bigip_facts module from [Exercise 1.1](../1.1-get-facts)</span>

## Step 4

Next, add a task for the objective listed above:

  - Display pool member status to the terminal window

HINT: <span style="background-color: #000000">
Remember to use the `register` keyword and the [debug module](https://docs.ansible.com/ansible/latest/modules/debug_module.html)</span>

## Step 5

Next, add a task for the objective listed above:

  - Store the pool members as a fact

HINT: <span style="background-color: #000000">
An easy way to set fact variables within a Playbook dynamically is using the [set_fact module](https://docs.ansible.com/ansible/latest/modules/set_fact_module.html)</span>

## Step 6

Next, add a task for the objective listed above:

  - Display pool member IP and port information to the terminal window

HINT: <span style="background-color: #000000">
Remember to use the `register` keyword and the [debug module](https://docs.ansible.com/ansible/latest/modules/debug_module.html)</span>

## Step 7

Next, add a task for the objective listed above:

  - Display pool member IP and port information to the terminal window

HINT: <span style="background-color: #000000">
Remember the [bigip_pool_member module](https://docs.ansible.com/ansible/latest/modules/bigip_pool_member_module.html), can refer to [Exercise 1.2](../1.2-add-node).  Also remember to look at the state parameter.</span>

## Step 8
Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ disable-pool-member.yml -e pool_member="YOUR MEMBER"
```
# Playbook Output

The output will look as follows.

```yaml
[student1@ansible ~]$ ansible-playbook disable-pool-member.yml

PLAY [SIMPLE DEBUG PLAYBOOK] *******************************************************************************

TASK [DISPLAY TEST_VARIABLE] *******************************************************************************
ok: [localhost] => {
    "test_variable": "my test variable"
}

PLAY RECAP *************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0
```
> Notice that the names you gave the play and task appear in this output. This is especially important when you have longer playbooks that include multiple tasks.

# Solution
The solution will be provided by the instructor if you are stuck.

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
