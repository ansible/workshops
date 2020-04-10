# Ad Hoc Commands, Templates and Variables

**Read this in other languages**: ![uk](../../../../images/uk.png) [English](README.md),  ![japan](../../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md).

* [Step 1 - Bonus Lab: Ad Hoc Commands](#step-1---bonus-lab-ad-hoc-commands)
* [Step 2 - Bonus Lab: Templates and Variables](#step-2---bonus-lab-templates-and-variables)
   * [Define the variables:](#define-the-variables)
   * [Prepare the template:](#prepare-the-template)
   * [Create the Playbook](#create-the-playbook)
   * [Run and test](#run-and-test)

You have finished the lab already. But it doesn’t have to end here. We prepared some slightly more advanced bonus labs for you to follow through if you like. So if you are done with the labs and still have some time, here are some more labs for you:

## Step 1 - Bonus Lab: Ad Hoc Commands

Create a new user "testuser" on `node1` and `node3` with a comment using an ad hoc command, make sure that it is not created on `node2`!

  - Find the parameters for the appropriate module using `ansible-doc user` (leave with `q`)

  - Use an Ansible ad hoc command to create the user with the comment "Test D User"

  - Use the "command" module with the proper invocation to find the userid

  - Delete the user and its directories, then check that the user has been deleted

> **Tip**
>
> Remember privilege escalation…​

> **Warning**
>
> **Solution below\!**

Your commands could look like these:

```bash
[student<X>@ansible ansible-files]$ ansible-doc -l | grep -i user
[student<X>@ansible ansible-files]$ ansible-doc user
[student<X>@ansible ansible-files]$ ansible node1,node3 -m user -a "name=testuser comment='Test D User'" -b
[student<X>@ansible ansible-files]$ ansible node1,node3 -m command -a " id testuser" -b
[student<X>@ansible ansible-files]$ ansible node2 -m command -a " id testuser" -b
[student<X>@ansible ansible-files]$ ansible node1,node3 -m user -a "name=testuser state=absent remove=yes" -b
[student<X>@ansible ansible-files]$ ansible web -m command -a " id testuser" -b
```

## Step 2 - Bonus Lab: Templates and Variables

You have learned the basics about Ansible templates, variables and handlers. Let’s combine all of these.

Instead of editing and copying `httpd.conf` why don’t you just define a variable for the listen port and use it in a template? Here is your job:

  - Define a variable `listen_port` for the `web` group with the value `8080` and another for `node2` with the value `80` using the proper files.

  - Copy the `httpd.conf` file into the template `httpd.conf.j2` that uses the `listen_port` variable instead of the hard-coded port number.

  - Write a Playbook that deploys the template and restarts Apache on changes using a handler.

  - Run the Playbook and test the result using `curl`.

> **Tip**
>
> Remember the `group_vars` and `host_vars` directories? If not, refer to the chapter "Ansible Variables".


> **Warning**
>
> **Solution below\!**

### Define the variables:


Add this line to `group_vars/web`:

```ini
listen_port: 8080
```

Add this line to `host_vars/node2`:

```ini
listen_port: 80
```
### Prepare the template:

  - Copy `httpd.conf` to `httpd.conf.j2`

  - Edit the "Listen" directive in `httpd.conf.j2` to make it look like this:

<!-- {% raw %} -->
```ini
[...]
Listen {{ listen_port }}
[...]
```
<!-- {% endraw %} -->

### Create the Playbook

Create a playbook called `apache_config_tpl.yml`:

```yaml
---
- name: Apache httpd.conf
  hosts: web
  become: yes
  tasks:
  - name: Create Apache configuration file from template
    template:
      src: httpd.conf.j2
      dest: /etc/httpd/conf/httpd.conf
    notify:
        - restart apache
  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
```

### Run and test

First run the playbook itself, then run curl against `node1` with port `8080` and `node2` with port `80`.

```bash
[student1@ansible ansible-files]$ ansible-playbook apache_config_tpl.yml
[...]
[student1@ansible ansible-files]$ curl http://18.195.235.231:8080
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
[student1@ansible ansible-files]$ curl http://35.156.28.209:80
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../../README.md#section-1---ansible-engine-exercises)
