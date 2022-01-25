# Gitlab Server Role

This sets up a RHEL device to be a Gitlab Server 

```
- name: Configure GitLab Host
  hosts: gitlab
  become: true
  gather_facts: true
  tags:
    - gitlab
  tasks:
    - include_role:
        name: ansible.workshops.common
    - include_role:
        name: ansible.workshops.gitlab_server
```
