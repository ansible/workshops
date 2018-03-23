# Exercise 4 - Using Ansible to Implement Security

In this exercise, we are going to use Ansible Tower to run DISA STIG and NIST 800-53 evaluations of our environment.  Note that the NIST 800-53 role also includes the execution of DISA STIG evaluation against targeted hosts.

* [DISA STIG controls](https://galaxy.ansible.com/MindPointGroup/RHEL7-STIG/)
* [NIST 800-53 controls](https://galaxy.ansible.com/rhtps/800-53/)

## Adding the DISA STIG and NIST 800-53 role to your Tower node

### Step 1:

In your wetty window (if you closed it, see the [SETUP](../setup.md) step, in your workbook), type the following:

```bash
sudo ansible-galaxy install rhtps.800-53
```

### Step 2:

Now that you have the role installed on your Tower node, we need to create a playbook that uses it.  First, let's create a storage directory for playbooks, so that we can reference them from a Tower project, and then we'll create the playbook:

```bash
sudo mkdir -p /var/lib/awx/projects/playbooks
```

### Step 3:

Let's create the needed playbook.  You should have a pretty good understanding of playbooks by now, so we won't go over this, in detail.  Please do feel free to ask questions, though, if there is something that you don't understand.

```bash
sudo vim /var/lib/awx/projects/playbooks/800-53.yml
```

Note the use of the [register](http://docs.ansible.com/ansible/latest/playbooks_conditionals.html#register-variables), [with_items](http://docs.ansible.com/ansible/latest/playbooks_loops.html#standard-loops), and [when](http://docs.ansible.com/ansible/latest/playbooks_conditionals.html#the-when-statement) directives. These are how Ansible implements variable creation, recursion, and conditionals, respectively.

```yml
{% raw %}
---
- hosts: web
  become: yes
  vars:
    scap_reports_dir: /tmp
    scap_profile: stig-rhel7-disa
  roles:
    - rhtps.800-53 

  tasks:
    - name: determine the most recent scap report
      command: ls -tr /tmp/scap_reports/
      register: results

    - name: create the scap directory in the web server content
      file:
        name: /var/www/html/scap
        state: directory
        mode: 0755

    - name: copy SCAP reports to the web server content directory
      copy:
        remote_src: True
        src: "/tmp/scap_reports/{{ item }}"
        dest: /var/www/html/scap
        mode: 0644
      with_items: "{{ results.stdout_lines }}"
      when: item | match("scan-xccdf-report-*")
{% endraw %}
```

### Step 4:

Save and quit from editing, and then we will move on to the in-Tower setup.

## Configuring a security project and job template in Ansible Tower

### Step 1:

In your Tower window, click on ![PROJECTS](at_projects_icon.png)

### Step 2:

Select ADD ![Add button](at_add.png)

### Step 3:

Enter the following values into your new project.  Note that the `PLAYBOOK DIRECTORY` item should show `playbooks`, as an option, when you click on it.

NAME |NIST 800-53 and DISA STIG
-----|-------------------------
DESCRIPTION|Security Project
ORGANIZATION|Default
SCM TYPE|Manual
PROJECT BASE PATH|/var/lib/awx/projects
PLAYBOOK DIRECTORY|playbooks

### Step 4:

Select SAVE ![Save button](at_save.png)

### Step 5:

In your Tower window, click on `TEMPLATES`

### Step 6:

Click on ADD ![Add button](at_add.png), and select `JOB TEMPLATE`

### Step 7:

Complete the form using the following values.  Note that the `PLAYBOOK` field should offer `800-53.yml` as an option, when clicked.

NAME |NIST 800-53 and DISA STIG Job Template
-----|--------------------------------------
DESCRIPTION|Template for security playbooks
JOB TYPE|Run
INVENTORY|Ansible Workshop Inventory
PROJECT|NIST 800-53 and DISA STIG
PLAYBOOK|800-53.yml
MACHINE CREDENTIAL|Ansible Workshop Credential
LIMIT|web
OPTIONS
a|[x] Enable Privilege Escalation

### Step 8:

Click SAVE ![Save button](at_save.png), to store your new template, and we are ready to run it.

Click on the rocketship icon ![Add button](at_launch_icon.png) next to the `NIST 800-53 Job Template` entry, to launch the job.

You can see what the job looks like, as it is executing, and what the SCAP results look like, when uploaded to your second node, in the panel, below.

![Job Status](at_800-53_job_status.png)
![SCAP Report](at_scap_report.png)


### End Result

You can watch the scan run against your managed node.  Note that each compliance check is named and detailed.

Once the check is complete, you can open a new tab in your web browser, and navigate to the following URL, where `workshopname` is the workshop prefix, and `#` is the number that your instructor gave you:

```bash
http://workshopname.node.#.redhatgov.io/scap
```

Click on the link called `scan-xccdf-report-...` to refiew the SCAP report that was generated.  Note the failures in the report; look at the machines, if you want, via your Wetty ssh session, to see what the problems might be.

---

[Click Here to return to the Ansible Lightbulb - Ansible Tower Workshop](../README.md)
