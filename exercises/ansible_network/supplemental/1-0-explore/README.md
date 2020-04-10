# Exercise 1.0 - Exploring the lab environment

Before you get started, please join us on slack! [Click here to join the ansiblenetwork slack](https://join.slack.com/t/ansiblenetwork/shared_invite/enQtMzEyMTcxMTE5NjM3LWIyMmQ4YzNhYTA4MjA2OTRhZDQzMTZkNWZlN2E3NzhhMWQ5ZTdmNmViNjk2M2JkYzJjODhjMjVjMGUxZjc2MWE).  This will allow you to chat with other network automation engineers and get help after the workshops concludes.

## Step 1

Navigate to the `networking-workshop` directory.


```
[student1@ansible ~]$ cd networking-workshop/
[student1@ansible networking-workshop]$
[student1@ansible networking-workshop]$

```

## Step 2

Run the `ansible` command with the `--version` command to look at what is configured:


```
[student1@ansible networking-workshop]$ ansible --version
ansible 2.6.2
  config file = /home/student1/.ansible.cfg
  configured module search path = [u'/home/student1/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, May  3 2017, 07:55:04) [GCC 4.8.5 20150623 (Red Hat 4.8.5-14)]
[student1@ansible networking-workshop]$


```

> Note: The ansible version you see might differ from the above output


This command gives you information about the version of Ansible, location of the executable, version of Python, search path for the modules and location of the `ansible configuration file`.

## Step 3

Use the `cat` command to view the contents of the `ansible.cfg` file.

```
[student1@ansible networking-workshop]$ cat ~/.ansible.cfg
[defaults]
connection = smart
timeout = 60
inventory = /home/student1/networking-workshop/lab_inventory/hosts
host_key_checking = False
private_key_file = /home/student1/.ssh/aws-private.pem
[student1@ansible networking-workshop]$

```

Note the following parameters within the `ansible.cfg` file:

 - `inventory`: shows the location of the ansible inventory being used
 - `private_key_file`: this shows the location of the private key used to login to devices



## Step 4

The scope of a `play` within a `playbook` is limited to the groups of hosts declared within an Ansible **inventory**. Ansible supports multiple [inventory](http://docs.ansible.com/ansible/latest/intro_inventory.html) types. An inventory could be a simple flat file with a collection of hosts defined within it or it could be a dynamic script (potentially querying a CMDB backend) that generates a list of devices to run the playbook against.

In this lab you will work with a file based inventory written in the **ini** format. Use the `cat` command to view the contents of your inventory:


```

[student1@ansible ~]$ cat ~/networking-workshop/lab_inventory/hosts
[all:vars]
ansible_port=22

[routers:children]
cisco
juniper

[cisco]
rtr1 ansible_host=35.182.226.163 private_ip=172.16.173.57
rtr2 ansible_host=35.183.197.179 private_ip=172.17.88.89

[juniper]
rtr3 ansible_host=35.183.209.131 private_ip=172.16.119.246
rtr4 ansible_host=35.183.244.146 private_ip=172.17.211.127

[cisco:vars]
ansible_user=ec2-user
ansible_network_os=ios

[juniper:vars]
ansible_user=jnpr
ansible_network_os=junos

[dc1]
rtr1
rtr3

[dc2]
rtr2
rtr4

[hosts]
node1 ansible_host=35.183.19.221 ansible_user=ec2-user private_ip=172.17.179.150

[control]
ansible ansible_host=35.183.137.160 ansible_user=ec2-user private_ip=172.16.45.102
[student1@ansible ~]$

```

## Step 5

In the above output every `[ ]` defines a group. For example `[dc1]` is a group that contains the hosts `rtr1` and `rtr2`. Groups can also be _nested_. The group `[routers]` is a parent group to the group `[cisco]`

> Parent groups are declared using the `children` directive. Having nested groups allows the flexibility of assigining more specific values to variables.


> Note: A group called **all** always exists and contains all groups and hosts defined within an inventroy.


We can associate variables to groups and hosts. Host variables are declared/defined on the same line as the host themselves. For example for the host `rtr1`:

```
rtr1 ansible_host=52.90.196.252 ansible_ssh_user=ec2-user private_ip=172.16.165.205 ansible_network_os=ios

```

 - `rtr1` - The name that Ansible will use.  This can but does not have to rely on DNS
 - `ansible_host` - The IP address that ansible will use, if not configured it will default to DNS
 - `ansible_ssh_user` - The user ansible will use to login to this host, if not configured it will default to the user the playbook is run from
 - `private_ip` - This value is not reserved by ansible so it will default to a [host variable](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables).  This variable can be used by playbooks or ignored completely.
- `ansible_network_os` - This variable is necessary while using the `network_cli` connection type within a play definition, as we will see shortly.

# Complete

You have completed lab exercise 1.0

---
[Click Here to return to the Ansible Linklight - Networking Workshop](../../README.md)
