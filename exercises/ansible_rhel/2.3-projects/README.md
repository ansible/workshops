# Exercise 2.3 - Projects & job templates

A Tower **Project** is a logical collection of Ansible Playbooks. You can manage your playbooks by placingthem into a source code management (SCM) system supported by Tower, including Git, Subversion, and Mercurial.

You should definitely keep your Playbooks under version control. In this lab we’ll use Playbooks kept in a Git repository.

## Setup Git Repository

For this demonstration we will use playbooks stored in a Git repository:

**https://github.com/TODO**


A Playbook to install the Apache webserver has already been commited to the directory **ApacheTODO**:

> **Tip**
> 
> Note the difference to other Playbooks you might have written\! Most importantly there is no `become` and `hosts` is set to `all`.

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

To configure and use this repository as a **Source Control Management (SCM)** system in Tower you have to create a **Project** that uses the repository

## Create the Project

  - Go to **Projects** in the side menu view click the ![plus](images/green_plus.png) button. Fill in the form:

  - **NAME:** ApacheTODO

  - **ORGANIZATION:** Default

  - **SCM TYPE:** Git

Now you need the URL to access the repo. Go to the Github repository mentioned above, choose the green **Clone or download** button on the right, click on **Use https** and copy the HTTPS URL.

> **Note**
> 
> If there is no **Use https** to click on, but a **Use SSH**, you are fine: just copy the URL. The important thing is that you copy the URL starting with **https**.

 Enter the URL into the Project configuration:

  - **SCM URL:** TODO
    
      - **SCM UPDATE OPTIONS:** Tick all three boxes to always get a fresh copy of the repository and to update the repository when launching a job.
    
      - Click **SAVE**

> **Tip**
> 
> The new Project will be synced automatically after creation.

Sync the Project again with the Git repository by going to the **Projects** view and clicking the circular arrow **Get latest SCM revision** icon to the right of the Project.

  - After starting the sync job, go to the **Jobs** view, find your job and have a look at the details.

What have you done in this section? You have:

  - Created a **Project** pointing to a Git repository using the new credentials

## Create a Job Template and Run a Job

A job template is a definition and set of parameters for running an Ansible job. Job templates are useful to execute the same job many times. So before running an Ansible **Job** from Tower you must create a **Job Template** that pulls together:

  - **Inventory**: On what hosts should the job run?

  - **Credentials** What credentials are needed to log into the hosts?

  - **Project**: Where is the Playbook?

  - **What** Playbook to use?

Okay, let’s just do that:

  - Go to the **Templates** view and click the ![plus](images/green_plus.png) button and choose **Job Template**.
    
      - **NAME:** Install Apache
    
      - **JOB TYPE:** Run
    
      - **INVENTORY:** Workshop Inventory
    
      - **PROJECT:** ApacheTODO
    
      - **PLAYBOOK:** apache\_install.ymlTODO
    
      - **CREDENTIAL:** Workshop Credentials
    
      - We need to run the tasks as root so check **Enable privilege escalation**
    
      - Click **SAVE**

Start a Job using this Job Template by going to the **Templates** view and clicking the rocket icon. Have a good look at the information the view provides.

> **Tip**
> 
> This might take some time because you configured the Project to update the SCM on launch.

After the Job has finished go to the **Jobs** view:

  - All jobs are listed here, you should see directly before the Playbook run an SCM update was started.

  - This is the Git update we configured for the **Project** on launch\!

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

  - In the **HOSTS** view select both hosts and click **RUN COMMANDS**

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

  - Go to the **Templates** view and launch the `Install Apache Ask` template.

  - It will now ask for the inventory to use, choose the `Webserver` inventory and click **LAUNCH**

  - Wait until the Job has finished and make sure it run only on `node1`

> **Tip**
> 
> The Job didn’t change anything because Apache was already installed in the latest version.

> **Tip**
> 
> Note or even test if you want to that if an Inventory is entered in the form, this will be the default choice when asked for an Inventory. If you leave the form empty, there will be no default selection.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
