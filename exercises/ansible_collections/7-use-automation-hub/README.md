## Table of Contents
- [Objective](#objective)
    - [Red Hat Automation Hub](#red-hat-automation-hub)
    - [Certified Content](#certified-content)
    - [Supported Automation](#supported-automation)
    - [Ansible Galaxy](#ansible-galaxy)
    - [How to use Automation Hub](#how-to-use-automation-hub)
    - [Accessing collections](#accessing-collections)
    - [Authenticate Tower to Automation Hub](#authenticate-tower-to-automation-hub)
- [Takeaways](#takeaways)


# Objective

# Red Hat Automation Hub
It is a service that is provided as part of the Red Hat SaaS Offering. It consists of the location where to discover and download only supported and certified Ansible Content Collections by Red Hat Partners. These content collections contain ways to consume automation, how-to-guides to implement them in your infrastructure. The support Automation Hub is included with Red Hat Automation Platform subscription.

## Certified Content
In the portal of Automation Hub, users have direct access to trusted content collections from Red Hat Certified Partners.

## Supported Automation
  Automation Hub provides a one-stop-shop for Ansible content that is backed by support from Red Hat and its partners to deliver additional reassurance for customers.

# Ansible Galaxy
Automation Hub provides a one-stop-shop for Ansible content that is backed by support from Red Hat and its partners to deliver additional reassurance for customers.

# How to use Automation Hub

## Accessing collections
Ansible collections can be used and downloaded from multiple locations. They can either be downloaded using a requirement file, statically included in the git repository or eventually installed separately in the virtual environment.
In the scope of this exercise, the focus is on how access content from Automation Hub. This requires an authentication token and authentication URL. To do, some configuration steps need to be done in Ansible Tower.

## Authenticate Tower to Automation Hub
 1. As user admin, navigate to the Settings > Jobs
 2. Set PRIMARY GALAXY SERVER URL to: https://cloud.redhat.com/api/automation-hub/
 3. Set PRIMARY GALAXY AUTHENTICATION URL to: https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
 4. Set PRIMARY GALAXY SERVER TOKEN to: <YOUR_OWN_TOKEN> 
                                  OR  
    Set  PRIMARY GALAXY SERVER USERNAME and PRIMARY GALAXY SERVER PASSWORD
 
# Takeaways
 
