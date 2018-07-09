### Section 1: Exploring the lab environment

#### Step 1

Navigate to the `networking-workshop` directory.

```
[vagrant@ansible ~]$ cd linklight/
[vagrant@ansible linklight]$

```

#### Step 2

Run the `ansible` command with the `--version` command to look at what is configured:

```
[vagrant@ansible linklight]$ ansible --version
ansible 2.7.0.dev0
  config file = /home/vagrant/.ansible.cfg
  configured module search path = [u'/home/vagrant/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Aug  4 2017, 00:39:18) [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)]
```

> Note: The ansible version you see might differ from the above output


This command gives you information about the version of Ansible, location of the executable, version of Python, search path for the modules and location of the `ansible configuration file`.

#### Step 3

Use the `cat` command to view the contents of the `ansible.cfg` file.


```
[vagrant@ansible linklight]$ cat ~/.ansible.cfg
[defaults]
deprecation_warnings=False
host_key_checking = False
inventory = /home/vagrant/linklight/vagrant-demo/arista/hosts
gathering = explicit
[paramiko_connection]
host_key_auto_add = True

```

Note the following parameter within the `ansible.cfg` file:

 - `inventory`: shows the location of the ansible inventory being used



#### Step 4

The scope of a `play` within a `playbook` is limited to the groups of hosts declared within an Ansible **inventory**. Ansible supports multiple [inventory](http://docs.ansible.com/ansible/latest/intro_inventory.html) types. An inventory could be a simple flat file with a collection of hosts defined within it or it could be a dynamic script (potentially querying a CMDB backend) that generates a list of devices to run the playbook against.

In this lab you will work with a file based inventory written in the **ini** format. Use the `cat` command to view the contents of your inventory:


```
[vagrant@ansible linklight]$ cat /home/vagrant/linklight/vagrant-demo/arista/hosts
[leafs]
leaf01 ansible_host=192.168.0.14
leaf02 ansible_host=192.168.0.15

[spines]
spine01 ansible_host=192.168.0.10
spine02 ansible_host=192.168.0.11

[network:children]
leafs
spines

[network:vars]
ansible_network_os=eos
ansible_connection=network_cli
ansible_user=admin
ansible_password=admin

[servers]
server01 ansible_host=192.168.0.31
server02 ansible_host=192.168.0.32

[datacenter:children]
leafs
spines
servers
```

#### Step 5

In the above output every `[ ]` defines a group. For example `[spines]` is a group that contains the hosts `spine01` and `spine02`. Groups can also be _nested_. The group `[network]` is a parent group to the group `[spines]` and `[leafs]`

> Parent groups are declared using the `children` directive. Having nested groups allows the flexibility of assigining more specific values to variables.


> Note: A group called **all** always exists and contains all groups and hosts defined within an inventory.


We can associate variables to groups and hosts. Host variables are declared/defined on the same line as the host themselves. For example for the host `leaf01`:

```
leaf01 ansible_host=192.168.0.14
```

 - `leaf01` - The name that Ansible will use.  This can but does not have to rely on DNS
 - `ansible_host` - The IP address that ansible will use, if not configured it will default to DNS

We can also define variable at a group var, indicated by the groupname:vars, for example `[network:vars]`

```
[network:vars]
ansible_network_os=eos
ansible_connection=network_cli
ansible_user=admin
ansible_password=admin
```

- `ansible_user` - The user ansible will use to login to hosts for this group, if not configured it will default to the user the playbook is run from
- `ansible_connection=network_cli` The connection method can be set in the inventory (or the playbook level).  The `network_cli` plugin is written specifically for network equipment and handles things like ensuring a persistent SSH connection across multiple tasks.
- `ansible_password` - this is the password that will be used to hosts for this group, for demonstration purposes we are using a plain-text password, this can be encrypted with Ansible vault.
- `ansible_network_os` - This variable is necessary while using the `network_cli` connection type within a play definition, as we will see shortly.

## Complete
You have completed Exercise 01.

[Return to training-course](../README.md)
