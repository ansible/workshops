# tower_utilities.tower_virtual_environments

## Description
An Ansible Role to manage Python virtual environments in Ansible Tower.

## Variables

See the [defaults/main.yml](defaults/main.yml) for a list of available variables and their meaning

## Playbook Examples
### Standard Role Usage
```yaml
---
- hosts: "all"
  roles:
    - role: "tower_virtual_environments"
      tower_venv_online_installs:
        - "ansible-tower-cli"
        - "boto"
```
### Imported Role
```yaml
---
- hosts: "all"
  vars:
    tower_venv_online_installs:
      - "ansible-tower-cli"
      - "boto"
  tasks:
    - name: "Ensure Ansible Prerequisites are installed"
      import_role:
        name: "tower_virtual_environments"
```
### Included Role
```yaml
---
- hosts: "all"
  tasks:
    - name: "Ensure Ansible Prerequisites are installed"
      include_role:
        name: "tower_virtual_environments"
      vars:
        tower_venv_online_installs:
          - "ansible-tower-cli"
          - "boto"
```
## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
[Eric Lavarde](https://github.com/ericzolf)
