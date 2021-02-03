# redhat_cop.tower_utilities.install

Ansible role to prep to install Ansible Tower.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml)

```yaml
tower_working_location: "/root/"
tower_force_setup: true

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

# Set isolated groups for isolated nodes if required
isolated_groups:
  - name: dmz1
    hostnames:
    - isolatednode0.dmz1.example.com
  - name: dmz2
    hostnames:
    - isolatednode0.dmz2.example.com
    - isolatednode1.dmz2.example.com

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
# Playbook to install Ansible Tower as a single node

- name: Install Ansible Tower
  hosts: tower
  become: true
  vars:
    tower_tower_releases_url: https://releases.ansible.com/ansible-tower/setup-bundle
    tower_tower_release_version: bundle-3.6.3-1.tar.gz
  roles:
    - redhat_cop.tower_utilities.install
```

```yaml
---
# Playbook to install Ansible Tower as a cluster

- name: Setup Ansible Tower
  hosts: localhost
  become: true
  vars:
    tower_hosts:
      - "clusternode[1:3].example.com"
    tower_database: "dbnode.example.com"
    tower_database_port: "5432"
  roles:
    - redhat_cop.tower_utilities.install
```

## License

MIT

## Author Information

Tom Page
