# Exercise 1.2 - Backing up Configurations

We are going to write our first Ansible **playbook**. The playbook is where you can take some of the ad-hoc commands from exercise 1.1 and make them a repeatable set of plays and tasks.

A playbook can have multiple plays and a play can have one or multiple tasks. The goal of a play is to map a group of hosts. The goal of a task is to implement modules against those hosts.

## Table of contents
- [Exploring the environment](#exploring-the-environment)
- [Playbook 1 - backup.yml](#playbook-1---backupyml)
- [Playbook 2 - host-routes.yml](#playbook-2---host-routesyml)
- [Answer Key](#answer-key)


## Exploring the environment
Before we run a playbook, lets explore
  - ansible.cfg - the ansible configuration files
  - inventory - hosts and groups configurations

### Step 1: Navigate to the networking-workshop directory

```bash
cd ~/networking-workshop
```

### Step 2: Look at the ansible configuration file

Run the `ansible` command with the `--version` command to look at what is configured:
```bash
[lcage@ip-172-16-74-150 ~]$ ansible --version
ansible 2.4.1.0
  config file = /home/lcage/.ansible.cfg
  configured module search path = [u'/home/lcage/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Oct 11 2015, 17:47:16) [GCC 4.8.3 20140911 (Red Hat 4.8.3-9)]
```
In the output provided the [ansible.cfg file](http://docs.ansible.com/ansible/latest/intro_configuration.html) location is shown.  Now cat the ansible.cfg to see the configuration parameters:
```bash
[lcage@ip-172-16-74-150 ~]$ cat ~/.ansible.cfg
[defaults]
connection = smart
timeout = 60
inventory = /home/lcage/networking-workshop/lab_inventory/hosts
host_key_checking = False
private_key_file = ~/.ssh/aws-private.pem
```
The two most important parameters are:
 - `inventory`: shows the location of the ansible inventory being used
 - `private_key_file`: this shows the location of the private key used to login to devices

### Step 3: Understand your inventory.
[Inventories](http://docs.ansible.com/ansible/latest/intro_inventory.html) are crucial to Ansible as they define remote nodes on which you wish to run your playbook(s). `cat` the inventory file:

```bash
cat ~/networking-workshop/lab_inventory/hosts
```

There are a total of 3 groups:
 - `[control]` - contains the `ansible` node that we are currently ssh’d into
 - `[routers]` - contains the two routers `rtr1` and `rtr2`
 - `[hosts]` - contains one linux host `host1` connected to `rtr2`

Let's analyze one of the hosts:
```bash
rtr1 ansible_host=54.174.116.49 ansible_ssh_user=ec2-user private_ip=172.16.3.183
```
 - `rtr1` - the name that ansible will use.  This can but does not have to rely on DNS
 - `ansible_host` - the IP address that ansible will use, if not configured it will default to DNS
 - `ansible_ssh_user` - the user ansible will use to login to this host, if not configured it will default to the user the playbook is run from
 - `private_ip` - this value is not reserved by ansible so it will default to a [host variable](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables).  This variable can be used by playbooks or ignored completely.


## Playbook 1 - backup.yml
A playbook for backing up Cisco IOS configurations.

**What you will learn:**
 - ios_facts module
 - register keyword
 - debug module
 - ios_config module backup parameter

 ---

### Step 1: Defining the Play

Let’s create our first playbook and name it backup.yml.

```bash
vim backup.yml
```

Let’s begin by defining the play and then understanding what each line accomplishes

```yml
---
- name: backup router configurations
  hosts: routers
  connection: network_cli
  gather_facts: no
```  

 - `---` Let’s us know that the following is a yaml file.
 - `hosts:` routers Defines the host group in your inventory on which this play will run against
 - `name:` backup router configurations This describes our play
 - `gather_facts: no` Tells Ansible to not run something called the setup module. The setup module is useful when targeting computing nodes (Linux, Windows), but not really used when targeting networking devices. We would use the necessary platform_facts module depending on type of nodes we’re targeting.
 - `connection: network_cli` tells Ansible to execute this python module on a network device

###  Step 2: Adding Tasks to Your Play

Now that we’ve defined your play, let’s add the necessary tasks to backup our routers.

Make sure all of your playbook statements are aligned in the way shown here.
If you want to see the entire playbook for reference, skip to the end of Section 4 of this exercise.

{% raw %}
```bash
  tasks:
    - name: gather ios_facts
      ios_facts:
      register: version

    - debug:
        msg: "{{version}}"

    - name: Backup configuration
      ios_config:
        backup: yes
```
{% endraw %}      

 - `tasks:` This denotes that one or more tasks are about to be defined
 - `name:` Each task should be given a name which will print to standard output when you run your playbook. Therefore, give your tasks a name that is short, sweet, and to the point

 The following section is using the ios_facts ansible module to gather IOS related facts. [Click here](http://docs.ansible.com/ansible/latest/ios_facts_module.html) to learn more about the ios_facts module.  The facts (i.e. information) is now available to us to use in subsequent tasks if we wish to do so.  Next, we are making a debug statement to display the output of what information is actually captured when using the ios_facts module so we know what is available to use.

{% raw %}
 ```bash
    - name: gather ios_facts
      ios_facts:
      register: version

    - debug:
        msg: "{{version}}"
```
{% endraw %}

The next three lines are calling the Ansible module ios_config and passing in the parameter backup: yes to capture the configuration of the routers and generate a backup file. Click here to see all options for the ios_config module.

```bash
    - name: Backup configuration
      ios_config:
        backup: yes
```

### Step 3: Review

Now that you’ve completed writing your playbook, it would be a shame not to keep it.  Use the write/quit method in vim to save your playbook, i.e. hit Esc then `:wq!`

[Yaml](http://yaml.org/) can be a bit particular about formatting especially around indentation/spacing.  Take note of the spacing and alignment:
{% raw %}
```
---
- name: backup router configurations
  hosts: routers
  connection: network_cli
  gather_facts: no

  tasks:
    - name: gather ios_facts
      ios_facts:
      register: version

    - debug:
        msg: "{‌{version}}"

    - name: Backup configuration
      ios_config:
        backup: yes
```       
{% endraw %}

### Step 4: Run the playbook

To run the playbook use the **ansible-playbook** command.

```bash
ansible-playbook backup.yml
```
In standard output, you should see something that looks similar to the following:
![Figure 2: backup playbook stdout](playbook-output.png)

#### Ansible Tip
 Want to test a playbook to see if your syntax is correct before executing it on remote systems?

 Try using `--syntax-check` If you run into any issues with your playbook running properly help find those issues like so:
 ```bash
 ansible-playbook backup.yml --syntax-check
 ```

### Step 5: List the files in the backup directory
You can view the backup files that were created by listing the backup directory.

```bash
ls backup
```

You can also view the contents of the backed up configuration files:
```bash
less backup/rtr1*
```
or

```bash
less backup/rtr2*
```

 ---
[Click Here to return to the Ansible Linklight - Networking Workshop](../README.md)
