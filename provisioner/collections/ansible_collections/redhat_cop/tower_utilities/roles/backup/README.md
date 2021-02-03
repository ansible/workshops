# redhat_cop.tower_utilities.Backup

Ansible role to backup Ansible Tower.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml)

```yaml
tower_working_location: "/root/"
backup_dest: "{{ tower_working_location }}/"
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

tower_ssh_connection_vars: ''
```

## tower_ssh_connection_vars

connection vars can be set in the inventory file through a list of vars

```yaml
tower_ssh_connection_vars:
  - name: ansible_connection
    value: ssh
  - name: ansible_user
    value: vagrant
  - name: ansible_ssh_pass
    value: vagrant
  - name: ansible_ssh_private_key_file
    value: /path/to/file
```

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner.

```sh
$ ansible-playbook playbook.yml -e @tower_vars.yml tower
```

```yaml
---
# Playbook to install Ansible Tower as a cluster

- name: Backup Ansible Tower
  hosts: localhost
  become: true
  vars:
    tower_hosts:
      - "clusternode[1:3].example.com"
    tower_database: "dbnode.example.com"
    tower_working_location: "{{playbook_dir}}"
  roles:
    - redhat_cop.tower_utilities.backup
```

## License

MIT

## Author Information

Sean Sullivan
