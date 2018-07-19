# Exercise 1 - Running Ad-hoc commands

For our first exercise, we are going to run some ad-hoc commands to help you get a feel for how Ansible works.  Ansible Ad-Hoc commands enable you to perform tasks on remote nodes without having to write a playbook.  They are very useful when you simply need to do one or two things quickly and often, to many remote nodes.

## Step 1.1 - Define your Inventory

Define your inventory.  Inventories are crucial to Ansible as they define remote machines on which you wish to run commands or your playbook(s). In this lab the inventory is provided by your instructor. The inventory is an ini formatted file listing your hosts, sorted in groups, additionally providing some variables. It looks like:

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

## Step 1.2 - Ping a host

Let's start with something really basic - pinging a host.  The `ping` module makes sure our web hosts are responsive.

```bash
ansible web -m ping
```

## Step 2:

Now let's see how we can run a good ol' fashioned Linux command and format the output using the `command` module.

```bash
ansible web -m command -a "uptime" -o
```

## Step 3:

Take a look at your web node's configuration.  The `setup` module displays ansible facts (and a lot of them) about an endpoint.

```bash
ansible web -m setup
```

## Step 4:

Now, let's install Apache using the `yum` module.

```bash
ansible web -m yum -a "name=httpd state=present" -b
```

## Step 5:

OK, Apache is installed now so let's start it up using the `service` module.

```bash
ansible web -m service -a "name=httpd state=started" -b
```

## Step 6:

Finally, let's clean up after ourselves.  First, stop the httpd service.

```bash
ansible web -m service -a "name=httpd state=stopped" -b
```

## Step 7:

Next, remove the Apache package.

```bash
ansible web -m yum -a "name=httpd state=absent" -b
```


---
**NOTE**

Like many Linux commands, `ansible` allows for long-form options as well as short-form.  For example:

```bash
ansible web --module-name ping
```

is the same as running

```bash
ansible web -m ping
```

We are going to be using the short-form options throughout this workshop.

---

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.md)
