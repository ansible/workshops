# Exercise 3 - Using Ansible to restore the backed up configuration

In the previous lab you learned how to backup the configuration of the 4 Arista switches. In this lab you will learn how to restore the configuration. The backups had been saved into a local directory called `backup`.

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

Our objective is to apply this "last known good configuraion backup" to the switches.

#### Step 1

On one of the switches (`leaf01`) manually make a change. For instance add a new loopback interface.

Log into `leaf01` and add the following:

```
leaf01#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
leaf01(config)#inter
leaf01(config)#interface loo
leaf01(config)#interface loopback 101
leaf01(config-if)#ip address 169.1.1.1 255.255.255.255
leaf01(config-if)#end
leaf01#

```

Now verify the newly created Loopback Interface

```
leaf01#sh run interface loopback 101
interface Loopback101
   ip address 169.1.1.1/32
```

#### Step 2

Step 1 simulates our "Out of process/band" changes on the network. This change needs to be reverted. So let's write a new playbook to apply the backup we collected from our previous lab to achieve this.

Create a file called `restore_config.yml` using your favorite text editor and add the following play definition:

```
---
- name: BACKUP ROUTER CONFIGURATIONS
  hosts: network
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      eos_config:
        replace: config
        src: "{{playbook_dir}}/backup/{{inventory_hostname}}.config"
```

#### Step 3

Go ahead and run the playbook.

```
[vagrant@ansible linklight]$ ansible-playbook restore.yml

PLAY [BACKUP ROUTER CONFIGURATIONS] **********************************************************************************************************************************************

TASK [BACKUP THE CONFIG] *********************************************************************************************************************************************************
changed: [spine02]
changed: [spine01]
changed: [leaf01]
changed: [leaf02]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=1    changed=1    unreachable=0    failed=0
leaf02                     : ok=1    changed=1    unreachable=0    failed=0
spine01                    : ok=1    changed=1    unreachable=0    failed=0
spine02                    : ok=1    changed=1    unreachable=0    failed=0
```

#### Step 4

Validate that the new loopback interface we added in **Step 1**  is no longer on the device.

```
[vagrant@ansible linklight]$ ssh admin@leaf01


leaf01#sh ip int br
Interface              IP Address         Status     Protocol         MTU
Ethernet1              192.168.0.14/24    up         up              1500
Management1            10.0.2.15/24       up         up              1500
leaf01#sh run int lo101
```

You have successfully backed up and restored configurations on your Arista switches!

## Complete
You have completed Exercise 03.

[Return to training-course](../README.md)
