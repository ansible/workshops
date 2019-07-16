# Exercise 2.7 - Wrap up

# Final Challenge or Putting it all Together

This is the final challenge where we try to put most of what you have learned together.

## Let’s set the stage

Your operations team and your application development team like what they see in Tower. To really use it in their environment they put together these requirements:

  - All webservers (`node1`, `node2` and `node3`) should go in one group

  - As the webservers can be used for development purposes or in production, there has to be a way to flag them accordingly as "stage dev" or "stage prod".
    
      - Currently `host1` is used as a development system and `host2` is in production.

  - Of course the content of the world famous application "index.html" will be different between dev and prod stages.
    
      - There should be a title on the page stating the environment
    
      - There should be a content field

  - The content writer `wweb` should have access to a survey to change the content for dev and prod servers.

## The Git Repository

All code is already in place - this is a Tower lab after all. Check out the **Ansible Workshop Examples** git repository at **https://github.com/ansible/workshop-examples**. There you will find the playbook **webcontent.yml**, which calls the role **role_webcontent**.

Compared to the previous Apache installation role there is a major difference: there are now two versions of an `index.html` template, and a task deploying the template file which has a variable as part of the source file name:
  
`dev_index.html.j2`

```html
<body>
<h1>This is a development webserver, have fun!</h1>
{{ dev_content }}
</body>
```

`prod_index.html.j2`

```html
<body>
<h1>This is a production webserver, take care!</h1>
{{ prod_content }}
</body>
```

`main.yml`

```yaml
[...]    
- name: Deploy index.html from template
  template:
    src: "{{ stage }}_index.html.j2"
    dest: /var/www/html/index.html
  notify: apache-restart
```

## Prepare Inventory

There is of course more then one way to accomplish this, but here is what you should do:

- Make sure all hosts are in the inventory group `Webserver` (add `node2` and `node3`)

- Define a variable `stage` with the value `dev` for the `Webserver` inventory:
  
    - Add `stage: dev` to the inventory `Webserver` by putting it into the **VARIABLES** field beneath the three start-yaml dashes.

- In the same way add a variable `stage: prod` but this time only for `node2` (by clicking the hostname) so that it overrides the inventory variable.

> **Tip**
> 
> Make sure to keep the three dashes that mark the YAML start\!

## Create the Template

- Create a new **Job Template** named `Create Web Content` that
  
    - targets the `Webserver` inventory
  
    - uses the Playbook `rhel/apache/webcontent.yml` from the new **Ansible Workshop Examples** Project
  
    - Defines two variables: `dev_content: default dev content` and `prod_content: default prod content` in the **EXTRA VARIABLES FIELD**
  
    - Uses `Workshop Credentials` and runs with privilege escalation

- Save and run the template

## Check the results

Make sure to use the IPs of your individual nodes in the following example:

```bash
$ curl http://22.33.44.55
<body>
<h1>This is a development webserver, have fun!</h1>
default dev content
</body>

$ curl http://33.44.55.66
<body>
<h1>This is a production webserver, take care!</h1>
default prod content
</body>
```

## Add Survey

- Add a survey to the Template to allow changing the variables `dev_content` and `prod_content`

- Add permissions to the Team `Web Content` so the Template **Create Web Content** can be executed by `wweb`.

- Run the survey as user `wweb`

- Check the results:

```bash
$ curl http://22.33.44.55
<body>
<h1>This is a development webserver, have fun!</h1>
This is somehow in development
</body>

$ curl http://33.44.55.66
<body>
<h1>This is a production webserver, take care!</h1>
This is my nice Prod Content
</body>
```

## Solution

> **Warning**
> 
> **Solution Not Below**

You have done all the required configuration steps in the lab already. If unsure, just refer back to the respective chapters.

# The End

Congratulations, you finished your labs\! We hope you enjoyed your first encounter with Ansible Tower as much as we enjoyed creating the labs.
----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-2---ansible-tower-exercises)
