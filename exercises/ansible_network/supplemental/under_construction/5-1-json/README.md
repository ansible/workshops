# Exercise 5-1: Working with JSON Output

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate the advantage of using structured output (in this case JSON) and pulling out useful information with show commands.

# Guide

## Step 1:

Using your text editor of choice create a new file called `json.yml`.

```
[student1@ansible ~]$ nano json.yml
```

>`vim` and `nano` are available on the control node, as well as Visual Studio and Atom via RDP

## Step 2:

Enter the following play definition into `json.yml`:

``` yaml
---
- name: JSON EXAMPLE
  hosts: arista
  gather_facts: no
```

- The `---` at the top of the file indicates that this is a YAML file.
- Always give your playbooks and tasks good, descriptive names. These names form part of the playbook output.
- The `hosts: arista`,  indicates the play is run only on the Arista network switches (this is pre-setup in inventory via `~/networking-workshop/lab_inventory/hosts`)
- `gather_facts: no` disables facts gathering.  We are not using any fact variables for this playbook.

## Step 3

Next, add the first `task`. This task will use the [eos_command module](https://docs.ansible.com/ansible/latest/modules/eos_command_module.html) to run an arbitrary command.  Using the pipe json (`| json`) it is possible to return the command in structured data.

```yaml
---
- name: JSON EXAMPLE
  hosts: arista
  gather_facts: no

  tasks:

    - name: RUN ARISTA COMMAND
      eos_command:
        commands: show interfaces eth1 | json
      register: command_output
```

## Step 4

Add an additional task to print the output to the terminal window using the debug module.

```
---
- name: RUN COMMAND AND PRINT TO TERMINAL WINDOW
  hosts: arista
  gather_facts: false

  tasks:

    - name: RUN ARISTA COMMAND
      eos_command:
        commands: show interfaces eth1 | json
      register: command_output

    - name: PRINT TO TERMINAL WINDOW
      debug:
        msg: "{{command_output.stdout}}"
```

## Step 5

Run the playbook - exit back into the command line of the control host and execute the following:

```
[student1@ansible ~]$ ansible-playbook json.yml
```
# Playbook Output

The output will look as follows.

```yaml
[student1@ansible ~]$ ansible-playbook json.yml

PLAY [RUN COMMAND AND PRINT TO TERMINAL WINDOW] ***********************************************************************************************************

TASK [RUN ARISTA COMMAND] *********************************************************************************************************************************
ok: [rtr2]
ok: [rtr4]

TASK [PRINT TO TERMINAL WINDOW] ***************************************************************************************************************************
ok: [rtr2] =>
  msg:
  - interfaces:
      Ethernet1:
        autoNegotiate: success
        bandwidth: 1000000000
        burnedInAddress: 02:f3:9e:70:cf:12
        description: ''
        duplex: duplexFull

<<<<rest of output removed for brevity>>>>
```

## Step 6

Now that structured output can be used, it is trivial to keep honing in on the value you want.  For example in the output above

```
  - interfaces:
      Ethernet1:
        autoNegotiate: success
        bandwidth: 1000000000
        burnedInAddress: 02:f3:9e:70:cf:12
```

to return the MAC address or what Arista is calling the `burnedInAddress` the following would work->

```
command_output.stdout[0].Ethernet1.burnedInAddress
```
which would return `02:f3:9e:70:cf:12`.

## Step 7

Without looking at the solution guide try to print out the IPv4 address.


# Solution
The finished Ansible Playbook is provided here for an Answer key.
[json.yml](json.yml)



You have finished this exercise.  [Click here to return to the lab guide](../README.md)
