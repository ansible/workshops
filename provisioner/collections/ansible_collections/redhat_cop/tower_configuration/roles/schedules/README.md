# tower_configuration.schedules
## Description
An Ansible Role to create Schedules in Ansible Tower.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx>12.0

## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_schedules`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add schedules task does not include sensitive information.
tower_configuration_schedules_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_schedules_secure_logging`|`False`|no|Whether or not to include the sensitive Schedules role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of Job Template|
|`new_name`|""|str|no|Setting this option will change the existing name (looked up via the name field).|
|`description`|`False`|no|str|Description to use for the job template.|
|`rrule`|""|yes|str|A value representing the schedules iCal recurrence rule. See the awx.awx.tower_schedule_rrule plugin for help constructing this value|
|`extra_data`|`{}`|no|dict|Extra vars for the job template. Only allowed if prompt on launch|
|`inventory`|""|no|str|Inventory applied to job template, assuming the job template prompts for an inventory.|
|`scm_branch`|Project default|no|str|Branch to use in the job run. Project default used if not set. Only allowed if `allow_override` set to true on project|
|`job_type`|Job template default|no|str|The job type used for the job template.|
|`job_tags`|""|no|str|Comma separated list of tags to apply to the job|
|`skip_tags`|""|no|str|Comma separated list of tags to skip for the job|
|`limit`|""|no|str|A host pattern to constrain the list of hosts managed or affected by the playbook|
|`diff_mode`|Job template default|no|bool|Enable diff mode for the job template|
|`verbosity`|Job template default|no|int|Level of verbosity for the job. Only allowed if configured to prompt on launch|
|`unified_job_template`|""|no|string|Name of unified job template to schedule. Required if state='present.|
|`enabled`|`true`|no|bool|Enabled processing of this job template|
|`state`|`present`|no|str|Desired state of the resource.|



### Standard Schedule Data Structure
#### Json Example
```json
"tower_schedules": [
    {
      "name": "Demo Schedule",
      "description": "A demonstration",
      "unified_job_template": "Demo Job Template",
      "rrule": "DTSTART:20191219T130551Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=1",
      "extra_data": {
        "scheduled": true
      },
      "verbosity": 1
    }
  ]

```
#### Yaml Example
```yaml
---
tower_schedules:
  - name: Demo Schedule
    description: A demonstration
    unified_job_template: Demo Job Template
    rrule: "DTSTART:20191219T130551Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=1"
    extra_data:
      scheduled: true
    verbosity: 1
```

## Playbook Examples
### Standard Role Usage
```yaml
- name: Add schedules to Tower
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    tower_schedules:
      - name: Demo Schedule
        description: A demonstration
        unified_job_template: Demo Job Template
        rrule: "DTSTART:20191219T130551Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=1"
        extra_data:
          scheduled: true
        verbosity: 1
  roles:
    - schedules
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
