# Workshop: Ansible Tower Basic Setup

### Topics Covered

* Credentials
* Inventory
* Users
* Roles & Permissions
* Projects
* Job Templates
* Running a Job (Playbook)

### What You Will Learn

* Setting up a new instance of Tower with all the parts needed to run an existing Ansible playbook.

### Requirements

* A running instance of Ansible Tower with sufficient permissions to create credentials, inventory sources, projects etc.

### Before You Begin

Before doing this assignment you will need to perform a task you typical won't have to do when setting up Ansible Tower: manually enter your inventory. Commonly, Ansible Tower will be setup with one or more dynamic inventory sources such as AWS EC2 or vSphere or internal CMDB as a source of truth. Given the size and static nature of the Lightbulb lab environment, taking the time to setup and configure dynamic inventory is unnecessary.

To make this process a bit easier, we now include a playbook to automatically import your inventory into tower to reduce the configuration needed. See the [Inventory Import README](../../tools/inventory_import/README.md) for additional details.

If you choose to run this playbook and its next steps, you can skip items 1 & 3 in the below assignment.

### The Assignment

NOTE: Create all new entities under the "Default" organization Ansible Tower create during setup unless noted otherwise.

1. Enter your lab inventory's groups and hosts into Tower. (See "Before You Begin" above.)
2. Create a machine credential called "Ansible Lab Machine" with the username and password for the hosts in your lab.
3. Create an inventory source called "Ansible Lightbulb Lab" and create the groups and hosts in your static inventory file.
4. Create a project called "Ansible Lightbulb Examples Project" with a SCM type of Git and URL of https://github.com/ansible/lightbulb. You should also enable "Update on Launch".
5. Create a Job Template called "Nginx Role Example" with the machine credential, inventory and project you created in the previous steps. Select "examples/nginx-role/site.yml" as the playbook.
6. Execute the job template. Check that it runs without errors and the web servers are serving the home page.
7. Add an extra variables of `nginx_test_message` with a string like "Hello World" then run the "Nginx Role Example" job template again. Again, check that it executes without errors and the web servers are serving the home page with the new test message.

### Extra Credit

Setup a self-service user simulation with the playbook

* Create a "Normal" user with the name "someuser"
* Assign the new user "Execute" permissions on the "Nginx Role Example" job template
* Create a user survey on the job template that enables users to update the test message on the home page
