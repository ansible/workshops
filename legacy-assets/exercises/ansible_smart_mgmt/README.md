# Ansible Workshop - Smart Management Automation

In this workshop you will learn how to get the most from your Red Hat Smart Management subscription and the Ansible Automation Platform.

## Table of Contents

# Table of Contents
- [Ansible Workshop - Smart Management Automation](#ansible-workshop---smart-management-automation)
  - [Table of Contents](#table-of-contents)
- [Table of Contents](#table-of-contents-1)
  - [Lab Diagram](#lab-diagram)
  - [Lab Setup](#lab-setup)
    - [Objective](#objective)
    - [Guide](#guide)
      - [Your Lab Environment](#your-lab-environment)
      - [**Step 1 - Setup Ansible Tower**](#step-1---setup-ansible-tower)
      - [**Step 2 - Create a Project**](#step-2---create-a-project)
      - [**Step 3 - Create Job Template**](#step-3---create-job-template)
  - [Config Management](#config-management)
  - [Security and Compliance](#security-and-compliance)


## Lab Diagram
## Lab Setup

### Objective
- Configure Activation Keys and Lifecycle environments
- Register Servers to Satellite Server

### Guide
#### Your Lab Environment

In this lab you'll work in a pre-configured lab environment. You will have access to the following hosts:

| Role                 | Inventory name |
| ---------------------| ---------------|
| Automation Platform  | ansible-1      |
| Satellite Server     | satellite      |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 3       | node3          |

#### **Step 1 - Setup Ansible Tower**

Login to the Automation Platform:

Open your browser and navigate to the Ansible Tower UI link provided on the attendance page. Login with the username `admin` and the password from your attendance page.

#### **Step 2 - Create a Project**

From the navigation section on the left side of the Automation Platform homepage, select **Project**. Click the green **Create** button in the top right corner. 

Create a project using the `https://github.com/willtome/automated-smart-management.git` as the source git repository. Enable the checkbox **Update on Launch**.

#### **Step 3 - Create Job Template**

## Config Management
## Security and Compliance
