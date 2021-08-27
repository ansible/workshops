# Exercise 5-0: The httpapi connection plugin

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate the use of the [httpapi connection plugin](https://docs.ansible.com/ansible/latest/plugins/connection/httpapi.html) to connection to, run a command and display network output to the terminal window.

# Guide

## Step 1:

Using your text editor of choice create a new file called `httpapi.yml`.

```
[student1@ansible ~]$ nano httpapi.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format).

Enter the following play definition into `httpapi.yml`:

``` yaml
---
- name: TURN ON HTTPAPI CONNECTION PLUGINS
  hosts: arista
  gather_facts: false
```

- The `---` at the top of the file indicates that this is a YAML file.
- Always give your playbooks and tasks good, descriptive names. These names form part of the playbook output.
- The `hosts: arista`,  indicates the play is run only on the Arista network switches (this is pre-setup in inventory via `~/networking-workshop/lab_inventory/hosts`)
- `gather_facts: no` disables facts gathering.  We are not using any fact variables for this playbook.

> One of the most common errors in YAML files is caused by incorrect spacing. See [Yaml Files in a Nutshell]https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux_atomic_host/7/html/getting_started_with_kubernetes/yaml_in_a_nutshell for a good overview of YAML files.

## Step 3

Next, add the first `task`. This task will use the [eos_eapi module](https://docs.ansible.com/ansible/latest/modules/eos_eapi_module.html) to turn on Arista eAPI.  This task has no required parameters, the defaults will be sufficient for the exercise.

```yaml
---
- name: TURN ON HTTPAPI CONNECTION PLUGINS
  hosts: arista
  gather_facts: false
  tasks:
    - name: TURN ON EAPI
      eos_eapi:
```

## Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook debug.yml
```
# Playbook Output

The output will look as follows.

```yaml
[student1@ansible ~]$ ansible-playbook httpapi.yml

PLAY [arista] ******************************************************************

TASK [TURN ON EAPI] ************************************************************
changed: [rtr2]
changed: [rtr4]

PLAY RECAP *********************************************************************
rtr2                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0
rtr4                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0
```
> Notice that the names you gave the play and task appear in this output. This is especially important when you have longer playbooks that include multiple tasks.

## Step 5

Modify the inventory to change the default connection plugin to httpapi.

```
[student1@ansible ~]$ nano ~/networking-workshop/lab_inventory/hosts
```

Modify the `[arista:vars]` section and change ansible_connection=network_cli to ansible connection=httpapi.

```
[arista:vars]
ansible_user=ec2-user
ansible_network_os=eos
ansible_connection=httpapi
ansible_become=true
ansible_become_method=enable
ansible_httpapi_use_ssl=true
ansible_httpapi_validate_certs=false
````

Save the file and return to the Linux CLI.

You can verify the eAPI is setup correctly with the `show management api http-commands`

# Solution
The finished Ansible Playbook is provided here for an Answer key.



You have finished this exercise.  [Click here to return to the lab guide](../README.md)
