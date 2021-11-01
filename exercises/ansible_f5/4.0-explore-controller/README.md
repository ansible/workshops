# Exercise 4.0: Explore Red Hat Ansible Automation Controller

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#objective)
- [Guide](#guide)
- [Takeaways](#takeaways)
- [Complete](#complete)

# Objective

Ansible Automation Controller is a web-based solution where you can centralize and control your IT infrastructure with a visual dashboard, role-based access control, job scheduling, integrated notifications and graphical inventory management. Ansible Automation Controller includes a REST API and CLI in addition to the web UI.

In this lab, you will log in and perform some basic configurations that will be used in later labs to perform automation tasks against your F5 BIG-IP device.  This exercise will cover:
- Determining the Ansible Automation Platform version
- Locating and understanding:
  - **Inventories**
  - **Credentials**
  - **Projects**
  - **Templates**

# Guide

## Step 1: Login to the Ansible Automation Platform

Open up your web browser and type in the Ansible control node's DNS name

>For example if the student was assigned the student1 workbench and the workshop name was `durham-workshop` the link would be:

    **https://student1.durham-workshop.rhdemo.io**

>This login information has been provided by the instructor at the beginning of class.

![Controller Login Window](images/login_window.png)
- The username will be `admin`
- password provided by instructor

After logging in the Job Dashboard will be the default view as shown below.
![Controller Job Dashboard](images/tower_login.png)

1. Click on the **?** information button on the top right of the user interface and then click **About**.

   ![information button link](images/information_button.png)

2. A window will pop up similar to the following:

   ![version info window](images/version_info.png)

   Take note that the Ansible Automation Controller version is provided here.

## Step 2: Examine the Inventory

An inventory is required for Red Hat Ansible Controller to be able to run jobs.  An inventory is a collection of hosts against which jobs may be launched, the same as an Ansible inventory file. In addition, Red Hat Ansible Controller can make use of an existing configuration management database (cmdb) such as ServiceNow or Infoblox DDI.

>More info on Inventories in respect to Ansible Controller can be found in the [documentation here](https://docs.ansible.com/automation-controller/latest/html/userguide/inventories.html)

1. Click on the **Inventories** button under **RESOURCES** on the left menu bar.  

   ![Inventories Button](images/inventories.png)

2. Under **Inventories**,  Click on the `Workshop Inventory`.  

3. Under the `Workshop Inventory`, click the **HOSTS** button at the top.  There will be hosts configured here.  Click on one of the devices.

4. Click on the `Workshop Inventory` link at the top of the page to return the top level menu.

5. Click on **GROUPS**.  This is where you can configure Group of hosts
   
   ![Inventory](images/inventory.png)

## Step 3: Examine the Workshop Project

A project is how Ansible Playbooks are imported into Red Hat Ansible Automation Controller.  You can manage playbooks and playbook directories by either placing them manually under the Project Base Path on your Ansible Tower server, or by placing your playbooks into a source code management (SCM) system supported by Controler, including Git, Subversion, and Mercurial etc.

> For more information on Projects in Controller, please [refer to the documentation](https://docs.ansible.com/automation-controller/latest/html/userguide/projects.html)

1. Click on the **Projects** button under **RESOURCES** on the left menu bar.  

   ![projects link](images/projects.png)

2. Under **PROJECTS** there will be one pre-configured projects, `Ansible official demo project`. Open it up by clicking on the object.

   Note that `Git` is listed for this project.  This means this project is using `Git` for SCM.

   ![project link](images/project.png)

3. Under the `Ansible official demo project` click the **SCM TYPE** drop down menu

   Note that Git, Mercurial and Subversion are some of the choices.  Return the choice to Git so that the Project continues to function correctly.

## Step 4: Examine the Workshop Credential

Credentials are utilized by the Red Hat Ansible Automation Platform for authentication when launching **Jobs** against machines, synchronizing with inventory sources, and importing project content from a version control system.  For the workshop we need a credential to authenticate to the network devices.

> For more information on Credentials in Automation Controller please [refer to the documentation](https://docs.ansible.com/automation-controller/latest/html/userguide/credentials.html).

1. Click on the **Credentials** button under **RESOURCES** on the left menu bar.  

   ![credentials link](images/credentials.png)

2. Under **CREDENTIALS** there will be two pre-configured credential, `Workshop Credential`.  Click on the `Workshop Credential`.  

3. Under the `Workshop Credential` examine the following:
   
   - The **CREDENTIAL TYPE** is a `Machine` credential.  
   - The **USERNAME** is set to `ec2-user`.
   - The **PASSWORD** is `blank`. This credential is using a key instead of a password.
   - The **SSH PRIVATE KEY** is already configured and is `ENCRYPTED`.

   ![credential](images/credential.png)

## Step 5: Examine the Job Template

Templates or Job Templates define the parameters that will be used when executing an Ansible playbook. These parameters include previously mentioned features such as which project and inventory will be used.
Additionally, parameters such as logging level and process forks allow for additional granularity on how playbooks are ran.

1. Click on the **Templates** button under **RESOURCES** on the left menu bar.  

   ![templates link](images/templates.png)

2. Under **TEMPLATES** there will be at least one pre-configured Job Template `INFRASTRUCTURE / Turn off IBM Community Grid`. Open it up by clicking on the object.

   ![template link](images/template.png)

# Takeaways

- Ansible needs an inventory to execute Ansible Playbooks against.  This inventory is identical to what users would use with the command line only Ansible project.  
- Ansible Automation Controller can sync to existing SCM (source control management) including `GitHub`.  
- Ansible Automation Controller can store and encrypt credentials including SSH private keys and plain-text passwords.  Ansible Automation Platform can also sync to existing credential storage systems such as CyberArk and Vault by HashiCorp
- Job Templates define the parameters that will be used when executing an Ansible playbook

# Complete

You have completed lab exercise 4.0

You have now examined all three components required to get started with Ansible Automation Controller.  A credential, an inventory and a project.  In the next exercise we will create a job template.

[Click here to return to the Ansible Network Automation Workshop](../README.md)
