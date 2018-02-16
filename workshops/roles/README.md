# Workshop: Roles

### Topics Covered

* Roles

### What You Will Learn

* How Ansible roles are developed and structured
* How to use a role in a playbook

### The Assignment

Your assignment is simple: refactor the Ansible playbook you've been developing into a role called "nginx-simple".

This assignment should result in a drop in replacement that is portable and more modular. It does not add any new tasks or functionality.

1. Initialize your role with `ansible-galaxy init` in a new subdirectory `roles/`.
1. Refactor your existing basic playbook and associated resources into your role.
1. Create a new playbook that uses the role still targeting the "web" group.
1. Remove any empty files and directories from your role.

#### Extra Credit

1. Refactor and merge the Nginx remove and uninstall playbook from the Basic Playbook Extra Credit assignments into your "nginx-simple" role. Create a separate playbook to execute that function of the role.

### Resources

* [Ansible Roles](http://docs.ansible.com/ansible/playbooks_roles.html#roles)
* [Create Roles (with ansible-galaxy)](http://docs.ansible.com/ansible/galaxy.html#create-roles)
* [inculde_role](http://docs.ansible.com/ansible/include_role_module.html)


