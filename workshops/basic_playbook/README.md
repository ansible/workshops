# Workshop: Basic Playbook

### Topics Covered

* Using `ansible-playbook`
* YAML syntax basics
* Basic Ansible playbook structure
* Tasks and modules
* Handlers
* Variables
* Loops

### What You Will Learn

* How to use `ansible-playbook`
* The basics of YAML syntax and Ansible playbook structure
* How to deploy and configure an application onto a group of hosts

### Before You Begin

If you're not familiar with the structure and authoring YAML files take a moment to read thru the Ansible [YAML Syntax](http://docs.ansible.com/ansible/YAMLSyntax.html) guide.

#### NOTE

You will need to assure each host in "web" group has setup the EPEL repository to find and install the nginx package with yum.

### The Assignment

Create an Ansible playbook that will assure nginx is present, configured and running on all hosts in the "web" group:

1. Has variables for `nginx_test_message` and `nginx_keepalive_timeout`.
1. Assures that the following yum packages are present on the each web host:
    * nginx
    * python-pip
    * python-devel
    * gcc
1. Assure that the uwsgi pip package is present on each host.
1. Generate a host-specific home page with the value of `nginx_test_message` for each host using the provided `index.html.j2` template.
1. Generate a configuration with the value of `nginx_keepalive_timeout` for each host using the provided `nginx.conf.j2` template.
1. Assure that nginx is running on each host.
1. The playbook should restart nginx if the homepage or configuration file is altered.

While developing the playbook use the `--syntax-check` to check your work and debug problems. Run your playbook in verbose mode using the `-v` switch to get more information on what Ansible is doing. Try `-vv` and `-vvv` for added verbosity. Also consider running `--check` to do a dry-run as you are developing. 

#### Extra Credit

1. Add a smoke test to your playbook using the `uri` module that test nginx is serving the sample home page.
1. Create a separate playbook that stops and removes nginx along with its configuration file and home page.

### Resources

* [YAML Syntax](http://docs.ansible.com/ansible/YAMLSyntax.html)
* [Intro to Ansible Playbooks](http://docs.ansible.com/ansible/playbooks_intro.html)
    * [Handlers](http://docs.ansible.com/ansible/playbooks_intro.html#handlers-running-operations-on-change)
    * [Variables](http://docs.ansible.com/ansible/playbooks_variables.html)
    * [Loops](http://docs.ansible.com/ansible/playbooks_loops.html)
* [yum module](http://docs.ansible.com/ansible/yum_module.html)
* [pip module](http://docs.ansible.com/ansible/pip_module.html)
* [template module](http://docs.ansible.com/ansible/template_module.html)
* [service module](http://docs.ansible.com/ansible/service_module.html)
* [uri module](http://docs.ansible.com/ansible/template_module.html)
* [file module](http://docs.ansible.com/ansible/file_module.html)
