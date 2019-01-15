# Exercise 1: Using the bigip_facts module

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)
- [Going Further](#going-further)

# Objective

Demonstrate use of the [BIG-IP Facts module](https://docs.ansible.com/ansible/latest/modules/bigip_facts_module.html) to grab facts (useful information) from a F5 BIG-IP device and display them to the terminal window using the [debug module](https://docs.ansible.com/ansible/latest/modules/debug_module.html).  

# Guide

## Step 1:

Using your text editor of choice create a new file called `bigip-facts.yml`.

```
[student1@ansible ~]$ nano bigip-facts.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format).

Enter the following play definition into `bigip-facts.yml`:

``` yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: no
```

- The `---` at the top of the file indicates that this is a YAML file.
- The `hosts: f5`,  indicates the play is run only on the F5 BIG-IP device
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: no` disables facts gathering.  We are not using any fact variables for this playbook.

## Step 3

Next, add the first `task`. This task will use the `bigip_facts` module to grab useful information from the BIG-IP device.

{% raw %}

``` yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: no


  tasks:

    - name: COLLECT BIG-IP FACTS
      bigip_facts:
        include: system_info
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: 8443
        validate_certs: no
      register: bigip_facts
```

{% endraw %}



>A play is a list of tasks. Tasks and modules have a 1:1 correlation.  Ansible modules are reusable, standalone scripts that can be used by the Ansible API, or by the ansible or ansible-playbook programs. They return information to ansible by printing a JSON string to stdout before exiting.

- `name: COLLECT BIG-IP FACTS` is a user defined description that will display in the terminal output.
- `bigip_facts:` tells the task which module to use.  Everything except `register` is a module parameter defined on the module documentation page.
- The `include: system_info` parameter tells the module only to grab system level information.
- The `server: "{{private_ip}}"` parameter tells the module to connect to the F5 BIG-IP IP address, which is stored as a variable `private_ip` in inventory
- The `user: "{{ansible_user}}"` parameter tells the module the username to login to the F5 BIG-IP device with
- The`password: "{{ansible_ssh_pass}}"` parameter tells the module the password to login to the F5 BIG-IP device with
- The `server_port: 8443` parameter tells the module the port to connect to the F5 BIG-IP device with
- `register: bigip_facts` tells the task to save the output to a variable bigip_facts

## Step 4

Next, add the second `task`. This task will use the `debug` module to print the output from bigip_facts variable we registered the facts to.

{% raw %}

```yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: no


  tasks:

    - name: COLLECT BIG-IP FACTS
      bigip_facts:
        include: system_info
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: 8443
        validate_certs: no
      register: bigip_facts

    - name: COMPLETE BIG-IP SYSTEM INFORMATION
      debug:
        var: bigip_facts
```

{% endraw %}


- The `name: COMPLETE BIG-IP SYSTEM INFORMATION` is a user defined description that will display in the terminal output.
- `debug:` tells the task to use the debug module.
- The `var: bigip_facts` parameter tells the module to display the variable bigip_facts.


## Step 5

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-facts.yml
```

## Step 6

Finally lets add two more tasks to get more specific info from facts gathered.

{% raw %}

```yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: no

  tasks:
    - name: COLLECT BIG-IP FACTS
      bigip_facts:
        include: system_info
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: 8443
        validate_certs: no
      register: bigip_facts

    - name: COMPLETE BIG-IP SYSTEM INFORMATION
      debug:
        var: bigip_facts

    - name: DISPLAY ONLY THE MAC ADDRESS
      debug:
        var: bigip_facts['ansible_facts']['system_info']['base_mac_address']

    - name: DISPLAY ONLY THE VERSION
      debug:
        var: bigip_facts['ansible_facts']['system_info']['product_information']['product_version']
```

{% endraw %}


- `var: bigip_facts['ansible_facts']['system_info']['base_mac_address']` displays the MAC address for the BIG-IP device
- `bigip_facts['ansible_facts']['system_info']['product_information']['product_version']` displays the product version BIG-IP device

>Because the bigip_facts module returns useful information in structured data, it is really easy to grab specific information without using regex or filters.  Fact modules are very powerful tools to grab specific device information that can be used in subsequent tasks, or even used to create dynamic documentation (reports, csv files, markdown).


## Step 7

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-facts.yml
```

# Playbook Output

The output will look as follows.

```yaml
[student1@ansible ~]$ ansible-playbook bigip-facts.yml

PLAY [GRAB F5 FACTS] ***********************************************************

TASK [COLLECT BIG-IP FACTS] ****************************************************
ok: [f5]

TASK [COMPLETE BIG-IP SYSTEM INFORMATION] **************************************
ok: [f5] => {
    "bigip_facts": {
        "ansible_facts": {
            "system_info": {
                "base_mac_address": "0A:D1:27:C1:84:76",
                "blade_temperature": [],
                "chassis_slot_information": [],
                "globally_unique_identifier": "0A:D1:27:C1:84:76",
                "group_id": "DefaultGroup",
                "hardware_information": [
<<output removed for brevity>>

---
TASK [DISPLAY ONLY THE MAC ADDRESS] *******************************************
ok: [f5] => {
    "bigip_facts['ansible_facts']['system_info']['base_mac_address']": "0A:D1:27:C1:84:76"
}

TASK [DISPLAY ONLY THE VERSION] ***********************************************
ok: [f5] => {
    "bigip_facts['ansible_facts']['system_info']['product_information']['product_version']": "13.1.0.2"
}

PLAY RECAP *********************************************************************
f5                         : ok=4    changed=0    unreachable=0    failed=0
```

# Solution

The finished Ansible Playbook is provided here for an Answer key.  Click here for [bigip-facts.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.1-get-facts/bigip-facts.yml).


# Going Further

For this bonus exercise add the `tags: debug` paramteter (at the task level) to the exiting debug task.

```yaml
- name: COMPLETE BIG-IP SYSTEM INFORMATION
  debug:
    var: bigip_facts
  tags: debug
```

Now re-run the playbook with the `--skip-tags-debug` command line option.

```
ansible-playbook bigip-facts.yml --skip-tags=debug
```

The Ansible Playbook will only run three tasks, skipping the `COMPLETE BIG-IP SYSTEM INFORMATION` task.

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
