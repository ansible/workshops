# Exercise 4: Ansible Network Resource Modules - Cisco Example

**Read this in other languages**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md)

## Table of Contents
<!-- TOC titleSize:2 tabSpaces:2 depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 skip:0 title:1 charForUnorderedList:* -->
## Table of Contents

  * [Objective](#objective)
  * [Guide](#guide)
    * [Step 1 - Verify SNMP configuration](#step-1---verify-snmp-configuration)
    * [Step 2 - Creating the Ansible Playbook](#step-2---creating-the-ansible-playbook)
    * [Step 3 - Examine the Ansible Playbook](#step-3---examine-the-ansible-playbook)
    * [Step 4 - Execute the Ansible Playbook](#step-4---execute-the-ansible-playbook)
    * [Step 5 - Verify SNMP configuration](#step-5---verify-snmp-configuration)
    * [Step 6 - Using the gathered parameter](#step-6---using-the-gathered-parameter)
    * [Step 7 - Execute the gathered playbook](#step-7---execute-the-gathered-playbook)
    * [Step 8 - Examine the files](#step-8---examine-the-files)
  * [Takeaways](#takeaways)
  * [Solution](#solution)
  * [Complete](#complete)

## Objective

Demonstration use of [Ansible Network Resource Modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)

Ansible network resource modules simplify and standardize how you manage different network devices. Network devices separate configuration into sections (such as interfaces and VLANs) that apply to a network service.

Network resource modules provide a consistent experience across different network devices.  This means you will get an identical experience across multiple vendors.  For example the **snmp_server** module will work identically for the following modules:

* `arista.eos.snmp_server`
* `cisco.ios.snmp_server`
* `cisco.nxos.snmp_server`
* `cisco.iosxr.snmp_server`
* `junipernetworks.junos.snmp_server`

Configuring [SNMP](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol) on network devices is an extremely common task, and mis-configurations can cause headaches and monitoring issues.  SNMP  configurations also tend to be identical across multiple network switches resulting in a perfect use case for automation.

This exercise will cover:

* Configuring SNMP on Cisco IOS
* Building an Ansible Playbook using the [cisco.ios.snmp_server module](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_snmp_server_module.html#ansible-collections-cisco-ios-ios-snmp-server-module).
* Understanding the `state: merged`
* Understanding the `state: gathered`

## Guide

### Step 1 - Verify SNMP configuration

* Login to an Cisco IOS router and verify the current SNMP configuration.

* From the control node terminal, you can `ssh rtr2` and type `enable`

  ```bash
  [student@ansible-1 ~]$ ssh rtr1


  rtr1#
  ```

* Use the command `show snmp` to examine the SNMP configuration:

  ```bash
  rtr1#show snmp
  %SNMP agent not enabled
  ```

* Use the `show run | s snmp` to examine the SNMP running-configuration on the Cisco device:

  ```bash
  rtr1#sh run | s snmp
  rtr1#
  ```

As you can see in the output above there is no SNMP configuration on the Cisco router.

### Step 2 - Creating the Ansible Playbook

*  Create a new file in Visual Studio Code named `resource.yml`

   ![new file](images/step1_new_file.png)

* Copy the following Ansible Playbook into your `resource.yml`

   ```yaml
  ---
  - name: configure SNMP
    hosts: cisco
    gather_facts: false

    tasks:

      - name: use snmp resource module
        cisco.ios.snmp_server:
          state: merged          
          config:            
            location: 'Durham'
            packet_size: 500
            communities:
              - acl_v4: acl_uq
                name: Durham-community
                rw: true
              - acl_v4: acl_uq
                name: ChapelHill-community
                rw: true                
   ```

### Step 3 - Examine the Ansible Playbook

* First lets examine the first four lines:

  ```yaml
  ---
  - name: configure SNMP
    hosts: cisco
    gather_facts: false
  ```

  * The `---` designates this is a [YAML](https://en.wikipedia.org/wiki/YAML) file which is what we write playbooks in.
  * `name` is the description of what this playbook does.
  * `hosts: cisco` will execute this playbook only on the Cisco network devices.  `cisco` is a [group](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inventory-basics-formats-hosts-and-groups) name.
  * `gather_facts: false` this will disable fact gathering for this play, by default this is turned on.


* For the second part we have one task that uses the `cisco.ios.snmp_server`

  ```yaml
    tasks:

    - name: use snmp resource module
      cisco.ios.snmp_server:
        state: merged
        config:
          location: 'Durham'
          packet_size: 500
          communities:
            - acl_v4: acl_uq
              name: Durham-community
              rw: true
            - acl_v4: acl_uq
              name: ChapelHill-community
              rw: true   
  ```

  * `name:` - just like the play, each task has a description for that particular task
  * `state: merged` - This is the default behavior of resource modules.  This will simply enforce that the supplied configuration exists on the network device.  There is actually seven parameters possible for resource modules:
    * merged
    * replaced
    * overridden
    * deleted
    * rendered
    * gathered
    * parsed

    Only two of these parameters will be covered in this exercise, but additional are available in the [supplemental exercises](../supplemental/README.md).
  * `config:` - this is the supplied SNMP configuration.  It is a list of dictionaries. The most important takeaway is that if the module was change from `cisco.ios.snmp_server` to `junipernetworks.junos.snmp_server` it would work identically.  This allows network engineers to focus on the network (e.g. SNMP configuration) versus the vendor syntax and implementation.

### Step 4 - Execute the Ansible Playbook

* Execute the playbook using the `ansible-navigator run`.  Since there is just one task we can use the `--mode stdout`

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* The output will look similar to the following:

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

  PLAY [configure SNMP] **********************************************************

  TASK [use snmp resource module] ***************************
  changed: [rtr1]

  PLAY RECAP *********************************************************************
  rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

* Re-running the playbook will demonstrate the concept of [idempotency](https://en.wikipedia.org/wiki/Idempotence)

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

  PLAY [configure SNMP] **********************************************************

  TASK [Override commands with provided configuration] ***************************
  ok: [rtr1]

  PLAY RECAP *********************************************************************
  rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

* As you can see in the output, everything will return `ok=1` indiciating that no changes were taken place.

### Step 5 - Verify SNMP configuration

* Login to an Cisco switch and verify the current SNMP configuration.

* From the control node terminal, you can `ssh rtr1`

* Use the command `show snmp` to examine the SNMP configuration:

  ```bash
  rtr1#show snmp
  Chassis: 99SDJQ9I6WK
  Location: Durham
  0 SNMP packets input
      0 Bad SNMP version errors
      0 Unknown community name
      0 Illegal operation for community name supplied
      0 Encoding errors
      0 Number of requested variables
      0 Number of altered variables
      0 Get-request PDUs
      0 Get-next PDUs
      0 Set-request PDUs
      0 Input queue packet drops (Maximum queue size 1000)
  0 SNMP packets output
      0 Too big errors (Maximum packet size 500)
      0 No such name errors
      0 Bad values errors
      0 General errors
      0 Response PDUs
      0 Trap PDUs
  Packets currently in SNMP process input queue: 0
  SNMP global trap: disabled

  SNMP logging: disabled
  ```

* Use the `show run | s snmp` to examine the SNMP running-confgiuration on the Cisco device:

  ```bash
  rtr1#show run | s snmp
  snmp-server community Durham-community RW acl_uq
  snmp-server community ChapelHill-community RW acl_uq
  snmp-server packetsize 500
  snmp-server location Durham
  ```

As you can see, the resource module configured the Cisco IOS-XE network device with the supplied configuration.  There are now two total SNMP communities.

### Step 6 - Using the gathered parameter

* Create a new playbook named `gathered.yml`

<!-- {% raw %} -->

  ```yaml
  ---
  - name: retrieve SNMP config
    hosts: cisco
    gather_facts: false

    tasks:

    - name: use SNMP resource module
      cisco.ios.snmp_server:
        state: gathered
      register: snmp_config

    - name: copy snmp_config to file
      copy:
        content: "{{ snmp_config | to_nice_yaml }}"
        dest: "{{ playbook_dir }}/{{ inventory_hostname }}_snmp.yml"
  ```
  <!-- {% endraw %} -->

* The first task is identical except the `state: merged` has been switched to `gathered`, the `config` is no longer needed since we are reading in the configuration (versus applying it to the network device), and we are using the `register` to save the output from the module into a variable named `snmp_config`

* The second task is copying the `snmp_config` variable to a flat-file.  The double curly brackets denotes that this is a variable.  

*  The `| to_nice_yaml` is a [filter](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html), that will transform the JSON output (default) to YAML.

* The `playbook_dir` and `inventory_hostname` are special variables also referred to as [magic variables](https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html).  The `playbook_dir` simply means the directory we executed the playbook from, and the `inventory_hostname` is the name of the device in our inventory.  This means the file will be saved as `~/network-workshop/rtr1_snmp.yml` for the cisco device(s).

### Step 7 - Execute the gathered playbook

* Execute the playbook using the `ansible-navigator run`.

  ```bash
  $ ansible-navigator run gathered.yml --mode stdout
  ```

* The output will look similar to the following:

  ```bash
  $ ansible-navigator run gathered.yml --mode stdout

  PLAY [retrieve SNMP config] ****************************************************

  TASK [use SNMP resource module] ************************************************
  ok: [rtr1]

  TASK [copy snmp_config to file] ************************************************
  changed: [rtr1]

  PLAY RECAP *********************************************************************
  rtr1                       : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

### Step 8 - Examine the files

* Open the newly created files that `gathered` the SNMP configuration from the Cisco network device(s).

* The files were stored under the device name, for example for rtr1: `~/network-workshop/rtr1_snmp.yml.

```bash
  $ cat rtr1_snmp.yml
  changed: false
  failed: false
  gathered:
      communities:
      -   acl_v4: acl_uq
          name: ChapelHill-community
          rw: true
      -   acl_v4: acl_uq
          name: Durham-community
          rw: true
      location: Durham
      packet_size: 500
```

## Takeaways

* Resource modules have a simple data structure that can be transformed to the network device syntax.  In this case the SNMP dictionary is transformed into the Cisco IOS-XE network device syntax.
* Resource modules are Idempotent, and can be configured to check device state.
* Resource Modules are bi-directional, meaning that they can gather facts for that specific resource, as well as apply configuration.  Even if you are not using resource modules to configure network devices, there is a lot of value for checking resource states.  
* The bi-directional behavior also allows brown-field networks (existing networks) to quickly turn their running-configuration into structured data.  This allows network engineers to get automation up running more quickly and get quick automation victories.

## Solution

The finished Ansible Playbook is provided here for an answer key:

-  [resource.yml](resource.yml)
-  [gathered.yml](gathered.yml)

## Complete

You have completed this lab exercise.

---


[Click here to return to the Ansible Network Automation Workshop](../../README.md)
