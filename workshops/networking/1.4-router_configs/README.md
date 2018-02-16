# Exercise 1.4 - Additional router configurations

Previous exercises showed you the basics of Ansible. In the exercise, we will build upon that and introduce additional Ansible concepts that allow you to add flexibility and power to your playbooks.

## Table of Contents
 - [Intro](#intro)
 - [Section 1 - Using variables in a playbook](#section-1---using-variables-in-a-playbook)
 - [Section 2 - Create a block for rtr1](#section-2---create-a-block-for-rtr1)
 - [Section 3 - Configuring rtr2](#section-3---configuring-rtr2)
 - [Section 4 - Review](#section-4-review)

## Intro

Ansible exists to make tasks simple and repeatable. We also know that not all systems are exactly alike and often require some slight change to the way an Ansible playbook is run.

- **Variables** are how we deal with differences between your systems, allowing you to account for a change in port, IP address or directory.
- **Loops** enable us to repeat the same task over and over again. For example, lets say you want to install 10 packages. By using an ansible loop, you can do that in a single task.
- **Blocks** allow for logical grouping of tasks and even in play error handling. Most of what you can apply to a single task can be applied at the block level, which also makes it much easier to set data or directives common to the tasks.

**jinja?** - jinja2 is used in Ansible to enable dynamic expressions and access to variables.

For a full understanding of variables, loops, blocks, and jinja2; check out our Ansible documentation on these subjects:
- [Ansible Variables](http://docs.ansible.com/ansible/playbooks_variables.html)
- [Ansible Loops](http://docs.ansible.com/ansible/playbooks_loops.html)
- [Ansible Handlers](http://docs.ansible.com/ansible/latest/playbooks_blocks.html)

## Section 1 - Using variables in a playbook

To begin, we are going to create a new playbook, and call it router_configs.yml

Navigate to the networking-workshop directory to create a new playbook

```bash
cd ~/networking-workshop
vim router_configs.yml
```
We are going to set 4 variables:
  - **ansible_network_os**: used by the Minimum Viable Platform Agnostic (MVPA) modules (also known as the **_net** modules) to determine the network os type.
  - **dns_servers**: a list of multiple DNS servers we want to configure on `rtr1` and `rtr2`
  - **host1_private_ip**: the private 172.17.X.X address that `host1` is using
  - **control_private_ip**: the private 172.16.X.X address that `ansible` is using


We need to grab the private_ips of the **host1** node and the **ansible** node:

 - The IP address can be determined by private_ip=x.x.x.x located at: `~/networking-workshop/lab_inventory/hosts`

The variable can also be called dynamically by calling hostvars as seen below:

{% raw %}
```yml
---
- name: Router Configurations
  hosts: routers
  gather_facts: no
  connection: local
  vars:
    ansible_network_os: ios
    dns_servers:
      - 8.8.8.8
      - 8.8.4.4
    host1_private_ip: "{{hostva‌rs['host1']['private_ip']}}"
    control_private_ip: "{{hostvars['ansible']['private_ip']}}"
```      
{% endraw %}

## Section 2: Create a block for rtr1
Create a block and add the tasks for rtr1 with conditionals. We’ll also add a comment for better documentation.

{% raw %}
```
    ##Configuration for R1
    - block:
      - name: Static route from R1 to R2
        net_static_route:
          prefix: "{{host1_private_ip}}"
          mask: 255.255.255.255
          next_hop: 10.0.0.2
      - name: configure name servers
        net_system:
          name_servers: "{{item}}"
        with_items: "{{dns_servers}}"
      when:
        - '"rtr1" in inventory_hostname'
```
{% endraw %}

 What the Helsinki is happening here!?
  - `vars:` You’ve told Ansible the next thing it sees will be a variable name.
  - `dns_servers` You are defining a list-type variable called dns_servers. What follows is a list of those the name servers.
  - {% raw %}`{‌{ item }}`{% endraw %} You are telling Ansible that this will expand into a list item like 8.8.8.8 and 8.8.4.4.
  - {% raw %}`with_items: "{‌{ dns_servers }}`{% endraw %} This is your loop which is instructing Ansible to perform this task on every `item` in `dns_servers`
  - `block:` This block will have a number of tasks associated with it.
  - `when:` the when clause is tied to the block. We’re telling ansible to run all the tasks within the block only when certain conditions are met.

## Section 3 - Configuring rtr2

There will be 4 tasks in this block
- net_interface
- ios_config
- net_static_route
- net_system

{% raw %}
```yml
##Configuration for R2
- block:
  - name: enable GigabitEthernet1 interface if compliant
    net_interface:
      name: GigabitEthernet1
      description: interface to host1
      state: present
  - name: dhcp configuration for GigabitEthernet1
    ios_config:
      lines:
        - ip address dhcp
      parents: interface GigabitEthernet1
  - name: Static route from R2 to R1
    net_static_route:
      prefix: "{{control_private_ip}}"
      mask: 255.255.255.255
      next_hop: 10.0.0.1
  - name: configure name servers
    net_system:
      name_servers: "{{item}}"
    with_items: "{{dns_servers}}"
  when:
    - '"rtr2" in inventory_hostname'
```
{% endraw %}

**So…​ what’s going on?**
  - [net_interface](http://docs.ansible.com/ansible/latest/net_interface_module.html): This module allows us to define the state of the interface (up, admin down, etc.) in an agnostic way. In this case, we are making sure that GigabitEthernet1 is up and has the correct description.
  - [ios_config](http://docs.ansible.com/ansible/latest/ios_config_module.html): We’ve used this module in previous playbooks. We could technically combine the two tasks (ip addr + static route). However, it’s sometimes preferred to break out the tasks according to what is being accomplished.
  - [net_system](https://docs.ansible.com/ansible/2.4/net_system_module.html): This module, similar to the net_interface allows us to manage the system attributes on network devices in an agnostic way. We’re utilizing this module along with loops to feed in the name_servers we want the router to have.
  - [net_static_route](https://docs.ansible.com/ansible/2.4/net_static_route_module.html): This module is utilized for managing static IP routes on network devices. It provides declarative management of static IP routes on network devices.

## Section 4 - Review

Your playbook is done! But don’t run it just yet, we’ll do that in our next exercise. For now, let’s take a second look to make sure everything looks the way you intended. If not, now is the time for us to fix it up.

# Complete
You have completed exercise 1.4

# Answer Key
To view and run the completed playbook move on to [Exercise 1.5!](../1.5-run_routing_configs)

 ---
[Click Here to return to the Ansible Lightbulb - Networking Workshop](../README.md)
