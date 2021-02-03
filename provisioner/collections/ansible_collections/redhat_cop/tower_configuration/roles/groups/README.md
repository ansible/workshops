# tower_configuration.groups
## Description
An Ansible Role to create Groups in Ansible Tower.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed

| Requiremed collections |
|:---:|
|awx.awx|

## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`tower_validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_config_file`|""|no|Path to the Tower or AWX config file.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_groups`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add groups task does not include sensitive information.
tower_configuration_groups_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_groups_secure_logging`|`False`|no|Whether or not to include the sensitive Group role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Group|
|`new_name`|""|yes|Name of Group, used in updating a Group.|
|`description`|`False`|no|Description of  of Group.|
|`inventory`|""|yes| Name of inventory|
|`variables`|{}|no| variables applicable to group.|
|`hosts`|""|no | hosts (list) in group|
|`children`|""|no|  List of groups that should be nested inside in this group|
|`state`|`present`|no|Desired state of the resource.|


### Standard Organization Data Structure
#### Json Example
```json
---
{
    "tower_group": [
      {
        "name": "PSQL_Servers",
        "description": "Default",
        "inventory": "Source Control",
        "variables": {
        "my_var": true
        }
      }
    ]
}
```
#### Yaml Example
```yaml
---
tower_group:
- name: PSQL_Servers
  description: Group for Postgres SQL Servers
  inventory: Default
  variables:
    myvars: example1
  hosts:
   - PSQL1
   - PSQL2
   - PSQL3
  children:
   - group1
   - group2
   - group3
```

## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Groups to Tower
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
        file: "json/groups.json"
        name: groups_json

    - name: Add Groups
      include_role:
        name: redhat_cop.tower_configuration.groups
      vars:
        tower_groups: "{{ groups_json.tower_groups }}"
```
## License
[MIT](LICENSE)

## Author
[Wei-Yen Tan](https://github.com/weiyentan)
[Andrew J. Huffman](https://github.com/ahuffman)
[Sean Sullivan](https://github.com/sean-m-sullivan)
