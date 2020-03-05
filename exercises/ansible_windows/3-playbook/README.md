Let’s begin by writing our first ansible **playbook**. The playbook is
where you list the steps you would like to automate into a repeatable
set of **plays** and **tasks**. To begin we will setup our directory
structure for storing our playbooks. This directory structure will sync
with a **source control management** (SCM) system to version our
playbooks. We will be using **git** as out SCM.

A playbook can have multiple plays and a play can have one or multiple
tasks. The goal of a **play** is to map a group of hosts. The goal of a
**task** is to implement modules against those hosts.

For our first playbook, we are only going to write 1 play and 3 tasks.

All of our playbooks will be stored in a single git **repository**.
Multiple users can use the same repository and git will manage file
conflicts and versions.

Overview
========

Starting at this task we are going to use Visual Studio Code as our
editor. In addition, we will use GitLab for source code control. This
will allow us to minimize development work on the linux command line.
Other editors or source code solutions can be used, but this will show
the general workflow.

Section 1: Creating a Directory Structure and Files for your Playbook
=====================================================================

There is a [best
practice](http://docs.ansible.com/ansible/playbooks_best_practices.html)
on the preferred directory structures for playbooks. We strongly
encourage you to read and understand these practices as you develop your
Ansible skills. That said, our playbook today is very basic and a
complex directory structure is not necessary.

Instead, we are going to create a very simple directory structure for
our playbook, and add just a couple of files.

**Step 1:**

Open Visual Studio Code

For this lab, we have already created a clone of your Git repository for
you.

To access it, click the link for VS Code Access from the workshop page.

![VS Code Access](images/3-vscode-access.png)

At this point in the Explorer sidebar you should have a *WORKSHOP_PROJECT*
section with only a README file in it.

![Student Playbooks Repo](images/3-vscode-open-folder.png)

**Step 2:** Create a directory called **iis\_basic** and a file called
`install_iis.yml`

Hover over the *WORKSHOP_PROJECT* section and click the *New Folder* button.
Create a folder called `iis_basic`. Then click that folder so it is
selected. Right click the new folder you’ve created and create a file
called `install_iis.yml`.

You should now have an editor open in the right pane that can be used
for creating your playbook.

![Empty install\_iis.yml](images/3-vscode-create-folders.png)

Section 2: Defining Your Play
=============================

Now that you are editing `install_iis.yml`, let’s begin by defining the
play and then understanding what each line accomplishes

```yaml
    ---
    - name: install the iis web service
      hosts: windows
```

- `---` Defines the beginning of YAML

- `name: install the iis web service` This describes our play

- `hosts: windows` Defines the host group in your inventory on which this
  play will run against

Section 3: Adding Tasks to Your Play
====================================

Now that we’ve defined your play, let’s add some tasks to get some
things done. Align (vertically) the **t** in `task` with the **h** in
`hosts`.
Yes, it does actually matter. In fact, you should make sure all of your
playbook statements are aligned in the way shown here. You also must use
spaces for indentation. Tabs are not valid YAML syntax.
If you want to see the entire playbook for reference, skip to the bottom
of this exercise.

<!-- {% raw %} -->
```yaml
      tasks:
       - name: install iis
         win_feature:
           name: Web-Server
           state: present

       - name: start iis service
         win_service:
           name: W3Svc
           state: started

       - name: Create website index.html
         win_copy:
           content: "{{ iis_test_message }}"
           dest: C:\Inetpub\wwwroot\index.html

       - name: Show website address
         debug:
           msg: "http://{{ ansible_host }}"
```
<!-- {% endraw %} -->

- `tasks:` This denotes that one or more tasks are about to be defined

- `- name:` Each task requires a name which will print to standard
  output when you run your playbook. Therefore, give your tasks a name
  that is short, sweet, and to the point

<!-- -->

```yaml
    win_feature:
      name: Web-Server
      state: present
```

- These three lines are calling the Ansible module **`win_feature`** to
  install the IIS Web Server. [Click
  here](http://docs.ansible.com/ansible/latest/win_feature_module.html)
  to see all options for the `win_feature` module.

<!-- -->
```yaml
    win_service:
      name: W3Svc
      state: started
```

- The next few lines are using the ansible module **win\_service** to
  start the IIS service. The `win_service` module is the preferred way
  of controlling services on remote hosts. [Click
  here](http://docs.ansible.com/ansible/latest/win_service_module.html)
  to learn more about the **`win_service`** module.

<!-- {% raw %} -->
```yaml
    win_copy:
      content: "{{ iis_test_message }}"
      dest: C:\Inetpub\wwwroot\index.html
```
<!-- {% endraw %} -->

- In this task, we use the win\_copy module to create a file with
  specific contents in it. We are getting a little more complex here
  as we are using a variable to source the contents. We won’t go into
  the variables just yet, since they will be showcased in a later
  lesson.

<!-- {% raw %} -->
```yaml
    debug:
      msg: http://{{ ansible_host }}
```
<!-- {% endraw %} -->

- This task uses the `debug` module to post a message at the end of playbook execution. This particular message prints out `http://` + the variable name that contains the IP address of the host we're running the playbook on (our Windows IIS server)

Section 4: Saving your Playbook
===============================

Now that you’ve completed writing your playbook, it would be a shame not
to keep it. Click `File > Save` from the menu.

And that should do it. You should now have a fully written playbook
called `install_iis.yml`.

But wait!!! We haven’t committed our changes from our **local** copy to
**git**. Click the Source Code icon as shown below (It is the middle on
the far left of the page that has the blue circle with \# 1 in it)

![Git Commit](images/3-vscode-click-commit.png)

Type in a commit message such as *Adding install\_iis.yml* in the text
box at the top of the sidebar. Click the check box above to commit. This
message is intended to describe the changes you made so that others
(including yourself) better understand what is changing when comparing
versions.

![Git Commit install\_iis.yml](images/3-vscode-commit.png)

Now you need to push the committed changes to your repository.

On the bottom left blue bar, click the section that contains the
circular arrows to push the changes.

![Git Push Origin](images/3-vscode-push.png)

This may take as long as 30 seconds to push. After your first push, you
may get a pop-up message asking if you would like to periodically run
git fetch. Because you’re the only one working on the git repo, you can
click **Yes** or **No**.

![Git Push Origin](images/3-vscode-push-initial-pop-up.png)

If you’re interested in validating the code is in git, you can connect
to GitLab to verify. Go back to the workshop page, and click the link under **GitLab Access** taking note of your username and password.

![GitLab access](images/3-vscode-gitlab-access.png)

You are ready to automate!

> **Note**
>
> Ansible (well, YAML really) can be a bit particular about formatting
> especially around indentation/spacing. When you get back to the
> office, read up on this [YAML
> Syntax](http://docs.ansible.com/ansible/YAMLSyntax.html) a bit more
> and it will save you some headaches later. In the meantime, your
> completed playbook should look like this. Take note of the spacing and
> alignment.

<!-- {% raw %} -->
```yaml
    ---
    - name: install the iis web service
      hosts: windows

      tasks:
        - name: install iis
          win_feature:
            name: Web-Server
            state: present

        - name: start iis service
          win_service:
            name: W3Svc
            state: started

        - name: Create website index.html
          win_copy:
            content: "{{ iis_test_message }}"
            dest: C:\Inetpub\wwwroot\index.html

        - name: Show website address
          debug:
            msg: http://{{ ansible_host }}
```
<!-- {% endraw %} -->
