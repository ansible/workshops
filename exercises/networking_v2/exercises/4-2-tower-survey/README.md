# Exercise 4-2: Creating a Survey

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate the use of Ansible Tower [survey feature](https://docs.ansible.com/ansible-tower/latest/html/userguide/job_templates.html#surveys). Surveys set extra variables for the playbook similar to ‘Prompt for Extra Variables’ does, but in a user-friendly question and answer way. Surveys also allow for validation of user input.

# Guide

## Step 1:

Open the web UI and click on the `Templates` link on the left menu.

![templates link](images/templates.png)

Click on the green `+` button to create a new job template (make sure to select `Job Template` and not `Workflow Template`)

| Parameter | Value |
|---|---|
| Name  | CONFIGURE BANNER  |
|  Job Type |  Run |
|  Inventory |  Workshop Inventory |
|  Project |  Workshop Project |
|  Playbook |  network_banner.yml |
|  Credential |  Workshop Credential |

Scroll down and click the green `save` button.


## Step 2:

To understand the next step we need to take a step back.  When we loaded this [workshop project](https://github.com/network-automation/tower_workshop) into Tower we have access to a variety of playbooks including this `network_banner.yml` playbook.  This specific Playbook makes use of the [net_banner](https://docs.ansible.com/ansible/latest/modules/net_banner_module.html) agnostic network module which looks like the following:

```
- name: LOAD BANNER ONTO NETWORK DEVICE
  net_banner:
    banner: login
    text: |
      "{{network_banner}}"
```

We can set the variable `network_banner` anywhere and overload the default on the Playbook.  We will do this with an Ansible Tower **survey**.

## Step 3:

Click on the blue add survey button

![add survey button](images/addsurvey.png)

Fill out the fields

| Parameter | Value |
|---|---|
| Prompt  | Please enter the login banner information  |
|  Description |  Please type into the text field the desired banner |
|  Answer Variable Name |  network_banner |
|  Answer type |  Textarea |
|  Required |  Checkmark |

It should look like this screenshot:
![workshop survey](images/survey.png)

Click the green +Add button

![add button](images/add.png)

Click the green Save button

## Step 3

Click the Jobs button the left menu.

![jobs button](images/jobs.png)

The Jobs link displays a list of jobs and their status–shown as completed successfully or failed, or as an active (running) job. Actions you can take from this screen include viewing the details and standard output of a particular job, relaunch jobs, or remove jobs.

![jobs link](images/jobslink.png)

The **BACKUP NETWORK CONFIG** job was the most recent (unless you have been launching more jobs).  Click on this job to return to the **Job Details View**.  Tower will save the history of every job launched and it is possible to see down to the task level of what happened on a particular job.



## Step 4

To understand where the Playbooks are that we imported via the Project, return to the command line of the control node.  Switch to the **awx** user.

```
sudo su - awx
```

You have now switched to the awx user, perform an ls to see what files are in here.

```
-bash-4.2$ ls
beat.db  favicon.ico  job_status  projects  public  uwsgi.stats  venv  wsgi.py
```

There is a **projects** folder here that directly corresponds to the Projects link in Ansible Tower.  Move into the projects directory to see what is available.

```
-bash-4.2$ cd projects/
-bash-4.2$ ls
_10__workshop_project  _10__workshop_project.lock
-bash-4.2$ cd _10__workshop_project
```

The number might not match exactly here, but the **workshop_project** directly corresponds to our WorkShop Project we created in the previous exercise.

Perform an ls -la to look at one files are available in this directory.

```
-bash-4.2$ ls -la
total 44
drwxr-xr-x. 9 awx awx 4096 Jan 22 19:27 .
drwxr-x---. 3 awx awx   69 Jan 22 19:33 ..
-rw-r--r--. 1 awx awx  652 Jan 22 15:45 ansible.cfg
drwxr-xr-x. 4 awx awx   33 Jan 22 18:41 eos
drwxr-xr-x. 8 awx awx  198 Jan 22 19:27 .git
drwxr-xr-x. 2 awx awx   21 Jan 22 15:45 group_vars
drwxr-xr-x. 4 awx awx   33 Jan 22 18:37 ios
drwxr-xr-x. 4 awx awx   33 Jan 22 18:49 junos
-rw-r--r--. 1 awx awx 2535 Jan 22 19:27 network_backup.yml
-rw-r--r--. 1 awx awx  247 Jan 22 15:45 network_banner.yml
-rw-r--r--. 1 awx awx  252 Jan 22 15:45 network_l3_interface.yml
-rw-r--r--. 1 awx awx  250 Jan 22 15:45 network_restore.yml
drwxr-xr-x. 2 awx awx   96 Jan 22 15:45 network_setup
-rw-r--r--. 1 awx awx  543 Jan 22 15:45 network_system.yml
-rw-r--r--. 1 awx awx  609 Jan 22 15:45 network_time.yml
-rw-r--r--. 1 awx awx  272 Jan 22 15:45 network_user.yml
-rw-r--r--. 1 awx awx  297 Jan 22 15:45 README.md
-rw-r--r--. 1 awx awx  712 Jan 22 15:45 sample-vars-auto.yml
drwxr-xr-x. 2 awx awx  103 Jan 22 15:45 templates
```

The Playbooks (shown as .yml files) should directly correspond to the Github repo: https://github.com/network-automation/tower_workshop


# Solution
You have finished this exercise.  

You have
 - created a job template for backing up network configurations
 - launched the job template from the Ansible Tower UI
 - looked under the covers on the control node to see where the Playbooks are being stored

[Click here to return to the lab guide](../README.md)
