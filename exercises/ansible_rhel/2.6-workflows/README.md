# Workshop Exercise - Workflows

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Table Contents

- [Workshop Exercise - Workflows](#workshop-exercise---workflows)
  - [Table Contents](#table-contents)
  - [Objective](#objective)
  - [Guide](#guide)
    - [Lab scenario](#lab-scenario)
      - [Web operations team](#web-operations-team)
      - [Web developers team](#web-developers-team)
    - [Set up projects](#set-up-projects)
    - [Set up job templates](#set-up-job-templates)
    - [Set up the workflow](#set-up-the-workflow)
    - [Launch workflow](#launch-workflow)

## Objective

The basic idea of a workflow is to link multiple Job Templates together. They may or may not share inventory, playbooks or even permissions. The links can be conditional:

* if job template A succeeds, job template B is automatically executed afterwards
* but in case of failure, job template C will be run.

And the workflows are not even limited to Job Templates, but can also include project or inventory updates.

This enables new applications for Ansible automation controller: different Job Templates can build upon each other. E.g. the networking team creates playbooks with their own content, in their own Git repository and even targeting their own inventory, while the operations team also has their own repos, playbooks and inventory.

In this lab you’ll learn how to setup a workflow.

## Guide

### Lab scenario

You have two departments in your organization:

* The web operations team that is developing playbooks in their own Git branch named `webops`
* The web developers team that is developing playbooks in their own Git branch named `webdev`.

When there is a new Node.js server to deploy, two things need to happen:

#### Web operations team

* `httpd`, `firewalld`, and `node.js` need to be installed, `SELinux` settings configured, the firewall needs to be opened, and `httpd` and `node.js` should get started.

#### Web developers team

* The most recent version of the web application needs to be deployed and `node.js` needs to be restarted.

In other words, the Web operations team prepares a server for application deployment, and the Web developers team deploys the application on the server.

---

To make things somewhat easier for you, everything needed already exists in a Github repository: playbooks, JSP-files etc. You just need to glue it together.

> **Note**
>
> In this example we use two different branches of the same repository for the content of the separate teams. In reality, the structure of your Source Control repositories depends on a lot of factors and could be different.

### Set up projects

First you have to set up the Git repo as a Project like you normally would.

> **Warning**
>
> If you are still logged in as user **wweb**, log out of and log in as user **admin**.

Within **Resources** -> **Projects**, click the **Add** button to create a project for the web operations team. Fill out the form as follows:

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Name</td>
    <td>Webops Git Repo</td>
  </tr>
  <tr>
    <td>Organization</td>
    <td>Default</td>
  </tr>
  <tr>
    <td>Default Execution Environment</td>
    <td>Default execution environment</td>
  </tr>
  <tr>
    <td>Source Control Credential Type</td>
    <td>Git</td>
  </tr>
  <tr>
    <td>Source Control URL</td>
    <td><code>https://github.com/ansible/workshop-examples.git</code></td>
  </tr>
  <tr>
    <td>Source Control Branch/Tag/Commit</td>
    <td><code>webops</code></td>
  </tr>
  <tr>
    <td>Options</td>
    <td><ul><li>✓ Clean</li><li>✓ Delete</li><li>✓ Update Revision on Launch</li></ul></td>
  </tr>
</table>

Click **Save**

---
Within **Resources** -> **Projects**, click the **Add** button to create a project for the web developers team. Fill out the form as follows:

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Name</td>
    <td>Webdev Git Repo</td>
  </tr>
  <tr>
    <td>Organization</td>
    <td>Default</td>
  </tr>
  <tr>
    <td>Default Execution Environment</td>
    <td>Default execution environment</td>
  </tr>
  <tr>
    <td>Source Control Credential Type</td>
    <td>Git</td>
  </tr>
  <tr>
    <td>Source Control URL</td>
    <td><code>https://github.com/ansible/workshop-examples.git</code></td>
  </tr>
  <tr>
    <td>Source Control Branch/Tag/Commit</td>
    <td><code>webdev</code></td>
  </tr>
  <tr>
    <td>Options</td>
    <td><ul><li>✓ Clean</li><li>✓ Delete</li><li>✓ Update Revision on Launch</li></ul></td>
  </tr>
</table>

Click **Save**

### Set up job templates

Now you have to create two Job Templates like you would for "normal" Jobs.

Within **Resources** -> **Templates**, click the **Add** button and choose **Add job template**:

  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Name</td>
      <td>Web App Deploy</td>
    </tr>
    <tr>
      <td>Job Type</td>
      <td>Run</td>
    </tr>
    <tr>
      <td>Inventory</td>
      <td>Workshop Inventory</td>
    </tr>
    <tr>
      <td>Project</td>
      <td>Webops Git Repo</td>
    </tr>
    <tr>
      <td>Execution Environment</td>
      <td>Default execution environment</td>
    </tr>
    <tr>
      <td>Playbook</td>
      <td><code>rhel/webops/web_infrastructure.yml</code></td>
    </tr>
    <tr>
      <td>Credentials</td>
      <td>Workshop Credential</td>
    </tr>
    <tr>
      <td>Limit</td>
      <td>web</td>
    </tr>
    <tr>
      <td>Options</td>
      <td>✓ Privilege Escalation</td>
    </tr>
  </table>

Click **Save**

---

Within **Resources** -> **Templates**, click the **Add** button and choose **Add job template**:

  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Name</td>
      <td>Node.js Deploy</td>
    </tr>
    <tr>
      <td>Job Type</td>
      <td>Run</td>
    </tr>
    <tr>
      <td>Inventory</td>
      <td>Workshop Inventory</td>
    </tr>
    <tr>
      <td>Project</td>
      <td>Webdev Git Repo</td>
    </tr>
    <tr>
      <td>Execution Environment</td>
      <td>Default execution environment</td>
    </tr>
    <tr>
      <td>Playbook</td>
      <td><code>rhel/webdev/install_node_app.yml</code></td>
    </tr>
    <tr>
      <td>Credentials</td>
      <td>Workshop Credential</td>
    </tr>
    <tr>
      <td>Limit</td>
      <td>web</td>
    </tr>
    <tr>
      <td>Options</td>
      <td>✓ Privilege Escalation</td>
    </tr>
  </table>

Click **Save**

> **Tip**
>
> If you want to know what the Ansible Playbooks look like, check out the Github URL and switch to the appropriate branches.

### Set up the workflow

Set up the workflow. Workflows are configured in the **Templates** view, you might have noticed you can choose between **Add job template** and **Add workflow template** when adding a template.

Within **Resources** -> **Templates**, click the **Add** button and choose **Add workflow template**:

  <table>
    <tr>
      <td><b>Name</b></td>
      <td>Deploy Webapp Server</td>
    </tr>
    <tr>
      <td><b>Organization</b></td>
      <td>Default</td>
    </tr>
  </table>

Click **Save**

After saving the template the **Workflow Visualizer** opens to allow you to build a workflow. You can later open the **Workflow Visualizer** again by using the button on the template details page and selecting **Visualizer** from the menu.

* Click on the **Start** button, a **Add Node|Web App Deploy** window opens. Assign an action to the node, via node type by selecting **Job Template**.

  ![start](images/start.png)

  ![Add Nodejs](images/add_node_nodejs.png)

* In this lab we’ll link our two jobs together, so select the **Node.js Deploy** job template and click **Save**.

* The node gets annotated with the name of the job template. Hover the mouse pointer over the node, you’ll see options to add a node (+), view node details (i), edit the node (pencil), link to an available node (chain), and delete the node (trash bin).

  ![workflow node](images/workflow_node.png)

* Hover over the node and click the (+) sign to add a new node.
* For the **Run Type** select **On Success** (default).
* For **Node Type** select **Job Template** and choose the **Web App Deploy** job template. 
Click **Save**.

![Add Node](images/add_node.png)

> **Tip**
>
> The type allows for more complex workflows. You could lay out different execution paths for successful and for failed playbook runs.

* Click **Save** in the top right corner of the **Visualizier** view.

> **Tip**
>
> The **Visualizer** has options for setting up more advanced workflows, please refer to the documentation.

### Launch workflow

From within the **Deploy Webapp Server** Details page, **Launch** the workflow.

  ![launch](images/launch.png)

Note how the workflow run is shown in the Jobs > Deploy Webapp Server Output. In contrast to a normal job template job execution, there is no playbook output when the job completes but the time to complete the job is displayed. If you want to look at the actual playbook run, hover over the node you wish to see the details on and click it. Within the Details view of the job, select the **Output** menu to see the playbook output. If you want to get back the **Output** view of the **Deploy WebappServer** workflow, under Views -> Jobs -> **XX - Deploy Webapp Server** will take you back to the Output overview. 

NOTE: Where `XX` is the number of the job run. 

![jobs view of workflow](images/job_workflow.png)

After the job was finished, check if everything worked fine: log into `node1`, `node2` or `node3` from your control host and run:

```bash
#> curl http://nodeX/nodejs
```

NOTE: `X` can be replaced with the appropriate number of the node you are checking.

You can also execute curl on the control host, pointing it towards the nodes and query the `nodejs` path, it should also show the simple nodejs application.

---
**Navigation**
<br>
[Previous Exercise](../2.5-rbac) - [Next Exercise](../2.7-wrap)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
