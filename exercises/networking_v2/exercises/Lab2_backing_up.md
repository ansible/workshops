# Lab 2 - Using Ansible to update and  back up router configurations

## Scenario 1 - Updating the router configurations using Ansible

Using Ansible you can update the configuration of routers either by pushing a configuration file to the device or you can push configuration lines directly to the device.

#### Step 1

Create a new file called `router_configs.yml` (use either `vim` or `nano` on the jumphost to do this or use a local editor on your laptop and copy the contents to the jumphost later). Add the following play definition to it:


``` yaml
---
- name: SNMP RO/RW STRING CONFIGURATION
  hosts: cisco
  gather_facts: no
  connection: network_cli

```

#### Step 2

Add a task to ensure that the SNMP strings `ansible-public` and `ansible-private` are present on all the routers. Use the `ios_config` module for this task

> Note: For help on the **ios_config** module, use the **ansible-doc ios_config** command from the command line or check docs.ansible.com. This will list all possible options with usage examples.


``` yaml

---
- name: SNMP RO/RW STRING CONFIGURATION
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW

```

#### Step 3

Run the playbook:

``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_config.yml

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************
changed: [rtr4]
changed: [rtr1]
changed: [rtr3]
changed: [rtr2]

PLAY RECAP **********************************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0   
rtr2                       : ok=1    changed=1    unreachable=0    failed=0   
rtr3                       : ok=1    changed=1    unreachable=0    failed=0   
rtr4                       : ok=1    changed=1    unreachable=0    failed=0   

[student1@ip-172-16-208-140 networking-workshop]$

```

Feel free to log in and check the configuration update.


#### Step 4

The `ios_config` module is idempotent. This means, a configuration change is  pushed to the device if and only if that configuration does not exist on the end hosts. To validate this, go ahead and re-run the playbook:


``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_config.yml  

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************************************************************************************************
ok: [rtr1]
ok: [rtr2]
ok: [rtr4]
ok: [rtr3]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0   
rtr2                       : ok=1    changed=0    unreachable=0    failed=0   
rtr3                       : ok=1    changed=0    unreachable=0    failed=0   
rtr4                       : ok=1    changed=0    unreachable=0    failed=0   

[student1@ip-172-16-208-140 networking-workshop]$



```

> Note: See that the **changed** parameter in the **PLAY RECAP** indicates 0 changes.


#### Step 5

Now update the task to add one more SNMP RO community string:


``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO

```



#### Step 6

This time however, instead of running the playbook to push the change to the device, execute it using the `--check` flag in combination with the `-v` or verbose mode flag:


``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_config.yml  --check -v
Using /home/student1/.ansible.cfg as config file

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************************************************************************************************
changed: [rtr3] => {"banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"]}
changed: [rtr1] => {"banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"]}
changed: [rtr2] => {"banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"]}
changed: [rtr4] => {"banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"]}

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0   
rtr2                       : ok=1    changed=1    unreachable=0    failed=0   
rtr3                       : ok=1    changed=1    unreachable=0    failed=0   
rtr4                       : ok=1    changed=1    unreachable=0    failed=0   

[student1@ip-172-16-208-140 networking-workshop]$

```

The `--check` mode in combination with the `-v` flag will display the exact changes that will be deployed to the end device without actually pushing the change. This is a great technique to validate the changes you are about to push to a device before pushing it.

> Go ahead and log into a couple of devices to validate that the change has not been pushed.


Also note that even though 3 commands are being sent to the device as part of the task, only the one command that is missing on the devices will be pushed.


#### Step 7

Finally re-run this playbook again without the `-v` or `--check` flag to push the changes.

``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_config.yml  

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************************************************************************************************
changed: [rtr1]
changed: [rtr2]
changed: [rtr4]
changed: [rtr3]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0   
rtr2                       : ok=1    changed=1    unreachable=0    failed=0   
rtr3                       : ok=1    changed=1    unreachable=0    failed=0   
rtr4                       : ok=1    changed=1    unreachable=0    failed=0   

[student1@ip-172-16-208-140 networking-workshop]$
```


#### Step 8

Rather than push individual lines of configuration, an entire configuration snippet can be pushed to the devices. Create a file called `secure_router.cfg` in the same directory as your playbook and add the following lines of configuration into it:

``` shell
line con 0
 exec-timeout 5 0
line vty 0 4
 exec-timeout 5 0
 transport input ssh
ip ssh time-out 60
ip ssh authentication-retries 5
service password-encryption
service tcp-keepalives-in
service tcp-keepalives-out

```


#### Step 9

Remember that a playbook contains a list of plays. Add a new play called `HARDEN IOS ROUTERS` to the `router_config.yml` playbook.

``` yaml

---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO


- name: HARDEN IOS ROUTERS
  hosts: cisco
  gather_facts: no
  connection: network_cli



