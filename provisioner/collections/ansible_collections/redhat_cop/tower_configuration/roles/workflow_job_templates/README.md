# tower_configuration.workflow_job_templates
## Description
An Ansible Role to create Workflow Job Templates in Ansible Tower.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Required Collections:
  awx.awx

## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_host`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`workflow_job_templates`|`see below`|yes|Data structure describing your workflow job templates described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add Workflow Job Templates task does not include sensitive information.
workflow_job_templates_secure_logging defaults to the value of tower_genie_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of genie roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`workflow_job_templates_secure_logging`|`False`|no|Whether or not to include the sensitive Workflow Job Templates role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables For Workflow Job Template
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of Workflow Job Template|
|`new_name`|""|str|no|Setting this option will change the existing name (looked up via the name field).|
|`description`|""|no|str|Description to use for the job template.|
|`organization`|""|""|no|list|Organization the workflow job template exists in. Used to lookup the object, cannot be changed with this module|
|`ask_inventory_on_launch`|""|no|bool|Prompt user for inventory on launch.|
|`ask_limit_on_launch`|""|no|bool|Prompt user for a limit on launch.|
|`ask_scm_branch_on_launch`|""|no|bool|Prompt user for scm branch on launch.|
|`ask_variables_on_launch`|""|no|bool|Prompt user for extra_vars on launch.|
|`extra_vars`|""|no|dict|Specify extra_vars for the template.|
|`inventory`|""|no|str|Inventory applied as a prompt, assuming job template prompts for inventory|
|`limit`|""|no|str|Limit applied as a prompt, assuming job template prompts for limit|
|`notification_templates_approvals`|""|no|list|The notifications on approval to use for this organization in a list.|
|`notification_templates_error`|""|no|list|The notifications on error to use for this organization in a list.|
|`notification_templates_started`|""|no|list|The notifications on started to use for this organization in a list.|
|`notification_templates_success`|""|no|list|The notifications on success to use for this organization in a list.|
|`scm_branch`|""|no|str|SCM branch applied as a prompt, assuming job template prompts for SCM branch|
|`state`|`present`|no|str|Desired state of the resource.|
|`survey_enabled`|""|no|bool|Enable a survey on the job template.|
|`survey_spec`|""|no|dict|JSON/YAML dict formatted survey definition.|
|`survey`|""|no|dict|JSON/YAML dict formatted survey definition. Alias of survey_spec|
|`webhook_service`|""|no|str|Service that webhook requests will be accepted from (github, gitlab)|
|`webhook_credential`|""|no|str|Personal Access Token for posting back the status to the service API|

