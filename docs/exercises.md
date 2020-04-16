# Create New Exercise Content

We encourage folks to create new exercise content, fork with your own content, and customize the workshop any way you want.  This will give you the flexibility to customize workshops for your own friends, customers, community or project!

## Table of Contents

* [Using your own fork](#using-your-own-fork)
   * [Practical Example](#practical-example)
* [Changing solution folder on control node](#changing-solution-folder-on-control-node)
   * [Practical Example](#practical-example-1)
* [Changing source folder for exercise solutions](#changing-source-folder-for-exercise-solutions)
   * [Practical Example](#practical-example-2)

# Using your own fork

When a workshop is provisioned, the control node for every workbench (where the Red Hat Ansible Automation is installed and executed from) will load solution exercises into `~/{{workshop}}-workshop`.  For example if you are running the `networking` workshop the home directory for every student will have `~/home/networking-workshop`.

This can be customized!  There are three variables that you can change with your provisioner code

   - `ansible_workshops_url` - points to the git repo where you want to load exercises from.  By default this uses [https://github.com/ansible/workshops.git](https://github.com/ansible/workshops.git) if this is not specified.
   - `version` - points to the git [branch](https://git-scm.com/docs/git-branch) for the specified git repo.  By default this uses `master`
   - `refspec` - points to the git [refspec](https://git-scm.com/book/en/v2/Git-Internals-The-Refspec).  By default this is set to `""` (nothing).

These variables are used in the `control_node` role which can found here: `provisioner/roles/control_node/tasks/main.yml`


## Practical Example

Here is the `extra_vars` example of provisioning the `workshop_type: rhel` with exercises from a forked repository on a different branch:

```
---
ec2_region: us-east-2
ec2_name_prefix: sean-workshop
admin_password: ansible123
student_total: 1
workshop_type: rhel
create_login_page: true
ansible_workshops_url: https://github.com/ipvsean/workshops.git
ansible_workshops_version: "test_branch"
```

This would load the exercises `/exercises/ansible_rhel` from fork `github.com/ipvsean/workshops.git` branch `test_branch` into the student home directory of `~/rhel-workshop`


# Changing solution folder on control node

It is possible to change the location of the destination folder where the exercises are loaded into with the `exercise_dest_location` variable.


## Practical Example

Here is the `extra_vars` example of provisioning the `workshop_type: rhel` with exercises from a forked repository on a different branch:

```
---
ec2_region: us-east-1
ec2_name_prefix: sean-workshop2
admin_password: ansible123
student_total: 1
workshop_type: rhel
create_login_page: true
ansible_workshops_url: https://github.com/ipvsean/workshops.git
ansible_workshops_version: "test_branch"
exercise_dest_location: "my_folder"
```

This would load the exercises `/exercises/ansible_rhel` from fork `github.com/ipvsean/workshops.git` branch `test_branch` into the student home directory of `~/my_folder`

# Changing source folder for exercise solutions

It is possible to change the location of the source folder with the `exercise_src_location` variable.  This defaults to `exercises/ansible_{{workshop_type}}`.  For example by default it would load `exercises/ansible_rhel` for the `workshop_type: rhel` workshop.

## Practical Example

Here is the `extra_vars` example of provisioning the `workshop_type: rhel` with different exercises from a forked repository on a different branch:

```
---
ec2_region: us-east-1
ec2_name_prefix: sean-workshop2
admin_password: ansible123
student_total: 1
workshop_type: rhel
create_login_page: true
ansible_workshops_url: https://github.com/ipvsean/workshops.git
ansible_workshops_version: "test_branch"
exercise_dest_location: "my_folder"
exercise_src_location: "exercises/my_exercises"
```

This would load the exercises `/exercises/my_exercises` from fork `github.com/ipvsean/workshops.git` branch `test_branch` into the student home directory of `~/my_folder`
