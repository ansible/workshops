Automated Smart Management Workshop: Setup and Demo Insights
----------------------------------------------------------------------

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md), ![france](../../../images/fr.png) [Français](README.fr.md).
<br>

**Introduction**<br>
This use-case will focus on connecting an individuals Red Hat Portal Account to the Automated Smart Management Workshop environment for the purposes of demostrating Insights functionality at the end of the workshop.  

This exercise is primarily targeted for a Red Hat SA to deliver a demo of the Insights services, though any individual with a Red Hat Portal Account, the appropriate account permissions and other prerequiistes could run through this exercise.

This exercise is perscriptive in its setup, yet open-ended in its implementation.

**Environment**
- Satellite 6.x 
- Ansible Automation Platform 4.x
- 3x RHEL 7  instances
- Red Hat Portal Account

**Exercise Scenario**
- Exercise: Setup Insights


Overview
-----------------------------------------------------------------

**Summary**<br>
- Insights is a hosted service on console.redhat.com.  In order to access this service you need a Red Hat Portal Account
- Since accounts are associated with subscriptions sharing an account widely could cause us to lose control of the account and subscription consumption
- Therefore this exercise will require the use of a personal portal account

Ok, let's get started...  

Pre-requisites
--------------

-   Exercise 0: Lab Setup

-   Information required for executing this exercise

    - Manifest created in your portal account targeted to Satellite 6.10 with appropriate subscriptions including a minimum of 2 RHEL Instance-based subscriptions with Smart Management and 1 Satellite Infrastructure subscription
        - Record the name ⇒ manifest_name 

    - Offline Token for accessing the Subscription Manager API
        - Access.redhat.com -> Subscriptions -> Manage -> RHSM API Tokens - Generate Token ⇒ offline_token

    - Your Organization ID 
        - Access.redhat.com -> Subscriptions -> Manager -> Activation Keys ⇒ rhsm_org_id OR
        - Console.redhat.com -> Settings -> Remote Host Configuration -> Activation Keys⇒ rhsm_org_id

    - Red Hat Account username and password
        - username ⇒ insights_user
        - password ⇒ insights_password


Exercise:
-----------------------------------------------------------------
**Login to your AAP UI's**
> **NOTE** The following are *example* URLs. Your student lab URLs will be different.
* Ansible Automation Platform URL<br>
    Example: https://student1.{random}.example.opentlc.com*

**Steps:**<br>
#### 1\. Logging into the Ansible Automation Platform (AAP)

-   Use a web browser on your computer to access the AAP GUI via the link found in the Environment above. And use the following username and password to login: *admin / <password_set_in_deploy_vars>*

![login screen](images/4-setupinsights-aap2-login.png)

-   Upon successful login, you will be able to see the Ansible Automation Platform dashboard.

#### 2\. Setup Insights Template

-   Use the side pane menu on the left to select **Templates**.

-   Scroll down to find **Setup / Insights**.

-   Note that it has the this template is a workflow template as indicated by the visualizer icon and type = Workflow Job Template

![Setup Insight](images/4-setupinsights-workflow-template.png)

-   Click ![visualizer Icon](images/4-setupinsights-visualizer.png) and review the workflow that will configure the environment for Insights

![Insights Workflow](images/4-setupinsights-insights-workflow.png)

- This workflow job template executes the following job templates

    - Insights / Replace Satellite Manifest - Replaces the Satellite manifest in the workshop with one that attaches to your account
    - Server /RHEL7 - Register - Registers the hosts to Satellite
    - Insights / Install and Register - Installs Insights and registers the 3 RHEL hosts to Insights.  It also runs the Insights Compliance role which installs the openscap packages on the host
    - Insights - Create Insights Credential - Creates the AAP Insights Credential using your portal account information
    - Insights - Create Insights Project - Creates an Insights Project in AAP that allows execution of any remediation automated created in Insights 

-   Prior to executing the workflow job template you MUST add variables to the template.  To do that:


