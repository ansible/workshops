# Exercise 8: Understanding RBAC in Ansible Tower

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png) [日本語](README.ja.md).

## Table of Contents

- [Objective](#Objective)
- [Guide](#Guide)
  - [Step 1: Login as network-admin](#step-1-login-as-network-admin)
  - [Step 2: Open the NETWORK ORGANIZATION](#step-2-open-the-network-organization)
  - [Step 3: Examine Teams](#step-3-examine-teams)
  - [Step 4: Examine the Netops Team](#step-4-examine-the-netops-team)
  - [Step 5: Login as network-admin](#step-5-login-as-network-admin)
  - [Step 6: Understand Team Roles](#step-6-understand-team-roles)
  - [Step 7: Job Template Permissions](#step-7-job-template-permissions)
  - [Step 8: Login as network-operator](#Step-8-login-as-network-operator)
  - [Step 9: Launching a Job Template](#step-9-launching-a-job-template)
  - [Bonus Step](#bonus-step)
- [Takeaways](#takeaways)


# Objective

One of the key benefits of using Ansible Tower is the control of users that use the system. The objective of this exercise is to understand Role Based Access Controls([RBACs](https://docs.ansible.com/ansible-tower/latest/html/userguide/security.html#role-based-access-controls)) with which Tower admins can define tenancies, teams, roles and associate users to those roles. This gives organizations the ability to secure the automation system and satisfy compliance goals and requirements.

# Guide

Lets review some Ansible Tower terminology:

- **Organizations:** Defines a tenancy for example *Network-org*, *Compute-org*. This might be reflective of internal organizational structure of the customer's organization.
- **Teams:** Within each organization, there may be more than one team. For instance *tier1-helpdesk*, *tier2-support*, *tier3-support*, *build-team* etc.
- **Users:** Users typically belong to teams. What the user can do within Tower is controlled/defined using **roles**
- **Roles:** Roles define what actions a user may perform. This can map very nicely to typical network organizations that have restricted access based on whether the user is a Level-1 helpdesk person, Level-2 or senior admin. Tower [documentation ](https://docs.ansible.com/ansible-tower/latest/html/userguide/security.html#built-in-roles)defines a set of built-in roles.

For more in depth details on RBAC terminology please refer to the [documentation](https://docs.ansible.com/ansible-tower/latest/html/userguide/security.html#role-based-access-controls)


## Step 1: Opening up Organizations

1. Login to Ansible Tower with the **admin** user.

   | Parameter | Value |
   |---|---|
   | username  | `admin`  |
   |  password|  provided by instructor |

2. Confirm that you are logged in as the **admin** user.

   ![admin user](images/RBAC_2.png)

3. Under the **ACCESS** section, click on **Organizations**

   As the *admin* user, you will be able to view all organizations configured for Ansible Tower:

   >Note: The orgs, teams and users were auto-populated for this workshop

4. Examine the organizations

   There are 2 organizations (other than Default):

   1. **RED HAT COMPUTE ORGANIZATION**
   2. **RED HAT NETWORK ORGANIZATION**

   ![organizations image](images/RBAC_3.png)

   >Observe that this page gives you a summary of all the teams, users, inventories, projects and job templates associated with it. If a Organization level admin is configure you will see that as well.

## Step 2: Open the NETWORK ORGANIZATION

1. Click on the **RED HAT NETWORK ORGANIZATION**.

   This brings up a section that displays the details of the organization.

   ![network organization image](images/RBAC_4.png)

2. Click on the **USERS** button to see users associated with this organization.

   >Observe that both the **network-admin** and **network-operator** users are associated with this organization.

## Step 3: Examine Teams

1. Click on **TEAMS** in the sidebar

   ![image identifying teams](images/RBAC_5.png )

2. Examine the teams.  The Ansible Tower admin  will be able to see all available teams.  There are four teams:

     1. Compute T1
     2. Compute T2
     3. Netadmin
     4. Netops   

   ![teams window image](images/RBAC_6.png )

## Step 4: Examine the Netops Team

1. Click on the **Netops** Team and then click on the **USERS** button. Pay attention to 2 particular users:
   1. network-admin
   2. network-operator

   ![image showing users](images/RBAC_7.png )

2. Observe the following two points:

   1. The **network-admin** user has administrative privileges for the **RED HAT NETWORK ORGANIZATION** organization.
   2. The **network-operator** is simply a member of the Netops team. We will log in as each of these users to understand the roles


## Step 5: Login as network-admin

1. Log out from the admin user by clicking the power symbol button in the top right corner of the Ansible Tower UI:

   Power Symbol: ![power symbol image](images/logout.png)

2. Login to the system with the **network-admin** user.

   | Parameter | Value |
   |---|---|
   | username  | network-admin  |
   |  password|  provided by instructor |

3. Confirm that you are logged in as the **network-admin** user.

   ![picture of network admin](images/RBAC_1.png)

4. Click on the **Organizations** link on the sidebar.

   You will notice that you only have visibility to the organization you are an admin of, the **REDHAT NETWORK ORGANIZATION**.  

   The following two Organizations are not seen anymore:
    - REDHAT COMPUTE ORGANIZATION
    - Default

5. Bonus step: Try this as the network-operator user (same password as network-admin).

   - What is the difference?
   - As the network operator are you able to view other users?
   - Are you able to add a new user or edit user credentials?

## Step 6: Understand Team Roles

1. To understand how different roles and therefore RBACs may be applied, log out and log back in as the **admin** user.

2. Navigate to **Inventories** and click on the  **Workshop Inventory**

3. Click on the **PERMISSIONS** button

   ![workshop inventory window](images/RBAC_8.png )

4. Examine the permissions assigned to each user

   ![permissions window](images/RBAC_9.png )

   Note the **TEAM ROLES** assigned for the **network-admin** and **network-operator** users. By assigning the **USE** Role, the **network-operator** user has been granted permission to use this particular inventory.

## Step 7: Job Template Permissions

1. Click on the **Templates** button in the left menu

2. Click on the **Network-Commands** Job Template

3. Click on the **PERMISSIONS** button at the top

   ![permissions window](images/RBAC_10.png )

   >Note how the same users have different roles for the job template. This highlights the granularity operators can introduce with Ansible Tower in controlling "Who gets access to what". In this example, the network-admin can update (**ADMIN**) the **Network-Commands** job template, whereas the network-operator can only **EXECUTE** it.


## Step 8: Login as network-operator

Finally, to see the RBAC in action!

1. Log out at admin and log back in as the **network-operator** user.

   | Parameter | Value |
   |---|---|
   | username  | `network-operator`  |
   |  password|  provided by instructor |

2. Navigate to **Templates** and click on the **Network-Commands** Job Template.

   ![network commands job template](images/RBAC_11.png )

3. Note that, as the *network-operator* user, you will have no ability to change any of the fields.


## Step 9: Launching a Job Template

1. Verify you are logged in as the `network-operator` user

2. Click on **Templates** link on the sidebar again

3. This time launch the **Network-Commands** template by clicking on the "rocket" icon:

   ![click the rocket icon](images/RBAC_12.png )

4. You will be prompted by a dialog-box that lets you choose one of the pre-configured show commands.

   ![pre configured survey image](images/RBAC_13.png )

5. Go ahead and choose a command and click ** Next***Launch* to see the playbook being executed and the results being displayed.

## Bonus Step

If time permits, log back in as the network-admin and add another show command you would like the operator to run. This will also help you see how the *Admin* Role of the network-admin user allows you to edit/update the job template.

# Takeaways

 - Using Ansible Tower's powerful RBAC feature, you can see it is easy to restrict access to operators to run prescribed commands on production systems without requiring them to have access to the systems themselves.
 - Ansible Tower can support multiple Organizations, multiple Teams and users.  Users can even belong to multiple Teams and Organizations if needed.  Something not covered in this exercise is that we do not need to manage users in Ansible Tower, we can use [enterprise authentication](https://docs.ansible.com/ansible-tower/latest/html/administration/ent_auth.html) including Active Directory, LDAP, RADIUS, SAML and TACACS+.
 - If there needs to be an exception (a user needs access but not his entire team) this is also possible.  The granularity of RBAC can be down to the credential, inventory or Job Template for an individual user.

---

# Complete

You have completed lab exercise 8

[Click here to return to the Ansible Network Automation Workshop](../README.md)
