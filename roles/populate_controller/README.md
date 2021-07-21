# Populate Tower Role

This role will populate tower/controller

Example:

```
- name: populate ansible tower
  hosts: '*ansible-1'
  become: true
  gather_facts: false

  tasks:
    - name: run populate_controller role
      include_role:
        name: ansible.workshops.populate_controller
```
