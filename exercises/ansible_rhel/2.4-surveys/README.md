# Exercise 2.4 - Surveys

You might have noticed the **ADD SURVEY** button in the **Template** configuration view. A survey is a way to create a simple form to ask for parameters that get used as variables when a **Template** is launched as a **Job**.

You have installed Apache on all hosts in the job you just run. Now we’re going to extend on this:

  - Use a Playbook and a role which has a Jinja2 template to deploy an **index.html** file.

  - Create a job **Template** with a survey to collect the values for the **index.html** template.

  - Launch the job **Template**

## Create the Project

The Playbook and the role with the Jinja template already exist in the repo **SurveyTODO** in Github. Head over to the Github UI and have a look at the content.

The playbook TODO merely references the role. Inside the role, note the two variables in the **templates/index.j2** template file marked by `{{…​}}`\. Also, check out the **Plays** in **tasks/main.yml** that deploy the file from the template. What is this Playbook doing? It creates a file (**dest**) on the managed hosts from the template (**src**).

> **Tip**
> 
> The role also deploys a static configuration for Apache. This is to make sure that all changes done in the previous chapters are overwritten and your examples work properly. TODO:Add httpd.conf and handlers to role:TODO

## Create a Template with a Survey

Now you create a new Template that includes a survey.

### Create Template

  - Go to **Templates**, click the ![plus](images/green_plus.png) button and choose **Job Template**

  - **NAME:** Create index.html

  - Configure the template to:
    
      - Use the **Project** and **Playbook**
    
      - To run on `node1`
    
      - To run in privileged mode

Try for yourself, the solution is below.

> **Warning**
> 
> **Solution Below\!**

  - **NAME:** Create index.html

  - **JOB TYPE:** Run

  - **INVENTORY:** Webserver

  - **Project:** TODO

  - **PLAYBOOK:** TODO

  - **CREDENTIAL:** Workshop Credentials

  - **OPTIONS:** Enable Privilege Escalation

  - Click **SAVE**

### Add the Survey

  - In the Template, click the **ADD SURVEY** button

  - Under **ADD SURVEY PROMPT** fill in:
    
      - **PROMPT:** First Line
    
      - **ANSWER VARIABLE NAME:** first\_line
    
      - **ANSWER TYPE:** Text

  - Click **+ADD**

  - In the same way add a second **Survey Prompt**
    
      - **PROMPT:** Second Line
    
      - **ANSWER VARIABLE NAME:** second\_line
    
      - **ANSWER TYPE:** Text

  - Click **+ADD**

  - Click **SAVE** for the Survey

  - Click **SAVE** for the Template

## Launch the Template

Now go back to the **Templates** view and launch **Create index.html**.

  - Before the actual launch the survey will ask for **First Line** and **Second Line**. Fill in some text and click **Next**. The next window shows the values, if all is good run the Job by clicking **Launch**.

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

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
