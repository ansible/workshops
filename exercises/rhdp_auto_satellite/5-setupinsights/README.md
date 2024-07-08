Automated Satellite Workshop: Insights Environment Setup 
----------------------------------------------------------------------

**Introduction**<br>
This use-case will focus on connecting an individual's Red Hat Portal Account to the Automated Satellite Workshop environment for the purposes of demonstrating Insights functionality at the end of the workshop.  

This exercise is primarily targeted for a Red Hat SA to deliver a demo of the Insights services, though any individual with a Red Hat Portal Account, the appropriate account permissions and other prerequiistes could run through this exercise.

This exercise is perscriptive in its setup, yet open-ended in its implementation.

**Environment**
- Satellite 6.x 
- Ansible Automation Platform 4.x
- 3x RHEL 7  instances
- Red Hat Portal Account with 2 availble Red Hat RHEL Instanced-based Subscriptions 
    - Please note - that this lab will consume 2 subscriptions for the duration of this workshop

**Exercise Scenario**
- Exercise: Setup Insights


Overview
-----------------------------------------------------------------

**Summary**<br>
- Insights is a hosted service on console.redhat.com.  In order to access this service you need a Red Hat Portal Account
- Since accounts are associated with subscriptions, sharing an account widely could cause a lost of control of the account and subscription consumption
- Therefore this exercise will require the use of a user portal account and will require 2 RHEL Subscriptions


Ok, let's get started...  

Prerequisites
--------------
-   Information required for executing this exercise

    - Manifest created in your portal account targeted to Satellite 6.14 with appropriate subscriptions including a minimum of 2 RHEL Instance-based subscriptions with Smart Management and 1 Satellite Infrastructure subscription
        - Record the name ⇒ manifest_name 

    - Offline Token for accessing the Subscription Manager API
        - access.redhat.com -> Subscriptions -> Manage -> RHSM API Tokens - Generate Token ⇒ offline_token

    - Your Organization ID 
        - access.redhat.com -> Subscriptions -> Manage -> Activation Keys ⇒ rhsm_org_id OR
        - console.redhat.com -> Settings -> Remote Host Configuration -> Activation Keys⇒ rhsm_org_id

    - Red Hat Account username and password
        - username ⇒ redhat_portal_username
        - password ⇒ redhat_portal_password


Exercise:
-----------------------------------------------------------------
**Login to your AAP UI's**
> **NOTE** The following are *example* URLs. Your student lab URLs will be different.
* Ansible Automation Platform URL<br>
    Example: https://ansible-1.{random}.sandbox{###}.opentlc.com*

**Steps:**<br>
#### 1\. Logging into the Ansible Automation Platform (AAP)

-   Use a web browser on your computer to access the AAP GUI via the link found in the Environment above. And use the following username and password to login: *admin / <password>*

![login screen](images/4-setupinsights-aap2-login.png)

-   Upon successful login, you will be able to see the Ansible Automation Platform dashboard.

#### 2\. Setup Insights Template

-   Use the side pane menu on the left to select **Templates**.

-   Scroll down to find **Z / SETUP / Insights**.

> **NOTE** This template is a workflow template as indicated by the visualizer icon and type = Workflow Job Template

![Setup Insight](images/4-setupinsights-workflow-template.png)

-   Click ![visualizer Icon](images/4-setupinsights-visualizer.png) and review the workflow that will configure the environment for Insights

![Insights Workflow](images/4-setupinsights-insights-workflow.png)

- This workflow job template executes the following job templates

    - Insights / Replace Satellite Manifest - Replaces the Satellite manifest in the workshop with one that attaches to your Red Hat Portal Account
    - SERVER / RHEL7 - Register - Registers the hosts to Satellite
    - Insights / Install and Register - Installs Insights and registers the 3 RHEL hosts to Insights.  It also runs the Insights Compliance role which installs the openscap packages on the hosts
    - Insights / Create Insights Credential - Creates the AAP Insights Credential using your portal account information
    - Insights / Create Insights Project - Creates an Insights Project in AAP that provides a project for remediation playbooks created in Insights to be consumed by AAP

> **NOTE** Prior to executing the workflow job template you **MUST** add variables to the template.  To do that:


-   Click ![pencil](images/4-setupinsights-pencil.png) to the right of **Z / SETUP / Insights**.  This will open the edit details window as shown below:

![setup-insights](images/4-setupinsights-variables.png)

-   Add the following variables captured during the prerequisites:

    - manifest_name
    - offline_token
    - rhsm_org_id
    - redhat_portal_username
    - redhat_portal_password

-   Once the variables are entered click Save

-   Then click Launch

-   Since we are registering hosts to Satellite during this workflow you will be presented with this screen

![complete survey](images/4-setupinsights-survey.png)

- Enter the information as follows:
    - Server Name or Pattern - node
    - Choose Environment - Dev

-   Click Next and then Launch and watch the workflow complete

> **NOTE** You may click on each job template being executed to see the details of that job template run)

-   A successful workflow run will show the following:

![workflow complete](images/4-setupinsights-workflow-complete.png)

At this point in the exercise the Ansible Satellite Workshop is now connected to your Red Hat Portal Account and is configured to support demonstrating Insights.