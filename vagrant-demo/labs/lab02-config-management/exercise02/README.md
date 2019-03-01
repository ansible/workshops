# Exercise 2 - Backing up the router configuration

In this scenario,  you will create a playbook to back-up Arista router configurations. In subsequent labs we will use this backed up configuration, to restore devices to their known good state.

> Note: Since this is a common day 2 operation for most network teams, you can pretty much re-use most of this content for your environment with minimum changes.

#### Step 1

Create a new file called `backup.yml` using your favorite text editor and add the following play definition:

``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: network
  gather_facts: no

```

#### Step 2

Use the `eos_config` Ansible module to write a new task. This task should back up the configuration of all devices defined in `network` group.

The `backup` parameter automatically creates a directory called `backup` within the playbook root and saves a time-stamped backup of the running configuration.

> Note: Use **ansible-doc eos_config** or check out **docs.ansible.com** for help on the module usage.


``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: network
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      eos_config:
        backup: yes
      register: config_output
```


Why are we capturing the output of this task into a variable called `config_output`? **Step 5** will reveal this.


#### Step 3

Go ahead and run the playbook:

```
[vagrant@ansible linklight]$ ansible-playbook backup.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] **********************************************************************************************************************************************

TASK [BACKUP THE CONFIG] *********************************************************************************************************************************************************
ok: [spine02]
ok: [spine01]
ok: [leaf02]
ok: [leaf01]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=1    changed=0    unreachable=0    failed=0
leaf02                     : ok=1    changed=0    unreachable=0    failed=0
spine01                    : ok=1    changed=0    unreachable=0    failed=0
spine02                    : ok=1    changed=0    unreachable=0    failed=0
```


#### Step 4

The playbook should now have created a directory called `backup`. Now, list the contents of this directory:


```
[vagrant@ansible linklight]$ ls -l backup
total 16
-rw-rw-r-- 1 vagrant vagrant 1356 Jun 22 03:03 leaf01_config.2018-06-22@03:03:58
-rw-rw-r-- 1 vagrant vagrant 1340 Jun 22 03:03 leaf02_config.2018-06-22@03:03:57
-rw-rw-r-- 1 vagrant vagrant 1297 Jun 22 03:03 spine01_config.2018-06-22@03:03:57
-rw-rw-r-- 1 vagrant vagrant 1297 Jun 22 03:03 spine02_config.2018-06-22@03:03:57
```

Feel free to open up these files using a text editor (`vim` & `nano` work as well) to validate their content.

#### Step 5

Since we will be using the backed up configurations as a source to restore the configuration. Let's rename them to reflect the device name.

In **Step 2** you captured the output of the task into a variable called `config_output`. This variable contains the name of the backup file. Use the `copy` Ansible module to make a copy of this file.

``` yaml
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: network
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      eos_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"
```


#### Step 6

Re-run the playbook.

```
[vagrant@ansible linklight]$ ansible-playbook backup.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] **********************************************************************************************************************************************

TASK [BACKUP THE CONFIG] *********************************************************************************************************************************************************
ok: [spine01]
ok: [spine02]
ok: [leaf02]
ok: [leaf01]

TASK [RENAME BACKUP] *************************************************************************************************************************************************************
changed: [spine01]
changed: [leaf02]
changed: [spine02]
changed: [leaf01]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=2    changed=1    unreachable=0    failed=0
leaf02                     : ok=2    changed=1    unreachable=0    failed=0
spine01                    : ok=2    changed=1    unreachable=0    failed=0
spine02                    : ok=2    changed=1    unreachable=0    failed=0
```

#### Step 7

Once again list the contents of the `backup` directory:

```
[vagrant@ansible linklight]$ ls -l backup
total 32
-rw-rw-r-- 1 vagrant vagrant 1356 Jun 22 03:05 leaf01.config
-rw-rw-r-- 1 vagrant vagrant 1356 Jun 22 03:05 leaf01_config.2018-06-22@03:05:37
-rw-rw-r-- 1 vagrant vagrant 1340 Jun 22 03:05 leaf02.config
-rw-rw-r-- 1 vagrant vagrant 1340 Jun 22 03:05 leaf02_config.2018-06-22@03:05:36
-rw-rw-r-- 1 vagrant vagrant 1297 Jun 22 03:05 spine01.config
-rw-rw-r-- 1 vagrant vagrant 1297 Jun 22 03:05 spine01_config.2018-06-22@03:05:36
-rw-rw-r-- 1 vagrant vagrant 1297 Jun 22 03:05 spine02.config
-rw-rw-r-- 1 vagrant vagrant 1297 Jun 22 03:05 spine02_config.2018-06-22@03:05:36
```

Notice that the directory now has another backed-up configuration but one that reflects the device's name.

## Complete
You have completed Exercise 02.

[Return to training-course](../README.md)
