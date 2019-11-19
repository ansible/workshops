# Exercise 1.7: Using the bigip_config module

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate use of the [BIG-IP config module](https://docs.ansible.com/ansible/latest/modules/bigip_config_module.html) to save the running configuration to disk

# Guide

## Step 1:

Using your text editor of choice create a new file called `bigip-config.yml`.

```
[student1@ansible ~]$ nano bigip-config.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format).

Enter the following play definition into `bigip-virtual-server.yml`:

``` yaml
---
- name: BIG-IP SETUP
  hosts: lb
  connection: local
  gather_facts: false
```

- The `---` at the top of the file indicates that this is a YAML file.
- The `hosts: f5`,  indicates the play is run only on the F5 BIG-IP device
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: no` disables facts gathering.  We are not using any fact variables for this playbook.

Do not exit the editor yet.

## Step 3

Next, add the `task`. This task will use the `bigip-config` to save the running configuration to disk

{% raw %}
``` yaml
  tasks:

  - name: SAVE RUNNING CONFIG ON BIG-IP
    bigip_config:
      provider:
        server: "{{private_ip}}"
        user: "{{ansible_user}}"
        password: "{{ansible_ssh_pass}}"
        server_port: 8443
        validate_certs: no
      save: yes
```
{% endraw %}


>A play is a list of tasks. Tasks and modules have a 1:1 correlation.  Ansible modules are reusable, standalone scripts that can be used by the Ansible API, or by the ansible or ansible-playbook programs. They return information to ansible by printing a JSON string to stdout before exiting.

- `name: SAVE RUNNING CONFIG ON BIG-IP` is a user defined description that will display in the terminal output.
- `bigip_config:` tells the task which module to use.
- The `server: "{{private_ip}}"` parameter tells the module to connect to the F5 BIG-IP IP address, which is stored as a variable `private_ip` in inventory
- The `provider:` parameter is a group of connection details for the BIG-IP.
- The `user: "{{ansible_user}}"` parameter tells the module the username to login to the F5 BIG-IP device with
- The `password: "{{ansible_ssh_pass}}"` parameter tells the module the password to login to the F5 BIG-IP device with
- The `server_port: 8443` parameter tells the module the port to connect to the F5 BIG-IP device with
- The `save: "yes""` parameter tells the module to save the running-config to startup-config.
  This operation is performed after any changes are made to the current running config. If no changes are made, the configuration is   
  still saved to the startup config. This option will always cause the module to return changed
- The `validate_certs: "no"` parameter tells the module to not validate SSL certificates.  This is just used for demonstration purposes   since this is a lab.

Save File and exit out of editor.

## Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-config.yml
```

# Playbook Output

```yaml
[student1@ansible]$ ansible-playbook bigip-config.yml

PLAY [BIG-IP SETUP] ************************************************************************************************************************

TASK [SAVE RUNNING CONFIG ON BIG-IP] ************************************************************************************************************************
changed: [f5]

PLAY RECAP *************************************************************************************************************
f5                         : ok=1    changed=1    unreachable=0    failed=0
```

# Solution

The finished Ansible Playbook is provided here for an Answer key.  Click here: [bigip-config.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.7-save-running-config/bigip-config.yml).

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
