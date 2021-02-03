# tower_configuration.license
## Description
An Ansible Role to deploy a license to Ansible Tower.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx

## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_license`|`see below`|yes|Data structure describing your license for Tower, described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add license task does not include sensitive information.
tower_configuration_license_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_license_secure_logging`|`False`|no|Whether or not to include the sensitive license role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`manifest`|""|yes|obj|File path to a Red Hat subscription manifest (a .zip file)|
|`eula_accepted`|""|yes|bool|Whether to accept the End User License Agreement for Ansible Tower|

For further details on fields see https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_plugins.html

### Standard Project Data Structure
#### Json Example
```json
---
{
    "tower_license": {
        "data": "{{ lookup('file', '/tmp/my_tower.license') }}",
        "eula_accepted": true
      }
}
```
#### Yaml Example
```yaml
---
tower_credential_input_sources:
  data: "{{ lookup('file', '/tmp/my_tower.license') }}"
  eula_accepted: true
```

## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Add License to Tower
  hosts: localhost
  gather_facts: false
  connection: local

  # Bring in vaulted Ansible Tower secrets
  vars_files:
    - "../var/tower-secrets.yml"

  tasks:

    - name: Get token for use during play
      uri:
        url: "https://{{ tower_hostname }}/api/v2/tokens/"
        method: POST
        user: "{{ tower_username }}"
        password: "{{ tower_passname }}"
        force_basic_auth: true
        status_code: 201
        validate_certs: false
      register: user_token
      no_log: true

    - name: Set Tower oath Token
      set_fact:
        tower_oauthtoken: "{{ user_token.json.token }}"

    - name: Import vars
      include_vars:
        file: "vars/extra_vars.yml"

    - name: Import JSON
      include_vars:
        file: "json/license.json"
        name: "license_json"

    - name: Add License
      include_role:
        name: redhat_cop.tower_configuration.license
      vars:
        tower_credential_input_sources: "{{ license_json.tower_license }}"
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
