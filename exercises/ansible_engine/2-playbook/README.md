# Exercise 2 - Writing Your First playbook


Now that you've gotten a sense of how ansible works, we are going to write our first ansible *playbook*.  The playbook is where you can take some of those ad-hoc commands you just ran and put them into a repeatable set of *plays* and *tasks*.

A playbook can have multiple plays and a play can have one or multiple tasks.  The goal of a *play* is to map a group of hosts.  The goal of a *task* is to implement modules against those hosts.

For our first playbook, we are only going to write one play and two tasks.


## Section 1: Creating a Directory Structure and Files for your Playbook

There is a [best practice](http://docs.ansible.com/ansible/playbooks_best_practices.html) on the preferred directory structures for playbooks.  We strongly encourage you to read and understand these practices as you develop your Ansible ninja skills.  That said, our playbook today is very basic and creating a complex structure will just confuse things.

Instead, we are going to create a very simple directory structure for our playbook, and add just a couple of files to it.


*Step 1:* Create a directory called *apache_basic* in your home directory and change directories into it

```bash
mkdir ~/apache_basic
cd ~/apache_basic
```

*Step 2:* Use `vi` or `vim` to open a file called `install_apache.yml`


## Section 2: Defining Your Play

Now that you are editing `install_apache.yml`, let's begin by defining the play and then understanding what each line accomplishes


```yml
---
- hosts: web
  name: Install the apache web service
  become: yes
```

- `---` Defines the beginning of YAML
- `hosts: web` Defines the host group in your inventory on which this play will run against
- `name: Install the apache web service` This describes our play
- `become: yes` Enables user privilege escalation.  The default is sudo, but su, pbrun, and [several others](http://docs.ansible.com/ansible/become.html) are also supported.


## Section 3: Adding Tasks to Your Play

Now that we've defined your play, let's add some tasks to get some things done.  Align (vertically) the *t* in `task` with the *b* `become`. Yes, it does actually matter.  In fact, you should make sure all of your playbook statements are aligned in the way shown here. If you want to see the entire playbook for reference, skip to the bottom of this exercise.


```yml
tasks:
 - name: install apache
   yum:
     name: httpd
     state: present

 - name: start httpd
   service:
     name: httpd
     state: started
```

- `tasks:` This denotes that one or more tasks are about to be defined
- `- name:` Each task requires a name which will print to standard output when you run your playbook.
Therefore, give your tasks a name that is short, sweet, and to the point


```yml
yum:
  name: httpd
  state: present
```


- These three lines are calling the Ansible module *yum* to install httpd.
[Click here](http://docs.ansible.com/ansible/yum_module.html) to see all options for the yum module.


```yml
service:
  name: httpd
  state: started
```

- The next few lines are using the ansible module *service* to start the httpd service.  The service module is the preferred way of controlling services on remote hosts. [Click here](http://docs.ansible.com/ansible/service_module.html) to learn more about the *service* module.


## Section 4: Saving your Playbook

Now that you've completed writing your playbook, it would be a shame not to keep it.

Use the `write/quit` method in `vi` or `vim` to save your playbook, i.e. `Esc :wq!`


And that should do it.  You should now have a fully written playbook called `install_apache.yml`. You are ready to automate!

---
**NOTE**
Ansible (well, YAML really) can be a bit particular about formatting especially around indentation/spacing.  When you all get back to the office,
read up on this [YAML Syntax](http://docs.ansible.com/ansible/YAMLSyntax.html) a bit more and it will save you some headaches later.  In the meantime, your completed playbook should look
like this.  Take note of the spacing and alignment.

---

```yml
---
- hosts: web
  name: Install the apache web service
  become: yes

  tasks:
    - name: install apache
      yum:
        name: httpd
        state: present

    - name: start httpd
      service:
        name: httpd
        state: started
```
---

[Click Here to return to the Ansible Linklight - Ansible Engine Workshop](../README.md)
