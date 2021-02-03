# tower_configuration.inventories
An Ansible role to create inventories in tower.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx

## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_inventories`|`see below`|yes|Data structure describing your inventories described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add inventories task does not include sensitive information.
tower_configuration_inventories_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_inventories_secure_logging`|`False`|no|Whether or not to include the sensitive Inventory role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of this inventory.|
|`description`|""|no|Description of this inventory.|
|`organization`|`False`|no|Organization this inventory belongs to.|
|`variables`|`False`|no|Variables for the inventory.|
|`kind`|`False`|no|The kind of inventory. Currently choices are '' and 'smart'|
|`host_filter`|`False`|no|The host filter field, useful only when 'kind=smart'|
|`state`|`present`|no|Desired state of the resource.|

### Standard Inventory Data Structure
#### Json Example
```json
---
{
  "tower_inventories": [
    {
      "name": "RHVM-01",
      "organization": "Satellite",
      "description": "created by Ansible Playbook - for RHVM-01"
    },
    {
      "name": "Test Inventory - Smart",
      "organization": "Default",
      "description": "created by Ansible Playbook",
      "kind": "smart",
      "host_filter": "name__icontains=localhost"
    }
  ]
}

```
#### Yaml Example
```yaml
---
tower_inventories:
  - name: RHVM-01
    organization: Satellite
    description: created by Ansible Playbook - for RHVM-01
  - name: Test Inventory - Smart
    organization: Default
    description: created by Ansible Playbook
    kind: smart
    host_filter:  "name__icontains=localhost"

```
## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Inventories to Tower
  hosts: localhost
  connection: local
  gather_facts: false

#Bring in vaulted Ansible Tower secrets
  vars_files:
    - ../tests/vars/tower_secrets.yml

  tasks:

    - name: Get token for use during play
      uri:
        url: "https://{{ tower_hostname }}/api/v2/tokens/"
        method: POST
        user: "{{ tower_username }}"
        password: "{{ tower_passname }}"
        force_basic_auth: yes
        status_code: 201
        validate_certs: no
      register: user_token
      no_log: True

    - name: Set Tower oath Token
      set_fact:
        tower_oauthtoken: "{{ user_token.json.token }}"

    - name: Import JSON
      include_vars:
        file: "json/tower_inventories.json"
        name: tower_inventories

    - name: Add Inventory Sources
      include_role:
        name: redhat_cop.tower_configuration.inventories
      vars:
        tower_inventory_sources: "{{ tower_labels.tower_inventories }}"
```

# License
[MIT](LICENSE)

# Author
[Edward Quail](mailto:equail@redhat.com)

[Andrew J. Huffman](https://github.com/ahuffman)

[Kedar Kulkarni](https://github.com/kedark3)
