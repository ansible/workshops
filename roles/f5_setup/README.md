# F5 Setup Role

This role is used for the F5 Automation Workshop (`workshop_type: f5`)

Example:

```
- name: setup f5 nodes
  hosts: f5
  become: false
  connection: local
  gather_facts: false
  vars:
    as3_uri: "https://github.com/F5Networks/f5-appsvcs-extension/releases"
  tasks:
    - include_role:
        name: ansible.workshops.f5_setup
```