### Variables For Workflow Job Template Node
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`workflow_job_template`|""|yes|str|The workflow job template the node exists in. Used for looking up the node, cannot be modified after creation.|
|`identifier`|""|yes|str|An identifier for this node that is unique within its workflow. It is copied to workflow job nodes corresponding to this node. This functions the same as the name field for other resources, however if it is not set, it will be set to a random UUID4 value. Recomended to use Column and row numbers for identifiers such as Node401. [Refer to this documentation for more](https://github.com/ansible/awx/blob/devel/docs/workflow.md)|
|`unified_job_template`|""|no|str|Name of unified job template to run in the workflow. Can be a job template, project, inventory source, etc. Omit if creating an approval node (not yet implemented).|
|`organization`|""|no|str|The organization of the workflow job template the node exists in. Used for looking up the workflow, not a direct model field.|
|`all_parents_must_converge`|""|no|bool|If enabled then the node will only run if all of the parent nodes have met the criteria to reach this node|
|`always_nodes`|""|no|list|Nodes that will run after this node completes.|
|`failure_nodes`|""|no|list|Nodes that will run after this node completes.|
|`success_nodes`|""|no|list|Nodes that will run after this node completes.|
|`verbosity`|""|no|str|Verbosity applied as a prompt, if job template prompts for verbosity|
|`state`|""|no|str|Desired state of the resource|
|`credentials`|""|no|list|Credentials to be applied to job as launch-time prompts.|
|`diff_mode`|""|no|bool|Run diff mode, applied as a prompt, if job template prompts for diff mode|
|`extra_data`|""|no|dict|Variables to apply at launch time. Will only be accepted if job template prompts for vars or has a survey asking for those vars. extra_data are extra_vars at the node level and named so to match the module and the API. These are only for "ask extra vars on prompt" on a given job template.|
|`inventory`|""|no|str|Inventory applied as a prompt, if job template prompts for inventory|
|`job_tags`|""|no|str|NJob tags applied as a prompt, if job template prompts for job tags|
|`job_type`|""|no|str|Job type applied as a prompt, if job template prompts for job type|
|`limit`|""|no|str|Limit to act on, applied as a prompt, if job template prompts for limit|
|`scm_branch`|""|no|str|SCM branch applied as a prompt, if job template prompts for SCM branch|
|`skip_tags`|""|no|str|Tags to skip, applied as a prompt, if job tempalte prompts for job tags|


### Surveys
Refer to the [Tower Api Guide](https://docs.ansible.com/ansible-tower/latest/html/towerapi/api_ref.html#/Job_Templates/Job_Templates_job_templates_survey_spec_create) for more information about forming surveys
|Variable Name|
|:---:|:---:|:---:|:---:|
|`name`|
|`description`|
|`spec`|
|`question_description`|""|
|`min`|""|
|`default`|""|
|`max`|""|
|`required`|""|
|`choices`|""|
|`new_question`|""|
|`variable`|""|
|`question_name`|""|
|`type`|""|

### Workflow Data Structures
This role accepts two data models. A simple starightforward easy to maintain model, and another based on the tower api. The 2nd one is more complicated and includes more detail, and is compatiable with tower import/export.

#### Standard Data structure model
```yaml
---
---
tower_workflows:
  - name: Simple workflow schema
    description: a basic workflow
    extra_vars: ''
    survey_enabled: false
    allow_simultaneous: false
    ask_variables_on_launch: false
    inventory:
    limit:
    scm_branch:
    ask_inventory_on_launch: false
    ask_scm_branch_on_launch: false
    ask_limit_on_launch: false
    webhook_service: ''
    webhook_credential:
    organization: Default
    schedules: []
    workflow_nodes:
      - all_parents_must_converge: false
        identifier: node101
        unified_job_template: RHVM-01
        credentials: []
        success_nodes:
          - node201
        failure_nodes: []
        always_nodes: []
      - all_parents_must_converge: false
        identifier: node201
        unified_job_template: test-template-1
        credentials: []
        success_nodes: []
        failure_nodes: []
        always_nodes: []
    notification_templates_started: []
    notification_templates_success: []
    notification_templates_error: []
    notification_templates_approvals: []
    survey_spec: {}

```
#### Tower Export Data structure model
##### Yaml Example
```yaml
---
tower_workflows:
  - name: Simple workflow schema
    description: a basic workflow
    extra_vars: ''
    survey_enabled: false
    allow_simultaneous: false
    ask_variables_on_launch: false
    inventory:
    limit:
    scm_branch:
    ask_inventory_on_launch: false
    ask_scm_branch_on_launch: false
    ask_limit_on_launch: false
    webhook_service: ''
    webhook_credential:
    organization:
      name: Default
    related:
      schedules: []
      workflow_nodes:
        - all_parents_must_converge: false
          identifier: node101
          unified_job_template:
            name: RHVM-01
          related:
            credentials: []
            success_nodes:
              - workflow_job_template:
                  name: Simple workflow schema
                identifier: node201
            failure_nodes: []
            always_nodes: []
        - all_parents_must_converge: false
          identifier: node201
          unified_job_template:
            name: test-template-1
          related:
            credentials: []
            success_nodes: []
            failure_nodes: []
            always_nodes: []
      notification_templates_started: []
      notification_templates_success: []
      notification_templates_error: []
      notification_templates_approvals: []
      survey_spec: {}

```

##### Json Example
```json
---
{
  "tower_workflows": [
    {
      "name": "Simple workflow schema",
      "description": "a basic workflow",
      "extra_vars": "",
      "survey_enabled": false,
      "allow_simultaneous": false,
      "ask_variables_on_launch": false,
      "inventory": null,
      "limit": null,
      "scm_branch": null,
      "ask_inventory_on_launch": false,
      "ask_scm_branch_on_launch": false,
      "ask_limit_on_launch": false,
      "webhook_service": "",
      "webhook_credential": null,
      "organization": {
        "name": "Default"
      },
      "related": {
        "schedules": [

        ],
        "workflow_nodes": [
          {
            "all_parents_must_converge": false,
            "identifier": "node101",
            "unified_job_template": {
              "name": "RHVM-01"
            },
            "related": {
              "credentials": [

              ],
              "success_nodes": [
                {
                  "workflow_job_template": {
                    "name": "Simple workflow schema"
                  },
                  "identifier": "node201"
                }
              ],
              "failure_nodes": [

              ],
              "always_nodes": [

              ]
            }
          },
          {
            "all_parents_must_converge": false,
            "identifier": "node201",
            "unified_job_template": {
              "name": "test-template-1"
            },
            "related": {
              "credentials": [

              ],
              "success_nodes": [

              ],
              "failure_nodes": [

              ],
              "always_nodes": [

              ]
            }
          }
        ],
        "notification_templates_started": [

        ],
        "notification_templates_success": [

        ],
        "notification_templates_error": [

        ],
        "notification_templates_approvals": [

        ],
        "survey_spec": {
        }
      }
    }
  ]
}
```


## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Playbook to configure ansible tower post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in tower_configs/tower_auth.yml
  # tower_hostname: ansible-tower-web-svc-test-project.example.com
  # tower_username: admin
  # tower_password: changeme
  pre_tasks:
    - name: Include vars from tower_configs directory
      include_vars:
        dir: ./yaml
        ignore_files: [tower_config.yml.template]
        extensions: ["yml"]
  roles:
    - {role: tower_configuration.workflow_job_templates, when: workflow_job_templates is defined}

```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
