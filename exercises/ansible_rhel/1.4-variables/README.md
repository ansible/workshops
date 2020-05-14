# Workshop Exercise - Using Variables

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
* [Intro to Variables](#intro-to-variables)
* [Step 1 - Create Variable Files](#step-1---create-variable-files)
* [Step 2 - Create index.html Files](#step-2---create-indexhtml-files)
* [Step 3 - Create the Playbook](#step-3---create-the-playbook)
* [Step 4 - Test the Result](#step-4---test-the-result)
* [Step 5 - Ansible Facts](#step-5---ansible-facts)
* [Step 6 - Challenge Lab: Facts](#step-6---challenge-lab-facts)
* [Step 7 - Using Facts in Playbooks](#step-7---using-facts-in-playbooks)

# Objective

Ansible supports variables to store values that can be used in Playbooks. Variables can be defined in a variety of places and have a clear precedence. Ansible substitutes the variable with its value when a task is executed.

This exercise covers variables, specifically
- How to use variable delimiters `{{` and `}}`
- What `host_vars` and `group_vars` are and when to use them
- How to use `ansible_facts`
- How to use the `debug` module to print variables to the console window

# Guide

## Intro to Variables

Variables are referenced in Ansible Playbooks by placing the variable name in double curly braces:

<!-- {% raw %} -->
```yaml
Here comes a variable {{ variable1 }}
```
<!-- {% endraw %} -->

Variables and their values can be defined in various places: the inventory, additional files, on the command line, etc.

The recommended practice to provide variables in the inventory is to define them in files located in two directories named `host_vars` and `group_vars`:

  - To define variables for a group "servers", a YAML file named `group_vars/servers.yml` with the variable definitions is created.

  - To define variables specifically for a host `node1`, the file `host_vars/node1.yml` with the variable definitions is created.

> **Tip**
>
> Host variables take precedence over group variables (more about precedence can be found in the [docs](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)).


## Step 1 - Create Variable Files

For understanding and practice let’s do a lab. Following up on the theme "Let’s build a web server. Or two. Or even more…​", you will change the `index.html` to show the development environment (dev/prod) a server is deployed in.

On the ansible control host, as the `student<X>` user, create the directories to hold the variable definitions in `~/ansible-files/`:

```bash
[student<X>@ansible ansible-files]$ mkdir host_vars group_vars
```

Now create two files containing variable definitions. We’ll define a variable named `stage` which will point to different environments, `dev` or `prod`:

  - Create the file `~/ansible-files/group_vars/web.yml` with this content:

```yaml
---
stage: dev
```

  - Create the file `~/ansible-files/host_vars/node2.yml` with this content:

```yaml
---
stage: prod
```

What is this about?

  - For all servers in the `web` group the variable `stage` with value `dev` is defined. So as default we flag them as members of the dev environment.

  - For server `node2` this is overridden and the host is flagged as a production server.

## Step 2 - Create web.html Files

Now create two files in `~/ansible-files/files/`:

One called `prod_web.html` with the following content:

```html
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

And the other called `dev_web.html` with the following content:

```html
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

## Step 3 - Create the Playbook

Now you need a Playbook that copies the prod or dev `web.html` file - according to the "stage" variable.

Create a new Playbook called `deploy_index_html.yml` in the `~/ansible-files/` directory.

> **Tip**
>
> Note how the variable "stage" is used in the name of the file to copy.

<!-- {% raw %} -->
```yaml
---
- name: Copy web.html
  hosts: web
  become: true
  tasks:
  - name: copy web.html
    copy:
      src: "{{ stage }}_web.html"
      dest: /var/www/html/index.html
```
<!-- {% endraw %} -->

  - Run the Playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook deploy_index_html.yml
```

## Step 4 - Test the Result

The Ansible Playbook copies different files as index.html to the hosts, use `curl` to test it.

For node1:
```
[student<X>@ansible ansible-files]$ curl http://node1
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

For node2:

```
[student1@ansible ansible-files]$ curl http://node2
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

For node3:
```
[student1@ansible ansible-files]$ curl http://node3
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

> **Tip**
>
> If by now you think: There has to be a smarter way to change content in files…​ you are absolutely right. This lab was done to introduce variables, you are about to learn about templates in one of the next chapters.

## Step 5 - Ansible Facts

Ansible facts are variables that are automatically discovered by Ansible from a managed host. Remember the "Gathering Facts" task listed in the output of each `ansible-playbook` execution? At that moment the facts are gathered for each managed nodes. Facts can also be pulled by the `setup` module. They contain useful information stored into variables that administrators can reuse.

To get an idea what facts Ansible collects by default, on your control node as your student user run:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup
```

This might be a bit too much, you can use filters to limit the output to certain facts, the expression is shell-style wildcard:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_eth0'
```
Or what about only looking for memory related facts:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_*_mb'
```

## Step 6 - Challenge Lab: Facts

  - Try to find and print the distribution (Red Hat) of your managed hosts. On one line, please.

> **Tip**
>
> Use grep to find the fact, then apply a filter to only print this fact.

> **Warning**
>
> **Solution below\!**

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep distribution
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_distribution' -o
```

## Step 7 - Using Facts in Playbooks

Facts can be used in a Playbook like variables, using the proper naming, of course. Create this Playbook as `facts.yml` in the `~/ansible-files/` directory:

<!-- {% raw %} -->
```yaml    
---
- name: Output facts within a playbook
  hosts: all
  tasks:
  - name: Prints Ansible facts
    debug:
      msg: The default IPv4 address of {{ ansible_fqdn }} is {{ ansible_default_ipv4.address }}
```
<!-- {% endraw %} -->

> **Tip**
>
> The "debug" module is handy for e.g. debugging variables or expressions.

Execute it to see how the facts are printed:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook facts.yml

PLAY [Output facts within a playbook] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node2]
ok: [node1]
ok: [ansible]

TASK [Prints Ansible facts] ****************************************************
ok: [node1] =>
  msg: The default IPv4 address of node1 is 172.16.190.143
ok: [node2] =>
  msg: The default IPv4 address of node2 is 172.16.30.170
ok: [node3] =>
  msg: The default IPv4 address of node3 is 172.16.140.196
ok: [ansible] =>
  msg: The default IPv4 address of ansible is 172.16.2.10

PLAY RECAP *********************************************************************
ansible                    : ok=2    changed=0    unreachable=0    failed=0   
node1                      : ok=2    changed=0    unreachable=0    failed=0   
node2                      : ok=2    changed=0    unreachable=0    failed=0   
node3                      : ok=2    changed=0    unreachable=0    failed=0   
```

----
**Navigation**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Previous Exercise](../3-playbook) - [Next Exercise](../5-surveys)
{% else %}
[Previous Exercise](../1.3-playbook) - [Next Exercise](../1.5-handlers)
{% endif %}
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
