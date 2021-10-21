# Private Automation Hub Role

This role will setup Private Automation Hub on the designated host.  This requires a file aap.tar.gz (see the aap_download role)

Example:

```
- name: configure private automation hub
  hosts: 'automation_hub'
  gather_facts: true
  become: true
  tasks:
    - include_role:
        name: ansible.workshops.private_automation_hub
      when:
        - automation_hub is defined
        - automation_hub
```
