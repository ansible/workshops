# Exercise 2.4 - Surveys

**Read this in other languages**: ![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md).

* [The Apache-configuration Role](#the-apache-configuration-role)
* [Create a Template with a Survey](#create-a-template-with-a-survey)
   * [Create Template](#create-template)
   * [Add the Survey](#add-the-survey)
* [Launch the Template](#launch-the-template)
* [What About Some Practice?](#what-about-some-practice)

You might have noticed the **ADD SURVEY** button in the **Template** configuration view. A survey is a way to create a simple form to ask for parameters that get used as variables when a **Template** is launched as a **Job**.

You have installed Apache on all hosts in the job you just run. Now we’re going to extend on this:

- Use a proper role which has a Jinja2 template to deploy an `index.html` file.

- Create a job **Template** with a survey to collect the values for the `index.html` template.

- Launch the job **Template**

Additionally, the role will also make sure that the Apache configuration is properly set up - in case it got mixed up during the other exercises.

> **Tip**
>
> The survey feature only provides a simple query for data - it does not support four-eye principles, queries based on dynamic data or nested menus.

## The Apache-configuration Role

The Playbook and the role with the Jinja template already exist in the Github repository **https://github.com/ansible/workshop-examples** in the directory `rhel/apache`**`.

 Head over to the Github UI and have a look at the content: the playbook `apache_role_install.yml` merely references the role. The role can be found in the `roles/role_apache` subdirectory.

 - Inside the role, note the two variables in the `templates/index.html.j2` template file marked by `{{…​}}`\.
 - Also, check out the tasks in `tasks/main.yml` that deploy the file from the template.

What is this Playbook doing? It creates a file (**dest**) on the managed hosts from the template (**src**).

The role also deploys a static configuration for Apache. This is to make sure that all changes done in the previous chapters are overwritten and your examples work properly.

Because the Playbook and role is located in the same Github repo as the `apache_install.yml` Playbook you don't have to configure a new project for this exercise.

## Create a Template with a Survey

Now you create a new Template that includes a survey.

### Create Template

- Go to **Templates**, click the ![plus](images/green_plus.png) button and choose **Job Template**

- **NAME:** Create index.html

- Configure the template to:

    - Use the `Ansible Workshop Examples` **Project**

    - Use the `apache_role_install.yml` **Playbook**

    - To run on `node1`

    - To run in privileged mode

Try for yourself, the solution is below.

> **Warning**
>
> **Solution Below\!**

- **NAME:** Create index.html

- **JOB TYPE:** Run

- **INVENTORY:** Webserver

- **Project:** Ansible Workshop Examples

- **PLAYBOOK:** `rhel/apache/apache_role_install.yml`

- **CREDENTIAL:** Workshop Credentials

- **OPTIONS:** Enable Privilege Escalation

- Click **SAVE**

> **Warning**
>
> **Do not run the template yet!**

### Add the Survey

- In the Template, click the **ADD SURVEY** button

- Under **ADD SURVEY PROMPT** fill in:

    - **PROMPT:** First Line

    - **ANSWER VARIABLE NAME:** `first_line`

    - **ANSWER TYPE:** Text

- Click **+ADD**

- In the same way add a second **Survey Prompt**

    - **PROMPT:** Second Line

    - **ANSWER VARIABLE NAME:** `second_line`

    - **ANSWER TYPE:** Text

- Click **+ADD**

- Click **SAVE** for the Survey

- Click **SAVE** for the Template

## Launch the Template

Now launch **Create index.html** job template.

Before the actual launch the survey will ask for **First Line** and **Second Line**. Fill in some text and click **Next**. The next window shows the values, if all is good run the Job by clicking **Launch**.

> **Tip**
>
> Note how the two survey lines are shown to the left of the Job view as **Extra Variables**.

After the job has completed, check the Apache homepage. In the SSH console on the control host, execute `curl` against the IP address of your `node1`:

```bash
$ curl http://22.33.44.55
<body>
<h1>Apache is running fine</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```
Note how the two variables where used by the playbook to create the content of the `index.html` file.

## What About Some Practice?

Here is a list of tasks:

> **Warning**
>
> **Please make sure to finish these steps as the next chapter depends on it\!**

- Take the inventory `Webserver` and add the other nodes, `node2` and `node3` as well.

- Run the **Create index.html** Template again.

- Verify the results on the other two nodes by using `curl` against their IP addresses.

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
