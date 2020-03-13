# Exercise 2.3 - Projects & job templates

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md).

* [Setup Git Repository](#setup-git-repository)
* [Create the Project](#create-the-project)
* [Create a Job Template and Run a Job](#create-a-job-template-and-run-a-job)
* [Challenge Lab: Check the Result](#challenge-lab-check-the-result)
* [What About Some Practice?](#what-about-some-practice)

A Tower **Project** is a logical collection of Ansible Playbooks. You can manage your playbooks by placing them into a source code management (SCM) system supported by Tower, including Git, Subversion, and Mercurial.

You should definitely keep your Playbooks under version control. In this lab we’ll use Playbooks kept in a Git repository.

## Setup Git Repository

For this demonstration we will use playbooks stored in a Git repository:

**https://github.com/ansible/workshop-examples**


A Playbook to install the Apache webserver has already been commited to the directory **rhel/apache**, `apache_install.yml`:

```yaml
---
- name: Apache server installed
  hosts: all

  tasks:
  - name: latest Apache version installed
    yum:
      name: httpd
      state: latest

  - name: latest firewalld version installed
    yum:
      name: firewalld
      state: latest

  - name: firewalld enabled and running
    service:
      name: firewalld
      enabled: true
      state: started

  - name: firewalld permits http service
    firewalld:
      service: http
      permanent: true
      state: enabled
      immediate: yes

  - name: Apache enabled and running
    service:
      name: httpd
      enabled: true
      state: started
```

> **Tip**
>
> Note the difference to other Playbooks you might have written\! Most importantly there is no `become` and `hosts` is set to `all`.

To configure and use this repository as a **Source Control Management (SCM)** system in Tower you have to create a **Project** that uses the repository

## Create the Project

  - Go to **RESOURCES → Projects** in the side menu view click the ![plus](images/green_plus.png) button. Fill in the form:

  - **NAME:** Ansible Workshop Examples

  - **ORGANIZATION:** Default

  - **SCM TYPE:** Git

Now you need the URL to access the repo. Go to the Github repository mentioned above, choose the green **Clone or download** button on the right, click on **Use https** and copy the HTTPS URL.

> **Note**
>
> If there is no **Use https** to click on, but a **Use SSH**, you are fine: just copy the URL. The important thing is that you copy the URL starting with **https**.

 Enter the URL into the Project configuration:

- **SCM URL:** `https://github.com/ansible/workshop-examples.git`

- **SCM UPDATE OPTIONS:** Tick the first three boxes to always get a fresh copy of the repository and to update the repository when launching a job.

- Click **SAVE**

The new Project will be synced automatically after creation. But you can also do this automatically: Sync the Project again with the Git repository by going to the **Projects** view and clicking the circular arrow **Get latest SCM revision** icon to the right of the Project.

After starting the sync job, go to the **Jobs** view: there is a new job for the update of the Git repository.

## Create a Job Template and Run a Job

A job template is a definition and set of parameters for running an Ansible job. Job templates are useful to execute the same job many times. So before running an Ansible **Job** from Tower you must create a **Job Template** that pulls together:

- **Inventory**: On what hosts should the job run?

- **Credentials** What credentials are needed to log into the hosts?

- **Project**: Where is the Playbook?

- **What** Playbook to use?

Okay, let’s just do that: Go to the **Templates** view, click the ![plus](images/green_plus.png) button and choose **Job Template**.

> **Tip**
>
> Remember that you can often click on magnfying glasses to get an overview of options to pick to fill in fields.

- **NAME:** Install Apache

- **JOB TYPE:** Run

- **INVENTORY:** Workshop Inventory

- **PROJECT:** Ansible Workshop Examples

- **PLAYBOOK:** `rhel/apache/apache_install.yml`

- **CREDENTIAL:** Workshop Credentials

- We need to run the tasks as root so check **Enable privilege escalation**

- Click **SAVE**

You can start the job by directly clicking the blue **LAUNCH** button, or by clicking on the rocket in the Job Templates overview. After launching the Job Template, you are automatically brought to the job overview where you can follow the playbook execution in real time:

![job exection](images/job_overview.png)

Since this might take some time, have a closer look at all the details provided:

- All details of the job template like inventory, project, credentials and playbook are shown.

- Additionally, the actual revision of the playbook is recorded here - this makes it easier to analyse job runs later on.

- Also the time of execution with start and end time is recorded, giving you an idea of how long a job execution actually was.

- On the right side, the output of the playbook run is shown. Click on a node underneath a task and see that detailed information are provided for each task of each node.

After the Job has finished go to the main **Jobs** view: All jobs are listed here, you should see directly before the Playbook run an SCM update was started. This is the Git update we configured for the **Project** on launch\!

## Challenge Lab: Check the Result

Time for a little challenge:

  - Use an ad hoc command on both hosts to make sure Apache has been installed and is running.

You have already been through all the steps needed, so try this for yourself.

> **Tip**
>
> What about `systemctl status httpd`?

> **Warning**
>
> **Solution Below**

- Go to **Inventories** → **Workshop Inventory**

- In the **HOSTS** view select all hosts and click **RUN COMMANDS**

- **MODULE:** command

- **ARGUMENTS:** systemctl status httpd

- **MACHINE CREDENTIALS:** Workshop Credentials

- Click **LAUNCH**

## What About Some Practice?

Here is a list of tasks:

> **Warning**
>
> Please make sure to finish these steps as the next chapter depends on it\!

- Create a new inventory called `Webserver` and make only `node1` member of it.

- Copy the `Install Apache` template using the copy icon in the **Templates** view

- Change the name to `Install Apache Ask`

- Change the **INVENTORY** setting of the Project so it will ask for the inventory on launch

- **SAVE**

- Launch the `Install Apache Ask` template.

- It will now ask for the inventory to use, choose the `Webserver` inventory and click **LAUNCH**

- Wait until the Job has finished and make sure it run only on `node1`

> **Tip**
>
> The Job didn’t change anything because Apache was already installed in the latest version.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
