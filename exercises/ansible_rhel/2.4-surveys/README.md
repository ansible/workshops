# Exercise - Surveys

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Table Contents

* [Objective](#objective)
* [Guide](#guide)
* [The Apache-configuration Role](#the-apache-configuration-role)
* [Create a Template with a Survey](#create-a-template-with-a-survey)
  * [Create Template](#create-template)
  * [Add the Survey](#add-the-survey)
* [Launch the Template](#launch-the-template)
* [What About Some Practice?](#what-about-some-practice)

## Objective

Demonstrate the use of Ansible Automation controller [survey feature](https://docs.ansible.com/automation-controller/latest/html/userguide/job_templates.html#surveys). Surveys set extra variables for the playbook similar to ‘Prompt for Extra Variables’ does, but in a user-friendly question and answer way. Surveys also allow for validation of user input.

## Guide

You have installed Apache on all hosts in the job you just ran. Now we’re going to extend on this:

* Use a proper role that has a Jinja2 template to deploy an `index.html` file.

* Create a job **Template** with a survey to collect the values for the `index.html` template.

* Launch the job **Template**

Additionally, the role will make sure that the Apache configuration is properly set up for this exercise.

> **Tip**
>
> The survey feature only provides a simple query for data - it does not support four-eye principles, queries based on dynamic data or nested menus.

### The Apache-configuration Role

The playbook and the role with the Jinja2 template already exist in the Github repository [https://github.com/ansible/workshop-examples](https://github.com/ansible/workshop-examples) in the directory `rhel/apache`.

 Head over to the Github UI and have a look at the content: the playbook `apache_role_install.yml` merely references the role. The role can be found in the `roles/role_apache` subdirectory.

* Inside the role, note the two variables in the `templates/index.html.j2` template file marked by `{{…​}}`\.
* Notice the tasks in `tasks/main.yml` that deploy the file from the template.

What is this playbook doing? It creates a file (**dest**) on the managed hosts from the template (**src**).

The role deploys a static configuration for Apache. This is to make sure that all changes done in the previous chapters are overwritten and your examples work properly.

Because the playbook and role is located in the same Github repo as the `apache_install.yml` playbook you don't have to configure a new project for this exercise.

### Create a Template with a Survey

Now you create a new Template that includes a survey.

#### Create Template

* Go to **Resources → Templates**, click the **Add** button and choose **Add job template**

* Fill out the following information:

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Name</td>
    <td>Create index.html</td>
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
    <td>Workshop Project</td>
  </tr>
  <tr>
    <td>Eecution Environment</td>
    <td>Default execution environment</td>
  </tr>
  <tr>
    <td>Playbook</td>
    <td><code>rhel/apache/apache_role_install.yml</code></td>
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
    <td>Privilege Escalation</td>
  </tr>
</table>

* Click **Save**

> **Warning**
>
> **Do not run the template yet!**

#### Add the Survey

* In the Template, click the **Survey** tab and click the **Add** button.

* Fill out the following information:

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Question</td>
    <td>First Line</td>
  </tr>
  <tr>
    <td>Answer Variable Name</td>
    <td>first_line</td>
  </tr>
  <tr>
    <td>Answer Type</td>
    <td>Text</td>
  </tr>
</table>

* Click **Save**
* Click the **Add** button

In the same fashion add a second **Survey Question**

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Question</td>
    <td>Second Line</td>
  </tr>
  <tr>
    <td>Answer Variable Name</td>
    <td>second_line</td>
  </tr>
  <tr>
    <td>Answer Type</td>
    <td>Text</td>
  </tr>
</table>

* Click **Save**

* Click the toggle to turn the Survey questions to **Survey Enabled**

### Launch the Template

Now launch **Create index.html** job template by selecting the **Details** tab and clicking the **Launch** button.

Before the actual launch the survey will ask for **First Line** and **Second Line**. Fill in some text and click **Next**. The **Preview** window shows the values, if all is good run the Job by clicking **Launch**.

After the job has completed, check the Apache homepage. In the SSH console on the control host, execute `curl` against `node1`:

```bash
$ curl http://node1
<body>
<h1>Apache is running fine</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```

Note how the two variables where used by the playbook to create the content of the `index.html` file.

---
**Navigation**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Previous Exercise](../4-variables) - [Next Exercise](../../ansible_rhel_90/6-system-roles/)
{% else %}
[Previous Exercise](../2.3-projects) - [Next Exercise](../2.5-rbac)
{% endif %}
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
