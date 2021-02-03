# tower_configuration.credentials
## Description
An Ansible Role to create Credentials in Ansible Tower.

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
|`tower_credentials`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add credentials task does not include sensitive information.
tower_configuration_credentials_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_credentials_secure_logging`|`False`|no|Whether or not to include the sensitive Credential role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Credential|
|`new_name`|""|yes|Name of Credential, used in updating a Credential.|
|`description`|`False`|no|Description of  of Credential.|
|`organization`|""|no|Organization this Credential belongs to. If provided on creation, do not give either user or team.|
|`credential_type`|""|no|Name of credential type. See below for list of options. More information in Ansible Tower documentation. |
|`inputs`|""|no|Credential inputs where the keys are var names used in templating. Refer to the Ansible Tower documentation for example syntax. Individual examples can be found at /api/v2/credential_types/ on an Tower.|
|`user`|""|no|User that should own this credential. If provided, do not give either team or organization. |
|`team`|""|no|Team that should own this credential. If provided, do not give either user or organization. |
|`state`|`present`|no|Desired state of the resource.|
|`update_secrets`|true|no|bool| True will always change password if user specifies password, even if API gives $encrypted$ for password. False will only set the password if other values change too.|

### Credential types
|Credential types|
|:---:|
|Amazon Web Services|
|Ansible Tower|
|GitHub Personal Access Token|
|GitLab Personal Access Token|
|Google Compute Engine|
|Insights|
|Machine|
|Microsoft Azure Resource Manager|
|Network|
|OpenShift or Kubernetes API Bearer Token|
|OpenStack|
|Red Hat CloudForms|
|Red Hat Satellite 6|
|Red Hat Virtualization|
|Source Control|
|Vault|
|VMware vCenter|

### Standard Organization Data Structure
#### Json Example
```json
---
{
    "tower_credentials": [
      {
        "name": "gitlab",
        "description": "Credentials for GitLab",
        "organization": "Default",
        "credential_type": "Source Control",
        "inputs": {
          "username": "person",
          "password": "password"
        }
      }
    ]
}
```
#### Yaml Example
```yaml
---
tower_credentials:
- name: gitlab
  description: Credentials for GitLab
  organization: Default
  credential_type: Source Control
  inputs:
    username: person
    password: password
```
## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Credentials to Tower
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
        file: "json/credentials.json"
        name: credentials_json

    - name: Add Credentials
      include_role:
        name: redhat_cop.tower_configuration.credentials
      vars:
        tower_credentials: "{{ credentials_json.tower_credentials }}"
```
## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
[Sean Sullivan](https://github.com/Wilk42)
