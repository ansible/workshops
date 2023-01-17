# Code Server Role

This roll will install [code server](https://github.com/cdr/code-server) onto a Red Hat Enterprise Linux (RHEL) node that also has Ansible Automation Platform installed (i.e. Tower/Controller).  It supports both Ansible Tower and Automation controller.

This is tested on RHEL 8.X

Example:

```
- name: configure ansible control node
  hosts: 'controller_hosts'
  gather_facts: true
  become: true
  vars:
    workshop_dns_zone: "demoredhat.com"
    admin_password: ansible123
    username: "student1"
    ec2_name_prefix: "my_workbench"

  tasks:
    - include_role:
        name: ansible.workshops.code_server
```

# Requirements

- AWS (Amazon Web Services) account with Route53 access - this role is only currently supported with route53 and uses the `community.aws.route53` module