```

#### Step 10

Add a task to this new play to push the configurations in the `secure_router.cfg` file you created in **STEP 8**


``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO


- name: HARDEN IOS ROUTERS
  hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT ROUTERS ARE SECURE
      ios_config:
        src: secure_router.cfg
```


#### Step 11

Go ahead and run the playbook.

``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts router_config.yml  

PLAY [UPDATE THE SNMP RO/RW STRINGS] ********************************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *************************************************************************************************************************************
ok: [rtr3]
ok: [rtr2]
ok: [rtr1]
ok: [rtr4]

PLAY [HARDEN IOS ROUTERS] *******************************************************************************************************************************************************************

TASK [ENSURE THAT ROUTERS ARE SECURE] *******************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr3]
changed: [rtr2]
changed: [rtr1]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=2    changed=1    unreachable=0    failed=0   
rtr2                       : ok=2    changed=1    unreachable=0    failed=0   
rtr3                       : ok=2    changed=1    unreachable=0    failed=0   
rtr4                       : ok=2    changed=1    unreachable=0    failed=0   

[student1@ip-172-16-208-140 networking-workshop]$

```




## Scenario 2 - Backing up the router configuration


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
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

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

[student1@ip-172-16-208-140 networking-workshop]$

```


#### Step 4

The playbook should now have created a directory called `backup`. Now, list the contents of this directory:


``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ls -l backup
total 1544
-rw-rw-r--. 1 student1 student1 393514 Jun 19 12:45 rtr1_config.2018-06-19@12:45:36
-rw-rw-r--. 1 student1 student1 393513 Jun 19 12:45 rtr2_config.2018-06-19@12:45:38
-rw-rw-r--. 1 student1 student1 390584 Jun 19 12:45 rtr3_config.2018-06-19@12:45:37
-rw-rw-r--. 1 student1 student1 390586 Jun 19 12:45 rtr4_config.2018-06-19@12:45:37
[student1@ip-172-16-208-140 networking-workshop]$

```

Feel free to open up these files using a text editor (`vim` & `nano` work as well) to validate their content.

#### Step 5

Since we will be using the backed up configurations as a source to restore the configuration. Let's rename them to reflect the device name.

In **Step 2** you captured the output of the task into a variable called `config_output`. This variable contains the name of the backup file. Use the `copy` Ansible module to make a copy of this file.



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

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"

```


#### Step 6

Re-run the playbook.



``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

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

[student1@ip-172-16-208-140 networking-workshop]$

```

#### Step 7

Once again list the contents of the `backup` directory:

``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ls -l backup
total 3088
-rw-rw-r--. 1 student1 student1 393514 Jun 19 13:35 rtr1.config
-rw-rw-r--. 1 student1 student1 393514 Jun 19 13:35 rtr1_config.2018-06-19@13:35:14
-rw-rw-r--. 1 student1 student1 393513 Jun 19 13:35 rtr2.config
-rw-rw-r--. 1 student1 student1 393513 Jun 19 13:35 rtr2_config.2018-06-19@13:35:13
-rw-rw-r--. 1 student1 student1 390584 Jun 19 13:35 rtr3.config
-rw-rw-r--. 1 student1 student1 390584 Jun 19 13:35 rtr3_config.2018-06-19@13:35:12
-rw-rw-r--. 1 student1 student1 390586 Jun 19 13:35 rtr4.config
-rw-rw-r--. 1 student1 student1 390586 Jun 19 13:35 rtr4_config.2018-06-19@13:35:13
[student1@ip-172-16-208-140 networking-workshop]$

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

```


> Note: The module parameter **line** is matching an exact line in the configuration file "Building configuration..."


#### Step 9

Before we run the playbook, we need to add one more task to remove the second line "Current configuration ...etc". Since this line has a variable entity (the number of bytes), we cannot use the `line` parameter of the `lineinfile` module. Instead, we'll use the `regexp` parameter to match on regular expressions and remove the line in the file:


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
~                            
```


#### Step 10

Now run the playbook.


``` shell
[student1@ip-172-16-208-140 networking-workshop]$ ansible-playbook -i lab_inventory/hosts backup.yml

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

[student1@ip-172-16-208-140 networking-workshop]$

```


#### Step 11

Use an editor to view the cleaned up files. The first 2 lines that we cleaned up in the earlier tasks should be absent:

``` shell
[student1@ip-172-16-208-140 networking-workshop]$ head -n 10 backup/rtr1.config

!
! Last configuration change at 14:25:42 UTC Tue Jun 19 2018 by ec2-user
!
version 16.8
downward-compatible-config 16.8
no service log backtrace
no service config
no service exec-callback
no service nagle
[student1@ip-172-16-208-140 networking-workshop]$

```

> Note: The **head** unix command will display the first N lines specified as an argument.
