# tower_configuration.credential_types
## Description
An Ansible Role to create Credential Types in Ansible Tower.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed

| Required collections |
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
|`tower_credential_types`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add credential type task does not include sensitive information.
tower_configuration_credential_types_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|:---:|:---:|:---:|:---:|
|`tower_configuration_credential_types_secure_logging`|`False`|no|Whether or not to include the sensitive Credential Type role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Credential Type|
|`new_name`|""|yes|Name of Credential Type, used in updating a Credential Type.|
|`description`|`False`|no|The description of the credential type to give more detail about it.|
|`injectors`|""|no|Enter injectors using either JSON or YAML syntax. Refer to the Ansible Tower documentation for example syntax. See not below on proper formating.|
|`inputs`|""|no|Enter inputs using either JSON or YAML syntax. Refer to the Ansible Tower documentation for example syntax.|
|`kind`|""|no|The type of credential type being added. Note that only cloud and net can be used for creating credential types.|
|`state`|`present`|no|Desired state of the resource.|

### Formating Injectors
Injectors use a standard Jinja templating format to describe the resource.

Example:
```json
{{ variable }}
```

Because of this it is difficult to provide tower with the required format for these fields.

The workaround is to use the following format:
```json
{  { variable }}
```
The role will strip the double space between the curly bracket in order to provide tower with the correct format for the Injectors.

### Input and Injector Schema
The following detais the data format to use for inputs and injectors. These can be in either YAML or JSON For the most up to date information and more details see [Custom Credential Types - Ansible Tower Documentation](https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_types.html)

#### Input Schema
```yaml
fields:
  - type: string
    id: username
    label: Username
  - type: string
    id: password
    label: Password
    secret: true
required:
  - username
  - password
```
#### Injector Schema
```json
{
  "file": {
      "template": "[mycloud]\ntoken={{ api_token }}"
  },
  "env": {
      "THIRD_PARTY_CLOUD_API_TOKEN": "{{ api_token }}"
  },
  "extra_vars": {
      "some_extra_var": "{{ username }}:{{ password }}"
  }
}
```

### Standard Organization Data Structure
#### Json Example
```json
---
{
    "tower_credential_types": [
      {
        "name": "REST API Credential",
        "description": "REST API Credential",
        "kind": "cloud",
        "inputs": {
          "fields": [
            {
              "type": "string",
              "id": "rest_username",
              "label": "REST Username"
            },
            {
              "secret": true,
              "type": "string",
              "id": "rest_password",
              "label": "REST Password"
            }
          ],
          "required": [
            "rest_username",
            "rest_password"
          ]
        },
        "injectors": {
          "extra_vars": {
            "rest_password": "{% raw %}{  { rest_password }}{% endraw %}",
            "rest_username": "{% raw %}{  { rest_username }}{% endraw %}"
          },
          "env": {
            "rest_username_env": "{% raw %}{  { rest_username }}{% endraw %}",
            "rest_password_env": "{% raw %}{  { rest_password }}{% endraw %}"
          }
        }
      }
    ]
}
```
#### Yaml Example
```yaml
---
tower_credential_types:
- name: REST API Credential
  description: REST API Credential
  inputs:
    fields:
    - type: string
      id: rest_username
      label: REST Username
    - secret: true
      type: string
      id: rest_password
      label: REST Password
    required:
    - rest_username
    - rest_password
  injectors:
    extra_vars:
      rest_password: "{% raw %}{  { rest_password }}{% endraw %}"
      rest_username: "{% raw %}{  { rest_username }}{% endraw %}"
    env:
      rest_username_env: "{% raw %}{  { rest_username }}{% endraw %}"
      rest_password_env: "{% raw %}{  { rest_password }}{% endraw %}"
```
## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Credential Types to Tower
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
        file: "json/credential_types.json"
        name: credential_types_json

    - name: Add Credential Types
      include_role:
        name: redhat_cop.tower_configuration.credential_types
      vars:
        tower_credential_types: "{{ credential_types_json.tower_credential_types }}"
```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
