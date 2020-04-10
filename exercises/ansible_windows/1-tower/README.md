Configuring Ansible Tower
=========================

There are a number of constructs in the Ansible Tower UI that enable
multi-tenancy, notifications, scheduling, etc. However, we are only
going to focus on a few of the key constructs that are required for this
workshop today.

- Credentials

- Projects

- Inventory

- Job Template

Logging into Tower
==================

Your Ansible Tower instance url and credentials were supplied to you on the page created for this workshop.

Your Ansible Tower license has already been applied for you, so after
logging in you should now see the Dashboard.

Creating a Machine Credential
=============================

Credentials are utilized by Tower for authentication when launching jobs
against machines, synchronizing with inventory sources, and importing
project content from a version control system.

There are many [types of
credentials](http://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html#credential-types)
including machine, network, and various cloud providers. In this
workshop, we are using a **machine** credential.

Step 1:
-------

Select CREDENTIALS from the left hand panel under resources

![Cred](images/1-tower-credentials.png)

Step 2:
-------

Click the ![Add](images/add.png) icon and add new credential

Step 3:
-------

Complete the form using the following entries:

| Key          | Value           |                                          |
|--------------|-----------------|------------------------------------------|
| Name         | Student Account |                                          |
| Organization | Default         |                                          |
| Type         | Machine         |                                          |
| Username     | student#        | **Replace # with your student number**   |
| Password     | *****           | Replace with your student password       |

![Add Machine Credential](images/1-tower-add-machine-credential.png)

Step 4:
-------

Select SAVE ![Save](images/at_save.png)  

Create an SCM Credential
========================

Our first credential was to access our Windows machines. We need another
to access our source code repository. Repeat the process as above, but
with the following details:

| Key          | Value                            |                                            |
|--------------|----------------------------------|--------------------------------------------|
| Name         | Git Credential                   |                                            |
| Description  | SCM credential for playbook sync |                                            |
| Organization | Default                          |                                            |
| Type         | Source Control                   |                                            |
| Username     | student#                         | Replace # with your student number         |
| Password     | *******                          | Replace ******* with your student password |

Select SAVE ![Save](images/at_save.png)  

![Add SCM Credential](images/1-tower-add-scm-credential.png)

Creating a Project
==================

A Project is a logical collection of Ansible playbooks, represented in
Tower. You can manage playbooks and playbook directories by either
placing them manually under the Project Base Path on your Tower server,
or by placing your playbooks into a source code management (SCM) system
supported by Tower, including Git, Subversion, and Mercurial.

Step 1:
-------
A **Project** is a logical collection of Ansible playbooks, represented in Tower. 

You can manage playbooks and playbook directories by either placing them manually on your Tower server, or by placing your playbooks into a source code management (SCM) system supported by Tower, including Git, Subversion, Mercurial, and Red Hat Insights.

In this environment, playbooks are stored in a git repository available on the workshop GitLab instance. Before a **Project** can be created in Ansible Tower, the git URL for the repository is needed. In order to obtain the URL to your project, login to the GitLab instance, select your workshop project and copy the `https` url presented after clicking the "Clone" button.

![Proj](images/1-gitlab-project.png)
![Clone](images/1-gitlab-clone.png)

The repo url will be used in **Step 3**

Step 2:
-------

Click **Projects** on the left hand panel.

![Proj](images/1-tower-project.png)

Click the ![Add](images/add.png) icon and add new project

Step 3:
-------

Complete the form using the following entries (**using your student
number in SCM URL**)

| Key            | Value                                                                   |                                                   |
|----------------|-------------------------------------------------------------------------|---------------------------------------------------|
| Name           | Ansible Workshop Project                                                |                                                   |
| Description    | Workshop playbooks                                                      |                                                   |
| Organization   | Default                                                                 |                                                   |
| SCM Type       | Git                                                                     |                                                   |
| SCM URL        | https://gitlab.**WORKSHOP**.rhdemo.io/**student#**/workshop_project.git | URL obtained from Step 1                          |
| SCM BRANCH     |                                                                         | Intentionally blank                               |
| SCM CREDENTIAL | Git Credential                                                          |                                                   |


SCM UPDATE OPTIONS

- [ ] Clean
- [ ] Delete on Update
- [x] Update Revision on Launch


![Defining a Project](images/1-tower-create-project.png)

Step 4:
-------

Select SAVE ![Save](images/at_save.png)

Step 5:
-------

Scroll down and validate that project has been successfully synchronized
against the source control repo upon saving. You should see a green icon
next to the project name in the list view at the bottom of the page.

![Succesfull Sync](images/1-tower-project-success.png)

Inventories
===========

An inventory is a collection of hosts against which jobs may be
launched. Inventories are divided into groups and these groups contain
the actual hosts. Inventories may be sourced manually, by entering host
names into Tower, or from one of Ansible Tower’s supported cloud
providers.

A static Inventory has already been created for you today. We will now
take a look at this inventory to show case the various features.

Step 1:
-------

Click **Inventories** from the left hand panel. You will see the
preconfigured Inventory listed. Click the Inventories' name **Windows
Workshop Inventory** or the Edit button. ![Edit](images/at_edit.png)

Step 2:
-------

You will now be viewing the Inventory. From here you can add Hosts,
Groups, or even add Variables specific to this Inventory.

![Edit Inventory](images/1-tower-edit-inventory.png)

We will be viewing the hosts, so click the **HOSTS** button.

Step 3:
-------

In the Hosts view, we can see every host associated with this
inventory. You will also see which groups a host is associated with.
Hosts can be associated with multiple groups. These groups can later
then be used to narrow down to the exact hosts we will later run our
playbooks on.

![Hosts View](images/1-tower-hosts-view.png)

Step 4:
-------

If you click the **GROUPS** button and then select the **Windows** group, you can inspect variables set at the group level that will apply to all hosts in that group.

![Group Edit](images/1-tower-group-edit.png)

Today, we have already defined a handful of variables to tell Ansible how to connect to hosts in this group. You do not have to define these variables as
a Group variable here, they could also be Host variables or reside
directly in your Template or Playbook. However, because these variables will be the same for **ALL** windows hosts in our environment, we defined them for the entire windows group.

By default, Ansible will attempt to use SSH to connect to any Host, so
for Windows we need to tell it utilize a different connection method, in
this case,
[WinRM](https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html).

**`ansible_connection: winrm`**

We also instruct Ansible to connect to the WinRM SSL port 5986 (the
non-SSL port runs on 5985 but is unencrypted).

**`ansible_port: 5986`**

We also tell Ansible to ignore the WinRM cert, since our lab doesn’t
have a proper certificate store setup.

**`ansible_winrm_server_cert_validation: ignore`**

Windows also has various authentication methods that we can utilize to
connect. Here we tell Ansible to use the **CredSSP** Transport Method to
authenticate to our Windows host:

**`ansible_winrm_transport: credssp`**



If you click the **HOSTS** button, you can view the hosts belonging to the windows group. If you click the link for the host on this page, you can view the host specific variables that have been defined.

![Host Edit](images/1-tower-host-edit.png)

**`ansible_host`**

This is the IP address of this particular server

**`ansible_password`** 

This is the password needed to connect to this server

**`ansible_user`**

This is the username that Ansible will use along with the password to connect to this server

These variables are very host specific thus have been defined at the host level instead of at the group level.

You can find more information about these and other settings in our
[Windows
Guides](https://docs.ansible.com/ansible/latest/user_guide/windows.html).
The authentication settings are particularly important and you will need
to review them and decide which method is best for your needs.

Replace the workshop name and student# i