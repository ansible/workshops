# tower_configuration.teams
## Description
An Ansible Role to create Teams in Ansible Tower.
## Variables

### Authentication
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_teams`|`see below`|yes|Data structure describing your Teams described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add teams task does not include sensitive information.
`tower_configuration_teams_secure_logging` defaults to the value of `tower_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_teams_secure_logging`|`False`|no|Whether or not to include the sensitive teams role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|


### Data structure `tower_teams:` should include following vars
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`||yes|str|The desired team name to create or modify|
|`new_name`||no|str|To use when changing a team's name.|
|`description`|omitted|no|str|The team description|
|`organization`||yes|str|The organization in which team will be created|
|`state`|`present`|no|str|Desired state of the resource.|

## Playbook Examples
### Standard Role Usage
``` yaml
---
- name: Test playbook for local testing
  hosts: localhost
  connection: local
  vars:
    tower_hostname: "https://tower.example.com"
    validate_certs: false
    tower_username: "admin"
    tower_password: "password"
    tower_teams:
      - name: "team1"
        desc: "My first team"
        organization: "Default"
      - name: "team2"
        desc: "My second team"
        organization: "Default"
      - name: "team3"
        desc: "My third team"
        organization: "Default"
  roles:
    - tower_teams
```

## License
[MIT](License)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
[Kedar Kulkarni](https://github.com/kedark3)
