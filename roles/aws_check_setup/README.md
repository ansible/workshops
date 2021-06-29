# AWS Check Setup Role

This role performs some checks to make sure the provisioner will work successfully.  The goal is to fail early (not waste time) and alert the operator to any possible AWS issue (e.g. missing info, etc)

Example:

```
- name: run AWS check setup if using AWS
  include_role:
    name: ansible.workshops.aws_check_setup
```
