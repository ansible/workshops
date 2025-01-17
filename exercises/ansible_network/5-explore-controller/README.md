# Exercise 5: Explore Ansible Automation Platform

**Read this in other languages**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md).

## Table of Contents

- [Exercise 5: Explore Ansible Automation Platform](#exercise-5-explore-ansible-automation-platform)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Guide](#guide)
    - [Step 1: Login to Ansible Automation Platform](#step-1-login-to-ansible-automation-platform)
    - [Step 2: Examine the Ansible Automation Platform Inventory](#step-2-examine-the-ansible-automation-platform-inventory)
    - [Step 3: Examine the Ansible Automation Platform Workshop Project](#step-3-examine-the-ansible-automation-platform-workshop-project)
    - [Step 4: Examine the Ansible Automation Platform Workshop Credential](#step-4-examine-the-ansible-automation-platform-workshop-credential)
  - [Takeaways](#takeaways)
  - [Complete](#complete)

## Objective

Explore and understand the lab environment.  This exercise will cover

* Determining the Ansible Automation Platform version running on the control node
* Locating and understanding:
  * **Inventory**
  * **Credentials**
  * **Projects**

## Guide

### Step 1: Login to Ansible Automation Platform

1.  Return to the workshop launch page provided by your instructor.

2.  Click on the link to the Ansible Automation Platform webUI.  You should see a login screen similar to the follow:

   Screenshot of Ansible Automation Platform login window.
![automation controller login window](images/automation_controller_login.png)

   * The username will be `admin`
   * password provided on launch page


3. After logging in the Job Dashboard will be the default view as shown below.

   ![dashboard](images/automation_controller_dashboard.png)

4. Click on the **?** button on the top right of the user interface and click **About**

   ![about button link](images/automation_controller_about.png)

5. A window will pop up similar to the following:

   ![version info window](images/automation_controller_about_info.png)


### Step 2: Examine the Ansible Automation Platform Inventory

An inventory is required for Ansible Automation Platform to be able to run jobs.  An inventory is a collection of hosts against which jobs may be launched, the same as an Ansible inventory file. In addition, Ansible Automation Platform can make use of an existing configuration management data base (cmdb) such as ServiceNow or Infoblox DDI.

> Note:
>
> More info on Inventories in respect to Ansible Automation Platform can be found in the [documentation here](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/latest/html/automation_controller_user_guide/controller-inventories)

1. Click on **Infrastructure** link under **Automation Execution** on the left menu bar, then click the **Inventories** link.

    ![Inventories Button](images/automation_controller_inventories.png)

2. Under Inventories click on the `Workshop Inventory`.

    ![Workshop Inventory Link](images/automation_controller_workshop_inventory.png)

3. Under the `Workshop Inventory` click the **Hosts** button at the top.  There will be four hosts here, rtr1 through rtr4 as well as the ansible control node.

   ![workshop inventory hosts](images/workshop_inventory_hosts.png)

4. Click on one of the devices.

   ![workshop inventory hosts rtr1](images/workshop_inventory_hosts_rtr1.png)

     Take note of the **VARIABLES** field.  The `host_vars` are set here including the `ansible_host` variable.

5. Click on **GROUPS**.  There will be multiple groups here including `routers` and `cisco`.  Click on one of the groups.

   ![workshop inventory groups](images/workshop_inventory_groups.png)

6. Click on one of the groups.

   ![workshop inventory group vars](images/workshop_inventory_group_vars.png)

     Take note of the **VARIABLES** field. The `group_vars` are set here including the `ansible_connection` and `ansible_network_os` variable.

### Step 3: Examine the Ansible Automation Platform Workshop Project

A project is how Ansible Playbooks are imported into Ansible Automation Platform.  You can manage playbooks and playbook directories by either placing them manually under the Project Base Path on your Ansible Automation Platform server, or by placing your playbooks into a source code management (SCM) system supported by Ansible Automation Platform, including Git (Github, Gitlab, etc).

> Note:
>
> For more information on Projects in Ansible Automation Platform, please [refer to the documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/latest/html/using_automation_execution/controller-projects)

1. Click on the **Projects** link under **Automation Execution** on the left menu bar.

   ![Workshop Project Link](images/automation_controller_projects.png)

2. Under **PROJECTS** there will be a `Workshop Project`.

    ![Workshop Project Link](images/workshop_project.png)

    Note that `GIT` is listed for this project.  This means this project is using Git for SCM.

3. Click on the `Workshop Project`.

  ![Workshop Project Detail](images/workshop_project_detail.png)

  > Note:
  >
  > Source Control URL is set to [https://github.com/network-automation/toolkit](https://github.com/network-automation/toolkitcredentials.html).

### Step 4: Examine the Ansible Automation Platform Workshop Credential

Credentials are utilized by Ansible Automation Platform for authentication when launching **Jobs** against machines, synchronizing with inventory sources, and importing project content from a version control system.  For the workshop we need a credential to authenticate to the network devices.

> Note:
>
> For more information on Credentials in Ansible Automation Platform please [refer to the documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/latest/html/automation_controller_user_guide/controller-credentials).

1. Click on the **Infrastructure** link under **Automation Execution** on the left menu bar, then click on the **Credentials** link

    ![credentials link](images/automation_controller_credentials.png)

2. Under **Credentials** there will be multiple pre-configured credentials, including `Workshop Credential`, `Controller Credential` and the `registry.redhat.io credential`.  Click on the `Workshop Credential`.

    ![Workshop Credential Link](images/workshop_credential.png)

3. Under the `Workshop Credential` examine the following:

* The **Credential type** is a **Machine** credential.
* The **Username** is set to `ec2-user`.
* The **SSH Private Key** is already configured, and is **Encrypted**.

{% include mesh.md %}

## Takeaways

<ul>
  <li>
    <strong>Ansible Automation Platform</strong> needs an <strong>inventory</strong> to execute Ansible Playbooks against.
    This inventory is identical to what users would use with the command line only Ansible project.
  </li>
  <li>
    <strong>Ansible Automation Platform</strong> can sync to existing SCM (source control management) including GitHub.
  </li>
  <li>
    <strong>Ansible Automation Platform</strong> can store and encrypt credentials including SSH private keys and plain-text passwords.
    <strong>Ansible Automation Platform</strong> can also sync to existing credential storage systems such as CyberArk and Vault by HashiCorp.
  </li>
</ul>


## Complete

You have completed lab exercise 5

You have now examined all three components required to get started with Ansible Automation Platform.  A **credential**, an **inventory** and a **project**.  In the next exercise we will create a job template.

---
[Previous Exercise](../4-resource-module/README.md) | [Next Exercise](../6-controller-job-template/README.md)

[Click here to return to the Ansible Network Automation Workshop](../README.md)
