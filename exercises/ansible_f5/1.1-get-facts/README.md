# Exercise 1.1: Using the bigip_device_info module

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)
- [Going Further](#going-further)

# Objective

Demonstrate use of the [BIG-IP Info module](https://docs.ansible.com/ansible/latest/collections/f5networks/f5_modules/bigip_device_info_module.html) to grab facts (useful information) from a F5 BIG-IP device and display them to the terminal window using the [debug module](https://docs.ansible.com/ansible/latest/modules/debug_module.html).  

# Guide

Make sure you are in the home directory

```
[student1@ansible f5-workshop]$ cd ~
```

## Step 1:

Using your text editor of choice create a new file called `bigip-info.yml`.

```
[student1@ansible ~]$ nano bigip-info.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format).

Enter the following play definition into `bigip-info.yml`:

``` yaml
---
- name: GRAB F5 FACTS
  hosts: f5
  connection: local
  gather_facts: false
```

- The `---` at the top of the file indicates that this is a YAML file.
- The `hosts: f5`,  indicates the play is run only on the F5 BIG-IP device
- `connection: local` tells the Playbook to run locally (rather than SSHing to itself)
- `gather_facts: no` disables facts gathering.  

Do not close editor yet.

## Step 3

Next, add the first `task`. This task will use the `bigip_device_info` module to grab useful information from the BIG-IP device.

{% raw %}
``` yaml
  tasks:
    - name: COLLECT BIG-IP FACTS
      f5networks.f5_modules.bigip_device_info:
        gather_subset:
          - system-info
        provider:
          server: "{{private_ip}}"
          user: "{{ansible_user}}"
          password: "{{ansible_password}}"
          server_port: 8443
          validate_certs: false
      register: device_facts
```
{% endraw %}

>A play is a list of tasks. Tasks and modules have a 1:1 correlation.  Ansible modules are reusable, standalone scripts that can be used by the Ansible API, or by the ansible or ansible-playbook programs. They return information to ansible by printing a JSON string to stdout before exiting.

- `name: COLLECT BIG-IP FACTS` is a user defined description that will display in the terminal output.
- `bigip_device_info:` tells the task which module to use.  Everything except `register` is a module parameter defined on the module documentation page.
- The `gather_subset: system_info` parameter tells the module only to grab system level information.
- The `provider:` parameter is a group of connection details for the BIG-IP.
- The `server: "{{private_ip}}"` parameter tells the module to connect to the F5 BIG-IP IP address, which is stored as a variable `private_ip` in inventory
- The `user: "{{ansible_user}}"` parameter tells the module the username to login to the F5 BIG-IP device with
- The`password: "{{ansible_password}}"` parameter tells the module the password to login to the F5 BIG-IP device with
- The `server_port: 8443` parameter tells the module the port to connect to the F5 BIG-IP device with. 8443 is what's being used in this lab, but could be different depending on the deployment.
- The `validate_certs: false` parameter tells the module to not validate SSL certificates.  This is just used for demonstration purposes since this is a lab.
- `register: device_facts` tells the task to save the output to a variable bigip_device_info

## Step 4

Next, append the second `task` to above . This task will use the `debug` module to print the output from device_facts variable we registered the facts to.

{% raw %}
```yaml
    - name: DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION
      debug:
        var: device_facts
```
{% endraw %}

- The `name: COMPLETE BIG-IP SYSTEM INFORMATION` is a user defined description that will display in the terminal output.
- `debug:` tells the task to use the debug module.
- The `var: device_facts` parameter tells the module to display the variable bigip_device_info.

Save the file and exit out of editor.

## Step 5

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-info.yml
```

The output will look as follows.
``` yaml
[student1@ansible ~]$ ansible-playbook bigip-info.yml

PLAY [GRAB F5 FACTS] **********************************************************

TASK [COLLECT BIG-IP FACTS] ***************************************************
ok: [f5]

TASK [DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION] *****************************
ok: [f5] =>
  device_facts:
    ansible_facts:
      discovered_interpreter_python: /usr/libexec/platform-python
    changed: false
    failed: false
    queried: true
    system_info:
      base_mac_address: 02:04:cc:f9:26:3c
      chassis_serial: dc9c21ec-8b80-ff90-87324c84c43b
      hardware_information:
      - model: Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz
        name: cpus
        type: base-board
        versions:
        - name: cache size
          version: 30720 KB
        - name: cores
          version: 2  (physical:2)
        - name: cpu MHz
          version: '2400.052'
        - name: cpu sockets
          version: '1'
        - name: cpu stepping
          version: '2'
      marketing_name: BIG-IP Virtual Edition
      package_edition: Point Release 4
      package_version: Build 0.0.5 - Tue Jun 16 14:26:18 PDT 2020
      platform: Z100
      product_build: 0.0.5
      product_build_date: Tue Jun 16 14:26:18 PDT 2020
      product_built: 200616142618
      product_changelist: 3337209
      product_code: BIG-IP
      product_jobid: 1206494
      product_version: 13.1.3.4
      time:
        day: 19
        hour: 17
        minute: 11
        month: 10
        second: 2
        year: 2020
      uptime: 4465

PLAY RECAP ********************************************************************
f5                         : ok=2    changed=0    unreachable=0    failed=0
```
## Step 6

Finally let's append two more tasks to get more specific info from facts gathered, to the above playbook.

{% raw %}
```yaml

    - name: DISPLAY ONLY THE MAC ADDRESS
      debug:
        var: device_facts['system_info']['base_mac_address']

    - name: DISPLAY ONLY THE VERSION
      debug:
        var: device_facts['system_info']['product_version']
```
{% endraw %}

- `var: device_facts['system_info']['base_mac_address']` displays the MAC address for  the Management IP on the BIG-IP device
- `device_facts['system_info']['product_version']` displays the product version BIG-IP device

>Because the bigip_device_info module returns useful information in structured data, it is really easy to grab specific information without using regex or filters.  Fact modules are very powerful tools to grab specific device information that can be used in subsequent tasks, or even used to create dynamic documentation (reports, csv files, markdown).

## Step 7

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook bigip-info.yml
```

# Playbook Output

The output will look as follows.

{% raw %}
```yaml
[student1@ansible ~]$ ansible-playbook bigip-info.yml

PLAY [GRAB F5 FACTS] **********************************************************

TASK [COLLECT BIG-IP FACTS] ***************************************************
ok: [f5]

TASK [DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION] *****************************
ok: [f5] =>
  device_facts:
    ansible_facts:
      discovered_interpreter_python: /usr/libexec/platform-python
    changed: false
    failed: false
    queried: true
    system_info:
      base_mac_address: 02:04:cc:f9:26:3c
      chassis_serial: dc9c21ec-8b80-ff90-87324c84c43b
      hardware_information:
      - model: Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz
        name: cpus
        type: base-board
        versions:
        - name: cache size
          version: 30720 KB
        - name: cores
          version: 2  (physical:2)
        - name: cpu MHz
          version: '2400.052'
        - name: cpu sockets
          version: '1'
        - name: cpu stepping
          version: '2'
      marketing_name: BIG-IP Virtual Edition
      package_edition: Point Release 4
      package_version: Build 0.0.5 - Tue Jun 16 14:26:18 PDT 2020
      platform: Z100
      product_build: 0.0.5
      product_build_date: Tue Jun 16 14:26:18 PDT 2020
      product_built: 200616142618
      product_changelist: 3337209
      product_code: BIG-IP
      product_jobid: 1206494
      product_version: 13.1.3.4
      time:
        day: 19
        hour: 17
        minute: 11
        month: 10
        second: 2
        year: 2020
      uptime: 4465

TASK [DISPLAY ONLY THE MAC ADDRESS] *******************************************
ok: [f5] =>
  "device_facts['system_info']['base_mac_address']": "0a:54:53:51:86:fc"

TASK [DISPLAY ONLY THE VERSION] ***********************************************
ok: [f5] =>
  "device_facts['system_info']['product_version']": "13.1.3.4"

PLAY RECAP ********************************************************************
f5                         : ok=4    changed=0    unreachable=0    failed=0
```
{% endraw %}

# Solution

The finished Ansible Playbook is provided here for an Answer key.  Click here for [bigip-info.yml](https://github.com/network-automation/linklight/blob/master/exercises/ansible_f5/1.1-get-facts/bigip-info.yml).

# Going Further

For this bonus exercise add the `tags: debug` paramteter (at the task level) to the existing debug task.

```yaml
    - name: DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION
      debug:
        var: device_facts
      tags: debug
```

Now re-run the playbook with the `--skip-tags-debug` command line option.

```
ansible-playbook bigip-info.yml --skip-tags=debug
```

The Ansible Playbook will only run three tasks, skipping the `DISPLAY COMPLETE BIG-IP SYSTEM INFORMATION` task.

You have finished this exercise.  [Click here to return to the lab guide](../README.md)
