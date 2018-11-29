# Exercise 1.4 - Additional router configurations

Previous exercises showed you the basics of Ansible. In the exercise, we will build upon that and introduce additional Ansible concepts that allow you to add flexibility and power to your playbooks.

## Table of Contents
 - [Intro](#intro)
 - [Section 1 - Using variables in a playbook](#section-1---using-variables-in-a-playbook)
 - [Section 2 - Create a block for rtr1](#section-2---create-a-block-for-rtr1)
 - [Section 3 - Configuring rtr2](#section-3---configuring-rtr2)
 - [Section 4 - Running your routing_configs playbook](#section-4---running-your-routing_configs-playbook)
 - [Section 5: Review](#section-5-review)
 - [Section 6: Test!](#section-6-test)

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
  - **ansible_network_os**: used to determine the network os type.
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
  connection: network_cli
  vars:
    ansible_network_os: ios
    dns_servers:
      - 8.8.8.8
      - 8.8.4.4
    host1_private_ip: "{{hostvars['host1']['private_ip']}}"
    control_private_ip: "{{hostvars['ansible']['private_ip']}}"
```      
{% endraw %}

## Section 2: Create a block for rtr1
Create a block and add the tasks for rtr1 with conditionals. We’ll also add a comment for better documentation.

{% raw %}
```
  tasks:
    ##Configuration for R1
    - block:
      - name: Static route from R1 to R2
        ios_static_route:
          prefix: "{{host1_private_ip}}"
          mask: 255.255.255.255
          next_hop: 10.0.0.2
      - name: configure name servers
        ios_system:
          name_servers: "{{item}}"
        with_items: "{{dns_servers}}"
      when:
        - '"rtr1" in inventory_hostname'
```
{% endraw %}

 What is happening here!?
  - `vars:` You’ve told Ansible the next thing it sees will be a variable name.
  - `dns_servers` You are defining a list-type variable called dns_servers. What follows is a list of those the name servers.
  - {% raw %}`{{ item }}`{% endraw %} You are telling Ansible that this will expand into a list item like 8.8.8.8 and 8.8.4.4.
  - {% raw %}`with_items: "{{ dns_servers }}`{% endraw %} This is your loop which is instructing Ansible to perform this task on every `item` in `dns_servers`
  - `block:` This block will have a number of tasks associated with it.
  - `when:` the when clause is tied to the block. We’re telling ansible to run all the tasks within the block only when certain conditions are met.

## Section 3 - Configuring rtr2

There will be 4 tasks in this block
- ios_interface
- ios_config
- ios_static_route
- ios_system

{% raw %}
```yml
    ##Configuration for R2
    - block:
      - name: enable GigabitEthernet1 interface if compliant
        ios_interface:
          name: GigabitEthernet1
          description: interface to host1
          state: present
      - name: dhcp configuration for GigabitEthernet1
        ios_config:
          lines:
            - ip address dhcp
          parents: interface GigabitEthernet1
      - name: Static route from R2 to R1
        ios_static_route:
          prefix: "{{control_private_ip}}"
          mask: 255.255.255.255
          next_hop: 10.0.0.1
      - name: configure name servers
        ios_system:
          name_servers: "{{item}}"
        with_items: "{{dns_servers}}"
      when:
        - '"rtr2" in inventory_hostname'
```
{% endraw %}

**So…​ what’s going on?**
  - [ios_interface](http://docs.ansible.com/ansible/latest/ios_interface_module.html): This module allows us to define the state of the interface (up, admin down, etc.) in an agnostic way. In this case, we are making sure that GigabitEthernet1 is up and has the correct description.
  - [ios_config](http://docs.ansible.com/ansible/latest/ios_config_module.html): We’ve used this module in previous playbooks. We could technically combine the two tasks (ip addr + static route). However, it’s sometimes preferred to break out the tasks according to what is being accomplished.
  - [ios_system](https://docs.ansible.com/ansible/2.4/ios_system_module.html): This module, similar to the ios_interface allows us to manage the system attributes on network devices in an agnostic way. We’re utilizing this module along with loops to feed in the name_servers we want the router to have.
  - [ios_static_route](https://docs.ansible.com/ansible/2.4/ios_static_route_module.html): This module is utilized for managing static IP routes on network devices. It provides declarative management of static IP routes on network devices.

## Section 4 - Running your routing_configs playbook

### Step 1: Make sure you are in the right directory.

```bash
cd ~/networking-workshop
```

### Step 2: Run your playbook

```bash
ansible-playbook router_configs.yml
```

## Section 5: Review

If successful, you should see standard output that looks very similar to the following. If not, just let us know. We’ll help get things fixed up.

![Figure 1: routing_configs stdout](playbookrun.png)

If the output is similar to the above, you have successfully run the playbook.

So, let’s briefly review what we accomplished:

 - We declared variables that lists the name servers we want to apply.
 - We then registered the values produced by the ios_facts module to use in the subsequent tasks in our playbook.
 - Next we created a block with a conditionals {using inventory_hostname}
 - If the conditionals were met, for rtr1, we applied the static route and name server configuration.
 - For rtr2 we enabled GigabitEthernet2 & configured it to receive an IP address from DHCP + the similar configurations that rtr1 received. {Static route & name servers}

## Section 6: Test!

You should now be able to ping your host that resides in a different VPC! We’ve bridged the two VPC’s via a GRE tunnel and added static routes to allow routing between the two subnets.

```bash
ping <private IP of host node>
```

IP of the host node is shown as private_ip=172.16.x.x in your inventory file @ ~/networking-workshop/lab_inventory/hosts

For example:
```bash
[ec2-user@ip-172-17-3-27 networking-workshop]$ ping 172.18.4.188
PING 172.18.4.188 (172.18.4.188) 56(84) bytes of data.
64 bytes from 172.18.4.188: icmp_seq=2 ttl=62 time=2.58 ms
64 bytes from 172.18.4.188: icmp_seq=3 ttl=62 time=3.52 ms
```
**Note** your IP will be different than 172.18.4.188!

**Help!** The ping doesn't work?
Sometimes the host routes (the route from the ansible control node to rtr1, and the host1 node to rtr2 are incorrectly setup, this should have been done by the provisioner, but we can fix it quickly with Ansible!)

Run the `host-routes.yml` playbook!

```bash
ansible-playbook host-routes.yml
```

# Answer Key
You can [click here](https://github.com/network-automation/linklight/blob/master/exercises/networking/1.4-router_configs/router_configs.yml).

# Complete
You have completed exercise 1.4

 ---
[Click Here to return to the Ansible Linklight - Networking Workshop](../README.md)
