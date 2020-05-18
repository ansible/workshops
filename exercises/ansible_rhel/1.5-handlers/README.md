# Workshop Exercise - Conditionals, Handlers and Loops

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objective](#objective)
* [Guide](#guide)
* [Step 1 - Conditionals](#step-1---conditionals)
* [Step 2 - Handlers](#step-2---handlers)
* [Step 3 - Simple Loops](#step-3---simple-loops)
* [Step 4 - Loops over hashes](#step-4---loops-over-hashes)

# Objective

Three foundational Ansible features are:  
- [Conditionals](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html)
- [Handlers](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#handlers-running-operations-on-change)
- [Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)

# Guide

## Step 1 - Conditionals

Ansible can use conditionals to execute tasks or plays when certain conditions are met.

To implement a conditional, the `when` statement must be used, followed by the condition to test. The condition is expressed using one of the available operators like e.g. for comparison:

|      |                                                                        |
| ---- | ---------------------------------------------------------------------- |
| \==  | Compares two objects for equality.                                     |
| \!=  | Compares two objects for inequality.                                   |
| \>   | true if the left hand side is greater than the right hand side.        |
| \>=  | true if the left hand side is greater or equal to the right hand side. |
| \<   | true if the left hand side is lower than the right hand side.          |
| \<= | true if the left hand side is lower or equal to the right hand side.   |

For more on this, please refer to the documentation: <http://jinja.pocoo.org/docs/2.10/templates/>

As an example you would like to install an FTP server, but only on hosts that are in the "ftpserver" inventory group.

To do that, first edit the inventory to add another group, and place `node2` in it. Make sure that that IP address of `node2` is always the same when `node2` is listed. Edit the inventory `~/lab_inventory/hosts` to look like the following listing:

```ini
[all:vars]
ansible_user=student1
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[ftpserver]
node2 ansible_host=22.33.44.55

[control]
ansible ansible_host=44.55.66.77
```

Next create the file `ftpserver.yml` on your control host in the `~/ansible-files/` directory:

```yaml
---
- name: Install vsftpd on ftpservers
  hosts: all
  become: yes
  tasks:
    - name: Install FTP server when host in ftpserver group
      yum:
        name: vsftpd
        state: latest
      when: inventory_hostname in groups["ftpserver"]
```

> **Tip**
>
> By now you should know how to run Ansible Playbooks, we’ll start to be less verbose in this guide. Go create and run it. :-)

Run it and examine the output. The expected outcome: The task is skipped on node1, node3 and the ansible host (your control host) because they are not in the ftpserver group in your inventory file.

```bash
TASK [Install FTP server when host in ftpserver group] *******************************************
skipping: [ansible]
skipping: [node1]
skipping: [node3]
changed: [node2]
```

# Step 2 - Handlers

Sometimes when a task does make a change to the system, an additional task or tasks may need to be run. For example, a change to a service’s configuration file may then require that the service be restarted so that the changed configuration takes effect.

Here Ansible’s handlers come into play. Handlers can be seen as inactive tasks that only get triggered when explicitly invoked using the "notify" statement. Read more about them in the [Ansible Handlers](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change) documentation.

As a an example, let’s write a Playbook that:

  - manages Apache’s configuration file `/etc/httpd/conf/httpd.conf` on all hosts in the `web` group

  - restarts Apache when the file has changed

First we need the file Ansible will deploy, let’s just take the one from node1. Remember to replace the IP address shown in the listing below with the IP address from your individual `node1`.

```
[student<X>@ansible ansible-files]$ scp 11.22.33.44:/etc/httpd/conf/httpd.conf ~/ansible-files/files/.
student<X>@11.22.33.44's password:
httpd.conf             
```

Next, create the Playbook `httpd_conf.yml`. Make sure that you are in the directory `~/ansible-files`.

```yaml
---
- name: manage httpd.conf
  hosts: web
  become: yes
  tasks:
  - name: Copy Apache configuration file
    copy:
      src: httpd.conf
      dest: /etc/httpd/conf/
    notify:
        - restart_apache
  handlers:
    - name: restart_apache
      service:
        name: httpd
        state: restarted
```

So what’s new here?

  - The "notify" section calls the handler only when the copy task actually changes the file. That way the service is only restarted if needed - and not each time the playbook is run.

  - The "handlers" section defines a task that is only run on notification.
<hr>

Run the Playbook. We didn’t change anything in the file yet so there should not be any `changed` lines in the output and of course the handler shouldn’t have fired.

  - Now change the `Listen 80` line in `~/ansible-files/files/httpd.conf` to:

```ini
Listen 8080
```

  - Run the Playbook again. Now the Ansible’s output should be a lot more interesting:

      - httpd.conf should have been copied over

      - The handler should have restarted Apache

Apache should now listen on port 8080. Easy enough to verify:

```bash
[student1@ansible ansible-files]$ curl http://node1
curl: (7) Failed connect to 22.33.44.55:80; Connection refused
[student1@ansible ansible-files]$ curl http://node1:8080
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```
Feel free to change the httpd.conf file again and run the playbook.

## Step 3 - Simple Loops

Loops enable us to repeat the same task over and over again. For example, lets say you want to create multiple users. By using an Ansible loop, you can do that in a single task. Loops can also iterate over more than just basic lists. For example, if you have a list of users with their coresponding group, loop can iterate over them as well. Find out more about loops in the [Ansible Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html) documentation.

To show the loops feature we will generate three new users on `node1`. For that, create the file `loop_users.yml` in `~/ansible-files` on your control node as your student user. We will use the `user` module to generate the user accounts.

<!-- {% raw %} -->
```yaml
---
- name: Ensure users
  hosts: node1
  become: yes

  tasks:
    - name: Ensure three users are present
      user:
        name: "{{ item }}"
        state: present
      loop:
         - dev_user
         - qa_user
         - prod_user
```
<!-- {% endraw %} -->

Understand the playbook and the output:

<!-- {% raw %} -->
  - The names are not provided to the user module directly. Instead, there is only a variable called `{{ item }}` for the parameter `name`.

  - The `loop` keyword lists the actual user names. Those replace the `{{ item }}` during the actual execution of the playbook.

  - During execution the task is only listed once, but there are three changes listed underneath it.
<!-- {% endraw %} -->

## Step 4 - Loops over hashes

As mentioned loops can also be over lists of hashes. Imagine that the users should be assigned to different additional groups:

```yaml
- username: dev_user
  groups: ftp
- username: qa_user
  groups: ftp
- username: prod_user
  groups: apache
```

The `user` module has the optional parameter `groups` to list additional users. To reference items in a hash, the `{{ item }}` keyword needs to reference the subkey: `{{ item.groups }}` for example.

Let's rewrite the playbook to create the users with additional user rights:

<!-- {% raw %} -->
```yaml
---
- name: Ensure users
  hosts: node1
  become: yes

  tasks:
    - name: Ensure three users are present
      user:
        name: "{{ item.username }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { username: 'dev_user', groups: 'ftp' }
        - { username: 'qa_user', groups: 'ftp' }
        - { username: 'prod_user', groups: 'apache' }

```
<!-- {% endraw %} -->

Check the output:

  - Again the task is listed once, but three changes are listed. Each loop with its content is shown.

Verify that the user `dev_user` was indeed created on `node1`:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a "id dev_user"
node1 | CHANGED | rc=0 >>
uid=1002(dev_user) gid=1002(dev_user) Gruppen=1002(dev_user),50(ftp)
```

----
**Navigation**
<br>
[Previous Exercise](../1.4-variables) - [Next Exercise](../1.6-templates)

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
