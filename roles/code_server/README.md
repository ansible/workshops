# Code Server Role

This roll will install [code server](https://github.com/cdr/code-server) onto a RHEL node that also has Ansible Automation Platform installed (i.e. Tower/Controller)

Example:

```
- include_role:
    name: ansible.workshops.code_server
  when:
    - code_server is defined
    - code_server
    - towerinstall is defined
    - towerinstall
```
