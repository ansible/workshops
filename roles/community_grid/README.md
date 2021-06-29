# Community Grid Role

This blog will outline this role:
https://www.ansible.com/blog/ansible-and-ibm-community-grid

Example:

```
- name: IBM community grid managed nodes
  hosts: "managed_nodes"
  become: true
  gather_facts: true

  tasks:
    - name: install boinc-client and register
      include_role:
        name: ansible.workshops.community_grid
      when:
        - ibm_community_grid is defined
        - ibm_community_grid
```
