# Exercise 4.2: Creating a Workflow

## Table of Contents
- [Exercise 4.2: Creating a Workflow](#exercise-42-creating-a-workflow)
  - [Table of Contents](#table-of-contents)
- [Objective](#objective)
- [Guide](#guide)
  - [Step 0: Prepare Job Templates](#step-0-prepare-job-templates)
  - [Step 1: Create a Workflow Template](#step-1-create-a-workflow-template)
  - [Step 2: The Workflow Visualizer](#step-2-the-workflow-visualizer)
  - [Step 3: Add *Create node* Job Template](#step-3-add-create-node-job-template)
  - [Step 4: Add *Create pool* Job Template](#step-4-add-create-pool-job-template)
  - [Step 5: Add *Create virtual server* Job Template](#step-5-add-create-virtual-server-job-template)
  - [Step 5: *Rollback node deploy* Template](#step-5-rollback-node-deploy-template)
  - [Step 6: *Rollback pool deploy* Template](#step-6-rollback-pool-deploy-template)
  - [Step 7: *Rollback virtual server* Template](#step-7-rollback-virtual-server-template)
  - [Step 8: Run the Workflow](#step-8-run-the-workflow)
- [Takeaways](#takeaways)
- [Complete](#complete)

# Objective

Demonstrate the use of [Ansible Tower workflow](https://docs.ansible.com/ansible-tower/latest/html/userguide/workflows.html) for F5 BIG-IP.  Workflows allow you to configure a sequence of disparate job templates (or workflow templates) that may or may not share inventory, playbooks, or permissions.

For this exercise we will ...

# Guide

## Step 0: Prepare Job Templates

Create the following templates by following `Lab 4.2`:
* Create node
* Create pool
* Create virtual server
* Rollback node deploy
* Rollback pool deploy
* Rollback virtual server deploy

## Step 1: Create a Workflow Template

1. Click on the **Templates** link on the left menu.  

2. Click on the green ![templates link](images/add.png) button. Select the **Workflow Template**.  

3. Fill out the the form as follows:

| Parameter | Value |
|---|---|
| Name  | Workshop Workflow  |
|  Organization |  Default |
|  Inventory |  Workshop Inventory |

4. Click on the **`Save`** button

![workflow creation](images/workflow.gif)

## Step 2: The Workflow Visualizer

1. When you click the **SAVE** the **WORKFLOW VISUALIZER** should automatically open.  If not, click on the blue **WORKFLOW VISUALIZER** button.  

2. By default only a green **START** button will appear.  Click on the **START** button.  

3. The **ADD A TEMPLATE** window will appear on the right.  Select the *creat_node* Job Template that was created in previous step(whatever you named it!).

   ![add a template](images/add-a-template.png)

   The `create_node` job template is now a node.  Job or workflow templates are linked together using a graph-like structure called nodes. These nodes can be jobs, project syncs, or inventory syncs. A template can be part of different workflows or used multiple times in the same workflow. A copy of the graph structure is saved to a workflow job when you launch the workflow.

## Step 3: Add *Create node* Job Template

1.  Select the **`Create node`** Job Template.  Use the drop down box to select run.  Click the green **SELECT** button.

    ![remove pool](images/create_node.png)

## Step 4: Add *Create pool* Job Template

1.  Hover over the **`Create node`** node and click the green **+** symbol.  The **ADD A TEMPLATE** will appear again.

2. Select the **`Create pool`** job template.  For the **Run** parameter select **On Success** from the drop down menu.  

   ![upgrade server](images/create_pool.png)

## Step 5: Add *Create virtual server* Job Template

1.  Hover over the **`Create pool`**  node and click the green **+** symbol.  The **ADD A TEMPLATE** will appear again.

2. Select the **`Create virtual server`** job template.  For the **Run** parameter select **On Success** from the drop down menu.  

   ![add pool](images/create_virtualserver.png)

## Step 5: *Rollback node deploy* Template

1.  Hover over the **Create node** node and click the green **+** symbol.  The **ADD A TEMPLATE** will appear again.

2. Select the **Rollback node deploy** job template.  For the **Run** parameter select **On Failure** from the drop down menu.  
3. Click the green **SELECT** button.  

   ![configure restore node](images/rollback_node.png)

## Step 6: *Rollback pool deploy* Template

1.  Hover over the **Create pool** node and click the green **+** symbol.  The **ADD A TEMPLATE** will appear again.

2. Select the **Rollback pool deploy** job template.  For the **Run** parameter select **On Failure** from the drop down menu.  
3. Click the green **SELECT** button.  

   ![configure restore node](images/rollback_pool.png)

## Step 7: *Rollback virtual server* Template

1.  Hover over the **Create virtual server** node and click the green **+** symbol.  The **ADD A TEMPLATE** will appear again.

2. Select the **Rollback virtual server deploy** job template.  For the **Run** parameter select **On Failure** from the drop down menu.  
3. Click the green **SELECT** button.  

   ![configure restore node](images/rollback_virtualserver.png)

## Step 8: Run the Workflow

1. Return to the **Templates** window

2. Click the rocket ship to launch the **Workshop Workflow** workflow template.

   ![workflow job launched](images/running-workflow.png)

    At any time during the workflow job you can select an individual job template by clicking on the node to see the status.

# Takeaways

You have
 - created a workflow template that create node, a pool, and virtual server
 - made the workflow robust, if either job template fails it will rollback the deployment
 - launched the workflow template and explored the **VISUALIZER**

---

# Complete

You have completed lab exercise 9

[Click here to return to the Ansible Network Automation Workshop](../README.md)