-   Click ![pencil](images/4-setupinsights-pencil.png) to the right of **Setup / Insights**.  This will open the edit details window as shown below:

![setup-insights](images/4-setupinsights-variables.png)

-   Add the following variables captured during the pre-requisites:

    - manifest_name
    - offline_token
    - rhsm_org_id
    - insights_user
    - insights_password

-   Once the variables are entered click Save

-   Then click Launch

-   Since we are registering hosts to Satellite during this workflow you will be presented with this screen

![complete survey](4-setupinsights-survey.png)

- Enter the information as follows:
    - Server Name or Pattern - node
    - Choose Environment - Dev

-   Click Next and then Launch and watch the workflow complete (Note - you may click on each job template being executed to see the details of that job template run)

-   A successful workflow run will show the following:

![workflow complete](4-setupinsights-workflow-complete.png)








#### 3\. Take CentOS node snapshot (optional, however, recommended for this exercise)

-   Use the side pane menu on the left to select **Templates**.

-   Click ![copy template](images/4-convert2rhel-copy-template-icon.png) to the right of **CONVERT2RHEL / 01 - Take node snapshot** to copy the template.

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
- Selecting launch will take you to the **Jobs > CONVERT2RHEL / 01 - Take node snapshot / CentOS7 Development** output window where you will be able to follow each task executed as part of the playbook. This will take approximately 5 mins to complete.

![centos-snapshot](images/4-convert2rhel-centos-snapshot.png)

#### 4\. Verify three tier application functionality on CentOS nodes - pre Centos update

- Use the side pane menu on the left to select **Templates**.

- Click ![launch](images/4-convert2rhel-aap2-launch.png) to the right of **CONVERT2RHEL / 97 - Three Tier App smoke test** to launch the job.
- Selecting launch will take you to the **Jobs > CONVERT2RHEL / 97 - Three Tier App smoke test** output window where you will be able to follow each task executed as part of the playbook. This will take approximately 30 secs to complete.

![3tier-smoketest](images/4-convert2rhel-3tier-smoketest.png)

#### 5\. Upgrade CentOS nodes to latest version

- Use the side pane menu on the left to select **Templates**.

- Click ![launch](images/4-convert2rhel-aap2-launch.png) to the right of **CONVERT2RHEL / 02 - Upgrade OS to latest release** to launch the job.

- Selecting launch will take you to the **Jobs > CONVERT2RHEL / 02 - Upgrade OS to latest release** output window where you will be able to follow each task executed as part of the playbook. This will take approximately 6 mins to complete.

![centos-update](images/4-convert2rhel-centos-update.png)

#### 6\. Verify three tier application functionality on CentOS nodes - post Centos update, pre Convert2RHEL

- Use the side pane menu on the left to select **Templates**.

- Click ![launch](images/4-convert2rhel-aap2-launch.png)to the right of **CONVERT2RHEL / 97 - Three Tier App smoke test** to launch the job.

- Selecting launch will take you to the **Jobs > CONVERT2RHEL / 97 - Three Tier App smoke test** output window. This will take approximately 30 secs to complete.

![3tier-smoketest-2](images/4-convert2rhel-3tier-smoketest-2.png)

#### 7\. Convert2RHEL - CentOS7 Development nodes to RHEL7 Development nodes

-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png) to the right of **CONVERT2RHEL / 03 - convert2rhel** to launch the job.

      - choose LE group to convert CentOS7_Dev
      - choose LE target RHEL7_Dev


- Selecting launch will take you to the **Jobs > CONVERT2RHEL / 03 - convert2rhel** output window. This will take approximately 11 mins to complete.

> **NOTE** with some pre-configuration, any combination is possible
![conversion-select](images/4-convert2rhel-conversion-select.png)
- click **Next** to continue
![conversion-confirm](images/4-convert2rhel-conversion-confirm.png)
- confirm CentOS and RHEL LE variables set via survey selections and click **Launch**
![conversion-complete](images/4-convert2rhel-conversion-complete.png)

