# Exercise 2 - First Ansible Playbook

**Read this in other languages**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
   * [Step 1 - Examine Ansible Playbook](#step-1---examine-ansible-playbook)
   * [Step 2 - Execute Ansible Playbook](#step-2---execute-ansible-playbook)
   * [Step 3 - Verify configuration on router](#step-3---verify-configuration-on-router)
   * [Step 4 - Validate idempotency](#step-4---validate-idempotency)
   * [Step 5 - Modify Ansible Playbook](#step-5---modify-ansible-playbook)
   * [Step 6 - Use check mode](#step-6---use-check-mode)
   * [Step 7 - Verify configuration is not present](#step-7---verify-configuration-is-not-present)
   * [Step 8 - Re-run the Ansible Playbook](#step-8---re-run-the-ansible-playbook)
   * [Step 9 - Verify configuration is applied](#step-9---verify-configuration-is-applied)
* [Takeaways](#takeaways)
* [Solution](#solution)
* [Complete](#complete)

## Objective

Use Ansible to update the configuration of routers.  This exercise will not create an Ansible Playbook, but use an existing one that has been provided.

This exercise will cover:

* examining an existing Ansible Playbook
* executing an Ansible Playbook on the command line using the `ansible-navigator` command
* check mode (the `--check` parameter)
* verbose mode (the `--verbose` or `-v` parameter)

## Guide

### Step 1 - Examine Ansible Playbook

Navigate to the `network-workshop` directory if you are not already there.

```bash
[student1@ansible ~]$ cd ~/network-workshop/
[student1@ansible network-workshop]$
[student1@ansible network-workshop]$ pwd
/home/student1/network-workshop
```

Examine the provided Ansible Playbook named `playbook.yml`.  Either open the file in Visual Studio Code or `cat` the file:

```yaml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      cisco.ios.config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
```

* `cat` - Linux command allowing us to view file contents
* `playbook.yml` - provided Ansible Playbook

We will explore in detail the components of an Ansible Playbook in the next exercise.  It is suffice for now to see that this playbook will run two Cisco IOS-XE commands

```sh
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Step 2 - Execute Ansible Playbook

Run the playbook using the `ansible-navigator` command.  The full command is:
```ansible-navigator run playbook.yml --mode stdout```

```bash
[student1@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[student1@ansible-1 network-workshop]$
```

* `--mode stdout` - By default `ansible-navigator` will run in interactive mode.  The default behavior can be modified by modifying the `ansible-navigator.yml`.  As playbooks get longer and involve multiple hosts the interactive mode allows you to "zoom in" on data in real-time, filter it, and navigate between various Ansible components.  Since this task only ran one task on one host the `stdout` is sufficient.

### Step 3 - Verify configuration on router

Verify that the Ansible Playbook worked.  Login to `rtr1` and check the running configuration on the Cisco IOS-XE device.

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Step 4 - Validate idempotency

The `cisco.ios.config` module is idempotent. This means, a configuration change is pushed to the device if and only if that configuration does not exist on the end hosts.

> Need help with Ansible Automation terminology?  Check out the [glossary here](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html) for more information on terms like idempotency.

To validate the concept of idempotency, re-run the playbook:

```bash
[student1@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
ok: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

> Note: See that the **changed** parameter in the **PLAY RECAP** indicates 0 changes.

Re-running the Ansible Playbook multiple times will result in the same exact output, with **ok=1** and **change=0**.  Unless another operator or process removes or modifies the existing configuration on rtr1, this Ansible Playbook will just keep reporting **ok=1** indicating that the configuration already exists and is configured correctly on the network device.

### Step 5 - Modify Ansible Playbook

Now update the task to add one more SNMP RO community string named `ansible-test`.

```sh
snmp-server community ansible-test RO
```

Use Visual Studio Code to open the `playbook.yml` file to add the command:


The Ansible Playbook will now look like this:

```yaml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      cisco.ios.config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO
```

Make sure to save the `playbook.yml` with the change.

### Step 6 - Use check mode

This time however, instead of running the playbook to push the change to the device, execute it using the `--check` flag in combination with the `-v` or verbose mode flag:

```bash
[student1@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout --check -v
Using /etc/ansible/ansible.cfg as config file

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1] => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python"}, "banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"], "warnings": ["To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device"]}

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The `--check` mode in combination with the `--verbose` flag will display the exact changes that will be deployed to the end device without actually pushing the change. This is a great technique to validate the changes you are about to push to a device before pushing it.

### Step 7 - Verify configuration is not present

Verify that the Ansible Playbook did not apply the `ansible-test` community.  Login to `rtr1` and check the running configuration on the Cisco IOS-XE device.

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Step 8 - Re-run the Ansible Playbook

Finally re-run this playbook again without the `-v` or `--check` flag to push the changes.

```bash
[student1@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Step 9 - Verify configuration is applied

Verify that the Ansible Playbook applied **ansible-test** community.  Login to `rtr1` and check the running configuration on the Cisco IOS-XE device.

```bash
[student1@ansible network-workshop]$ ssh rtr1

rtr1#sh run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
snmp-server community ansible-test RO
```

## Takeaways

* the **config** (e.g. cisco.ios.config) modules are idempotent, meaning they are stateful
* **check mode** ensures the Ansible Playbook does not make any changes on the remote systems
* **verbose mode** allows us to see more output to the terminal window, including which commands would be applied
* This Ansible Playbook could be scheduled in **Automation controller** to enforce the configuration.  For example this could mean the Ansible Playbook could be run once a day for a particular network.  In combination with **check mode** this could just be a read only Ansible Playbook that sees and reports if configuration is missing or modified on the network.

## Solution

The finished Ansible Playbook is provided here for an answer key: [playbook.yml](../playbook.yml).

## Complete

You have completed lab exercise 2

---
[Previous Exercise](../1-explore/README.md) | [Next Exercise](../3-facts/README.md)

[Click here to return to the Ansible Network Automation Workshop](../README.md)
