# tower_configuration.tower_role
## Description
An Ansible Role to create RBAC Entries in Ansible Tower.

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
|`tower_rbac`|`see below`|yes|Data structure describing your RBAC entries described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add rbac task does not include sensitive information.
`tower_configuration_rbac_secure_logging` defaults to the value of `tower_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_rbac_secure_logging`|`False`|no|Whether or not to include the sensitive rbac role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`user`|""|no|str|The user for which the role applies|
|`team`|""|no|str|The team for which the role applies|
|`role`|""|no|str (see note below)|The role which is applied to one of {`target_team`, `inventory`, `job_template`, `target_team`, `inventory`, `job_template`} for either `user` or `team` |
|`target_team`|""|no|str|The team the role applies against|
|`target_teams`|""|no|list|The teams the role applies against|
|`inventory`|""|no|str|The inventory the role applies against|
|`inventories`|""|no|list|The inventories the role applies against|
|`job_template`|""|no|str|The job template the role applies against|
|`job_templates`|""|no|list|The job templates the role applies against|
|`workflow`|""|no|str|The workflow the role applies against|
|`workflows`|""|no|list|The workflows the role applies against|
|`credential`|""|no|str|The credential the role applies against|
|`credentials`|""|no|list|The credentials the role applies against|
|`organization`|""|no|str|The organization the role applies against|
|`organizations`|""|no|list|The organizations the role applies against|
|`lookup_organization`|""|no|str|Organization the inventories, job templates, projects, or workflows the items exists in.Used to help lookup the object, for organizaiton roles see organization. If not provided, will lookup by name only, which does not work with duplicates.|
|`project`|""|no|str|The project the role applies against|
|`projects`|""|no|list|The project the role applies against|
|`state`|`present`|no|str|Desired state of the resource.|

#### Role
`role` must be one of the following:
- `admin`
- `read`
- `member`
- `execute`
- `adhoc`
- `update`
- `use`
- `auditor`
- `project_admin`
- `inventory_admin`
- `credential_admin`
- `workflow_admin`
- `notification_admin`
- `job_template_admin`

### Standard RBAC Data Structure
#### Json Example
```json
{
  "tower_rbac": [
    {
      "user": "jdoe",
      "target_team": "My Team",
      "role": "member"
    },
    {
      "team": "My Team",
      "organization": "Default",
      "role": "execute"
    }
  ]
}
```
#### Yaml Example
```yaml
---
tower_rbac:
- user: jdoe
  target_team: "My Team"
  role: member
- team: "My Team"
  organization: "Default"
  role: execute
```

## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add RBAC entry to Tower
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
        file: "json/rbac.json"
        name: rbac_json

    - name: Add Projects
      include_role:
        name: tower_rbac
      vars:
        tower_rbac: "{{ rbac_json.tower_rbac }}"
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
