# Exercise 1 - Updating the configurations using Ansible

Using Ansible you can update the configuration of switches either by pushing a configuration file to the device or you can push configuration lines directly to the device.

#### Step 1

Create a new file called `configs.yml` (use either `vim` or `nano` on the jumphost to do this or use a local editor on your laptop and copy the contents to the jumphost later). Add the following play definition to it:


``` yaml
---
- name: SNMP RO/RW STRING CONFIGURATION
  hosts: network
  gather_facts: no
```

#### Step 2

Add a task to ensure that the SNMP strings `ansible-public` and `ansible-private` are present on all the switches. Use the `eos_config` module for this task

> Note: For help on the **eos_config** module, use the **ansible-doc eos_config** command from the command line or check docs.ansible.com. This will list all possible options with usage examples.


``` yaml
---
- name: SNMP RO/RW STRING CONFIGURATION
  hosts: network
  gather_facts: no

  tasks:
    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      eos_config:
        commands:
          - snmp-server community ansible-public ro
          - snmp-server community ansible-private rw
```

#### Step 3

Run the playbook:

```[vagrant@ansible linklight]$ ansible-playbook configs.yml

PLAY [SNMP RO/RW STRING CONFIGURATION] *******************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] **************************************************************************************************************************
changed: [spine01]
changed: [leaf01]
changed: [spine02]
changed: [leaf02]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=1    changed=1    unreachable=0    failed=0
leaf02                     : ok=1    changed=1    unreachable=0    failed=0
spine01                    : ok=1    changed=1    unreachable=0    failed=0
spine02                    : ok=1    changed=1    unreachable=0    failed=0
```

Feel free to log in and check the configuration update.


#### Step 4

The `eos_config` module is idempotent. This means, a configuration change is  pushed to the device if and only if that configuration does not exist on the end hosts. To validate this, go ahead and re-run the playbook:


```
[vagrant@ansible linklight]$ ansible-playbook configs.yml

PLAY [SNMP RO/RW STRING CONFIGURATION] *******************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] **************************************************************************************************************************
ok: [spine01]
ok: [leaf02]
ok: [leaf01]
ok: [spine02]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=1    changed=0    unreachable=0    failed=0
leaf02                     : ok=1    changed=0    unreachable=0    failed=0
spine01                    : ok=1    changed=0    unreachable=0    failed=0
spine02                    : ok=1    changed=0    unreachable=0    failed=0
```

> Note: See that the **changed** parameter in the **PLAY RECAP** indicates 0 changes.


#### Step 5

Now update the task to add one more SNMP RO community string:


``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: network
  gather_facts: no

  tasks:
    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      eos_config:
        commands:
          - snmp-server community ansible-public ro
          - snmp-server community ansible-private rw
          - snmp-server community ansible-test ro
```

#### Step 6

This time however, instead of running the playbook to push the change to the device, execute it using the `--check` flag in combination with the `-v` or verbose mode flag:


```
[vagrant@ansible linklight]$ ansible-playbook configs.yml --check -v
Using /home/vagrant/.ansible.cfg as config file

PLAY [UPDATE THE SNMP RO/RW STRINGS] *********************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] **************************************************************************************************************************
changed: [spine01] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1529602311", "updates": ["snmp-server community ansible-test ro"]}
changed: [leaf01] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1529602311", "updates": ["snmp-server community ansible-test ro"]}
changed: [spine02] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1529602311", "updates": ["snmp-server community ansible-test ro"]}
changed: [leaf02] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1529602312", "updates": ["snmp-server community ansible-test ro"]}

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=1    changed=1    unreachable=0    failed=0
leaf02                     : ok=1    changed=1    unreachable=0    failed=0
spine01                    : ok=1    changed=1    unreachable=0    failed=0
spine02                    : ok=1    changed=1    unreachable=0    failed=0
```

The `--check` mode in combination with the `-v` flag will display the exact changes that will be deployed to the end device without actually pushing the change. This is a great technique to validate the changes you are about to push to a device before pushing it.

> Go ahead and log into a couple of devices to validate that the change has not been pushed.

Also note that even though 3 commands are being sent to the device as part of the task, only the one command that is missing on the devices will be pushed.

#### Step 7

Finally re-run this playbook again without the `-v` or `--check` flag to push the changes.

```
[vagrant@ansible linklight]$ ansible-playbook configs.yml

PLAY [UPDATE THE SNMP RO/RW STRINGS] *********************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] **************************************************************************************************************************
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


#### Step 8

Rather than push individual lines of configuration, an entire configuration snippet can be pushed to the devices. Create a file called `system.cfg` in the same directory as your playbook and add the following lines of configuration into it:

``` shell
ip name-server vrf default 8.8.4.4
ip name-server vrf default 8.8.8.8
ip domain-name ansible.com
ntp server time.google.com
```


#### Step 9

Remember that a playbook contains a list of plays. Add a new play called `CONFIGURE SYSTEM SERVICES` to the `config.yml` playbook.

``` yaml

---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: network
  gather_facts: no

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      eos_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO


- name: CONFIGURE SYSTEM SERVICES
  hosts: network
  gather_facts: no
```

#### Step 10

Add a task to this new play to push the configurations in the `system.cfg` file you created in **STEP 8**


``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: network
  gather_facts: no

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      eos_config:
        commands:
          - snmp-server community ansible-public ro
          - snmp-server community ansible-private rw
          - snmp-server community ansible-test ro


- name: CONFIGURE SYSTEM SERVICES
  hosts: network
  gather_facts: no

  tasks:

    - name: LOAD THE SYSTEM CFG FILE
      eos_config:
        src: system.cfg
```


#### Step 11

Go ahead and run the playbook.  Output below is from a subsequent run, instead of OK, your first run will contain CHANGED.

``` [vagrant@ansible linklight]$ ansible-playbook configs.yml

PLAY [UPDATE THE SNMP RO/RW STRINGS] *********************************************************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] **************************************************************************************************************************
ok: [leaf01]
ok: [spine01]
ok: [spine02]
ok: [leaf02]

PLAY [CONFIGURE SYSTEM SERVICES] *************************************************************************************************************************************************

TASK [LOAD THE SYSTEM CFG FILE] **************************************************************************************************************************************************
ok: [spine02]
ok: [leaf01]
ok: [spine01]
ok: [leaf02]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=2    changed=0    unreachable=0    failed=0
leaf02                     : ok=2    changed=0    unreachable=0    failed=0
spine01                    : ok=2    changed=0    unreachable=0    failed=0
spine02                    : ok=2    changed=0    unreachable=0    failed=0
```

## Complete
You have completed Exercise 01.

[Return to training-course](../README.md)
