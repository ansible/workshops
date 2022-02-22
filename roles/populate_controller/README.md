# Populate automation controller role

This role will populate automation controller.  The FQCN (fully qualified collection name) is `ansible.workshops.populate_controller`

- [Overview - Automation controller](https://www.ansible.com/products/controller)
- [Documentation - Automation controller](https://docs.ansible.com/automation-controller/latest/html/quickstart/index.html)

This role uses the [redhat_cop.controller_configuration](https://github.com/redhat-cop/tower_configuration) collection to populate Automation controller with specific projects, credentials and job templates for use with the Ansible Automation Workshops.  In tern the `redhat-cop.controller_configuration` uses the `ansible.controller` collection or `awx.awx` collection depending on if you are using downstream or upstream.

Example:

```
- name: populate automation controller
  hosts: '*ansible-1'
  become: true
  gather_facts: false

  tasks:
    - name: run populate_controller role
      include_role:
        name: ansible.workshops.populate_controller
```
