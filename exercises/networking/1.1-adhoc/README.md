# Exercise 1.1 - Running Ad-hoc commands

Before you get started, please join us on slack! [Click here to join the ansiblenetwork slack](https://join.slack.com/t/ansiblenetwork/shared_invite/enQtMzEyMTcxMTE5NjM3LWIyMmQ4YzNhYTA4MjA2OTRhZDQzMTZkNWZlN2E3NzhhMWQ5ZTdmNmViNjk2M2JkYzJjODhjMjVjMGUxZjc2MWE).  This will allow you to chat with other network automation engineers and get help after the workshops concludes.

For our first exercise, we are going to run some ad-hoc commands to help you get a feel for how Ansible works. Ansible Ad-Hoc commands enable you to perform tasks on remote nodes without having to write a playbook. They are very useful when you simply need to do one or two things quickly and often, to many remote nodes.

Like many commands, `ansible` allows for long-form options as well as short-form. For example:

```bash
ansible control --module-name ping
```

is the same as running
```
ansible control -m ping
```
We are going to be using the short-form options throughout this workshop

## Table of Contents
 - [Step 1: Ping](#step-1-ping)
 - [Step 2: Command](#step-2-command)
 - [Step 3: ios_facts](#step-3-ios_facts)
 - [Step 4: ios_command](#step-4-ios_command)
 - [Step 5: ios_banner](#step-5-ios_banner)
 - [Step 6: ios_banner removal](#step-6-ios_banner-removal)

### Step 1: Ping

Let’s start with something really basic - pinging a linux host. Note that this is not an ICMP ping but rather a python script being executed on the host.

```bash
ansible control -m ping
```

To figure out all the options associated with an Ansible module each module has a documentation page.  Check out the [Ansible ping module here](http://docs.ansible.com/ansible/latest/ping_module.html)

### Step 2: Command
Now let’s see how we can run a good ol' fashioned Linux command and format the output using the command module.
```bash
ansible control -m command -a "uptime" -o
```

Ansible documentation page for the [command module](http://docs.ansible.com/ansible/latest/command_module.html)

### Step 3: ios_facts

Let’s switch gears and take a look at our routers. The ios_facts module displays ansible facts (and a lot of them) about an ios device.

```bash
ansible routers -m ios_facts -c network_cli
```

Ansible documentation page for the [ios_facts module](http://docs.ansible.com/ansible/latest/ios_facts_module.html)

### Step 4: ios_command

Now, let’s get an interface summary using the ios_command module

```bash
ansible routers -m ios_command -a 'commands="show ip int br"' -c network_cli
```
Ansible documentation for the [ios_command module](http://docs.ansible.com/ansible/latest/ios_command_module.html)
### Step 5: ios_banner
Let's check the banner on the routers before changing them
```bash
ansible routers -m ios_command -a 'commands="show banner motd"' -c network_cli
```
You'll see that we currently have no motd banners

Let's go ahead and add the motd banner using the ios_banner module!

```bash
ansible routers -m ios_banner -a 'banner=motd text="Ansible is awesome!" state=present' -c network_cli
```
Now, let's run our test again to see the change!
```bash
ansible routers -m ios_command -a 'commands="show banner motd"' -c local
```
Ansible documentation on the [ios_banner module](http://docs.ansible.com/ansible/latest/ios_banner_module.html)

### Step 6: ios_banner removal

Finally, let’s revert back and remove the banner.

```bash
ansible routers -m ios_banner -a 'banner=motd state=absent' -c network_cli
```
Feel free to check again using the ios_command

# Complete
You have completed lab exercise 1.1

 ---
[Click Here to return to the Ansible Linklight - Networking Workshop](../README.md)
