# Connectivity Test Role

This role is reused multiple times to make sure nodes are online and responding and ready to be automated

Example:

```
- name: wait for all nodes to have SSH reachability
  hosts: "managed_nodes:control_nodes:attendance"
  become: true
  gather_facts: false
  tasks:
    - include_role:
        name: ansible.workshops.connectivity_test
```
