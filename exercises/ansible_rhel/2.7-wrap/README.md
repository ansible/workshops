# Workshop Exercise - Wrap up

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
  * [Let’s set the stage](#lets-set-the-stage)
  * [The Git Repository](#the-git-repository)
  * [Prepare Inventory](#prepare-inventory)
  * [Create the Template](#create-the-template)
  * [Check the results](#check-the-results)
  * [Add Survey](#add-survey)
  * [Solution](#solution)
* [The End](#the-end)

## Objective

This is the final challenge where we try to put most of what you have learned together.

## Guide

### Let’s set the stage

Your operations team and your application development team likes what they see in Ansible automation controller. To really use it in their environment they put together these requirements:

* All webservers (`node1`, `node2` and `node3`) should go in one group

* As the webservers can be used for development purposes or in production, there has to be a way to flag them accordingly as "stage dev" or "stage prod".

  * Currently `node1` and `node3` are used as a development system and `node2` is in production.

* Of course the content of the world famous application "index.html" will be different between dev and prod stages.

  * There should be a title on the page stating the environment
  * There should be a content field

* The content writer `wweb` should have access to a survey to change the content for dev and prod servers.

### The Git Repository

All code is already in place - this is a automation controller lab after all. Check out the **Workshop Project** git repository at [https://github.com/ansible/workshop-examples](https://github.com/ansible/workshop-examples). There you will find the playbook `webcontent.yml`, which calls the role `role_webcontent`.

Compared to the previous Apache installation role there is a major difference: there are now two versions of an `index.html` template, and a task deploying the template file which has a variable as part of the source file name:

`dev_index.html.j2`

<!-- {% raw %} -->

```html
<body>
<h1>This is a development webserver, have fun!</h1>
{{ dev_content }}
</body>
```

<!-- {% endraw %} -->

`prod_index.html.j2`

<!-- {% raw %} -->

```html
<body>
<h1>This is a production webserver, take care!</h1>
{{ prod_content }}
</body>
```

<!-- {% endraw %} -->

`main.yml`

<!-- {% raw %} -->

```yaml
[...]
- name: Deploy index.html from template
  template:
    src: "{{ stage }}_index.html.j2"
    dest: /var/www/html/index.html
  notify: apache-restart
```

<!-- {% endraw %} -->

### Prepare Inventory

There is of course more then one way to accomplish this, but for the purposes of this lab, we will use Ansible automation controller.

Within **Resources** -> **Inventories** and select 'Workshop Inventory'.

Within the **Groups** tab, click the **Add** button and create a new inventory group labeled `Webserver` and click **Save**.

Within the **Details** tab of the `Webserver` group, click on **Edit**. Within the **Variables** textbox define a variable labeled `stage` with the value `dev` and click **Save**.

```yaml
---
stage: dev
```

Within the **Details** tab of the `Webserver` inventory, click the **Hosts** tab, click the **Add** button and **Add existing host**. Select `node1`, `node2`, `node3` as the hosts to be part of the `Webserver` inventory.


Within **Resources** -> **Inventories**, select the `Workshop` Inventory. Click on the `Hosts` tab and click on `node2`.  Click on `Edit` and add the `stage: prod` variable in the **Variables** window. This overrides the inventory variable due to order of operations of how the variables are accessed during playbook execution.


Within the **Variables** textbox define a variable labeled `stage` with the value of `prod` and click **Save**.

```yaml
---
ansible_host: <IP_of_node2>
stage: prod
```
> **Tip**
>
> Make sure to keep the three dashes that mark the YAML start and the `ansible_host` line in place\!

### Create the Template

Within **Resources** -> **Templates**, select the **Add** button and **Add job template** as follows:

  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Name</td>
      <td>Create Web Content</td>
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
      <td>Execution Environment</td>
      <td>Default execution environment</td>
    </tr>
    <tr>
      <td>Playbook</td>
      <td>rhel/apache/webcontent.yml</td>
    </tr>
    <tr>
      <td>Credentials</td>
      <td>Workshop Credential</td>
    </tr>
    <tr>
      <td>Variables</td>
      <td>dev_content: "default dev content", prod_content: "default prod content"</td>
    </tr>
    <tr>
      <td>Options</td>
      <td>Privilege Escalation</td>
    </tr>
  </table>

Click **Save**.

Run the template by clicking the **Launch** button.


### Check the Results

This time we use the power of Ansible to check the results: execute uri to get the web content from each node, orchestrated by an Ansible playbook labeled `check_url.yml`

> **Tip**
>
> We are using the `ansible_host` variable in the URL to access every node in the inventory group.

<!-- {% raw %} -->

```yaml
---
- name: Check URL results
  hosts: web

  tasks:
    - name: Check that you can connect (GET) to a page and it returns a status 200
      uri:
        url: "http://{{ ansible_host }}"
        return_content: yes
      register: content

    - debug:
       var: content.content
```

```bash
[student<X>@ansible-1 ~]$ ansible-navigator run check_url.yml -m stdout
```

Snippet of output:

```bash
TASK [debug] *******************************************************************
ok: [node1] => {
    "content.content": "<body>\n<h1>This is a development webserver, have fun!</h1>\ndev wweb</body>\n"
}
ok: [node2] => {
    "content.content": "<body>\n<h1>This is a production webserver, take care!</h1>\nprod wweb</body>\n"
}
ok: [node3] => {
    "content.content": "<body>\n<h1>This is a development webserver, have fun!</h1>\ndev wweb</body>\n"
}
```

<!-- {% endraw %} -->

### Add Survey

* Add a Survey to the template to allow changing the variables `dev_content` and `prod_content`.
** In the Template, click the **Survey** tab and click the **Add** button.
** Fill out the following information:

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Question</td>
    <td>What should the value of dev_content be?</td>
  </tr>
  <tr>
    <td>Answer Variable Name</td>
    <td>dev_content</td>
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
    <td>What should the value of prod_content be?</td>
  </tr>
  <tr>
    <td>Answer Variable Name</td>
    <td>prod_content</td>
  </tr>
  <tr>
    <td>Answer Type</td>
    <td>Text</td>
  </tr>
</table>

* Click **Save**
* Click the toggle to turn the Survey questions to **On**

* Click **Preview** for the Survey

* Add permissions to the team `Web Content` so the template **Create Web Content** can be executed by `wweb`.
* Within the **Resources** -> **Templates**, click **Create Web Content** and add **Access** to the user `wweb` the ability to execute the template.
  * **Select a Resource Type** -> click **Users**, click **Next**.
  * **Select Items from List** -> select the checkbox `wweb`, click **Next**.
  * **Select Roles to Apply** -> select the checkbox **Execute** and click **Save**.
* Run the survey as user `wweb`
  * Logout of the user `admin` of your Ansible automation controller.
  * Login as `wweb` and go to **Resources** -> **Templates** and run the **Create Web Content** template.

Check the results again from your automation controller host. We will use the dedicated `uri` module within an Ansible playbook. As arguments it needs the actual URL and a flag to output the body in the results.

<!-- {% raw %} -->


```bash
[student<X>@ansible-1 ~]$ ansible-navigator run check_url.yml -m stdout
```

<!-- {% endraw %} -->

### Solution

> **Warning**
>
> **Solution Not Below**

You have done all the required configuration steps in the lab already. If unsure, just refer back to the respective chapters.

## The End

Congratulations, you finished your labs\! We hope you enjoyed your first encounter with Ansible automation controller as much as we enjoyed creating the labs.

----
**Navigation**
<br>
[Previous Exercise](../2.6-workflows)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-automation-controller-exercises)
