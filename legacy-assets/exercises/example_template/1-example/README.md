# Exercise 1: Using the debug module

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate the use of the [debug module](https://docs.ansible.com/ansible/latest/modules/debug_module.html) to display a variable to the terminal window.

# Guide

## Step 1:

Using your text editor of choice create a new file called `debug.yml`.

```
[student1@ansible ~]$ nano debug.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format).

Enter the following play definition into `debug.yml`:

``` yaml
---
- name: SIMPLE DEBUG PLAYBOOK
  hosts: localhost
  connection: local
  gather_facts: no
```

- The `---` at the top of the file indicates that this is a YAML file.
- Always give your playbooks and tasks good, descriptive names. These names form part of the playbook output.
- The `hosts: localhost`,  indicates the play is run only on the Ansible control node
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: no` disables facts gathering.  We are not using any fact variables for this playbook.

> One of the most common errors in YAML files is caused by incorrect spacing. See [Yaml Files in a Nutshell]https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux_atomic_host/7/html/getting_started_with_kubernetes/yaml_in_a_nutshell for a good overview of YAML files.

## Step 3

Next, add the variables section `vars`. There will be one variable called `test_variable`.  The variable will have a string `"my test variable"`.

```yaml
---
- name: SIMPLE DEBUG PLAYBOOK
  hosts: localhost
  gather_facts: no

  vars:
    test_variable: "my test variable"
```

## Step 4

Next, add the first `task`. This task will use the `debug` module to print out the variable `test_variable`.

``` yaml
---
- name: SIMPLE DEBUG PLAYBOOK
  hosts: localhost
  connection: local
  gather_facts: no

  vars:
    test_variable: "my test variable"

  tasks:
    - name: DISPLAY TEST_VARIABLE
      debug:
        var: test_variable
```

>A play is a list of tasks. Tasks and modules have a 1:1 correlation.  Ansible modules are reusable, standalone scripts that can be used by the Ansible API, or by the ansible or ansible-playbook programs. They return information to ansible by printing a JSON string to stdout before exiting.

## Step 5

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook debug.yml
```
# Playbook Output

The output will look as follows.

```yaml
[student1@ansible ~]$ ansible-playbook debug.yml

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
The finished Ansible Playbook is provided here for an Answer key.

```yaml
---
- name: SIMPLE DEBUG PLAYBOOK
  hosts: localhost
  gather_facts: no

  vars:
    test_variable: "my test variable"

  tasks:
    - name: DISPLAY TEST_VARIABLE
      debug:
        var: test_variable
```

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
