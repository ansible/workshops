# Workshop Exercise - Running Ad-hoc commands

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
* [Step 1 - Work with your Inventory](#step-1---work-with-your-inventory)
* [Step 2 - The Ansible Configuration Files](#step-2---the-ansible-configuration-files)
* [Step 3 - Ping a host](#step-3---ping-a-host)
* [Step 4 - Listing Modules and Getting Help](#step-4---listing-modules-and-getting-help)
* [Step 5 - Use the command module:](#step-5---use-the-command-module)
* [Step 6 - The copy module and permissions](#step-6---the-copy-module-and-permissions)
* [Challenge Lab: Modules](#challenge-lab-modules)

# Objective

For our first exercise, we are going to run some ad-hoc commands to help you get a feel for how Ansible works.  Ansible Ad-Hoc commands enable you to perform tasks on remote nodes without having to write a playbook.  They are very useful when you simply need to do one or two things quickly and often, to many remote nodes.

This exercise will cover
- Locating and understanding the Ansible configuration file (`ansible.cfg`)
- Locating and understanding an `ini` formatted inventory file
- Executing ad hoc commands

# Guide

## Step 1 - Work with your Inventory

To use the ansible command for host management, you need to provide an inventory file which defines a list of hosts to be managed from the control node. In this lab the inventory is provided by your instructor. The inventory is an ini formatted file listing your hosts, sorted in groups, additionally providing some variables. It looks like:

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
ansible ansible_host=44.55.66.77
```

Ansible is already configured to use the inventory specific to your environment. We will show you in the next step how that is done. For now, we will execute some simple commands to work with the inventory.

To reference inventory hosts, you supply a host pattern to the ansible command. Ansible has a `--list-hosts` option which can be useful for clarifying which managed hosts are referenced by the host pattern in an ansible command.

The most basic host pattern is the name for a single managed host listed in the inventory file. This specifies that the host will be the only one in the inventory file that will be acted upon by the ansible command. Run:

```bash
[student<X@>ansible ~]$ ansible node1 --list-hosts
  hosts (1):
    node1
```

An inventory file can contain a lot more information, it can organize your hosts in groups or define variables. In our example, the current inventory has the groups `web` and `control`. Run Ansible with these host patterns and observe the output:

```bash
[student<X@>ansible ~]$ ansible web  --list-hosts
[student<X@>ansible ~]$ ansible web,ansible --list-hosts
[student<X@>ansible ~]$ ansible 'node*' --list-hosts
[student<X@>ansible ~]$ ansible all --list-hosts
```

As you see it is OK to put systems in more than one group. For instance, a server could be both a web server and a database server. Note that in Ansible the groups are not necessarily hierarchical.

> **Tip**
>
> The inventory can contain more data. E.g. if you have hosts that run on non-standard SSH ports you can put the port number after the hostname with a colon. Or you could define names specific to Ansible and have them point to the "real" IP or hostname.

## Step 2 - The Ansible Configuration Files

The behavior of Ansible can be customized by modifying settings in Ansible’s ini-style configuration file. Ansible will select its configuration file from one of several possible locations on the control node, please refer to the [documentation](https://docs.ansible.com/ansible/latest/reference_appendices/config.html).

> **Tip**
>
> The recommended practice is to create an `ansible.cfg` file in the directory from which you run Ansible commands. This directory would also contain any files used by your Ansible project, such as the inventory and playbooks. Another recommended practice is to create a file `.ansible.cfg` in your home directory.

In the lab environment provided to you an `.ansible.cfg` file has already been created and filled with the necessary details in the home directory of your `student<X>` user on the control node:

```bash
[student<X>@ansible ~]$ ls -la .ansible.cfg
-rw-r--r--. 1 student<X> student<X> 231 14. Mai 17:17 .ansible.cfg
```

Output the content of the file:

```bash
[student<X>@ansible ~]$ cat .ansible.cfg
[defaults]
stdout_callback = yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student<X>/lab_inventory/hosts
```

There are multiple configuration flags provided. Most of them are not of interest here, but make sure to note the last line: there the location of the inventory is provided. That is the way Ansible knew in the previous commands what machines to connect to.

Output the content of your dedicated inventory:

```bash
[student<X>@ansible ~]$ cat /home/student<X>/lab_inventory/hosts
[all:vars]
ansible_user=student<X>
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[control]
ansible ansible_host=44.55.66.77
```

> **Tip**
>
> Note that each student has an individual lab environment. The IP addresses shown above are only an example and the IP addresses of your individual environments are different. As with the other cases, replace **\<X\>** with your actual student number.

## Step 3 - Ping a host

> **Warning**
>
> **Don’t forget to run the commands from the home directory of your student user, `/home/student<X>`. That is where your `.ansible.cfg` file is located, without it Ansible will not know what which inventory to use.**

Let's start with something really basic - pinging a host. To do that we use the Ansible `ping` module. The `ping` module makes sure our target hosts are responsive. Basically, it connects to the managed host, executes a small script there and collects the results. This ensures that the managed host is reachable and that Ansible is able to execute commands properly on it.

> **Tip**
>
> Think of a module as a tool which is designed to accomplish a specific task.

Ansible needs to know that it should use the `ping` module: The `-m` option defines which Ansible module to use. Options can be passed to the specified modul using the `-a` option.

```bash
[student<X>@ansible ~]$ ansible web -m ping
node2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
[...]
```

As you see each node reports the successful execution and the actual result - here "pong".

## Step 4 - Listing Modules and Getting Help

Ansible comes with a lot of modules by default. To list all modules run:

```bash
[student<X>@ansible ~]$ ansible-doc -l
```

> **Tip**
>
> In `ansible-doc` leave by pressing the button `q`. Use the `up`/`down` arrows to scroll through the content.

To find a module try e.g.:

```bash
[student<X>@ansible ~]$ ansible-doc -l | grep -i user
```

Get help for a specific module including usage examples:

```bash
[student<X>@ansible ~]$ ansible-doc user
```

> **Tip**
>
> Mandatory options are marked by a "=" in `ansible-doc`.

## Step 5 - Use the command module:

Now let's see how we can run a good ol' fashioned Linux command and format the output using the `command` module. It simply executes the specified command on a managed host:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a "id"
node1 | CHANGED | rc=0 >>
uid=1001(student1) gid=1001(student1) Gruppen=1001(student1) Kontext=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```
In this case the module is called `command` and the option passed with `-a` is the actual command to run. Try to run this ad hoc command on all managed hosts using the `all` host pattern.

Another example: Have a quick look at the kernel versions your hosts are running:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r'
```

Sometimes it’s desirable to have the output for a host on one line:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r' -o
```

> **Tip**
>
> Like many Linux commands, `ansible` allows for long-form options as well as short-form.  For example `ansible web --module-name ping` is the same as running `ansible web -m ping`.  We are going to be using the short-form options throughout this workshop.

## Step 6 - The copy module and permissions

Using the `copy` module, execute an ad hoc command on `node1` to change the contents of the `/etc/motd` file. **The content is handed to the module through an option in this case**.

Run the following, but **expect an error**:

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd'
```

As mentioned this produces an **error**:

```bash
    node1 | FAILED! => {
        "changed": false,
        "checksum": "a314620457effe3a1db7e02eacd2b3fe8a8badca",
        "failed": true,
        "msg": "Destination /etc not writable"
    }
```

The output of the ad hoc command is screaming **FAILED** in red at you. Why? Because user **student\<X\>** is not allowed to write the motd file.

Now this is a case for privilege escalation and the reason `sudo` has to be setup properly. We need to instruct Ansible to use `sudo` to run the command as root by using the parameter `-b` (think "become").

> **Tip**
>
> Ansible will connect to the machines using your current user name (student\<X\> in this case), just like SSH would. To override the remote user name, you could use the `-u` parameter.

For us it’s okay to connect as `student<X>` because `sudo` is set up. Change the command to use the `-b` parameter and run again:

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd' -b
```

This time the command is a success:

```
node1 | CHANGED => {
    "changed": true,
    "checksum": "4458b979ede3c332f8f2128385df4ba305e58c27",
    "dest": "/etc/motd",
    "gid": 0,
    "group": "root",
    "md5sum": "65a4290ee5559756ad04e558b0e0c4e3",
    "mode": "0644",
    "owner": "root",
    "secontext": "system_u:object_r:etc_t:s0",
    "size": 19,
    "src": "/home/student1/.ansible/tmp/ansible-tmp-1557857641.21-120920996103312/source",
    "state": "file",
    "uid": 0
```

Use Ansible with the generic `command` module to check the content of the motd file:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a 'cat /etc/motd'
node1 | CHANGED | rc=0 >>
Managed by Ansible
```

Run the `ansible node1 -m copy …​` command from above again. Note:

  - The different output color (proper terminal config provided).
  - The change from `"changed": true,` to `"changed": false,`.
  - The first line says `SUCCESS` instead of `CHANGED`.

> **Tip**
>
> This makes it a lot easier to spot changes and what Ansible actually did.

## Challenge Lab: Modules

  - Using `ansible-doc`

      - Find a module that uses Yum to manage software packages.

      - Look up the help examples for the module to learn how to install a package in the latest version.

  - Run an Ansible ad hoc command to install the package "squid" in the latest version on `node1`.

> **Tip**
>
> Use the copy ad hoc command from above as a template and change the module and options.

> **Warning**
>
> **Solution below\!**

```
[student<X>@ansible ~]$ ansible-doc -l | grep -i yum
[student<X>@ansible ~]$ ansible-doc yum
[student<X>@ansible ~]$ ansible node1 -m yum -a 'name=squid state=latest' -b
```

----
**Navigation**
<br>
[Previous Exercise](../1.1-setup) - [Next Exercise](../1.3-playbook)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
