# Exercise 7: Creating a Survey

**Read this in other languages**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
   * [Step 1: Create a Job Template](#step-1-create-a-job-template)
   * [Step 2: Examine the playbook](#step-2-examine-the-playbook)
   * [Step 3: Create a survey](#step-3-create-a-survey)
   * [Step 4: Launch the Job Template](#step-4-launch-the-job-template)
   * [Step 5: Verify the banner](#step-5-verify-the-banner)
*  [Takeaways](#takeaways)
*  [Complete](#complete)

## Objective

Demonstrate the use of Automation controller [survey feature](https://docs.ansible.com/automation-controller/latest/html/userguide/job_templates.html#surveys). Surveys set extra variables for the playbook similar to ‘Prompt for Extra Variables’ does, but in a user-friendly question and answer way. Surveys also allow for validation of user input.

## Guide

### Step 1: Create a Job Template

1. Open the web UI and click on the `Templates` link on the left menu.

   ![templates link](images/controller_templates.png)

2. Click on the blue `Add` button and select **Add job template** to create a new job template (make sure to select `Job Template` and not `Workflow Template`)

   | Parameter | Value |
   |---|---|
   | Name  | Network-Banner |
   |  Job Type |  Run |
   |  Inventory |  Workshop Inventory |
   |  Project |  Workshop Project |
   | Execution Environment | Default execution environment |
   |  Playbook |  `playbooks/network_banner.yml` |
   |  Credential |  Workshop Credential |

3. Scroll down and click the blue `Save` button.

### Step 2: Examine the playbook

Here is what the  `network_banner.yml` Ansible Playbook looks like:

<!-- {% raw %} -->

```yaml
---
- name: set router banners
  hosts: routers
  gather_facts: no

  tasks:
    - name: load banner onto network device
      vars:
        - network_banner:  "{{ net_banner | default(None) }}"
        - banner_type: "{{ net_type | default('login') }}"
      name: "../roles/banner"
```

<!-- {% endraw %} -->

> Note: You can also view the Ansible Playbook here: [https://github.com/network-automation/toolkit](https://github.com/network-automation/toolkit)

The role **banner** has a very simple `main.yml` file:

<!-- {% raw %} -->

```yaml
- name: configure banner
  include_tasks: "{{ ansible_network_os }}.yml"
```

<!-- {% endraw %} -->

The `ansible_network_os` variable is being used to parameterize the network OS and create a vendor neutral playbook.

If you are working with a junos device, this playbook would call for a task file called `junos.yml`.  If you are using an IOS-XE device, this playbook would call for a task file called `ios.yml`. This file will in turn contain the platform specific tasks:

<!-- {% raw %} -->

```yaml
---
- name: add the junos banner
  junos_banner:
    text: "{{ network_banner }}"
    banner: "{{ banner_type }}"
```

<!-- {% endraw %} -->

> Note: Please observe that there are task files created for ios, nxos, eos and junos for this playbook.

Also note that we are passing in 2 variables to the task file.

1. `network_banner`: This variable is populated using the `net_banner` variable

2. `banner_type`: This variable is populated by a variable named `net_type`

### Step 3: Create a survey

In this step you will create a *"survey"* of user input form to collect input from the user and populate the values for the variables `net_banner` and `banner_type`

1. Click on the **Survey** tab within the Network-Banner Job Template

   ![add survey button](images/controller_job_survey.png)

2. Click the blue **Add** button

   ![add survey button](images/controller_add_survey.png)

3. Fill out the fields

   | Parameter | Value |
   |---|---|
   | Question  | Please enter the banner text |
   |  Description |  Please type into the text field the desired banner |
   |  Answer Variable Name |  `net_banner` |
   |  Answer type |  Textarea |
   |  Required |  Checkmark |

   For example:

   ![workshop survey](images/controller_survey_q_one.png)

4. Click the green `Add` button to create another question

   ![add survey button](images/controller_add_survey.png)

5. Next we will create a survey prompt to gather the `banner_type`. This will either be "motd" or "login" and will default to "login" per the playbook above.

   | Parameter               | Value                          |
   |-------------------------|--------------------------------|
   | Question                | Please enter the  banner type  |
   | Description             | Please choose an option        |
   | Answer Variable Name    | `net_type`                    |
   | Answer type             | Multiple Choice(single select) |
   | Multiple Choice Options | login <br>motd                        |
   | default answer          | login                          |
   | Required                | Checkmark                      |

   For example:

   ![workshop survey](images/controller_survey_q_two.png)

5. Click Save

6. Click the toggle switch to activate the survey and turn it On

   ![workshop survey toggle](images/controller_survey_toggle.png)

7. Click **Back to Templates**

### Step 4: Launch the Job Template

1. Click on the rocket ship to launch the job template.

   ![rocket launch](images/controller_launch_template.png)

   The job will immediately prompt the user to set the banner and the type.

2. Type in the banner message you want for the routers.

3. Choose between `login` and `motd`.

4. Click next to see how the survey rendered the input as extra vars for the Ansible Playbook.  For this example the banner text is set as "This router was configured by Ansible".

   ![survey screen](images/controller_survey.png)

5. Click the blue **Launch** button to kick off the job.

   ![launch button](images/controller_launch.png)

Let the job run to completion.  Let the instructor know if anything fails.

### Step 5: Verify the banner

1. Login to one of the routers and see the banner setup

   ```sh
   [student1@ansible]$ ssh rtr1
   ```

   The banner will appear on login.  Here is an example from above:

   ```
   [student1@ansible-1 ~]$ ssh rtr1
  Warning: Permanently added 'rtr1,3.237.253.154' (RSA) to the list of known hosts.

  This router was configured by Ansible
  ```

2. Verify on additional routers

## Takeaways

You have successfully demonstrated

* Creation of a Job Template for configuring a banner on multiple network operating systems including Arista EOS, Cisco IOS and Juniper Junos.
* Creation of a self service survey for the Job Template to fill out the `network_banner` and `banner_type` variables
* Executing a Job Template on all four routers, loading a banner on them simultaneously

## Complete

You have completed lab exercise 7

---
[Previous Exercise](../6--controller-job-template/README.md) | [Next Exercise](../8-controller-rbac/README.md)

[Click here to return to the Ansible Network Automation Workshop](../README.md)
