# Exercise 4 - Network Configuration with Jinja Templates

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Takeaways](#takeaways)
- [Solution](#solution)

# Objective

Demonstration templating a network configuration and pushing it a device

- Use and understand group [variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) to store the IP addresses we want.
- Use the [Jinja2 template lookup plugin](https://docs.ansible.com/ansible/latest/plugins/lookup.html)
- Demonstrate use of the network automation [cli_config module](https://docs.ansible.com/ansible/latest/modules/cli_config_module.html)

# Guide

#### Step 1

This step will cover creating Ansible variables for use in an Ansible Playbook. This exercise will use the following IP address schema for loopbacks addresses on rtr1 and rtr2:

Device  | Loopback100 IP |
------------ | ------------- |
rtr1  | 192.168.100.1/32 |
rtr2  | 192.168.100.2/32 |

Variable information can be stored in host_vars and group_vars.  For this exercise create a folder named `group_vars`:

```bash
[student1@ansible network-workshop]$ mkdir ~/network-workshop/group_vars
```

Now create a file in this directory name `all.yml` using your text editor of choice.  Both vim and nano are installed on the control node.

```
[student1@ansible network-workshop]$ nano group_vars/all.yml
```

The interface and IP address information above must be stored as variables so that the Ansible playbook can use it. Start by making a simple YAML dictionary that stores the table listed above. Use a top level variable (e.g. `nodes`) so that a lookup can be performed based on the `inventory_hostname`:

```yaml
nodes:
  rtr1:
    Loopback100: "192.168.100.1"
  rtr2:
    Loopback100: "192.168.100.2"
```

Copy the YAML dictionary we created above into the group_vars/all.yml file and save the file.  

>All devices are part of the group **all** by default.  If we create a group named **cisco** only network devices belonging to that group would be able to access those variables.

#### Step 2

Create a new template file named `template.j2`:

```
[student1@ansible network-workshop]$ nano template.j2
```

Copy the following into the template.j2 file:

<!-- {% raw %} -->
```yaml
{% for interface,ip in nodes[inventory_hostname].items() %}
interface {{interface}}
  ip address {{ip}} 255.255.255.255
{% endfor %}
```
<!-- {% endraw %} -->


Save the file.

#### Step 3

This step will explain and elaborate on each part of the newly created template.j2 file.

<!-- {% raw %} -->
```yaml
{% for interface,ip in nodes[inventory_hostname].items() %}
```
<!-- {% endraw %} -->

<!-- {% raw %} -->
- Pieces of code in a Jinja template are escaped with `{%` and `%}`.  The `interface,ip` breaks down the dictionary into a key named `interface` and a value named `ip`.
<!-- {% endraw %} -->

- The `nodes[inventory_hostname]` does a dictionary lookup in the `group_vars/all.yml` file.  The **inventory_hostname** is the name of the hostname as configured in Ansible's inventory host file.  When the playbook is executed against `rtr1` inventory_hostname will be `rtr1`, when the playbook is executed against `rtr2`, the inventory_hostname will be `rtr2` and so forth.  

>The inventory_hostname variable is considered a [magic variable](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#magic-variables-and-how-to-access-information-about-other-hosts) which is automatically provided.  

- The keyword `items()` returns a list of dictionaries.  In this case the dictionary's key is the interface name (e.g. Loopback100) and the value is an IP address (e.g. 192.168.100.1)

<!-- {% raw %} -->
```yaml
interface {{interface}}
  ip address {{ip}} 255.255.255.255
```
<!-- {% endraw %} -->

- Variables are rendered with the curly braces like this: `{{ variable_here }}`  In this case the variable name key and value only exist in the context of the loop.  Outside of the loop those two variables don't exist.  Each iteration will re-assign the variable name to new values based on what we have in our variables.

Finally:
<!-- {% raw %} -->
```
{% endfor %}
```
<!-- {% endraw %} -->

- In Jinja we need to specify the end of the loop.

#### Step 4

Create the Ansible Playbook config.yml:

```
[student1@ansible network-workshop]$ nano config.yml
```

Copy the following Ansible Playbook to the config.yml file:

<!-- {% raw %} -->
```
---
- name: configure network devices
  hosts: rtr1,rtr2
  gather_facts: false
  tasks:
    - name: configure device with config
      cli_config:
        config: "{{ lookup('template', 'template.j2') }}"
```
<!-- {% endraw %} -->

- This Ansible Playbook has one task named *configure device with config*
- The **cli_config** module is vendor agnostic.  This module will work identically for an Arista, Cisco and Juniper device.  This module only works with the **network_cli** connection plugin.
- The cli_config module only requires one parameter, in this case **config** which can point to a flat file, or in this case uses the lookup plugin.  For a list of all available lookup plugins [visit the documentation](https://docs.ansible.com/ansible/latest/plugins/lookup.html)  
- Using the template lookup plugin requires two parameters, the plugin type *template* and the corresponding template name *template.j2*.

#### Step 5

Execute the Ansible Playbook:

```
[student1@ansible network-workshop]$ ansible-playbook config.yml
```

The output should look as follows.

```
[student1@ansible ~]$ ansible-playbook config.yml

PLAY [rtr1,rtr2] ********************************************************************************

TASK [configure device with config] ********************************************************************************
changed: [rtr1]
changed: [rtr2]

PLAY RECAP ********************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
rtr2                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Step 6

Use the command `show ip int br` to verify the IP addresses have been confirmed on the network devices.

```
[student1@ansible network-workshop]$ ssh rtr1

rtr1#show ip int br | include Loopback100
Loopback100            192.168.100.1   YES manual up                    up
```

# Takeaways

- The [Jinja2 template lookup plugin](https://docs.ansible.com/ansible/latest/plugins/lookup.html) can allow us to template out a device configuration.
- The `*os_config` (e.g. ios_config) and cli_config modules can source a jinja2 template file, and push directly to a device.  If you want to just render a configuration locally on the control node, use the [template module](https://docs.ansible.com/ansible/latest/modules/template_module.html).
- Variables are mostly commonly stored in group_vars and host_vars.  This short example only used group_vars.

# Solution

The finished Ansible Playbook is provided here for an answer key: [config.yml](config.yml).

The provided Ansible Jinja2 template is provided here: [template.j2](template.j2).

---

# Complete

You have completed lab exercise 4

[Click here to return to the Ansible Network Automation Workshop](../README.md)
