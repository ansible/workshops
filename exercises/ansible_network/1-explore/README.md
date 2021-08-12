# Exercise 1 - Exploring the lab environment

**Read this in other languages**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md).

## Table of Contents

* [Objective](#objective)
* [Diagram](#diagram)
* [Guide](#guide)

## Objective

Explore and understand the lab environment.  This exercise will cover:

* Determining the `ansible-core` version running on the control node
* Locating and understanding the Ansible configuration file (`ansible.cfg`)
* Locating and understanding an `ini` formatted inventory file

These first few lab exercises will be exploring the command-line utilities of the Ansible Automation Platform.  This includes

- [ansible-navigator](https://github.com/ansible/ansible-navigator) - a command line utility and text-based user interface (TUI) for running and developing Ansible automation content.
- [ansible-core](https://docs.ansible.com/core.html) - the base executable that provides the framework, language and functions that underpin the Ansible Automation Platform.  It also includes various cli tools like `ansible`, `ansible-playbook` and `ansible-doc`.  Ansible Core acts as the bridge between the upstream community with the free and open source Ansible and connects it to the downstream enterprise automation offering from Red Hat, the Ansible Automation Platform.
- [Execution Environments](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) - not specifically covered in this workshop because the built-in Ansible Execution Environments already included all the Red Hat supported collections which includes all the network collections we use for this workshop.  Execution Environments are container images that can be utilized as Ansible execution.
- [ansible-builder](https://github.com/ansible/ansible-builder) - not specifically covered in this workshop, `ansible-builder` is a command line utility to automate the process of building Execution Environments.

If you need more information on new Ansible Automation Platform components bookmark this landing page [https://red.ht/AAP-20](https://red.ht/AAP-20)


<table>
<thead>
  <tr>
    <th>asdf</th>
  </tr>
</thead>
</table>


<table><tr><td>
Before you get started, please join us on slack! <a href="https://join.slack.com/t/ansiblenetwork/shared_invite/zt-3zeqmhhx-zuID9uJqbbpZ2KdVeTwvzw">Click here to join the ansiblenetwork slack</a>.  This will allow you to chat with other network automation engineers and get help after the workshops concludes.  If the link goes stale please email <a href="mailto:ansible-network@redhat.com">Ansible Technical Marketing</a>
</tr></td></table>

## Diagram

![Red Hat Ansible Automation](https://github.com/ansible/workshops/raw/devel/images/ansible_network_diagram.png)

There are four routers, named rtr1, rtr2, rtr3 and rtr4.  This diagram is always available on the [network automation workshop table of contents](../README.md).  The SSH configuration file (~/.ssh/config) is already setup on the control node.  This means you can SSH to any router from the control node without a login:

For example to connect to rtr1 from the Ansible control node, type:

```bash
[student1@ansible ~]$ ssh rtr1
```

## Guide

### Step 1

Navigate to the `network-workshop` directory on the Ansible control node.  The word `ansible` indicates the hostname, and that you are on the correct host.

```bash
[student1@ansible ~]$ cd ~/network-workshop/
[student1@ansible network-workshop]$
[student1@ansible network-workshop]$ pwd
/home/student1/network-workshop
```

* `~` - the tilde in this context is a shortcut for `/home/student1`
* `cd` - Linux command to change directory
* `pwd` - Linux command for print working directory.  This will show the full path to the current working directory.

### Step 2

Run the `ansible` command with the `--version` command to look at what is configured:

```bash
ansible [core 2.11.2]
  config file = /home/student1/.ansible.cfg
  configured module search path = ['/home/student1/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.8/site-packages/ansible
  ansible collection location = /home/student1/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.8.6 (default, Jan 22 2021, 11:41:28) [GCC 8.4.1 20200928 (Red Hat 8.4.1-1)]
  jinja version = 2.10.3
  libyaml = True
```

> Note: The ansible version you see might differ from the above output

This command gives you information about the version of Ansible, location of the executable, version of Python, search path for the modules and location of the `ansible configuration file`.

### Step 3

Use the `cat` command to view the contents of the `ansible.cfg` file.

```bash
[student1@ansible-1 ~]$ cat ~/.ansible.cfg
[defaults]
stdout_callback = community.general.yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student1/lab_inventory/hosts
[persistent_connection]
connect_timeout = 200
command_timeout = 200
```

Note the following parameters within the `ansible.cfg` file:

* `inventory`: shows the location of the ansible inventory being used

For a full listing of every configurable knob checkout the [example ansible.cfg on Github](https://github.com/ansible/ansible/blob/devel/examples/ansible.cfg)

### Step 4

The scope of a `play` within a `playbook` is limited to the groups of hosts declared within an Ansible **inventory**. Ansible supports multiple [inventory](http://docs.ansible.com/ansible/latest/intro_inventory.html) types. An inventory could be a simple flat file with a collection of hosts defined within it or it could be a dynamic script (potentially querying a CMDB backend) that generates a list of devices to run the playbook against.

In this lab you will work with a file based inventory written in the **ini** format. Use the `cat` command to view the contents of your inventory:

```bash
[student1@ansible ~]$ cat ~/lab_inventory/hosts
```

```bash
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

### Step 5

In the above output every `[ ]` defines a group. For example `[dc1]` is a group that contains the hosts `rtr1` and `rtr3`. Groups can also be _nested_. The group `[routers]` is a parent group to the group `[cisco]`

> Parent groups are declared using the `children` directive. Having nested groups allows the flexibility of assigining more specific values to variables.

We can associate variables to groups and hosts.

> Note: A group called **all** always exists and contains all groups and hosts defined within an inventory.

Host variables can be defined on the same line as the host themselves. For example for the host `rtr1`:

```sh
rtr1 ansible_host=18.222.121.247 private_ip=172.16.129.86
```

* `rtr1` - The name that Ansible will use.  This can but does not have to rely on DNS
* `ansible_host` - The IP address that ansible will use, if not configured it will default to DNS
* `private_ip` - This value is not reserved by ansible so it will default to a [host variable](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables).  This variable can be used by playbooks or ignored completely.

Group variables groups are declared using the `vars` directive. Having groups allows the flexibility of assigning common variables to multiple hosts. Multiple group variables can be defined under the `[group_name:vars]` section. For example look at the group `cisco`:

```sh
[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios
ansible_connection=network_cli
```

* `ansible_user` - The user ansible will be used to login to this host, if not configured it will default to the user the playbook is run from
* `ansible_network_os` - This variable is necessary while using the `network_cli` connection type within a play definition, as we will see shortly.
* `ansible_connection` - This variable sets the [connection plugin](https://docs.ansible.com/ansible/latest/plugins/connection.html) for this group.  This can be set to values such as `netconf`, `httpapi` and `network_cli` depending on what this particular network platform supports.

### Step 6

We can also use the `ansible-navigator` TUI to explore inventory.

Run the `ansible-navigator inventory` command to bring up inventory in the TUI:

![ansible-navigator tui](images/ansible-navigator.png)

Pressing **0** or **1** on your keyboard will open groups or hosts respectively.

![ansible-navigator groups](images/ansible-navigator-groups.png)

Press the **Esc** key to go up a level, or you can zoom in to an individual host:

![ansible-navigator host](images/ansible-navigator-rtr-1.png)

## Complete

You have completed lab exercise 1

---
[Click Here to return to the Ansible Network Automation Workshop](../README.md)
