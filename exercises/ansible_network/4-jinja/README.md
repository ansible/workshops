# Exercise 04 - Network Configuration with Jinja Templates

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Ansible Variables](#ansible-variables)
- [Jinja Templates](#jinja-templates)
- [Creating a template](#creating-a-template)
- [The Playbook](#the-playbook)
- [Looking at the results](#looking-at-the-results)
- [Complete](#complete)

# Objective

For this exercise we are going to template a network configuration and push it to a device.

We will
  - Demonstrate use of the network automation [cli_config module](https://docs.ansible.com/ansible/latest/modules/cli_config_module.html)
- Use the [Jinja2 template lookup plugin](https://docs.ansible.com/ansible/latest/plugins/lookup.html)
 - Use and understand group [variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) to store the IP addresses we want.

# Guide

## Ansible Variables

Here is the IP address schema for the loopbacks addresses:

Device  | Loopback IP |
------------ | ------------- |
rtr1  | 172.16.0.1/32 |
rtr2  | 172.16.0.2/32 |
rtr3  | 172.16.0.3/32 |
rtr4  | 172.16.0.4/32 |

We need to store the information about the IP address schema so that our playbook can use it.  Lets start by making a simple yaml dictionary that stores the table listed above. We will use the top level variable `nodes` so we can do a lookup based on the inventory_hostname.  

Lets look at what this can look like:
```
nodes:
  rtr1:
    Loopback100: "192.168.100.1"
```

Now continue creating the variables for rtr2, rtr3 and rtr4.

```
nodes:
  rtr1:
    Loopback100: "192.168.100.1"
  rtr2:
    Loopback100: "192.168.100.2"
  rtr3:
    Loopback100: "192.168.100.3"
  rtr4:
    Loopback100: "192.168.100.4"
```

Where do we want to store this information?  Create a folder named `group_vars`:

```
[student1@ansible networking-workshop]$ mkdir group_vars
```

Now create a file in this directory name `all.yml` using your text editor of choice.  Both vim and nano are installed on the control node.

```
[student1@ansible networking-workshop]$ nano group_vars/all.yml
```

All devices are part of the group **all** by default.  If we create a group named **cisco** only network devices belonging to that group would be able to access those variables.

Copy the yaml dictionary we created above into the group_vars/all.yml file and save the file.  If you want to easily import this data model we created to Ansible Tower please check out this [blog post](https://www.ansible.com/blog/three-quick-ways-to-move-your-ansible-inventory-into-red-hat-ansible-tower).  It is trivial to sync your inventory and variables with a SCM tool like Github to Ansible Tower.


## Jinja Templates

On Linux hosts we can use the [template module](http://docs.ansible.com/ansible/latest/template_module.html) to render [jinja templates](http://jinja.pocoo.org/).  When using the connection plugin **network_cli** the template module will just run locally on the control node for both the src and dest (as opposed to with Linux hosts where the src will be on the control node, and the dest will be on the inventory device the Playbook is being run against).  We always have the option to template files locally, then push them to network devices, or we can directly push them to device without the intermediate step of rendering them before we push.

Lets look at a simplified example Ansible Playbook to illustrate this concept.

Create a simple Ansible Playbook file that looks like this:
```
[student1@ansible networking-workshop]$ nano test.yml
```

Feel free to cut and paste this into your text editor of choice:
```
---
- hosts: cisco
  gather_facts: false
  connection: network_cli
  tasks:
    - name: create routing config
      template:
        src: ./test.j2
        dest: ./test.cfg
```

For this simplified example we will use host vars.  The vars for this example is under `host_vars/rtr1.yml`:

```yaml
[student1@ansible networking-workshop]$ cat host_vars/rtr1.yml
loopback: "192.168.1.0"
```

That means this variable `loopback` is specific only to the `rtr1` device.

Now lets create a Jinja2 template.  The test.j2 for this example is:
{% raw %}
```
[student1@ansible networking-workshop]$ cat test.j2
interface Loopback500
    address {{loopback}} 255.255.255.255
```
{% endraw %}

Running the Ansible Playbook will now render the Jinja2 template into a flat-file.  Since this will only work on `rtr1` we can use the `-l` to limit the play to just the single host.

```
[student1@ansible networking-workshop]$ ansible-playbook test.yml -l rtr1

PLAY [cisco] *******************************************************************

TASK [create network config] ***************************************************
ok: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0
```

The Ansible Playbook create the `test.cfg` file with the rendered template:

```yaml
[student1@ansible networking-workshop]$ cat test.cfg
interface Loopback500
    address 192.168.1.0 255.255.255.255
```

Jinja2 is very powerful and has lots of features.  The most commonly used ones to template configs are conditionals and loops [which you can read more about here](http://jinja.pocoo.org/docs/2.10/templates/).  We will cover a simple loop in the next section.


## Creating a template

The **inventory_hostname** is the name of the hostname as configured in Ansible's inventory host file.  When the playbook is executed against `rtr1` inventory_hostname will be `rtr1`, when the playbook is executed against `rtr2`, the inventory_hostname will be `rtr2` and so forth.  The inventory_hostname variable is considered a [magic variable](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#magic-variables-and-how-to-access-information-about-other-hosts) which is automatically provided.  This `inventory_hostname` variable will exists regardless if you have facts or not (`gather_facts: false` or `gather_facts: true`).

We need to combine what we learned about Jinja templates to take advantage of our variables stored in `group_vars/all.yml`.  We need to create a loop that configures every interface on the switch.  Right now we just have 1 key, value pair (loopback100 and a corresponding IP address) per device.  However templates make it easy to configure dozens of addresses quickly and effectively.  In fact you will not notice the time difference between 54 interfaces being templated or a single loopback from Ansible's perspective.

Lets create a new template file named `template.j2`:

```
[student1@ansible networking-workshop]$ nano template.j2
```

We can easily create a loop in Jinja that iterates over each interface:

{% raw %}
```
{% for key,value in nodes[inventory_hostname].iteritems() %}
interface {{ key }}
  ip address {{ value }} 255.255.255.255
{% endfor %}
```
{% endraw %}

Save this Jinja template so we can use it below.

First, lets break down this template line by line:

{% raw %}
```yaml
{% for key,value in nodes[inventory_hostname].iteritems() %}
```
{% endraw %}

{% raw %}
- Pieces of code in a Jinja template are escaped with `{%` and `%}`.  The `key,value` allows us to break down the dictionary into a key named key and a value named value.  We can use both the key (an interface name, e.g. Loopback500) and the value (an ip address, e.g. 192.168.100.1/32).
{% endraw %}

- The `nodes[inventory_hostname]` allows us to do a lookup in our `group_vars/all.yml` file.  As you build Ansible Playbook variables you can make the choice to break up variables into `host_vars` files per host or using larger aggregated `group_vars`.  In practice you will see a mix of both depending on the use-case.  Your instructor can elaborate on storing variables and the data models he or she has seen in practice.  In general the simpler the data model the more consumable it will be by other Ansible Playbook writers.

- The `iteritems()` is a Pythonism that allows to iterate over the dictionary.

Now lets look at the next section:

{% raw %}
```yaml
interface {{ key }}
  ip address {{ value }} 255.255.255.255
```
{% endraw %}

- Variables are rendered with the curly braces like this: `{{ variable_here }}`  In this case the variable name key and value only exist in the context of the loop.  Outside of the loop those two variables don't exist.  Each iteration will re-assign the variable name to new values based on what we have in our variables.

Finally:
{% raw %}
```
{% endfor %}
```
{% endraw %}

- In Jinja we need to specify the end of the loop.  You can also use loops within loops, but in general it is best practice to keep your Jinja templates as simple as possible.  Rather than having a single very complex template that covers all use-cases, it usually will make more sense to have multiple Jinja templates.

## The Playbook

With the network automation `cli_config` module, the src can set from a Jinja template.  This means you don't need two tasks to render, then push config.  You can use one task like this:

Create the Ansible Playbook:

```
[student1@ansible networking-workshop]$ nano config.yml
```

Feel free to cut and paste this Ansible Playbook:

{% raw %}
```
---
- hosts: cisco
  gather_facts: false
  connection: network_cli
  tasks:
    - name: configure device with config
      cli_config:
        config: "{{ lookup('template', 'template.j2') }}"
```
{% endraw %}

To run the playbook use the `ansible-playbook` command:

```
[student1@ansible networking-workshop]$ ansible-playbook config.yml

PLAY [cisco] *******************************************************************

TASK [configure device with config] ********************************************
changed: [rtr3]
changed: [rtr2]
changed: [rtr4]
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0
rtr2                       : ok=1    changed=1    unreachable=0    failed=0
rtr3                       : ok=1    changed=1    unreachable=0    failed=0
rtr4                       : ok=1    changed=1    unreachable=0    failed=0
```

## Check the configuration
Use the command `show ip int br` to check the IP addresses on multiple interfaces

```
[student1@ansible networking-workshop]$ ssh rtr1


rtr1#sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       172.16.151.195  YES DHCP   up                    up
Loopback0              192.168.1.101   YES manual up                    up
Loopback1              10.1.1.101      YES manual up                    up
Loopback100            192.168.100.1   YES manual up                    up
Tunnel0                10.100.100.1    YES manual up                    up
Tunnel1                10.200.200.1    YES manual up                    up
VirtualPortGroup0      192.168.35.101  YES TFTP   up                    up
```


## Complete
You have completed Exercise 4.

[Return to training-course](../README.md)
