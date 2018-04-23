# Exercise 01 - Performing Configuration Backups

For this exercise we are going to start with a brown field problem.  One of the first things people want to automate is configuration backup.  For this exercise we will be using the [vyos_config module](http://docs.ansible.com/ansible/latest/vyos_config_module.html).  We will use Ansible to grab configurations from the network, and store them locally on the ansible control node (where Ansible is being executed from).

# DEFAULT USERNAME AND PASSWORD FOR VYOS

If you are running these training exercises on vagrant (default)
**username**: vagrant
**password**: vagrant

If you are using a non-vagrant vyos image:
**username**: vyos
**password**: vyos

## Table of Contents

- [The Playbook](#the-playbook)
- [Looking at the results](#looking-at-the-results)
- [Complete](#complete)

## The Playbook

Lets look at a simple 1-task playbook that can accomplish this.

```yml
---
- hosts: network
  connection: network_cli
  tasks:
    - vyos_config:
        backup: yes
```

To run the playbook use the `ansible-playbook` command.  The default password is **vagrant** for the vyos vagrant image.

```bash
ansible-playbook backup.yml -u vagrant -k
```
Parameter | Explanation
------------ | -------------
ansible-playbook | Ansible executable for running playbooks
backup.yml | the name of the playbook
-u vagrant | specifies user vagrant
-k | prompts us for password

## Looking at the results

This will create a folder called `backup` that contains time stamped entires for each device that the playbook ran on:

```bash
[vagrant@ansible exercise01]$ ls
backup  backup.yml
[vagrant@ansible exercise01]$ ls backup
leaf01_config.2018-02-07@02:37:29  leaf02_config.2018-02-07@02:37:28  spine01_config.2018-02-07@02:37:28  spine02_config.2018-02-07@02:37:28
```

cat a file to see the backup file
```
[vagrant@ansible exercise01]$ cat backup/leaf01_config.2018-02-07\@02\:44\:13
set interfaces ethernet eth0 address 'dhcp'
set interfaces ethernet eth0 duplex 'auto'
set interfaces ethernet eth0 hw-id '08:00:27:de:74:b3'
set interfaces ethernet eth0 smp_affinity 'auto'
set interfaces ethernet eth0 speed 'auto'
<--output removed for brevity-->
```

## Complete
You have completed exercise 01.

[Return to training-course](../README.md)
