# Supplemental Exercise: Ansible Network Resource Modules

**Read this in other languages**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md)

## Table of Contents

  * [Objective](#objective)
    * [Step 1 - Manually modify the Arista configuration](#step-1---manually-modify-the-arista-configuration)
    * [Step 2 - Run the playbook](#step-2---run-the-playbook)
    * [Step 3 - Modify the playbook](#step-3---modify-the-playbook)
    * [Step 4 - Run replaced playbook](#step-4---run-replaced-playbook)
    * [Step 5 - Add a VLAN to rtr2](#step-5---add-a-vlan-to-rtr2)
    * [Step 6 - Use overridden parameter](#step-6---use-overridden-parameter)
    * [Step 7 - using rendered parameter](#step-7---using-rendered-parameter)
    * [Step 8 - Using the parsed parameter](#step-8---using-the-parsed-parameter)
  * [Takeaways](#takeaways)
  * [Solution](#solution)
  * [Complete](#complete)

## Objective

Demonstration use of [Ansible Network Resource Modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)

This exercise builds upon [exercise 4 - Ansible Network Resource Modules](../../4-resource-module/).  Please complete that exercise before starting this one.

There are two parts to this exercise:

1.  Cover additional configuration `state` parameters:

  * `replaced`
  * `overridden`

  and contrast them to what we saw with `merged`.

2. Cover additional read-only `state` parameters

  * `rendered`
  * `parsed`

  and contrast them to the `gathered` parameter.

### Step 1 - Manually modify the Arista configuration

* Login to an Arista switch.  We are assuming the configuration from exercise 4 is already applied

  ```bash
  vlan 20
     name desktops
  !
  vlan 30
     name servers
  !
  vlan 40
     name printers
  !
  vlan 50
     name DMZ
  ```

* From the control node terminal, you can `ssh rtr2` and type `enable`

  ```bash
  $ ssh rtr2
  Last login: Wed Sep  1 13:44:55 2021 from 44.192.105.112
  rtr2>enable
  ```

* Use the command `configure terminal` to manually edit the Arista configuration:

  ```bash
  rtr2#configure terminal
  rtr2(config)#
  ```
* Now configure vlan 50 to `state suspend`

  ```bash
  rtr2(config)#vlan 50
  rtr2(config-vlan-50)#state ?
    active   VLAN Active State
    suspend  VLAN Suspended State

  rtr2(config-vlan-50)#state suspend
  ```

* Save the configuration

  ```bash
  rtr2(config-vlan-50)#exit
  rtr2(config)#end
  rtr2#copy running-config startup-config
  Copy completed successfully.
  ```

* Examine the configuration

  ```bash
  rtr2#sh run | s vlan
  vlan 20
     name desktops
  !
  vlan 30
     name servers
  !
  vlan 40
     name printers
  !
  vlan 50
     name DMZ
     state suspend
  ```

  * The running-configuration no longer matches our playbook!  vlan 50 is now in state suspend.

### Step 2 - Run the playbook

* Execute the playbook using the `ansible-navigator run`.

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* The output will look similar to the following:

  ```bash
  [student1@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4]
  ok: [rtr2]

  PLAY RECAP *********************************************************************
  rtr2                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
  ```

* The playbook did **NOT** modify the configuration.  The `state: merged` only enforces that the config provided exists on the network device.  Lets contrast this to `replaced`.  If you login to the Arista network device the `state: suspend` will still be there.

### Step 3 - Modify the playbook

* Modify the `resource.yml` playbook so that `state: merged` is now `state: replaced`

* The playbook should look like the following:

  ```yaml
  ---
  - name: configure VLANs
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: replaced
        config:
          - name: desktops
            vlan_id: 20
          - name: servers
            vlan_id: 30
          - name: printers
            vlan_id: 40
          - name: DMZ
            vlan_id: 50
  ```

### Step 4 - Run replaced playbook

* Execute the playbook using the `ansible-navigator run`.  Since there is just one task we can use the `--mode stdout`

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* The output will look similar to the following:

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  changed: [rtr4]
  changed: [rtr2]

  PLAY RECAP *********************************************************************
  rtr2                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```
* Now examine the config on rtr2, the `state: suspend` is now gone.  Replaced will enforce (for the specified VLANs) the supplied configurations.  This means that since `state: suspend` was not supplied, and NOT the default for a VLAN, it will remove it from the network device.

### Step 5 - Add a VLAN to rtr2

* Create vlan 100 on `rtr2`

  ```bash
  rtr2(config)#vlan 100
  rtr2(config-vlan-100)#name ?
    WORD  The ASCII name for the VLAN
  rtr2(config-vlan-100)#name artisanal
  ```

*  We can assume that someone has created this VLAN outside of automation (e.g. they hand-crafted a VLAN i.e. artisanal VLAN)  This is referred to as "out of band" network changes.  This is very common in the network industry because a network engineer solved a problem, but then never documented or circled back to remove this configuration.  This manual cofiguration change does not match best practices or their documented policy.  This could cause issues where someone tries to use this VLAN in the future, and not aware of this configuration.

  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active   
  20    desktops                         active   
  30    servers                          active   
  40    printers                         active   
  50    DMZ                              active   
  100   artisanal                        active   
  ```

* Re-run the playbook again.  The VLAN 100 is NOT removed.

### Step 6 - Use overridden parameter

* Modify the playbook again, this time using the `state: overridden`

    ```yaml
    ---
    - name: configure VLANs
      hosts: arista
      gather_facts: false

      tasks:

      - name: use vlans resource module
        arista.eos.vlans:
          state: overridden
          config:
            - name: desktops
              vlan_id: 20
            - name: servers
              vlan_id: 30
            - name: printers
              vlan_id: 40
            - name: DMZ
              vlan_id: 50
    ```
* Execute the playbook using the `ansible-navigator run`.

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```
* Login back into the `rtr2` device and examine the VLANs
  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active   
  20    desktops                         active   
  30    servers                          active   
  40    printers                         active   
  50    DMZ                              active
  ```

* The artisanal VLAN 100 has been removed!  Now the same resource modules can be used to not only configure network devices, but enforce which VLANs are configured.  This is referred to as policy enforcement, and a huge part of configuration management.  Going from `merged` to `replaced` to `overridden` will often match the automation journey for a network team as they gain more and more confidence with automation.

### Step 7 - using rendered parameter

Now lets return to using read-only parameters.  These parameters do not modify the configuration on a network device.  In exercise 4, we used the `state: gathered` to retrieve the VLAN configuration from the Arista network device.  This time we will use `rendered` to get the Arista commands that generate the configuration:

* Modify the `resource.yml` playbook to `state: rendered`

* Register the output from the task to a variable named `rendered_config`

* Add a `debug` task to print the output to the terminal window

* The playbook will look like the following:

  ```yaml
  - name: use vlans resource module
    arista.eos.vlans:
      state: rendered
      config:
        - name: desktops
          vlan_id: 20
        - name: servers
          vlan_id: 30
        - name: printers
          vlan_id: 40
        - name: DMZ
          vlan_id: 50
    register: rendered_config

  - name: use vlans resource module
    debug:
      msg: "{{ rendered_config }}"
  ```

* Execute the playbook using the `ansible-navigator run`.

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

* The output will look like the following:

  ```bash
  [student1@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr2]
  ok: [rtr4]

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "rendered": [
              "vlan 20",
              "name desktops",
              "vlan 30",
              "name servers",
              "vlan 40",
              "name printers",
              "vlan 50",
              "name DMZ"
          ]
      }
  }
  ok: [rtr2] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "rendered": [
              "vlan 20",
              "name desktops",
              "vlan 30",
              "name servers",
              "vlan 40",
              "name printers",
              "vlan 50",
              "name DMZ"
          ]
      }
  }

  PLAY RECAP *********************************************************************
  rtr2                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```

* Specifically the `rendered` key will display the Arista commands that are used to generate the configuration!  This allows network automators to know exactly what commands would be run and executed before they actually run automation to apply the commands.

### Step 8 - Using the parsed parameter

Finally lets cover the parsed parameter.  This parameter is used when a existing file contains the network device configuration.  Imagine there was already a backup performed.

* First lets backup a configuration.  Here is a simple playbook for doing a configuration backup.  The playbook is [backup.yml](backup.yml).

  ```yaml
  ---
  - name: backup config
    hosts: arista
    gather_facts: false

    tasks:

    - name: retrieve backup
      arista.eos.config:
        backup: true
        backup_options:
          filename: "{{ inventory_hostname }}.txt"
  ```

* Execute the playbook:

  ```bash
  $ ansible-navigator run backup.yml --mode stdout
  ```

* Verify the backups were created:

  ```bash
  $ ls backup
  rtr2.txt  rtr4.txt
  ```

* Now modify the `resource.yml` playbook to use the `parsed` playbook:

  ```yaml
  ---
  - name: use parsed
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: parsed
        running_config: "{{ lookup('file', 'backup/{{ inventory_hostname }}.txt') }}"
      register: parsed_config

    - name: print to terminal screen
      debug:
        msg: "{{ parsed_config }}"
  ```

* There is a couple additional changes:

  * instead of `config` we are using `running-config` and pointing to the backup file.
  * We are registering the output from the module to `parsed_config` varaible
  * We are using the debug module to print the `parsed_config` variable

* Execute the playbook:

    ```bash
    $ ansible-navigator run resource.yml --mode stdout
    ```

* The output will look like the following:

  ```yaml
  [student1@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [use parsed] **************************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4]
  ok: [rtr2]

  TASK [print to terminal screen] ************************************************
  ok: [rtr2] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "parsed": [
              {
                  "name": "desktops",
                  "state": "active",
                  "vlan_id": 20
              },
              {
                  "name": "servers",
                  "state": "active",
                  "vlan_id": 30
              },
              {
                  "name": "printers",
                  "state": "active",
                  "vlan_id": 40
              },
              {
                  "name": "DMZ",
                  "state": "active",
                  "vlan_id": 50
              }
          ]
      }
  }
  ok: [rtr4] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "parsed": [
              {
                  "name": "desktops",
                  "state": "active",
                  "vlan_id": 20
              },
              {
                  "name": "servers",
                  "state": "active",
                  "vlan_id": 30
              },
              {
                  "name": "printers",
                  "state": "active",
                  "vlan_id": 40
              },
              {
                  "name": "DMZ",
                  "state": "active",
                  "vlan_id": 50
              }
          ]
      }
  }

  PLAY RECAP *********************************************************************
  rtr2                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```

* In the output above you will see that the flat-file backup was parsed into structured data:

  ```json
  "parsed": [
      {
          "name": "desktops",
          "state": "active",
          "vlan_id": 20
      }
  ```

* The default output is JSON but can be easily transformed into YAML.

## Takeaways

We covered two additional configuration `state` parameters:

  * `replaced` - enforced config for specified VLANs
  * `overridden`- enforced config for ALL vlans

Going from `merged` to `replaced` to `overridden` follows the automation adoption journey as network teams gain more confidence with automation.  

We covered additional read-only `state` parameters

  * `rendered` - shows commands that would generate the desired configuration
  * `parsed` - turned a flat-file configuration (such as a backup) into structured data (versus modifying the actual device)

These allow network automators to use resource modules in additional scenarios, such as disconnected environments. Network resource modules provide a consistent experience across different network devices.

The [documentation guide](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html) provided additional info of using network resource modules.

## Solution

The finished Ansible Playbook is provided here for an answer key:

-  [overridden.yml](overridden.yml)
-  [backup.yml](backup.yml)
-  [parsed.yml](parsed.yml)


## Complete

You have completed the supplemental lab!


---
[Click here to return to supplemental exercises](../README.md)

[Click here to return to the Ansible Network Automation Workshop](../../README.md)
