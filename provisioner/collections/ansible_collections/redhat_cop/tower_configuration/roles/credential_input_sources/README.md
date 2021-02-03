# tower_configuration.credential_input_sources
## Description
An Ansible Role to create credential input sources in Ansible Tower, the below example is for Cyberark as an input source, change accordingly to match your input source type.

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
|`tower_credential_input_sources`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add credential input source task does not include sensitive information.
tower_configuration_credential_input_sources_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_credential_input_sources_secure_logging`|`False`|no|Whether or not to include the sensitive credential_input_source role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`target_credential`|""|yes|str|Name of credential to have the input source applied|
|`input_field_name`|""|yes|str|Name of field which will be written by the inout source|
|`source_credential`|""|str|no|Name of the source credential which points to a credential source|
|`metadata`|""|str|no|The metadata applied to the source.|
|`description`|`False`|no|str|Description to use for the credential input source.|
|`state`|`present`|no|str|Desired state of the resource.|

For further details on fields see https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_plugins.html

### Standard Project Data Structure
#### Json Example
```json
---
{
    "tower_credential_input_sources": [
      {
        "source_credential": "cyberark",
        "target_credential": "gitlab",
        "input_field_name": "password",
        "metadata": {
          "object_query": "Safe=MY_SAFE;Object=AWX-user",
          "object_query_format": "Exact"
        },
        "description": "Fill the gitlab credential from CyberArk"
      }
    ]
}
```
#### Yaml Example
```yaml
---
tower_credential_input_sources:
  - source_credential: cyberark
    target_credential: gitlab
    input_field_name: password
    metadata:
      object_query: "Safe=MY_SAFE;Object=AWX-user"
      object_query_format: "Exact"
    description: Fill the gitlab credential from CyberArk
```

## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Add credential input source to tower
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
        file: "json/cred_input_src.json"
        name: "cred_input_src_json"

    - name: Add Credential Input Source
      include_role:
        name: redhat_cop.tower_configuration.credential_input_sources
      vars:
        tower_credential_input_sources: "{{ cred_input_src_json.tower_credential_input_sources }}"
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
