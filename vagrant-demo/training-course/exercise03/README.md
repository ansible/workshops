# Exercise 03 - Configuring System Services

For this exercise we are going to configure the hostname, domain name and name servers (DNS servers) for the network devices.  For all three of these we can use the [vyos_system module](http://docs.ansible.com/ansible/latest/vyos_system_module.html).  

## Table of Contents

- [The Playbook](#the-playbook)
- [Looking at the results](#looking-at-the-results)
   - [Hostname](#hostname)
   - [Domain Name](#domain-Name)
   - [DNS Servers](#dns-Servers)
- [Complete](#complete)

## The Playbook

Look at the following playbook:

```yml
---
- hosts: network
  connection: network_cli
  tasks:
  - name: configure domain-name and name_server
    vyos_system:
      host_name: "{{inventory_hostname}}"
      domain_name: test.example.com
      name_server:
        - 8.8.8.8
        - 8.8.4.4
```

In the above lets elaborate on what `inventory_hostname` is.  This is a variable that is defined by our inventory.  For this training course the inventory is located under [training-course/hosts](../hosts).  Each host is stored as an `inventory_hostname`.  To get more info on variables visit the [docs page](http://docs.ansible.com/ansible/latest/playbooks_variables.html)

To run the playbook use the `ansible-playbook` command.  The default password is **vagrant** for the vyos vagrant image.

```bash
ansible-playbook system.yml -u vagrant -k
```
Parameter | Explanation
------------ | -------------
ansible-playbook | Ansible executable for running playbooks
system.yml | the name of the playbook
-u vagrant | specifies user vagrant
-k | prompts us for password

## Looking at the results

Login to a device:
```
ssh vagrant@leaf01
```

To see what Ansible configured:

### Hostname

```bash
vagrant@leaf01:~$ show host name
leaf01
```


### Domain Name

```bash
vagrant@leaf01:~$ show host domain
test.example.com
```

### DNS Servers

```
vagrant@vyos:~$ show configuration | grep name-server
    name-server 8.8.8.8
    name-server 8.8.4.4
```

## Complete
You have completed exercise 03.

[Return to training-course](../README.md)
