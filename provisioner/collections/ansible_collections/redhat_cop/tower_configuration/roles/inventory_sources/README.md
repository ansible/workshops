# tower_configuration.inventory_sources
An Ansible role to create inventory sources.

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
|`tower_projects`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add inventory_source task does not include sensitive information.
tower_configuration_inventory_sources_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_inventory_sources_secure_logging`|`False`|no|Whether or not to include the sensitive Inventory Sources role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|The name to use for the inventory source.|
|`new_name`|""|no|A new name for this assets (will rename the asset).|
|`description`|`False`|no|The description to use for the inventory source.|
|`inventory`|""|yes|Inventory the group should be made a member of.|
|`source`|""|no|The source to use for this group.|
|`source_path`|""|no|For an SCM based inventory source, the source path points to the file within the repo to use as an inventory.|
|`source_script`|""|no|Inventory script to be used when group type is C(custom).|
|`source_vars`|""|no|The variables or environment fields to apply to this source type.|
|`enabled_var`|""|no|The variable to use to determine enabled state e.g., "status.power_state".|
|`enabled_value`|""|no|Value when the host is considered enabled, e.g., "powered_on".|
|`host_filter`|""|no|If specified, Tower will only import hosts that match this regular expression.|
|`credential`|""|no|Credential to use for the source.|
|`source_regions`|""|no|Regions for cloud provider.|
|`instance_filters`|""|no|Comma-separated list of filter expressions for matching hosts.|
|`group_by`|""|no|Limit groups automatically created from inventory source.|
|`overwrite`|""|no|Delete child groups and hosts not found in source.|
|`overwrite_vars`|""|no|Override vars in child groups and hosts with those from external source.|
|`custom_virtualenv`|""|no|Local absolute file path containing a custom Python virtualenv to use.|
|`timeout`|""|no|The amount of time (in seconds) to run before the task is canceled.|
|`verbosity`|""|no|The verbosity level to run this inventory source under.|
|`update_on_launch`|""|no|Refresh inventory data from its source each time a job is run.|
|`update_cache_timeout`|""|no|Time in seconds to consider an inventory sync to be current.|
|`source_project`|""|no|Project to use as source with scm option|
|`update_on_project_update`|""|no|Update this source when the related project updates if source is C(scm)|
|`state`|`present`|no|Desired state of the resource.|
|`notification_templates_started`|""|no|The notifications on started to use for this inventory source in a list.|
|`notification_templates_success`|""|no|The notifications on success to use for this inventory source in a list.|
|`notification_templates_error`|""|no|The notifications on error to use for this inventory source in a list.|

### Standard Inventory Source Data Structure
#### Json Example
```json
---
{
  "tower_inventory_sources": [
    {
      "name": "RHVM-01",
      "source": "rhv",
      "inventory": "RHVM-01",
      "credential": "admin@internal-RHVM-01",
      "description": "created by Ansible Tower",
      "overwrite": true,
      "update_on_launch": true,
      "update_cache_timeout": 0
    }
  ]
}

```
#### Yaml Example
```yaml
---
tower_inventory_sources:
  - name: RHVM-01
    source: rhv
    inventory: RHVM-01
    credential: admin@internal-RHVM-01
    description: created by Ansible Tower
    overwrite: true
    update_on_launch: true
    update_cache_timeout: 0

```
## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Projects to Tower
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

    - name: Set Tower oauth Token
      set_fact:
        tower_oauthtoken: "{{ user_token.json.token }}"

    - name: Import JSON
      include_vars:
        file: "json/sources.json"
        name: sources_json

    - name: Add Inventory Sources
      include_role:
        name: redhat_cop.tower_configuration.inventory_sources
      vars:
        tower_inventory_sources: "{{ sources_json.sources }}"
```

# License
[MIT](LICENSE)

# Author
[Edward Quail](mailto:equail@redhat.com)

[Andrew J. Huffman](https://github.com/ahuffman)

[Kedar Kulkarni](https://github.com/kedark3)
