# Exercise 2 - First Ansible Playbook

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Takeaways](#takeaways)
- [Solution](#solution)

# Objective

Use Ansible to update the configuration of routers.  This exercise will not create an Ansible Playbook, but use an existing provided one.

This exercise will cover
- examining an existing Ansible Playbook
- executing an Ansible Playbook on the command line using the `ansible-playbook` command
- check mode (the `--check` parameter)
- verbose mode (the `--verbose` or `-v` parameter)

# Guide

#### Step 1

Navigate to the `network-workshop` directory if you are not already there.

```bash
[student1@ansible ~]$ cd ~/network-workshop/
[student1@ansible network-workshop]$
[student1@ansible network-workshop]$ pwd
/home/student1/network-workshop
```

Examine the provided Ansible Playbook named `playbook.yml`.  Feel free to use your text editor of choice to open the file.  The sample below will use the Linux `cat` command.

```bash
[student1@ansible network-workshop]$ cat playbook.yml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
```

 - `cat` - Linux command allowing us to view file contents
 - `playbook.yml` - provided Ansible Playbook

We will explore in detail the components of an Ansible Playbook in the next exercise.  It is suffice for now to see that this playbook will run two Cisco IOS-XE commands

```
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

#### Step 3

Run the playbook using the `ansible-playbook` command:

```bash
[student1@ansible network-workshop]$ ansible-playbook playbook.yml

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Step 4

Verify that the Ansible Playbook worked.  Login to `rtr1` and check the running configuration on the Cisco IOS-XE device.

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```


#### Step 5

The `ios_config` module is idempotent. This means, a configuration change is pushed to the device if and only if that configuration does not exist on the end hosts.

>Need help with Ansible Automation terminology?  Check out the [glossary here](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html) for more information on terms like idempotency.

To validate the concept of idempotency, re-run the playbook:

```bash
[student1@ansible network-workshop]$  ansible-playbook playbook.yml

PLAY [snmp ro/rw string configuration] **************************************************************************************

TASK [ensure that the desired snmp strings are present] *********************************************************************
ok: [rtr1]

PLAY RECAP ******************************************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[student1@ansible network-workshop]$
```

> Note: See that the **changed** parameter in the **PLAY RECAP** indicates 0 changes.

Re-running the Ansible Playbook multiple times will result in the same exact output, with **ok=1** and **change=0**.  Unless another operator or process removes or modifies the existing configuration on rtr1, this Ansible Playbook will just keep reporting **ok=1** indicating that the configuration already exists and is configured correctly on the network device.  


#### Step 6

Now update the task to add one more SNMP RO community string named `ansible-test`.  

```
snmp-server community ansible-test RO
```

Use the text editor of your choice to open the `playbook.yml` file to add the command:

```bash
[student1@ansible network-workshop]$ nano playbook.yml
```

The Ansible Playbook will now look like this:

``` yaml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO
```

#### Step 7

This time however, instead of running the playbook to push the change to the device, execute it using the `--check` flag in combination with the `-v` or verbose mode flag:


```bash
[student1@ansible network-workshop]$ ansible-playbook playbook.yml --verbose --check
Using /home/student1/.ansible.cfg as config file

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1] => changed=true
  ansible_facts:
    discovered_interpreter_python: /usr/bin/python
  banners: {}
  commands:
  - snmp-server community ansible-test RO
  updates:
  - snmp-server community ansible-test RO

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The `--check` mode in combination with the `--verbose` flag will display the exact changes that will be deployed to the end device without actually pushing the change. This is a great technique to validate the changes you are about to push to a device before pushing it.

#### Step 8

Verify that the Ansible Playbook did not apply the `ansible-test` community.  Login to `rtr1` and check the running configuration on the Cisco IOS-XE device.

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```


#### Step 9

Finally re-run this playbook again without the `-v` or `--check` flag to push the changes.

```bash
[student1@ansible network-workshop]$ ansible-playbook playbook.yml

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP ******************************************************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Step 10

Verify that the Ansible Playbook applied `ansible-test` community.  Login to `rtr1` and check the running configuration on the Cisco IOS-XE device.

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#sh run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
snmp-server community ansible-test RO
```

# Takeaways

- the ***os_config** (e.g. ios_config) modules are idempotent, meaning they are stateful
- **check mode** ensures the Ansible Playbook does not make any changes on the remote systems
- **verbose mode** allows us to see more output to the terminal window, including which commands would be applied
- This Ansible Playbook could be scheduled in **Red Hat Ansible Tower** to enforce the configuration.  For example this could mean the Ansible Playbook could be run once a day for a particular network.  In combination with **check mode** this could just be a read only Ansible Playbook that sees and reports if configuration is missing or modified on the network.

# Solution

The finished Ansible Playbook is provided here for an answer key: [playbook.yml](../playbook.yml).

---

# Complete

You have completed lab exercise 2

[Click here to return to the Ansible Network Automation Workshop](../README.md)
