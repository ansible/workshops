Automated Smart Management Workshop: CentOS/RHEL migration and upgrade
----------------------------------------------------------------------

**Introduction**<br>
This use-case will focus on conversion and migration from older CentOS versions to RHEL 8.3 (latest version as of Feb 2020). While we only show this process for a few systems, however, it can be scaled to a larger number of physical, virtual or cloud hosts using content repos provided by [Red Hat Satellite](https://www.redhat.com/en/technologies/management/satellite) (included in [Red Hat Smart Management](https://www.redhat.com/en/technologies/management/smart-management)). The upgrade process will be driven with automation built and run using [Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible).

**Environment**
- Satellite 6.8, Ansible Automation Platform 4.0.0
- 3x CentOS 7 instances 
- 3x RHEL 7  instances

**Upgrade Scenario**
- Exercise: Convert CentOS 7 to RHEL 7, then upgrade to RHEL 8
    - Covers CentOS 7 to RHEL 7 conversion
    - RHEL 7 to RHEL 8 upgrade

Overview
-----------------------------------------------------------------

**Summary**<br>
- Remember, during initial environment setup, we created a backup of the instance data (in case a fallback or restore is needed. Better safe than sorry.)
- We will utilize an additional project in Ansible Automation Platform, "Three Tier App / Dev", which will allow us to install (take a guess) a three tier application stack across the three CentOS nodes. Additionally, the project also provides a means to test/verify functionality of the application components, which we will perform pre RHEL conversion.
- Next, we employ the Convert2RHEL utility to convert the CentOS nodes to RHEL. There are many sources of information on this handy utility, here are several of note:
    - [How to convert from CentOS or Oracle Linux to RHEL](https://access.redhat.com/articles/2360841) (Jan 2021)
    - [Converting from CentOS to RHEL with Convert2RHEL and Satellite](https://www.redhat.com/en/blog/converting-centos-rhel-convert2rhel-and-satellite) (March 2020)
    - [Convert2RHEL: How to update RHEL-like systems in place to subscribe to RHEL](https://www.redhat.com/en/blog/convert2rhel-how-update-rhel-systems-place-subscribe-rhel) (Jan 2020)
- Verify functionality of the application stack post RHEL conversion.
- Lastly, we will perform an in-place upgrade RHEL 7 to 8 (WIP)

Things to consider if doing this in dev/test/stage-beta/prod:
- Commercial and/or in-house developed application version(s) support with the host OS
- Bootloader changes
- Network connection and network time synchonizations


| **A Note about using Satellite vs. Ansible Automation Platform for this...**<br>  | 
| ------------- | 
| Out of the box, Satellite 6 supports [RHEL systems roles](https://access.redhat.com/articles/3050101) (a collection of Ansible Roles) for a limited set of administration tasks. An Ansible Automation Platform subscription is need to execute more complex Ansible jobs, such as OS conversions and upgrades. Using these two solutions together ensures you have the best tool for the job for:<br>- Content Management (Satellite)<br>- OS Patching & Standardized Operating Environments (Satellite)<br>- Provisioning: OS, Infra Services and Applications/Other (Satellite and/or Ansible Automation Platform)<br>- Configuration of Infra and Apps (Ansible Automation Platform)<br><br>Reference: [Scope of Support for Ansible Components included with Red Hat Satellite 6](https://access.redhat.com/articles/3616041) |


Ok, let's get started...  

Pre-requisites
--------------

-   Exercise 0 : Lab Setup

-   Organization to be used = Default Organization

-   Location to be used = Default Location

-   A content view = RHEL7

-   Lifecycle environments = Dev, QA, Prod

Exercise:
-----------------------------------------------------------------
**Login to your Satellite & AAP UI's**
> **NOTE** The following are *example* URLs. Your student lab URLs will be different.
* Ansible Automation Platform URL<br>
    * *Example: https://student1.smrtmgmt013.mw01.redhatpartnertech.net*
* Ansible Automation Platform login/password 
* Satellite URL<br> 
    * *Example: https://student1-sat.smrtmgmt013.mw01.redhatpartnertech.net (Note the -sat added to the URL)*
* Satellite login/password (same as above)

Note that in the following steps that are being performed on AAP, at any time, over on the Satellite console, review the registered hosts via clicking Hosts => All Hosts.  Refresh the Hosts page to see changes as they occur a result from the automation being peformed via AAP.

**Steps:**<br>
#### 1\. Logging into the Ansible Automation Platform (AAP)

-   Use a web browser on your computer to access the AAP GUI via the link found in the Environment above. And use the following username and password to login: *admin / <password_set_in_deploy_vars>*

![login screen](images/4-convert2rhel-aap2-login.png)

-   Upon successful login, you will be able to see the Ansible Automation Platform dashboard.

#### 2\. Install Three Tier Application Stack

-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **CONVERT2RHEL / 96 - Three Tier App deployment** to launch the job.

![3tier-install](images/4-convert2rhel-3tier-install.png)

#### 3\. Take CentOS node snapshot (optional, however, recommended for this exercise)

-   Use the side pane menu on the left to select **Templates**.

-   Click ![copy template](images/4-convert2rhel-copy-template-icon.png)to the right of **CONVERT2RHEL / 01 - Take node snapshot** to copy the template.

![template-copy](images/4-convert2rhel-template-copy.png)

-   Click the newly created job template **CONVERT2RHEL / 01 - Take node snapshot @ some-timestamp**

-   Click **Edit** at the bottom left. 
    - Edit the name to **CONVERT2RHEL / 01 - Take node snapshot / CentOS7 Development**
    - In the **Variables** section, within *tags* remove:

    "short_name": "node*",

    ...and add:

    "ContentView": "CentOS7",

    "Environment": "Dev",

![template-edit](images/4-convert2rhel-template-edit.png)

- Review the changes, then at the bottom left, click **Save**
- Verify the template name change, as well as the tag adjustments in the **Variables** section then click **Launch**

![centos-snapshot](images/4-convert2rhel-centos-snapshot.png)

#### 4\. Verify three tier application functionality on CentOS nodes - pre Centos update

-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **CONVERT2RHEL / 97 - Three Tier App smoke test** to launch the job.

![3tier-smoketest](images/4-convert2rhel-3tier-smoketest.png)

#### 5\. Upgrade CentOS nodes to latest version

-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **CONVERT2RHEL / 02 - Upgrade OS to latest release** to launch the job.

![centos-update](images/4-convert2rhel-centos-update.png)

#### 6\. Verify three tier application functionality on CentOS nodes - post Centos update, pre Convert2RHEL

-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **CONVERT2RHEL / 97 - Three Tier App smoke test** to launch the job.

![3tier-smoketest-2](images/4-convert2rhel-3tier-smoketest-2.png)

#### 7\. Convert2RHEL - CentOS7 Development nodes to RHEL7 Development nodes

-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **CONVERT2RHEL / 03 - convert2rhel** to launch the job.

      - choose LE group to convert CentOS7_Dev
      - choose LE target RHEL7_Dev
> **NOTE** with some pre-configuration, any combination is possible
![conversion-select](images/4-convert2rhel-conversion-select.png)
- click **Next** to continue
![conversion-confirm](images/4-convert2rhel-conversion-confirm.png)
- confirm CentOS and RHEL LE variables set via survey selections and click **Launch**
![conversion-complete](images/4-convert2rhel-conversion-complete.png)

#### 8\. Query Satellite to get post conversion node-related details, set EC2 instance tags based on these details
-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **EC2 / Set instance tags based on Satellite(Foreman) facts** to launch the job.
![instance-tags](images/4-convert2rhel-instance-tags.png)

#### 9\. Update inventories via dynamic sources
-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **CONTROLLER / Update inventories via dynamic sources** to launch the job.
	  - Select "CentOS7" for Inventory To Update
      - select "Dev" for Choose Environment
      - Click **Next**, confirm prompted values, then click **Launch**
![centos-inventory](images/4-convert2rhel-centos-inventory.png)

-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **CONTROLLER / Update inventories via dynamic sources** to launch the job.
    - template CONTROLLER / Update inventories via dynamic sources
	  - Select "RHEL7" for Inventory To Update
      - select "Dev" for Choose Environment
      - Click **Next**, confirm prompted values, then click **Launch**
![rhel-inventory](images/4-convert2rhel-rhel-inventory.png)

#### 10\. Create student credential
-   Use the side pane menu on the left to select **Credentials**.
-   Click **Add**
	  - Name: Student Credential
      - Organization: Default
      - Credential Type: Machine
      - Username: student1 (example shown, use your assigned student name/number)
      - Password: same password as Ansible Automation Platform login/password
-   Click **Save**
![student-credential](images/4-convert2rhel-student-credential.png)

#### 11\. Copy template CONVERT2RHEL / 97 - Three Tier App smoke test to template CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development
-   Use the side pane menu on the left to select **Templates**.

-   Click ![copy template](images/4-convert2rhel-copy-template-icon.png)to the right of **CONVERT2RHEL / 97 - Three Tier App smoke test** to copy the template.

![template-copy](images/4-convert2rhel-template-copy-2.png)

-   Click the newly created job template **CONVERT2RHEL / 97 - Three Tier App smoke test @ some-timestamp**

-   Click **Edit** at the bottom left. 
    - Edit the name to **CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development**
    - Click ![lookup](images/4-convert2rhel-lookup-icon.png)under Inventory and select the radio button for **RHEL7 Development**, followed by **Select**.
    - Click ![lookup](images/4-convert2rhel-lookup-icon.png)under Credentials and select the radio button for **Student Credential**, followed by **Select**.
    - Review the changes, then scroll down and on the bottom left, click **Save**
    - Click **Launch** to run the new job template **CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development**

![3tier-smoketest-3](images/4-convert2rhel-3tier-smoketest-3.png)

> **EXTRA CREDIT - Convert2RHEL workflow template**
Create a workflow template incorporating the above standalone templates into a complete CentOS to RHEL conversion workflow!

>**EXTRA CREDIT - Infrastructure-as-Code "Choose Your Own Adventure"**
  - Fork Automated Smart Management repo to individual GitHub account
Before we begin, you'll need to fork the Automated Smart Management repo into your personal GitHub account.  If you do not have an individual GitHub account, you will need to create one to proceed. Utilization of a source code management (SCM) system is central to the "infrastructure as code" concepts put forth in this lab exercise, and in this case, GitHub is our SCM.

Once logged into [GitHub](https://github.com) navigate to the [Red Hat Partner Tech repo for Automated Smart Management](https://github.com/redhat-partner-tech/automated-smart-management) repo. Next, on the Automated Smart Management repo page, in the top, upper right of the page, click "Fork".  This will create a "forked" Automated Smart Management repo in your personal GitHub account.

[Switch the "Automated Management" project in AAP to utilize your newly cloned repo](https://github.com/your-github-username/automated-smart-management.git). The following files are some good places to start looking to see where you can adjust the Extra Vars instance tags to select/filter what particular instances that a job template/playbook gets run against:

`group_vars/control/inventories.yml`

`group_vars/control/job_templates.yml`

Once the updates are made, commit and push these changes to the cloned repo, followed by running the "SETUP / Controller" job template, which will propogate the changes to AAP itself.
...
