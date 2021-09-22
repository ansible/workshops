# Workshop Exercise - The Ansible Basics

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
* [Step 1 - Work with your Inventory](#step-1---work-with-your-inventory)
* [Step 2 - Listing Modules and Getting Help](#step-2---listing-modules-and-getting-help)

## Objective

In this exercise, we are going to explore the latest Ansible command line utility `ansible-navigator` to learn how to work with inventory files and the listing of modules when needing assistance. The goal is to familarize yourself with how `ansible-navigator` works and how it can be used to enrich your Ansible experience. 

This exercise will cover

* Working with inventory files
* Locating and understanding an `ini` formatted inventory file
* Listing modules and getting help when trying to use them

## Guide

### Step 1 - Work with your Inventory

An inventory file is a text file that specifices the nodes that will be managed by the control machine. The nodes to be managed may include a list of hostnames or IP addresses of those nodes. The inventory file allows for nodes to be organized into groups by declaring a host group name within square brackets ([]).

To use the `ansible-navigator` command for host management, you need to provide an inventory file which defines a list of hosts to be managed from the control node. In this lab, the inventory is provided by your instructor. The inventory file is an `ini` formatted file listing your hosts, sorted in groups, additionally providing some variables. It looks like:

```bash
[all:vars]
ansible_user=student1
ansible_ssh_pass=PASSWORD
ansible_port=22

[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible-1 ansible_host=44.55.66.77
```

Ansible is already configured to use the inventory specific to your environment. We will show you in the next step how that is done. For now, we will execute some simple commands to work with the inventory.

To reference all the inventory hosts, you supply a pattern to the `ansible-navigator` command. `ansible-navigator inventory` has a `--list` option which can be useful for displaying all the hosts that are part of an inventory file including what groups they are assocaited with. 


```bash
[student<X>@ansible-1 rhel_workshop]$ cd /home/student<X>
[student<X>@ansible-1 ~]$ ansible-navigator inventory --list -m stdout
{
    "_meta": {
        "hostvars": {
            "ansible-1": {
                "ansible_host": "3.236.186.92",
                "ansible_port": 22,
                "ansible_ssh_pass": "password",
                "ansible_user": "student1"
            },
            "node1": {
                "ansible_host": "3.239.234.187",
                "ansible_port": 22,
                "ansible_ssh_pass": "password",
                "ansible_user": "student1"
            },
            "node2": {
                "ansible_host": "75.101.228.151",
                "ansible_port": 22,
                "ansible_ssh_pass": "password",
                "ansible_user": "student1"
            },
            "node3": {
                "ansible_host": "100.27.38.142",
                "ansible_port": 22,
                "ansible_ssh_pass": "password",
                "ansible_user": "student1"
            }
        }
    },
    "all": {
        "children": [
            "control",
            "ungrouped",
            "web"
        ]
    },
    "control": {
        "hosts": [
            "ansible-1"
        ]
    },
    "web": {
        "hosts": [
            "node1",
            "node2",
            "node3"
        ]
    }
}

```

NOTE: `-m` is short for `--mode` which allows for the mode to be switched to standard output instead of using the text-based user interface (TUI).

If the `--list` is too verbose, the option of `--graph` can be used to provide a more condensed version of `--list`.

```bash
[student1@ansible-1 ~]$ ansible-navigator inventory --graph -m stdout
@all:
  |--@control:
  |  |--ansible-1
  |--@ungrouped:
  |--@web:
  |  |--node1
  |  |--node2
  |  |--node3

```

We can clearly see that nodes: `node1`, `node2`, `node3` are part of the `web` group, while `ansible-1` is part of the `control` group.


An inventory file can contain a lot more information, it can organize your hosts in groups or define variables. In our example, the current inventory has the groups `web` and `control`. Run Ansible with these host patterns and observe the output:

Using the `ansible-navigator inventory` command, we can also run commands that provide information only for one host or group. For example, give the following commands a try to see their output. 

```bash
[student<X>@ansible-1 ~]$ ansible-navigator inventory --graph web -m stdout
[student<X>@ansible-1 ~]$ ansible-navigator inventory --graph control -m stdout
[student<X>@ansible-1 ~]$ ansible-navigator inventory --host node1 -m stdout
```

> **Tip**
>
> The inventory can contain more data. E.g. if you have hosts that run on non-standard SSH ports you can put the port number after the hostname with a colon. Or you could define names specific to Ansible and have them point to the "real" IP or hostname.


### Step 2 - Listing Modules and Getting Help

Ansible comes with a lot of modules by default. To list all modules run:

```bash
[student<X>@ansible-1 ~]$ ansible-navigator doc -l -m stdout
```

> **Tip**
>
> In `ansible-navigator doc` leave by pressing the button `q`. Use the `up`/`down` arrows to scroll through the content.

To find a module try e.g.:

```bash
[student<X>@ansible-1 ~]$ ansible-navigator doc -l -m stdout | grep -i user
```

Get help for a specific module including usage examples:

```bash
[student<X>@ansible-1 ~]$ ansible-navigator doc user -m stdout
```

---
**Navigation**
<br>
[Previous Exercise](../1.1-setup) - [Next Exercise](../1.3-playbook)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
