Automated Smart Management Workshop: Explore Insights
----------------------------------------------------------------------

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md), ![france](../../../images/fr.png) [Français](README.fr.md).
<br>

**Introduction**<br>
This use-case will focus on exploring some of the services available on Red Hat Insights at console.redhat.com.  

Prerequisites
--------------

-   Exercise 0: Lab Setup

-   Exercise 4: Insights Setup

#### Explore Insights on console.redhat.com

This exercise is much less prescriptive and is designed to provide the student with some general guidance to get started.  This exercise will look at console.redhat.com

-   Login to console.redhat.com using portal account credentials

-   Select Red Hat Enterprise Linux -> Red Hat Insights

-   This will bring you to the Overview page which depicts a dashboard of the hosts that are registered to Insights

    - Explore this dashboard noting that each box addresses an Insights Service

-   Click on Inventory

    - Note that the hosts registered during the Setup / Insights Workflow Template job run are present at the top of the list

    - Click into each host to see the details of each host on the General Information tab

![inventory-general-information](images/5-exploreinsights-inventory-general.png)

- Click on each of the other tabs to see the information that Insights has collected about each host.  For example click on Vulnerability.  This view will show all the vulnerabilities for that host

- Note that on the right most column labeled Remediation you will see Playbook listed on many of these vulnerabilities.  This indicates that an Ansible Playbook has been created to correct this issue.  In the next exercise we will demonstrate how to do that.

![host-vulnerability-information](images/5-exploreinsights-host-vulnerabilities.png)

- Let's now look at all hosts associated with a Service.  In this example let's use Vulnerability service

    - On the left hand navigation pane click on Vulnerability -> CVEs.  This view will show the vulnerabilities for all systems registered to Red Hat Insights

![account-vulnerability-information](images/5-exploreinsights-account-vulnerabilities.png)

- Navigate around the Insights services to gain more understanding of Red Hat Insights.