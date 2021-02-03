# tower_configuration.job_templates
## Description
An Ansible Role to create Job Templates in Ansible Tower.

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
|`tower_templates`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add job_template task does not include sensitive information.
tower_configuration_job_templates_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_job_templates_secure_logging`|`False`|no|Whether or not to include the sensitive Job Template role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of Job Template|
|`new_name`|""|str|no|Setting this option will change the existing name (looked up via the name field).|
|`description`|`False`|no|str|Description to use for the job template.|
|`job_type`|`run`|no|str|The job type to use for the job template(run, check).|
|`inventory`|""|no|str|Name of the inventory to use for the job template.|
|`organization`|""|no|str|Organization the job template exists in. Used to help lookup the object, cannot be modified using this module. The Organization is inferred from the associated project|
|`project`|""|no|str|Name of the project to use for the job template.|
|`playbook`|""|no|str|Path to the playbook to use for the job template within the project provided.|
|`credentials`|""|no|list|List of credentials to use for the job template.|
|`forks`|""|no|int|The number of parallel or simultaneous processes to use while executing the playbook.|
|`limit`|""|no|str|A host pattern to further constrain the list of hosts managed or affected by the playbook|
|`verbosity`|""|no|int|Control the output level Ansible produces as the playbook runs. 0 - Normal, 1 - Verbose, 2 - More Verbose, 3 - Debug, 4 - Connection Debug .|
|`extra_vars`|""|no|dict|Specify extra_vars for the template.|
|`job_tags`|""|no|str|Comma separated list of the tags to use for the job template.|
|`force_handlers`|""|no|bool|Enable forcing playbook handlers to run even if a task fails.|
|`skip_tags`|""|no|str|Comma separated list of the tags to skip for the job template.|
|`start_at_task`|""|no|str|Start the playbook at the task matching this name.|
|`diff_mode`|""|no|bool|Enable diff mode for the job template |
|`use_fact_cache`|""|no|bool|Enable use of fact caching for the job template.|
|`host_config_key`|""|no|str|Allow provisioning callbacks using this host config key.|
|`ask_scm_branch_on_launch`|""|no|bool|Prompt user for scm branch on launch.|
|`ask_diff_mode_on_launch`|""|no|bool|Prompt user to enable diff mode show changes to files when supported by modules.|
|`ask_variables_on_launch`|""|no|bool|Prompt user for extra_vars on launch.|
|`ask_limit_on_launch`|""|no|bool|Prompt user for a limit on launch.|
|`ask_tags_on_launch`|""|no|bool|Prompt user for job tags on launch.|
|`ask_skip_tags_on_launch`|""|no|bool|Prompt user for job tags to skip on launch.|
|`ask_job_type_on_launch`|""|no|bool|Prompt user for job type on launch.|
|`ask_verbosity_on_launch`|""|no|bool|Prompt user to choose a verbosity level on launch.|
|`ask_inventory_on_launch`|""|no|bool|Prompt user for inventory on launch.|
|`ask_credential_on_launch`|""|no|bool|Prompt user for credential on launch.|
|`survey_enabled`|""|no|bool|Enable a survey on the job template.|
|`survey_spec`|""|no|dict|JSON/YAML dict formatted survey definition.|
|`survey`|""|no|dict|JSON/YAML dict formatted survey definition. Alias of survey_spec|
|`become_enabled`|""|no|bool|Activate privilege escalation.|
|`allow_simultaneous`|""|no|bool|Allow simultaneous runs of the job template.|
|`timeout`|""|no|int|Maximum time in seconds to wait for a job to finish (server-side).|
|`job_slice_count`|""|no|int|The number of jobs to slice into at runtime. Will cause the Job Template to launch a workflow if value is greater than 1.|
|`webhook_service`|""|no|str|Service that webhook requests will be accepted from (github, gitlab)|
|`webhook_credential`|""|no|str|Personal Access Token for posting back the status to the service API|
|`scm_branch`|""|no|str|Branch to use in job run. Project default used if blank. Only allowed if project allow_override field is set to true.|
|`labels`|""|no|list|The labels applied to this job template|
|`custom_virtualenv`|""|no|str|Local absolute file path containing a custom Python virtualenv to use.|
|`notification_templates_started`|""|no|list|The notifications on started to use for this organization in a list.|
|`notification_templates_success`|""|no|list|The notifications on success to use for this organization in a list.|
|`notification_templates_error`|""|no|list|The notifications on error to use for this organization in a list.|
|`state`|`present`|no|str|Desired state of the resource.|


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

### Standard Project Data Structure
#### Json Example
```json
---
{
    "templates": [
        {
            "name": "Survey Template with vars",
            "job_type": "run",
            "inventory": "Demo Inventory",
            "survey_enabled": true,
            "survey": "{{ lookup('template', 'template_surveys/basic_survey.json') | regex_replace('\\n', '') }}",
            "project": "Tower Config",
            "playbook": "helloworld.yml",
            "credentials": [
                "Demo Credential"
              ],
            "extra_vars": "{{ survey_extra_vars }}",
            "notification_templates_error": [
                "Slack_for_testing"
              ]
        },
        {
            "name": "No Survey Template no vars",
            "job_type": "run",
            "inventory": "Demo Inventory",
            "project": "Tower Config",
            "playbook": "helloworld.yml",
            "credentials": [
                "Demo Credential"
              ],
            "survey": {},
            "extra_vars": "{{ empty_master_vars }}",
            "notification_templates_error": [
                "Slack_for_testing"
              ]
        }
    ]
}
```
#### Yaml Example
```yaml
---
templates:
- name: Survey Template with vars
  job_type: run
  inventory: Demo Inventory
  survey_enabled: true
  survey: "{{ lookup('template', 'template_surveys/basic_survey.json') | regex_replace('\\n', '') }}"
  project: Tower Config
  playbook: helloworld.yml
  credentials:
  - Demo Credential
  extra_vars: "{{ survey_extra_vars }}"
  notification_templates_error:
  - Slack_for_testing
- name: No Survey Template no vars
  job_type: run
  inventory: Demo Inventory
  project: Tower Config
  playbook: helloworld.yml
  credentials:
  - Demo Credential
  survey: {}
  extra_vars: "{{ empty_master_vars }}"
  notification_templates_error:
  - Slack_for_testing
```
### Survey Data Structure
#### Json Example
```json
{
    "name": "Basic Survey",
    "description": "Basic Survey",
    "spec": [
      {
        "question_description": "Name",
        "min": 0,
        "default": "",
        "max": 128,
        "required": true,
        "choices": "",
        "new_question": true,
        "variable": "basic_name",
        "question_name": "Basic Name",
        "type": "text"
      },
      {
        "question_description": "Choosing yes or no.",
        "min": 0,
        "default": "yes",
        "max": 0,
        "required": true,
        "choices": "yes\nno",
        "new_question": true,
        "variable": "option_true_false",
        "question_name": "Choose yes or no?",
        "type": "multiplechoice"
      },
      {
        "question_description": "",
        "min": 0,
        "default": "",
        "max": 0,
        "required": true,
        "choices": "group1\ngroup2\ngroup3",
        "new_question": true,
        "variable": "target_groups",
        "question_name": "Select Group:",
        "type": "multiselect"
      }
    ]
  }
```
## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Job Templates to Tower
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
        file: "json/templates.json"
        name: job_templates_json

    - name: Add Projects
      include_role:
        name: redhat_cop.tower_configuration.job_templates
      vars:
        tower_templates: "{{ job_templates_json.tower_templates }}"
```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
