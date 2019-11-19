# Exercise 7: Creating a Survey

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
   - [Step 1: Create a Job Template](#step-1-create-a-job-template)
   - [Step 2: Examine the playbook](#step-2-examine-the-playbook)
   - [Step 3: Create a survey](#step-3-create-a-survey)
   - [Step 4: Launch the Job Template](#step-4-launch-the-job-template)
   - [Step 5: Verify the banner](#step-5-verify-the-banner)
- [Takeaways](#takeaways)

# Objective

Demonstrate the use of Ansible Tower [survey feature](https://docs.ansible.com/ansible-tower/latest/html/userguide/job_templates.html#surveys). Surveys set extra variables for the playbook similar to ‘Prompt for Extra Variables’ does, but in a user-friendly question and answer way. Surveys also allow for validation of user input.

# Guide

## Step 1: Create a Job Template

1. Open the web UI and click on the `Templates` link on the left menu.

   ![templates link](images/templates.png)

2. Click on the green `+` button to create a new job template (make sure to select `Job Template` and not `Workflow Template`)

   | Parameter | Value |
   |---|---|
   | Name  | Network-Banner |
   |  Job Type |  Run |
   |  Inventory |  Workshop Inventory |
   |  Project |  Workshop Project |
   |  Playbook |  `network_banner.yml` |
   |  Credential |  Workshop Credential |

3. Scroll down and click the green `SAVE` button.  


## Step 2: Examine the playbook

Here is what the  `network_banner.yml` Ansible Playbook looks like:

<!-- {% raw %} -->
```yml
---
- name: set router banners
  hosts: routers
  gather_facts: no

  tasks:
    - name: load banner onto network device
      vars:
        - network_banner:  "{{ net_banner | default(None) }}"
        - banner_type: "{{ net_type | default('login') }}"
      include_role:
        name: banner
```
<!-- {% endraw %} -->


> Note: You can also view the Ansible Playbook here: [https://github.com/network-automation/tower_workshop](https://github.com/network-automation/tower_workshop)

The role **banner** has a very simple `main.yml` file:

<!-- {% raw %} -->
```yml
- name: configure banner
  include_tasks: "{{ ansible_network_os }}.yml"
```
<!-- {% endraw %} -->

The `ansible_network_os` variable is being used to parameterize the network OS and create a vendor neutral playbook.

If you are working with a junos device, this playbook would call for a task file called `junos.yml`.  If you are using an IOS-XE device, this playbook would call for a task file called `ios.yml`. This file will in turn contain the platform specific tasks:

<!-- {% raw %} -->
```yml
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


## Step 3: Create a survey


In this step you will create a *"survey"* of user input form to collect input from the user and populate the values for the variables `net_banner` and `banner_type`



1. Click on the blue add survey button

   ![add survey button](images/addsurvey.png)

2. Fill out the fields

   | Parameter | Value |
   |---|---|
   | Prompt  | Please enter the banner text |
   |  Description |  Please type into the text field the desired banner |
   |  Answer Variable Name |  `net_banner` |
   |  Answer type |  Textarea |
   |  Required |  Checkmark |

   For example:

   ![workshop survey](images/survey.png)

3. Click the green `+Add` button

   ![add button](images/add.png)

4. Next we will create a survey prompt to gather the `banner_type`. This will either be "motd" or "login" and will default to "login" per the playbook above.

   | Parameter               | Value                          |
   |-------------------------|--------------------------------|
   | Prompt                  | Please enter the  banner type  |
   | Description             | Please choose an option        |
   | Answer Variable Name    | `net_type`                    |
   | Answer type             | Multiple Choice(single select) |
   | Multiple Choice Options | login <br>motd                        |
   | default answer          | login                          |
   | Required                | Checkmark                      |

   For example:

   ![workshop survey](images/survey_2.png)

5. Click the green `+Add` button

   ![add button](images/add.png)

6. Click the green **SAVE** button to save the survey.  This will exit back to the main job template window.  Scroll down and click the second green **SAVE** button to exit to the job templates window.

## Step 4: Launch the Job Template

1. Click on the rocket ship to launch the job template.

   ![rocket launch](images/rocket.png)

   The job will immediately prompt the user to set the banner and the type.  

2.  Type in the banner message you want for the routers.

3.  Choose between `login` and `motd`.

4. Click next to see how the survey rendered the input as extra vars for the Ansible Playbook.  For this example screen shot the word ANSIBLE rendered into ASCII art.

   ![survey screen](images/surveyscreen.png)

5. Click the green **LAUNCH** button to kick off the job.

   ![launch button](images/launch.png)

Let the job run to completion.  Let the instructor know if anything fails.


## Step 5: Verify the banner

1. Login to one of the routers and see the banner setup

   ```
   [student1@ansible]$ ssh rtr4
   ```

   The banner will appear on login.  Here is an example from the **ANSIBLE** shown above.

   ![terminal output screen](images/terminal_output.png)

2. Verify on additional routers

# Takeaways

You have successfully demonstrated
 - Creation of a Job Template for configuring a banner on multiple network operating systems including Arista EOS, Cisco IOS and Juniper Junos.
 - Creation of a self service survey for the Job Template to fill out the `network_banner` and `banner_type` variables
 - Executing a Job Template on all four routers, loading a banner on them simultaneously

---

# Complete

You have completed lab exercise 7

[Click here to return to the Ansible Network Automation Workshop](../README.md)
