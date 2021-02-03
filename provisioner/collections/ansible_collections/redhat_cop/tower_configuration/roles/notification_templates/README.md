# tower_configuration.notification_templates
## Description
An Ansible Role to add notification templates to Ansible Tower.

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
|`tower_notification_templates`|`see below`|yes|Data structure describing your notification entries described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add notification task does not include sensitive information.
`tower_configuration_notification_secure_logging` defaults to the value of `tower_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_notification_secure_logging`|`False`|no|Whether or not to include the sensitive notification role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|The name of the notification.|
|`new_name`|""|yes|str|Setting this option will change the existing name (looked up via the name field.|
|`description`|""|no|str|The description of the notification.|
|`organization`|""|no|str|The organization applicable to the notification.|
|`notification_type`|""|no|str|The type of notification to be sent.|
|`notification_configuration`|""|no|str|The notification configuration file. Note providing this field would disable all depreciated notification-configuration-related fields.|
|`messages`|""|no|list|Optional custom messages for notification template. Assumes any instance of two space __ are used for adding variables and removes them. Does not effect single space.|
|`state`|`present`|no|str|Desired state of the resource.|


### Standard notification Data Structure
#### Json Example
```json
{
  "tower_notification_templates": [
    {
      "name": "irc-satqe-chat-notification",
      "description": "Notify us on job in IRC!",
      "organization": "Satellite",
      "notification_type": "irc",
      "notification_configuration": {
        "use_tls": false,
        "use_ssl": false,
        "password": "",
        "port": 6667,
        "server": "irc.freenode.com",
        "nickname": "Ansible-Tower-Stage-Bot-01",
        "targets": [
          "#my-channel"
        ]
      }
    },
    {
      "name": "Email notification",
      "description": "Send out emails for tower jobs",
      "organization": "Satellite",
      "notification_type": "email",
      "notification_configuration": {
        "username": "",
        "sender": "tower0@example.com",
        "recipients": [
          "admin@example.com"
        ],
        "use_tls": false,
        "host": "smtp.example.com",
        "use_ssl": false,
        "password": "",
        "port": 25
      }
    }
  ]
}
```
#### Yaml Example
```yaml
---
tower_notification_templates:
  - name: irc-satqe-chat-notification
    description: Notify us on job in IRC!
    organization: Satellite
    notification_type: irc
    notification_configuration:
      use_tls: false
      use_ssl: false
      password: ''  # this is required even if there's no password
      port: 6667
      server: irc.freenode.com
      nickname: Ansible-Tower-Stage-Bot-01
      targets:
      - "#my-channel"
    messages:
      success:
        body: '{"fields": {"project": {"id": "11111"},"summary": "Lab {  { job.status
          }} Ansible Tower {  { job.name }}","description": "{  { job.status }} in {  {
          job.name }} {  { job.id }} {  {url}}","issuetype": {"id": "1"}}}'
  - name: Email notification
    description: Send out emails for tower jobs
    organization: Satellite
    notification_type: email
    notification_configuration:
      username: ''  # this is required even if there's no username
      sender: tower0@example.com
      recipients:
      - admin@example.com
      use_tls: false
      host: smtp.example.com
      use_ssl: false
      password: ''  # this is required even if there's no password
      port: 25
```

## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add notification entry to Tower
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
        file: "json/notification.json"
        name: notification_json

    - name: Add Notifications
      include_role:
        name: tower_notification_templates
      vars:
        tower_notification_templates: "{{ notification_json.tower_notification_templates }}"
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
[Sean Sullivan](https://github.com/sean-m-sullivan)
