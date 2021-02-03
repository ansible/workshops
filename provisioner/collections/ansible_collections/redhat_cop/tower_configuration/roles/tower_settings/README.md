# tower_configuration.tower_settings
An Ansible role to alter Settings in tower.

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
|`tower_settings`|`see below`|yes|Data structure describing your settings described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add settings task does not include sensitive information.
tower_configuration_settings_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_settings_secure_logging`|`False`|no|Whether or not to include the sensitive Settings role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
There are two choices for entering settings. Either provide as a single dict under `settings` or individually as `name` `value`. In the first case `tower_settings` will simply be an individual dict, but in the second case, it will be a list.

### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`settings`|{}|no|Dict of key-value pairs of settings|
|`name`|""|no|Name of the setting to set.|
|`value`|""|no|Value of the setting.|

### Standard Setting Data Structure - as a dict
#### Json Example
```json
---
{
  "tower_settings": {
    "settings": {
      "AUTH_LDAP_USER_DN_TEMPLATE": "uid=%(user)s,ou=Users,dc=example,dc=com",
      "AUTH_LDAP_BIND_PASSWORD": "password"
    }
  }
}

```
#### Yaml Example
```yaml
---
tower_settings:
  settings:
    AUTH_LDAP_USER_DN_TEMPLATE: "uid=%(user)s,ou=Users,dc=example,dc=com"
    AUTH_LDAP_BIND_PASSWORD: "password"

```

### Standard Setting Data Structure - as a list
#### Json Example
```json
---
{
  "tower_settings": [
    {
      "name": "AUTH_LDAP_USER_DN_TEMPLATE",
      "value": "uid=%(user)s,ou=Users,dc=example,dc=com"
    },
    {
      "name": "AUTH_LDAP_BIND_PASSWORD",
      "value": "password"
    }
  ]
}

```
#### Yaml Example
```yaml
---
tower_settings:
  - name: AUTH_LDAP_USER_DN_TEMPLATE
    value: "uid=%(user)s,ou=Users,dc=example,dc=com"
  - name: AUTH_LDAP_BIND_PASSWORD
    value: "password"
```

## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Settings to Tower
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
        file: "json/tower_settings.json"
        name: settings_json

    - name: Add Settings
      include_role:
        name: redhat_cop.tower_configuration.tower_settings
      vars:
        tower_settings: "{{ settings_json.tower_settings }}"
```

# License
[MIT](LICENSE)

# Author
[Kedar Kulkarni](https://github.com/kedark3)
[Sean Sullivan](https://github.com/Wilk42)
