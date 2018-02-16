# Workshop: Ad-Hoc Commands

### Topics Covered

* Ansible Modules
* Facts
* Inventory and Groups
* `ansible` command-line options: `-i -m -a -b --limit`

### What You Will Learn

* How to test your Ansible configuration and connectivity
* How to get and display Ansible facts
* How to install a package

### The Assignment

Perform the following operations using ad-hoc commands:

1. Test that Ansible is setup correctly to communicate with all hosts in your inventory using the `ping` module.
1. Fetch and display to STDOUT Ansible facts using the `setup` module.
1. Setup and enable the EPEL package repository on the hosts in the "web" group using the yum module.
    * CentOS systems use the latest `epel-release` package
    * RHEL systems should use https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

#### Extra Credit

1. Fetch and display only the "virtual" subset of facts for each host.
1. Fetch and display the value of fully qualified domain name (FQDN) of each host from their Ansible facts.
1. Display the uptime of all hosts using the `command` module. 
1. Ping all hosts **except** the 'control' host using the `--limit` option

### Reference

* `ansible --help`
* [ping module](http://docs.ansible.com/ansible/ping_module.html)
* [setup module](http://docs.ansible.com/ansible/setup_module.html)
* [yum module](http://docs.ansible.com/ansible/yum_module.html)
* [command module](http://docs.ansible.com/ansible/command_module.html)
* [Introduction To Ad-Hoc Commands](http://docs.ansible.com/ansible/intro_adhoc.html)
