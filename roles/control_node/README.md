# Control Node Role

This role will setup control nodes for Ansible Automation Workshops (same for all workshop types)

Example:

```
- name: configure ansible control node
  hosts: '*ansible-1'
  gather_facts: true
  become: true
  vars:
    tower_license: "{{ hostvars['localhost']['tower_license'] }}"
    use_manifest: "{{ hostvars['localhost']['use_manifest'] }}"
    default_tower_url: "{{ hostvars['localhost']['default_tower_url'] }}"
  pre_tasks:
    - debug:
        var: tower_license
  tasks:
    - include_role:
        name: ansible.workshops.control_node
```
