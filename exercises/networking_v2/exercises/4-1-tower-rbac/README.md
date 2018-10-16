# Exercise 1: Using the debug module

## Table of Contents

- [Objective](#Objective)
- [Guide](#Guide)
- [Playbook Output](#Playbook_Output)
- [Solution](#Solution)

# Objective

Demonstrate use of the [debug module](https://docs.ansible.com/ansible/latest/modules/debug_module.html) to display a variable to the terminal window.

# Guide

## Step 1:

## Step 2

For this step the goal is to create some custom teams.  A Team is a subdivision of an organization with associated users, projects, credentials, and permissions. Teams provide a means to implement role-based access control schemes and delegate responsibilities across organizations.

>More info on teams can be found in the [documentation here](https://docs.ansible.com/ansible-tower/latest/html/userguide/teams.html#teams).

Instead of manually creating the teams in the Web UI, an Ansible Playbook will be used to automate it.  This Playbook will use the [tower_team module](https://docs.ansible.com/ansible/latest/modules/tower_team_module.html).

For this exercise there will be three teams created
- netop - Network Operator
- neteng - Network Engineer
- netadmin - Network Administrator

```
---
- name: TOWER CONFIGURATION IN PLAYBOOK FORM
  hosts: control
  connection: local
  gather_facts: no
  tasks:

    - name: Create tower team
      tower_team:
        name: "{{item}}"
        organization: Default
        state: present
        tower_username: admin
        tower_password: ansible
        tower_host: https://localhost
      loop:
        - netop
        - neteng
        - netadmin
```

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
- The `hosts: localhost`,  indicates the play is run only on the Ansible control node
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: no` disables facts gathering.  We are not using any fact variables for this playbook.


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

Next, add the first `task`. This task will use the `debug` module to print out the variable test_variable.

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

#### Step 5

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
