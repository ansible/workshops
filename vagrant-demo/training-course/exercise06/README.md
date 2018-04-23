# Exercise 05 - Configuring ACLs

For this exercise we are going to configure [Access Lists](https://en.wikipedia.org/wiki/Access_control_list) using the [vyos_config](http://docs.ansible.com/ansible/latest/vyos_config_module.html) module.  For this particular exercise we are going to create a rule on spine01, that blocks everyone from reaching his loopback address 10.0.0.1/32.

## Table of Contents

- [Intro to ACLs on vyos](#intro-to-acls-on-vyos)
- [os_config using lines parameter](#os_config-using-lines-parameter)
- [Using Templates](#using-templates)
- [The Playbook](#the-playbook)
- [Looking at the results](#looking-at-the-results)
- [Complete](#complete)



## Intro to ACLs on vyos

We are showing one way to configure an ACL on the vyos platform.  To read more [please read their documentation](https://wiki.vyos.net/wiki/User_Guide#Firewall).  This intro is being provided because ACLs on vyos can be slightly different from both iptables (netfilter) and Cisco IOS.

To create an ACL on vyos, we use the special keyword **firewall**.  First we will create a group, which is where we define our network.

```bash
set firewall group network-group BLOCK_LOOPBACK network '10.0.0.1/32'
```

Then we will build the actual rule with just the **firewall name**.  For simplicity we will make the network-group and firewall name the same thing.  We are going to do 3 things:

- make the rule **action** reject
- make the destination **10.0.0.1/32** (tie it to the network-group)
- block all protocols

Here is the vyos commands that would be applied in configuration mode:
```bash  
set firewall name BLOCK_LOOPBACK rule 10 action 'reject'
set firewall name BLOCK_LOOPBACK rule 10 destination group network-group 'BLOCK_LOOPBACK'
set firewall name BLOCK_LOOPBACK rule 10 protocol 'all'
```

## os_config using lines parameter

It is possible to use the vyos_config module to simply apply the set commands to the vyos box.

```yml
- name: show configuration on ethernet devices eth0 and eth1
  vyos_config:
    lines:
      - set firewall group network-group BLOCK_LOOPBACK network '10.0.0.1/32'
      - set firewall name BLOCK_LOOPBACK rule 10 action 'reject'
      - set firewall name BLOCK_LOOPBACK rule 10 destination group network-group 'BLOCK_LOOPBACK'
      - set firewall name BLOCK_LOOPBACK rule 10 protocol 'all'
```

A [loop](http://docs.ansible.com/ansible/latest/playbooks_loops.html) can be used to cycle through multiple access lists.  However it is more scalable to create a jinja2 template and push it to the device (see next section).

## Using Templates

We can use templates combined with vyos_config to make a more scalable solution.

Lets start by making a simple yaml dictionary that represents a rule.  This is an example, and is user defined.  We could be more or less granular with the amount of knobs we show (in the form of a key value pairs in the dictionary).  For example in the following example we are not showing a knob for blocking or accepting ACls based on the source, but only showing how to block based on the destination:

```yaml
- name: BLOCK_LOOPBACK
  ipv4_network_dest: 10.0.0.1/32
  sequence: 10
  action: reject
  protocol: all
  interfaces: ["eth2", "eth3"]
```

This dictionary can also be written in an abbreviated form:
```yaml
- { name: BLOCK_LOOPBACK, ipv4_network_dest: 10.0.0.1/32, sequence: 10, action: reject, protocol: all, interfaces: ["eth2", "eth3"] }
```

Look at the [template by clicking here](acl.j2).  The template could be provided in two ways:

- show configuration - which shows the rendered configuration
- show configuration commands - which shows the commands that build the rendered configuration

we will built a template based on the rendered configuration, but we could easily do either method depending on someone's preference.

Here is a snipped from the full [acl.j2](acl.j2):

```jinja2
{% for dict in acl_data[inventory_hostname] -%}
network-group {{ dict["name"] }}
    network {{ dict["ipv4_network_dest"] }}
{% endfor -%}
```

For our demonstration we only have 1 dictionary, so the loop is not necessary (but makes this more future-proof and scalable).  Running the template module (or os_config module) on the above jinja2 template will render:

```
network-group BLOCK_LOOKBACK {
    network 10.0.0.1/32
}
```


## The Playbook

Look at the following playbook:

```yml
---
- hosts: spine01
  connection: network_cli
  vars:
    acl_data:
      spine01:
          - { name: BLOCK_LOOPBACK, ipv4_network_dest: 10.0.0.1/32, sequence: 10, action: reject, protocol: all, interfaces: ["eth2", "eth3"] }
  tasks:
    - name: push config to device
      vyos_config:
        src: ./acl.j2
        save: yes
```

To run the playbook use the `ansible-playbook` command.  The default password is **vagrant** for the vyos vagrant image.

```bash
ansible-playbook acl.yml -u vagrant -k
```
Parameter | Explanation
------------ | -------------
ansible-playbook | Ansible executable for running playbooks
system.yml | the name of the playbook
-u vagrant | specifies user vagrant
-k | prompts us for password

# Looking at the results

Login to a device other than spine01:
```
ssh vagrant@spine02
```

Use the `ping` command to make sure we get a **Destination Port Unreachable**

```
vagrant@spine02:~$ ping 10.0.0.1 count 4
PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
From 10.0.0.1 icmp_seq=1 Destination Port Unreachable
From 10.0.0.1 icmp_seq=2 Destination Port Unreachable
From 10.0.0.1 icmp_seq=3 Destination Port Unreachable
From 10.0.0.1 icmp_seq=4 Destination Port Unreachable

--- 10.0.0.1 ping statistics ---
4 packets transmitted, 0 received, +4 errors, 100% packet loss, time 2998ms
```

## Complete
You have completed exercise 06.

[Return to training-course](../README.md)
