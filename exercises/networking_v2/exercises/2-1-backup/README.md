# Exercise 2.1 - Backing up the router configuration


In this realistic scenario,  you will create a playbook to back-up Cisco router configurations. In subsequent labs we will use this backed up configuration, to restore devices to their known good state.

> Note: Since this is a common day 2 operation for most network teams, you can pretty much re-use most of this content for your environment with minimum changes.

#### Step 1

Create a new file called `backup.yml` using your favorite text editor and add the following play definition:

``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

```

#### Step 2

Use the `ios_config` Ansible module to write a new task. This task should back up the configuration of all devices defined in `cisco` group.

The `backup` parameter automatically creates a directory called `backup` within the playbook root and saves a time-stamped backup of the running configuration.

> Note: Use **ansible-doc ios_config** or check out **docs.ansible.com** for help on the module usage.


``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      ios_config:
        backup: yes
      register: config_output
```


Why are we capturing the output of this task into a variable called `config_output`? **Step 5** will reveal this.


#### Step 3

Go ahead and run the playbook:

``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] *********************************************************************************************************************************************************

TASK [BACKUP THE CONFIG] ********************************************************************************************************************************************************************
ok: [rtr1]
ok: [rtr3]
ok: [rtr4]
ok: [rtr2]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0   
rtr2                       : ok=1    changed=0    unreachable=0    failed=0   
rtr3                       : ok=1    changed=0    unreachable=0    failed=0   
rtr4                       : ok=1    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```


#### Step 4

The playbook should now have created a directory called `backup`. Now, list the contents of this directory:


``` shell
[student1@ansible networking-workshop]$ ls -l backup
total 1544
-rw-rw-r--. 1 student1 student1 393514 Jun 19 12:45 rtr1_config.2018-06-19@12:45:36
-rw-rw-r--. 1 student1 student1 393513 Jun 19 12:45 rtr2_config.2018-06-19@12:45:38
-rw-rw-r--. 1 student1 student1 390584 Jun 19 12:45 rtr3_config.2018-06-19@12:45:37
-rw-rw-r--. 1 student1 student1 390586 Jun 19 12:45 rtr4_config.2018-06-19@12:45:37
[student1@ansible networking-workshop]$

```

Feel free to open up these files using a text editor (`vim` & `nano` work as well) to validate their content.

#### Step 5

Since we will be using the backed up configurations as a source to restore the configuration. Let's rename them to reflect the device name.

In **Step 2** you captured the output of the task into a variable called `config_output`. This variable contains the name of the backup file. Use the `copy` Ansible module to make a copy of this file.



``` yaml
{%raw%}
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      ios_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"
{%endraw%}
```


#### Step 6

Re-run the playbook.



``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] *********************************************************************************************************************************************************

TASK [BACKUP THE CONFIG] ********************************************************************************************************************************************************************
ok: [rtr3]
ok: [rtr4]
ok: [rtr2]
ok: [rtr1]

TASK [RENAME BACKUP] ************************************************************************************************************************************************************************
changed: [rtr1]
changed: [rtr4]
changed: [rtr2]
changed: [rtr3]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=2    changed=1    unreachable=0    failed=0   
rtr2                       : ok=2    changed=1    unreachable=0    failed=0   
rtr3                       : ok=2    changed=1    unreachable=0    failed=0   
rtr4                       : ok=2    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```

#### Step 7

Once again list the contents of the `backup` directory:

``` shell
[student1@ansible networking-workshop]$ ls -l backup
total 3088
-rw-rw-r--. 1 student1 student1 393514 Jun 19 13:35 rtr1.config
-rw-rw-r--. 1 student1 student1 393514 Jun 19 13:35 rtr1_config.2018-06-19@13:35:14
-rw-rw-r--. 1 student1 student1 393513 Jun 19 13:35 rtr2.config
-rw-rw-r--. 1 student1 student1 393513 Jun 19 13:35 rtr2_config.2018-06-19@13:35:13
-rw-rw-r--. 1 student1 student1 390584 Jun 19 13:35 rtr3.config
-rw-rw-r--. 1 student1 student1 390584 Jun 19 13:35 rtr3_config.2018-06-19@13:35:12
-rw-rw-r--. 1 student1 student1 390586 Jun 19 13:35 rtr4.config
-rw-rw-r--. 1 student1 student1 390586 Jun 19 13:35 rtr4_config.2018-06-19@13:35:13
[student1@ansible networking-workshop]$

```

Notice that the directory now has another backed-up configuration but one that reflects the device's name.



#### Step 8

If we were to try and manually restore the contents of this file to the respective device there are two lines in the configuration that will raise errors:

``` shell
Building configuration...

Current configuration with default configurations exposed : 393416 bytes

```
These lines have to be "cleaned up" to have a restorable configuration.

Write a new task using Ansible's `lineinfile` module to remove the first line.


``` yaml
{%raw%}
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      ios_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"

    - name: REMOVE NON CONFIG LINES
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        line: "Building configuration..."
        state: absent
{%endraw%}
```


> Note: The module parameter **line** is matching an exact line in the configuration file "Building configuration..."


#### Step 9

Before we run the playbook, we need to add one more task to remove the second line "Current configuration ...etc". Since this line has a variable entity (the number of bytes), we cannot use the `line` parameter of the `lineinfile` module. Instead, we'll use the `regexp` parameter to match on regular expressions and remove the line in the file:


``` yaml
{%raw%}
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: cisco
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      ios_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"

    - name: REMOVE NON CONFIG LINES
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        line: "Building configuration..."
        state: absent

    - name: REMOVE NON CONFIG LINES - REGEXP
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        regexp: 'Current configuration.*'
        state: absent
{%endraw%}                          
```


#### Step 10

Now run the playbook.


``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] *********************************************************************************************************************************************************

TASK [BACKUP THE CONFIG] ********************************************************************************************************************************************************************
ok: [rtr2]
ok: [rtr4]
ok: [rtr1]
ok: [rtr3]

TASK [RENAME BACKUP] ************************************************************************************************************************************************************************
changed: [rtr2]
changed: [rtr4]
changed: [rtr3]
changed: [rtr1]

TASK [REMOVE NON CONFIG LINES] **************************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr1]
changed: [rtr2]
changed: [rtr3]

TASK [REMOVE NON CONFIG LINES - REGEXP] *****************************************************************************************************************************************************
changed: [rtr1]
changed: [rtr3]
changed: [rtr2]
changed: [rtr4]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=4    changed=3    unreachable=0    failed=0   
rtr2                       : ok=4    changed=3    unreachable=0    failed=0   
rtr3                       : ok=4    changed=3    unreachable=0    failed=0   
rtr4                       : ok=4    changed=3    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```


#### Step 11

Use an editor to view the cleaned up files. The first 2 lines that we cleaned up in the earlier tasks should be absent:

``` shell
[student1@ansible networking-workshop]$ head -n 10 backup/rtr1.config

!
! Last configuration change at 14:25:42 UTC Tue Jun 19 2018 by ec2-user
!
version 16.8
downward-compatible-config 16.8
no service log backtrace
no service config
no service exec-callback
no service nagle
[student1@ansible networking-workshop]$

```

> Note: The **head** unix command will display the first N lines specified as an argument.

# Complete

You have completed lab exercise 2.1

---
[Click Here to return to the Ansible Linklight - Networking Workshop](../../README.md)
