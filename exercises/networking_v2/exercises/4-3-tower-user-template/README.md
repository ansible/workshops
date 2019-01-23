# Exercise 4-2: Creating a Tower Job Template - User Template

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Playbook Output](#playbook-output)
- [Solution](#solution)

# Objective

Demonstrate a vendor agnostic job template for user creation.  This job will configure a specified user through a survey.

This exercise will differ from the previous exercise by automating the creation of the survey.  We will use a supplied survey specification file (`user.json`) along with the [tower_job_template module](https://docs.ansible.com/ansible/latest/modules/tower_job_template_module.html) to quickly provision the job into Ansible Tower.

# Guide

## Step 1:

Make sure you are on the control node cli. Using your favorite text editor (`vim` and `nano` are available on the control host) create a new file called `userjob.yml`.

```
---
- name: TOWER CONFIGURATION IN PLAYBOOK FORM
  hosts: ansible
  connection: local
  become: yes
  gather_facts: no
  tasks:

    - name: CREATE USER JOB TEMPLATE
      tower_job_template:
        name: "CONFIGURE USER"
        job_type: "run"
        inventory: "Workshop Inventory"
        project: "Workshop Project"
        playbook: "network_user.yml"
        credential: "Workshop Credential"
        survey_enabled: true
        survey_spec: "{{ lookup('template', '{{playbook_dir}}/user.json') }}"
        tower_username: admin
        tower_password: ansible
        tower_host: https://localhost
```

## Step 2:

Launch the job with the `ansible-playbook` command.

## Step 3

Click the Jobs button the left menu.

![jobs button](images/jobs.png)

The Jobs link displays a list of jobs and their status–shown as completed successfully or failed, or as an active (running) job. Actions you can take from this screen include viewing the details and standard output of a particular job, relaunch jobs, or remove jobs.

![jobs link](images/jobslink.png)

The **BACKUP NETWORK CONFIG** job was the most recent (unless you have been launching more jobs).  Click on this job to return to the **Job Details View**.  Tower will save the history of every job launched and it is possible to see down to the task level of what happened on a particular job.

# Solution
You have finished this exercise.  

You have
 - created a job template for backing up network configurations
 - launched the job template from the Ansible Tower UI
 - looked under the covers on the control node to see where the Playbooks are being stored

[Click here to return to the lab guide](../README.md)
