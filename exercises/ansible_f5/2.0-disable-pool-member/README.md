# Exercise 2.0 - Disabling a pool member

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

For this last exercise instead of prescriptive step-by-step walkthrough a framework of objectives with hints for each step will be provided.  

Demonstrate the removal of a node from the pool.  Build a Playbook that:
  - Retrieve Facts from BIG-IP for the pools present on the BIG-IP (in our example only one pool is present)
  - Display pools available
  - Store the pool name as a fact
  - Display pool member IP and port information to the terminal window
  - Prompt the user to disable a particular member or disable all members of the pool
  - Forces the appropriate pool members offline

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

- name:  Disabling a pool member
  hosts: f5
  connection: local
  gather_facts: false

```
## Step 3

Add a task to set a fact for the provider. Once you set the provider you can re-use this key in future tasks instead of giving the server/user/password/server_port and validate_certs info to each task. 

```
---
- name: "Disabling a pool member"
  hosts: lb
  gather_facts: false
  connection: local

  tasks:
  - name: Setup provider
    set_fact:
     provider:
      server: "{{private_ip}}"
      user: "{{ansible_user}}"
      password: "{{ansible_ssh_pass}}"
      server_port: "443"
      validate_certs: "no"
```

Now in the next task you can use provider as follows:

```
bigip_device_facts:
  provider: "{{provider}}"
  gather-subset:
    ltm-pools
```
You DO NOT need to pass the server_ip/user/password etc. for each module going forward

## Step 5

Next, add a tasks section and create a task for the objective listed above:

  - Retrieve Facts from BIG-IP for the subset ltm-pools

HINT: <span style="background-color: #000000;a: #000000">Try using the bigip_device_facts module from <a href="../1.1-get-facts" style="color: #000000">Exercise 1.1</a></span>

## Step 6

Next, add a task for the objective listed above:

  - Display the pool information to the terminal window

HINT: <span style="background-color: #000000">
Remember to use the `register` keyword and the <a href="https://docs.ansible.com/ansible/latest/modules/debug_module.html" style="color: #000000">debug module</a></span>

## Step 7

Next, add a task for the objective listed above:

  - Store the pool name as a fact

HINT: <span style="background-color: #000000">
An easy way to set fact variables within a Playbook dynamically is using the <a href="https://docs.ansible.com/ansible/latest/modules/set_fact_module.html" style="color: #000000">set_fact module</a></span>

## Step 8

Next, add a task for the objective listed above:

  - Display members belonging to the pool

HINT: <span style="background-color: #000000">
Remember to use the `register` keyword and the <a href="https://docs.ansible.com/ansible/latest/modules/debug_module.html" style="color: #000000">debug</a></span>

## Step 9

Next, add a task for the objective listed above:

  - Prompt the user to enter a Host:Port to disable a particular member or 'all' to disable all members

HINT: <span style="background-color: #000000">
Remember the <a href="https://docs.ansible.com/ansible/latest/user_guide/playbooks_prompts.html" style="color: #000000">prompts</a> module</a></span>

## Step 10
Next, add a task for the objective listed above:

  - Read the prompt information and disable all members or a single member based on the input from the user
  
HINT: <span style="background-color: #000000">
Remember to use <a href="https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html"style="color: #000000">'when' and 'loops' </a></span>
  
## Step 10
Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook disable-pool-member.yml
```

# Playbook Output

The output will look as follows.

```yaml
<< TO BE ADDED>>
```

# Solution
The solution will be provided by the instructor if you are stuck.  The GUI should show something similar to the following with a black diamond indicating the specified node was forced offline.

![f5bigip-gui](f5bigip-gui.png)

--
You have finished this exercise.  [Click here to return to the lab guide](../README.md)
