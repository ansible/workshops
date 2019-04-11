# Exercise 01 - Configuring IP Addresses with Jinja Templates

For this exercise we are going to configure all the IP addresses for our IP fabric using the [eos_config](http://docs.ansible.com/ansible/latest/eos_config_module.html) module.

## Table of Contents

- [Jinja Templates](#jinja-templates)
- [Ansible Variables](#ansible-variables)
- [Creating a template](#creating-a-template)
- [The Playbook](#the-playbook)
- [Looking at the results](#looking-at-the-results)
- [Complete](#complete)

## Jinja Templates

On Linux hosts we can use the [template module](http://docs.ansible.com/ansible/latest/template_module.html) to render [jinja templates](http://jinja.pocoo.org/).  When using the connection **network_cli** the template module will just run locally for both the src and dest (as opposed to with Linux hosts where the src will be on the control node, and the dest will be on the inventory device the Playbook is being run against).  Lets look at a task of this:

```
- name: create routing config
  template:
    src: ./test.j2
    dest: ./test_config/test.cfg
```

The vars for this example are:

```yaml
spine01:
  loopback1: "172.16.0.1/32"
```

The test.j2 for this example is:
```
interface Loopback1    
    address {{spine01.loopback1}}

```

Running the task above will render test.cfg:

```yaml
interface Loopback1
    address 172.16.0.1/32
```

Jinja2 is very powerful and has lots of features.  The most commonly used ones to template configs are conditionals and loops [which you can read more about here](http://jinja.pocoo.org/docs/2.10/templates/).  With the networking **os_config** modules (i.e. eos_config) the src can set from a jinja template.  This means you don't need two tasks to render, then push config.  You can use one task like this:

```
- name: push config to device
  eos_config:
    src: ./ospf.j2
    save_when: changed
```

## Ansible Variables

Here is the IP address schema used for this network.

Device Left | Left IP | Right IP | Device Right
------------ | ------------- | ------------- | -------------
spine01 eth2 | 172.16.200.1/30 | 172.16.200.2/30 | eth2 leaf01
spine01 eth3 | 172.16.200.5/30 | 172.16.200.6/30 | eth2 leaf02
spine02 eth2 | 172.16.200.17/30 | 172.16.200.18/30 | eth3 leaf01
spine02 eth3 | 172.16.200.21/30 | 172.16.200.22/30 | eth3 leaf02

In addition the loopbacks are:

Device  | Loopback IP |
------------ | ------------- |
spine01 eth2 | 172.16.0.1/32 |
spine01 eth3 | 172.16.0.2/32 |
spine02 eth2 | 172.16.0.3/32 |
spine02 eth3 | 172.16.0.4/32 |

We need to store the information about the IP address schema so that our playbook can use it.  Lets start by making a simple yaml dictionary that represents spine01's connections. Lets see what that dictionary would look like.  For simplicity (and demonstration purposes) we will put all the variables into one file.  We will use the top level variable `nodes` just so we can do a lookup based on the inventory_hostname.  

The **inventory_hostname** is the name of the hostname as configured in Ansible's inventory host file.  When the playbook is executed against leaf01 inventory_hostname will be leaf01, when the playbook is executed against leaf02, the inventory_hostname will be leaf02 and so forth.  The inventory_hostname variable is considered a [magic variable](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#magic-variables-and-how-to-access-information-about-other-hosts) which is automatically provided.

Lets look at what this can look like:
```
nodes:
  spine01:
    Loopback1: "172.16.0.1/32"
    Ethernet2: "172.16.200.1/30"
    Ethernet3: "172.16.200.5/30"
```

Now continue creating the variables for spine02, leaf01 and leaf02.

## Creating a template

Now we need to combine what we learned about jinja templates to take advantage of our variables.  We need to create a loop that configures every interface on the switch.

For example we want to configure an interface like this:
```
interface Ethernet2
   no switchport
   ip address 172.16.200.2/30
```

We can easily create a loop in jinja that iterates over each interface:
```
{% for interface in nodes[inventory_hostname] -%}
interface {{interface}}
  no switchport
  ip address {{nodes[inventory_hostname][interface]}}
{% endfor %}
```

There is one problem!  We are also configuring the loopbacks, and `no switchport` is not a valid command for the loopback interface.  We can make a simple **if** statement to check for loopback addresses:
```
{% for interface in nodes[inventory_hostname] -%}
interface {{interface}}
{% if "Loopback" not in interface %}
  no switchport
{% endif %}
  ip address {{nodes[inventory_hostname][interface]}}
{% endfor %}
```

Save this jinja template as ospf.j2 (we will add OSPF to it in the next exercise)

## The Playbook

We can store variables in multiple places.  There is [extensive documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) and most Ansible users elect to use a combination of host_vars and group_vars.  For simplicity we will just define the vars in our playbook itself.

Look at the following playbook:

```yml
---
- name: configure OSPF
  hosts: network
  vars:
    nodes:
      spine01:
        Loopback1: "172.16.0.1/32"
        Ethernet2: "172.16.200.1/30"
        Ethernet3: "172.16.200.5/30"
      spine02:
        Loopback1: "172.16.0.2/32"
        Ethernet2: "172.16.200.17/30"
        Ethernet3: "172.16.200.21/30"
      leaf01:
        Loopback1: "172.16.0.3/32"
        Ethernet2: "172.16.200.2/30"
        Ethernet3: "172.16.200.18/30"
      leaf02:
        Loopback1: "172.16.0.4/32"
        Ethernet2: "172.16.200.6/30"
        Ethernet3: "172.16.200.22/30"

  tasks:
    - name: push config to device
      eos_config:
        src: ./ospf.j2
        save_when: changed
```

While the playbook may seem long, it only contains 1 task.  To run the playbook use the `ansible-playbook` command.

```bash
ansible-playbook ospf.yml
```
Parameter | Explanation
------------ | -------------
ansible-playbook | Ansible executable for running playbooks
ospf.yml | the name of the playbook


```
[vagrant@ansible linklight]$ ansible-playbook ospf.yml

PLAY [configure OSPF] ************************************************************************************************************************************************************

TASK [push config to device] *****************************************************************************************************************************************************
changed: [leaf01]
changed: [spine02]
changed: [spine01]
changed: [leaf02]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=1    changed=1    unreachable=0    failed=0
leaf02                     : ok=1    changed=1    unreachable=0    failed=0
spine01                    : ok=1    changed=1    unreachable=0    failed=0
spine02                    : ok=1    changed=1    unreachable=0    failed=0
```

## Check the configuration
Use the command `show ip int br` to check the IP addresses on multiple interfaces

```
[vagrant@ansible linklight]$ ssh admin@leaf01
Password:
Last login: Thu Jun 21 21:20:42 2018 from 192.168.0.2
leaf01#show ip int br
Interface              IP Address         Status     Protocol         MTU
Ethernet1              192.168.0.14/24    up         up              1500
Ethernet2              172.16.200.2/30    up         up              1500
Ethernet3              172.16.200.18/30   up         up              1500
Loopback1              172.16.0.3/32      up         up             65535
Management1            10.0.2.15/24       up         up              1500
leaf01#
```


## Complete
You have completed Exercise 01.

[Return to training-course](../README.md)
