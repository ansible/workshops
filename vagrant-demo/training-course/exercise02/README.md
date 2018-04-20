# Exercise 02 - Using the os_facts Module

For this exercise we are going to grab specific information from the network.  For every [network platform](https://access.redhat.com/articles/3185021) there is a `os_facts` module.  In this case we are going to use the [vyos_facts](http://docs.ansible.com/ansible/latest/vyos_facts_module.html) module to collect information.  

## Table of Contents

- [The Playbook](#the-playbook)
- [Looking at the results](#looking-at-the-results)
- [Using Specific facts](#using-specific-facts)
- [Looking at the results part 2](#looking-at-the-results-part-2)
- [Complete](#complete)


## The Playbook

Lets first see what information we can gather through facts.  We will register the output from the `vyos_facts` module and use the `debug` module to display it to our terminal.

```yml
---
- hosts: network
  connection: network_cli
  tasks:
    - name: gather facts for vyos
      vyos_facts:
        gather_subset: all
      register: vyos_debug

    - name: look at config
      debug: var=vyos_debug
```

To run the playbook use the `ansible-playbook` command.  The default password is **vagrant** for the vyos vagrant image.

```bash
ansible-playbook facts.yml -u vagrant -k
```
Parameter | Explanation
------------ | -------------
ansible-playbook | Ansible executable for running playbooks
facts.yml | the name of the playbook
-u vagrant | specifies user vagrant
-k | prompts us for password

## Looking at the results

In your terminal window there will be a bunch of JSON output per network device.  Here is an example of output for the leaf02 host:

```yml
<--output above removed for brevity-->
            "ansible_net_hostname": "leaf02",
            "ansible_net_model": "VirtualBox",
            "ansible_net_serialnum": "0",
            "ansible_net_version": "VyOS"
<--output below removed for brevity-->
```

## Using Specific facts

This time instead of debugging the entire output, lets just use a few specific facts per network device.  Here is the next playbook [specific_facts.yml](specific_facts.yml):

```
---
- hosts: network
  connection: network_cli
  tasks:
    - name: gather facts for vyos
      vyos_facts:
        gather_subset: all

    - name: look at config
      debug:
        msg: The device {{ansible_net_hostname}} is model {{ansible_net_model}} running {{ansible_net_version}}
```

## Looking at the results part 2
The debug statement is now much more succinct with just the details we specified:

```bash
TASK [look at config] *********************************************************
ok: [leaf02] => {
    "failed": false,
    "msg": "The device leaf02 is model VirtualBox running VyOS"
}
ok: [spine01] => {
    "failed": false,
    "msg": "The device spine01 is model VirtualBox running VyOS"
}
ok: [leaf01] => {
    "failed": false,
    "msg": "The device leaf01 is model VirtualBox running VyOS"
}
ok: [spine02] => {
    "failed": false,
    "msg": "The device spine02 is model VirtualBox running VyOS"
}
```

**NOTE:** vyos is actually a Linux distribution so it does not run on switch or router hardware like you will see from vendors like Cisco, Juniper, Arista, etc.  The [setup module](http://docs.ansible.com/ansible/latest/setup_module.html) is written for Linux hosts and will also work on VyOS providing much more details.

## Complete
You have completed exercise 02.

[Return to training-course](../README.md)
