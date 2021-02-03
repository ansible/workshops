# tower_configuration_applications
## Description
An Ansible Role to create Applications in Ansible Tower.


## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx


## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_applications`|`see below`|yes|Data structure describing your applications, described below.||


### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add application task does not include sensitive information.
tower_configuration_applications_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_applications_secure_logging`|`False`|no|Whether or not to include the sensitive Application role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|


## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of application|
|`organization`|""|yes|str|Name of the organization for the application|
|`description`|""|no|str|Description to use for the application.|
|`authorization_grant_type`|"password"|yes|str|Grant type for tokens in this application, "password" or "authorization-code"|
|`client_type`|"public"|yes|str|Application client type, "confidential" or "public"|
|`redirect_uris`|""|no|str|Allowed urls list, space separated. Required with "autorization-code" grant type|
|`skip_authorization`|"false"|yes|bool|Set True to skip authorization step for completely trusted applications.|
|`state`|`present`|no|str|Desired state of the application.|



### Standard Project Data Structure
#### Json Example
```json
---
 {
    "tower_applications": [
      {
        "name": "Tower Config Default Application",
        "description": "Generic application, which can be used for oauth tokens",
        "organization": "Default",
        "state": "present",
        "client_type": "confidential",
        "authorization_grant_type": "password"
      }
    ]
}
```
#### Ymal Example
```yaml
---
tower_applications:
  - name: "Tower Config Default Application"
    description: "Generic application, which can be used for oauth tokens"
    organization: "Default"
    state: "present"
    client_type: "confidential"
    authorization_grant_type: "password"
```

## Playbook Examples
### Standard Role Usage
```yaml
tower_applications:
  - name: MyCustomApplication
    description: For user personal access tokens generated for use within CustomApplication.
    organization: Satellite
    client_type: confidential
    authorization_grant_type: password
    state: present
```
## License
[MIT](LICENSE)

## Author
[Mike Shriver](https://github.com/mshriver)
