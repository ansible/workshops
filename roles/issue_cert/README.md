# Issue Cert Role

Used by the AWS DNS role (maybe this is a bad idea?)


Example:

(pulled from AWS DNS role)

```
- name: create DNS entries for Automation Controller and SSL cert
  block:
    - name: create DNS entries for each Ansible control node
      include_tasks: create.yml

    - name: configure SSL cert for Automation Controller
      vars:
        dns_name: "{{username}}.{{ec2_name_prefix|lower}}.{{workshop_dns_zone}}"
      include_role:
        name: ansible.workshops.issue_cert
```
