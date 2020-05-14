# Workshop Exercise - Role-based access control

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Table Contents

* [Objective](#objective)
* [Guide](#guide)
* [Ansible Tower Users](#ansible-tower-users)
* [Ansible Tower Teams](#ansible-tower-teams)
* [Granting Permissions](#granting-permissions)
* [Test Permissions](#test-permissions)

# Objective

You have already learned how Ansible Tower separates credentials from users. Another advantage of Ansible Tower is the user and group rights management.  This exercise demonstrates Role Based Access Control (RBAC)

# Guide

## Ansible Tower Users

There are three types of Tower Users:

- **Normal User**: Have read and write access limited to the inventory and projects for which that user has been granted the appropriate roles and privileges.

- **System Auditor**: Auditors implicitly inherit the read-only capability for all objects within the Tower environment.

- **System Administrator**: Has admin, read, and write privileges over the entire Tower installation.

Let’s create a user:

- In the Tower menu under **ACCESS** click **Users**

- Click the green plus button

- Fill in the values for the new user:

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>FIRST NAME </td>
    <td>Werner</td>
  </tr>
  <tr>
    <td>LAST NAME</td>
    <td>Web</td>
  </tr>
  <tr>
    <td>Organization</td>
    <td>Default</td>
  </tr>         
  <tr>
    <td>EMAIL</td>
    <td>wweb@example.com</td>
  </tr>
  <tr>
    <td>USERNAME</td>
    <td>wweb</td>
  </tr>  
  <tr>
    <td>PASSWORD</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>CONFIRM PASSWORD</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>USER TYPE</td>
    <td>Normal User</td>
  </tr>                           
</table>




    - Confirm password

- Click **SAVE**

## Ansible Tower Teams

A Team is a subdivision of an organization with associated users, projects, credentials, and permissions. Teams provide a means to implement role-based access control schemes and delegate responsibilities across organizations. For instance, permissions may be granted to a whole Team rather than each user on the Team.

Create a Team:

- In the menu go to **ACCESS → Teams**

- Click the green plus button and create a team named `Web Content`.

- Click **SAVE**

Now you can add a user to the Team:

- Switch to the Users view of the `Web Content` Team by clicking the **USERS** button.

- Click the green plus button, tick the box next to the `wweb` user and click **SAVE**.

Now click the **PERMISSIONS** button in the **TEAMS** view, you will be greeted with "No Permissions Have Been Granted".

Permissions allow to read, modify, and administer projects, inventories, and other Tower elements. Permissions can be set for different resources.

## Granting Permissions

To allow users or teams to actually do something, you have to set permissions. The user **wweb** should only be allowed to modify content of the assigned webservers.

Add the permission to use the template:

- In the Permissions view of the Team `Web Content` click the green plus button to add permissions.

- A new window opens. You can choose to set permissions for a number of resources.

    - Select the resource type **JOB TEMPLATES**

    - Choose the `Create index.html` Template by ticking the box next to it.

- The second part of the window opens, here you assign roles to the selected resource.

    - Choose **EXECUTE**

- Click **SAVE**

## Test Permissions

Now log out of Tower’s web UI and in again as the **wweb** user.

- Go to the **Templates** view, you should notice for wweb only the `Create
  index.html` template is listed. He is allowed to view and launch, but not to edit the Template. Just open the template and try to change it.

- Run the Job Template by clicking the rocket icon. Enter the survey content to your liking and launch the job.

- In the following **Jobs** view have a good look around, note that there where changes to the host (of course…​).

Check the result: execute `curl` again on the control host to pull the content of the webserver on the IP address of `node1` (you could of course check `node2` and `node3`, too):

```bash
$ curl http://22.33.44.55
```

Just recall what you have just done: You enabled a restricted user to run an Ansible Playbook

  - Without having access to the credentials

  - Without being able to change the Playbook itself

  - But with the ability to change variables you predefined\!

Effectively you provided the power to execute automation to another user without handing out your credentials or giving the user the ability to change the automation code. And yet, at the same time the user can still modify things based on the surveys you created.

This capability is one of the main strengths of Ansible Tower\!

----
**Navigation**
<br>
[Previous Exercise](../2.4-surveys) - [Next Exercise](../2.6-workflows)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
