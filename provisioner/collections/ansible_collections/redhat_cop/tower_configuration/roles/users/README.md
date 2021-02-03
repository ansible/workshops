# tower_configuration.users
## Description
An Ansible Role to add users to Ansible Tower.

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
|`tower_user_accounts`|`see below`|yes|Data structure describing your user entries described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add user task does not include sensitive information.
`tower_configuration_user_secure_logging` defaults to the value of `tower_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_user_secure_logging`|`False`|no|Whether or not to include the sensitive user role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`username`|""|yes|str|The username of the user|
|`password`|""|yes|str|The password of the user|
|`email`|""|yes|str|The email of the user|
|`first_name`|""|no|str|The first name of the user|
|`last_name`|""|no|str|The last name of the user|
|`is_superuser`|false|no|bool|Whether the user is a superuser|
|`is_auditor`|false|no|bool|Whether the user is an auditor|
|`state`|`present`|no|str|Desired state of the resource.|
|`update_secrets`|true|no|bool| True will always change password if user specifies password, even if API gives $encrypted$ for password. False will only set the password if other values change too.|

### Standard user Data Structure
#### Json Example
```json
{
  "tower_user_accounts": [
    {
      "user": "jsmith",
      "is_superuser": false,
      "password": "p4ssword",
      "email": "jsmith@example.com"
    }
  ]
}
```
#### Yaml Example
```yaml
---
tower_user_accounts:
  - user: tower_user
    is_superuser: false
    password: tower_password
```

## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add user entry to Tower
  hosts: localhost
  connection: local
  gather_facts: false
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
      no_log: True

    - name: Set Tower oath Token
      set_fact:
        tower_oauthtoken: "{{ user_token.json.token }}"

    - name: Import JSON
      include_vars:
        file: "json/user.json"
        name: user_json

    - name: Add Projects
      include_role:
        name: tower_user
      vars:
        tower_user_accounts: "{{ user_json.tower_user }}"
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
