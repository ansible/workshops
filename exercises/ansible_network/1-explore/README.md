# Exercise 1 - Exploring the lab environment

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Diagram](#diagram)
- [Guide](#guide)
- [Takeaways](#takeaways)

# Objective

Explore and understand the lab environment.  This exercise will cover
- Determining the Ansible version running on the control node
- Locating and understanding the Ansible configuration file (`ansible.cfg`)
- Locating and understanding an `ini` formatted inventory file

Before you get started, please join us on slack! [Click here to join the ansiblenetwork slack](https://join.slack.com/t/ansiblenetwork/shared_invite/enQtNTU4ODIyNzA1MDkyLThiYmQ3MmNkMWRmOTdjYjMxNzdlNDc4OTk5YTc1ZDBiNDAwOTZlZjE0NDliODJiMjJhMDBkZWM4Nzg2NjkzNDA).  This will allow you to chat with other network automation engineers and get help after the workshops concludes.

# Diagram

![Red Hat Ansible Automation Lab Diagram](../../../images/network_diagram.png)

There are four routers, named rtr1, rtr2, rtr3 and rtr4.  This diagram is always available on the [network automation workshop table of contents](../README.md).  The SSH configuration file (~/.ssh/config) is already setup so you can easily SSH to any router from the control node.

For example to connect to rtr1 from the Ansible control node, type:

```bash
[student1@ansible ~]$ ssh rtr1
```

This will not require a username or password.

# Guide

## Step 1

Navigate to the `network-workshop` directory on the Ansible control node.  The word `ansible` indicates the hostname, and that you are on the correct host.

```
[student1@ansible ~]$ cd ~/network-workshop/
[student1@ansible network-workshop]$
[student1@ansible network-workshop]$ pwd
/home/student1/network-workshop
```
 - `~` - the tilde in this context is a shortcut for `/home/student1`
 - `cd` - Linux command to change directory
 - `pwd` - Linux command for print working directory.  This will show the full path to the current working directory.

## Step 2

Run the `ansible` command with the `--version` command to look at what is configured:


```
[student1@ansible ~]$ ansible --version
ansible 2.8.1
  config file = /home/student1/.ansible.cfg
  configured module search path = [u'/home/student1/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Jun 11 2019, 12:19:05) [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
```

> Note: The ansible version you see might differ from the above output

This command gives you information about the version of Ansible, location of the executable, version of Python, search path for the modules and location of the `ansible configuration file`.

## Step 3

Use the `cat` command to view the contents of the `ansible.cfg` file.

```
[student1@ansible ~]$ cat ~/.ansible.cfg
[defaults]
stdout_callback = yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student1/lab_inventory/hosts
[persistent_connection]
connect_timeout = 60
command_timeout = 60
```

Note the following parameters within the `ansible.cfg` file:

 - `inventory`: shows the location of the ansible inventory being used

## Step 4

The scope of a `play` within a `playbook` is limited to the groups of hosts declared within an Ansible **inventory**. Ansible supports multiple [inventory](http://docs.ansible.com/ansible/latest/intro_inventory.html) types. An inventory could be a simple flat file with a collection of hosts defined within it or it could be a dynamic script (potentially querying a CMDB backend) that generates a list of devices to run the playbook against.

In this lab you will work with a file based inventory written in the **ini** format. Use the `cat` command to view the contents of your inventory:

```bash
[student1@ansible ~]$ cat ~/lab_inventory/hosts
```

```
[all:vars]
ansible_ssh_private_key_file=/home/student1/.ssh/aws-private.pem

[routers:children]
cisco
juniper
arista

[cisco]
rtr1 ansible_host=18.222.121.247 private_ip=172.16.129.86
[arista]
rtr2 ansible_host=18.188.194.126 private_ip=172.17.158.197
rtr4 ansible_host=18.221.5.35 private_ip=172.17.8.111
[juniper]
rtr3 ansible_host=3.14.132.20 private_ip=172.16.73.175

[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios
ansible_connection=network_cli

[juniper:vars]
ansible_user=ec2-user
ansible_network_os=junos
ansible_connection=netconf

[arista:vars]
ansible_user=ec2-user
ansible_network_os=eos
ansible_connection=network_cli
ansible_become=true
ansible_become_method=enable

[dc1]
rtr1
rtr3

[dc2]
rtr2
rtr4

[control]
ansible ansible_host=13.58.149.157 ansible_user=student1 private_ip=172.16.240.184
```

## Step 5

In the above output every `[ ]` defines a group. For example `[dc1]` is a group that contains the hosts `rtr1` and `rtr3`. Groups can also be _nested_. The group `[routers]` is a parent group to the group `[cisco]`

> Parent groups are declared using the `children` directive. Having nested groups allows the flexibility of assigining more specific values to variables.


> Note: A group called **all** always exists and contains all groups and hosts defined within an inventory.


We can associate variables to groups and hosts.

Host variables can be defined on the same line as the host themselves. For example for the host `rtr1`:

```
rtr1 ansible_host=18.222.121.247 private_ip=172.16.129.86
```

 - `rtr1` - The name that Ansible will use.  This can but does not have to rely on DNS
 - `ansible_host` - The IP address that ansible will use, if not configured it will default to DNS
 - `private_ip` - This value is not reserved by ansible so it will default to a [host variable](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables).  This variable can be used by playbooks or ignored completely.

Group variables groups are declared using the `vars` directive. Having groups allows the flexibility of assigning common variables to multiple hosts. Multiple group variables can be defined under the `[group_name:vars]` section. For example look at the group `cisco`:

```
[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios
ansible_connection=network_cli
```

 - `ansible_user` - The user ansible will be used to login to this host, if not configured it will default to the user the playbook is run from
 - `ansible_network_os` - This variable is necessary while using the `network_cli` connection type within a play definition, as we will see shortly.
 - `ansible_connection` - This variable sets the [connection plugin](https://docs.ansible.com/ansible/latest/plugins/connection.html) for this group.  This can be set to values such as `netconf`, `httpapi` and `network_cli` depending on what this particular network platform supports.


# Complete

You have completed lab exercise 1

---
[Click Here to return to the Ansible Network Automation Workshop](../README.md)
