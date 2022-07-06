# Control Node Role

This role will setup control nodes for Ansible Automation Workshops (same for all workshop types)

Example:

```
- name: configure ansible control node
  hosts: '*ansible-1'
  gather_facts: true
  become: true
  tasks:
    - include_role:
        name: ansible.workshops.control_node_always
```
