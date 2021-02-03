# ansible-tower-cert

Ansible role to install Ansible Tower Certificate.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml)

```yaml
tower_cert_location: "{{ playbook_dir }}/tower.cert"
tower_cert_key_location: "{{ playbook_dir }}/tower.key"
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
    - ansible-tower-install
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
    - ansible-tower-install
```

## License

MIT

## Author Information

Tom Page