If you look in Satellite now (**Hosts > All Hosts**), you will see that all CentOS notes have been converted to RHEL 7.9 nodes.

![3tier-smoketest-2](images/4-convert2rhel-converstion-complete.png)

#### 8\. Query Satellite to get post conversion node-related details, set EC2 instance tags based on these details
-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png) to the right of **EC2 / Set instance tags based on Satellite(Foreman) facts** to launch the job.
![instance-tags](images/4-convert2rhel-instance-tags.png)

- Selecting launch will take you to the **Jobs > EC2 / Set instance tags based on Satellite(Foreman) facts** output window. This will take approximately 30 secs to complete.

#### 9\. Update inventories via dynamic sources
-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png) to the right of **CONTROLLER / Update inventories via dynamic sources** to launch the job.
    - Select "CentOS7" for Inventory To Update
    - Select "Dev" for Choose Environment
    - Click **Next**, confirm prompted values, then click **Launch**
    - Selecting launch will take you to the **Jobs > CONTROLLER / Update inventories via dynamic sources** output window. This will take approximately 30 secs to complete.
![centos-inventory](images/4-convert2rhel-centos-inventory.png)

-   Use the side pane menu on the left to select **Templates**.

-   Click ![launch](images/4-convert2rhel-aap2-launch.png) to the right of **CONTROLLER / Update inventories via dynamic sources** to launch the job.
    - template CONTROLLER / Update inventories via dynamic sources
    - Select "RHEL7" for Inventory To Update
      - select "Dev" for Choose Environment
      - Click **Next**, confirm prompted values, then click **Launch**
    - Selecting launch will take you to the **Jobs > CONTROLLER / Update inventories via dynamic sources** output window. This will take approximately 30 secs to complete.
    ![rhel-inventory](images/4-convert2rhel-rhel-inventory.png)

    - If you look in **Inventories > RHEL7 Development** you will now see that nodes[1-6] are in the inventory.
    ![rhel-inventory](images/4-convert2rhel-converstion-hosts.png)  

#### 10\. Create a converted RHEL credential
-   Use the side pane menu on the left to select **Credentials**.
-   Click ![copy template](images/4-convert2rhel-copy-template-icon.png) to the right of **Workshop Credential** to copy the credential.

![credential-copy](images/4-convert2rhel-workshop-credential-copy.png)

-   Click the newly created credential **Workshop Credential @ some-timestamp**

-   Click **Edit** at the bottom left.
    - Edit the name to **Converted RHEL Credential**
    - Change the username from "ec2-user" to "centos"

![converted-RHEL-credential](images/4-convert2rhel-workshop-credential.png)

-   Click **Save**

#### 11\. Copy template CONVERT2RHEL / 97 - Three Tier App smoke test to template CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development
-   Use the side pane menu on the left to select **Templates**.

-   Click ![copy template](images/4-convert2rhel-copy-template-icon.png) to the right of **CONVERT2RHEL / 97 - Three Tier App smoke test** to copy the template.

![template-copy](images/4-convert2rhel-template-copy-2.png)

-   Click the newly created job template **CONVERT2RHEL / 97 - Three Tier App smoke test @ some-timestamp**

-   Click **Edit** at the bottom left.
    - Edit the name to **CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development**
    - Click ![lookup](images/4-convert2rhel-lookup-icon.png) under Inventory and select the radio button for **RHEL7 Development**, followed by **Select**.
    - Click ![lookup](images/4-convert2rhel-lookup-icon.png) under Credentials and select the radio button for **Converted RHEL Credential**, followed by **Select**.
    - Review the changes, then scroll down and on the bottom left, click **Save**
    - Click **Launch** to run the new job template **CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development**
    - Selecting launch will take you to the **Jobs > CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development** output window. This will take approximately 30 secs to complete.

![3tier-smoketest-3](images/4-convert2rhel-3tier-smoketest-3.png)


The Three Tier App smoke test template should have completed successfully, which shows that we were able to complete the migration from CentOS 7 to RHEL 7, and when that process finished, our 3 tier application still functioned.

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
