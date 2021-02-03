# redhat_cop.tower_utilities.restore

Ansible role to restore a backup of Ansible Tower.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml)

```yaml
# Role Vars
tower_working_location: "/root/"
restore_file: "tower-backup-latest.tar.gz"
restore_location: "{{ tower_working_location }}/{{ restore_file }}"

# Tower variables
tower_admin_password: "password"

# Postgresql variables
tower_pg_database: "awx"
tower_pg_username: "awx"
tower_pg_password: "password"

# RabbitMQ variables
tower_rabbitmq_username: tower
tower_rabbitmq_password: "password"
tower_rabbitmq_cookie: "cookiemonster"
tower_rabbitmq_port: 5672
tower_rabbitmq_vhost: tower
tower_rabbitmq_use_long_name: false

tower_releases_url: https://releases.ansible.com/ansible-tower/setup
tower_setup_file: ansible-tower-setup-{{ tower_release_version }}.tar.gz

tower_hosts:
  - "localhost ansible_connection=local"

tower_database: ""
tower_database_port: ""
```

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner.

```sh
$ ansible-playbook playbook.yml -e @tower_vars.yml tower
```

```yaml
---
# Playbook to install Ansible Tower as a cluster

- name: Restore Ansible Tower
  hosts: localhost
  become: true
  vars:
    tower_hosts:
      - "clusternode[1:3].example.com"
    tower_database: "dbnode.example.com"
    tower_working_location: "{{playbook_dir}}"
    restore_location: "{{playbook_dir}}/tower-backup-latest.tar.gz"
  roles:
    - redhat_cop.tower_utilities.restore
```

## License

MIT

## Author Information

Sean Sullivan
