# Managing networks hasn't changed in 30 years

- Networks are mission critical
- Every network is a unique snowflake
- Ad-hoc changes that proliferate 
- Vendor specific implementations
- Testing is expensive/impossible

Note: TODO - check on branding/lettering



# According to Gartner...
<section data-background-image="images/gartner.svg"></section>




# Automation considerations

- Compute is no longer the slowest link in the chain
- Businesses demand that networks deliver at the speed of cloud 
- Automation of repeatable tasks 
- Bridge silos

Note: TODO - Transition slide from problem to solution.



# What is Ansible?
Red Hat Ansible network automation is enterprise software for automating and managing IT infrastructure.

As a vendor agnostic framework Ansible can automate Arista (EOS), Cisco (IOS, IOS XR, NX-OS), Juniper (JunOS), Open vSwitch and VyOS.

Ansible Tower is an enterprise framework for controlling, securing and managing your Ansible automation with a **UI and RESTful API.**



    

<section data-background-image="images/simple-powerful-agentless-diagram.svg">
</section>



# Ansible: The universal automation framework
<section data-background-image="images/language.svg"></section>



<section data-background-image="images/network_automation.svg"></section>



# Common use cases 

- Backup and restore device configurations
- Upgrade network device OS
- Ensure configuration compliance
- Generate dynamic documentation



# Common use cases - automating discrete tasks
- Ensure VlANs are present/absent
- Enable/Disable netflow on WAN interfaces
- Manage firewall access list entries




# How Ansible Works

![how it works](images/local_execution.svg)




# Understanding Ansible vocabulary
<img src="images/how-ansible-works-diagram-01.svg" />



# Playbooks

<img src="images/how-ansible-works-diagram-02.svg" />


# Inventory
<img src="images/networking-how-ansible-works-diagram-05.svg" />



# Modules & Tasks
<img src="images/how-ansible-works-diagram-03.svg" />



# Plugins
<img src="images/how-ansible-works-diagram-04.svg" />



# Understanding inventory
<div class="columns">
    <div class="col">
<pre>
```
10.1.1.2
192.168.1.2
core1.nw.com
core2.nw.com
access1.nw.com
access2.nw.com
```</pre>

</div>
<div></div>




# Inventory - Groups

<div class="columns">
    <div class="col">
    There is always a group called **"all"** by default
<pre>
```
[atl]
10.1.1.2
192.168.1.2
    
[core]
core1.nw.com
core2.nw.com
    
[access]
access1.nw.com
access2.nw.com
```</pre>

</div>

<div>
Groups can be nested
<pre>
```
[DC:children]
core
access

[east-coast:children]
DC
atl

[atl]
10.1.1.2
192.168.1.2
    
[core]
core1.nw.com
core2.nw.com
    
[access]
access1.nw.com
access2.nw.com
```</pre></div>



# Inventory - variables

<div class="columns">
    <div class="col">

<pre>
```
[all:vars]
ansible_username=admin
ansible_password=pa55w0rd
snmp_ro=public123
snmp_rw=private123

[east-coast:vars]
ntp_server=10.99.99.99
anycast=169.1.1.1

[DC:children]
core
access

[east-coast:children]
DC
atl

[atl]
10.1.1.2 snmp_ro=atl123 
192.168.1.2
    
[core]
core1.nw.com snmp_ro=corepub123 snmp_rw=corepri123
core2.nw.com
    
[access]
access1.nw.com ansible_username=localadmin
access2.nw.com 
```</pre>
</div>
<div> 
<p>- Group variables apply for all devices in that group </p>
<p>- Host variables apply to the host and overrides group vars </p>
</div> 



# A sample playbook

<div class="columns">
    <div class="col">
<pre>
```
---
- name: DEPLOY VLANS 
  hosts: access
  connection: network_cli
  gather_facts: no
  
  
  tasks:
    
    - name: ENSURE VLANS EXIST
      nxos_vlan:
        vlan_id: 100
        admin_state: up
        name: WEB
        
```</pre>

</div>
<div>
<p>- Playbook is a list of plays. </p>

<p>- Each play is a list of tasks.</p>

<p>- Tasks invoke modules.</p>

A playbook can contain more than one play

</div>



# Lab Time

#### Lab 1: Section 1

In this lab you will explore the lab environment and build familiarity with the lab inventory.

Approximate time: 20 mins



# Playbook definition for network automation

- Target play execution using **`hosts`**
- Define the connection : **`network_cli`**
- About **`gather_facts`**



# Running a playbook

``` bash
[student1@control-node networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************
ok: [rtr1]
ok: [rtr4]
ok: [rtr3]
ok: [rtr2]

PLAY RECAP **********************************************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0   
rtr2                       : ok=1    changed=0    unreachable=0    failed=0   
rtr3                       : ok=1    changed=0    unreachable=0    failed=0   
rtr4                       : ok=1    changed=0    unreachable=0    failed=0   

[student1@ip-172-16-101-121 networking-workshop]$

```




# Displaying output

Use the optional **verbose** flag during playbook execution 

``` bash
student1@control-node networking-workshop]$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml  -v
Using /home/student1/.ansible.cfg as config file

PLAY [GATHER INFORMATION FROM ROUTERS] ******************************************************************

TASK [GATHER ROUTER FACTS] ******************************************************************************
ok: [rtr3] => {"ansible_facts": {"ansible_net_all_ipv4_addresses": ["10.100.100.3", "192.168.3.103", "172.16.235.46", 
"192.168.35.101", "10.3.3.103"], "ansible_net_all_ipv6_addresses": [], "ansible_net_filesystems": ["bootflash:"],
"ansible_net_gather_subset": ["hardware", "default", "interfaces"], "ansible_net_hostname": "rtr3", "ansible_net_image": 
"boot:packages.conf", "ansible_net_interfaces": {"GigabitEthernet1": {"bandwidth": 1000000, "description": null, "duplex":"Full", 
"ipv4": [{"address": "172.16.235.46", "subnet": "16"}], "lineprotocol": "up ", "macaddress": "0e93.7710.e63c", "mediatype": "Virtual",
"mtu": 1500, "operstatus": "up", "type": "CSR vNIC"}, "Loopback0": {"bandwidth": 8000000, "description": null, "duplex": null, "ipv4": [{"address": "192.168.3.103", "subnet": "24"}], "lineprotocol": "up ", "macaddress": "192.168.3.103/24", "mediatype": null, 
"mtu": 1514, "operstatus": "up", "type": null}, "Loopback1": {"bandwidth": 8000000, "description": null, 
"duplex": null, "ipv4": [{"address": "10.3.3.103", 
"subnet": "24"}], "lineprotocol": "up ", "macaddress": "10.3.3.103/24", "mediatype": null, "mtu": 1514, "operstatus": "up", "type": null},
"Tunnel0": {"bandwidth": 100, "description": null, "duplex": null, "ipv4": [{"address": "10.100.100.3", "subnet": "24"}]

.
.
.
.
.
<output truncated for readability>
```

_Increase the level of verbosity by adding more "v's" -vvvv_



# Limiting playbook execution

Playbook execution can be limited to a subset of devices using the **--limit** flag.

``` bash
$ ansible-playbook -i lab_inventory/hosts gather_ios_data.yml  -v --limit rtr1
```



# A note about special variables

Other than the user defined variables, Ansible supports many **special** inbuilt variables. For example

| Variable           | Explanation                                           |
|--------------------|-------------------------------------------------------|
| ansible_*          | Output of fact gathering                              |
| inventory_hostname | Name of the device the task is executing against      |
| hostvars           | A dictionary variable whose key is inventory_hostname |
|                    |                                                       |



# Displaying output - The "debug" module
The **debug** module is used like a "print" statement in most programming languages.
Variables are accessed using "{{ }}" - quoted curly braces


#### Demo of the debug module





# Modules
Modules do the actual work in ansible, they are what gets executed in each playbook task. 
          <div class="columns">
            <div class="col">
              <ul>
                <li>\*os_facts</li>
                <li>\*os_command</li>
                <li>\*os\_config</li>
                <li>more modules depending on platform</li>
              </ul>
            </div>
            <div class="col">
              <ul>
                <li>Arista EOS = eos\_</li>
                <li>Cisco IOS/IOS-XE = ios\_</li>
                <li>Cisco NX-OS = nxos\_</li>
                <li>Cisco IOS-XR = iosxr\_</li>
                <li>Juniper Junos = junos\_</li>
                <li>VyOS = vyos\_</li>
              </ul>
            </div>
          </div>




# Modules per network platform

```
  tasks:
    - name: configure eos system properties
      eos_system:
        domain_name: ansible.com
        vrf: management
      when: ansible_network_os == 'eos'

    - name: configure nxos system properties
      nxos_system:
        domain_name: ansible.com
        vrf: management
      when: ansible_network_os == 'nxos'
        
```



# Modules Documentation

<div class="columns">
    <div class="col">
    <p><strong>http://docs.ansible.com/</strong></p>
    </div>
<div class="col">
<img src="images/modules-doc-screenshots.png" />
</div>
            
            



# Modules Documentation
``` bash
# List out all modules installed
$ ansible-doc -l
...
ios_banner                                Manage multiline banners on Cisco IOS devices
ios_command                               Run commands on remote devices running Cisco IOS
ios_config                                Manage Cisco IOS configuration sections
...

# Read documentation for installed module
$ ansible-doc ios_command
> IOS_COMMAND

     Sends arbitrary commands to an ios node and returns the results read from the
     device. This module includes an argument that will cause the module to wait for a
     specific condition before returning or timing out if the condition is not met. This
     module does not support running commands in configuration mode. Please use
     [ios_config] to configure IOS devices.

Options (= is mandatory):
...
```






# Variables
Ansible can work with metadata from various sources and manage their context in the form of variables.

- Command line parameters
- Plays and tasks
- Files
- Inventory
- Discovered facts
- Roles



# Variable Precedence
The order in which the same variable from different sources will override each other.

<div class="columns">
  <div class="col">
    <ol>
      <li>extra vars</li>
      <li>task vars (only for the task)</li>
      <li>block vars (only for tasks in block)</li>
      <li>role and include vars</li>
      <li>play vars_files</li>
      <li>play vars_prompt</li>
      <li>play vars</li>
      <li>set_facts</li>
    </ol>
  </div>
  <div class="col">
    <ol start="9" class="col">
      <li>registered vars</li>
      <li>host facts</li>
      <li>playbook host_vars</li>
      <li>playbook group_vars</li>
      <li><strong>inventory host_vars</strong></li>
      <li><strong>inventory group_vars</strong></li>
      <li>inventory vars</li>
      <li>role defaults</li>
    </ol>
  </div>
</div>



# Tasks
Tasks are the application of a module to perform a specific unit of work.

- **file**: A directory should exist
- **yum**: A package should be installed

There are also tasks for network devices as well

- **ios_facts**: collect the version of code running on Cisco IOS/IOS-XE
- **ios_system**: configure DNS server(s) on Cisco IOS/IOS-XE
- **nxos_snmp_user**: add an SNMP user on Cisco NX-OS
- **eos_command**: turn off a port on Arista EOS
- **junos_banner**: manage the banner on Juniper Junos OS




# Example Tasks in a Play

``` yaml
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




# Plays & Playbooks
Plays are ordered sets of tasks to execute against host selections from your inventory. A playbook is a file containing one or more plays.




# Playbook Example

``` yaml
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
        msg: "{{version}}"

    - name: Backup configuration
      ios_config:
        backup: yes
                  
```




# Human-Meaningful Naming

 <pre><code data-noescape>

   ---
   - <mark>name: backup router configurations</mark>
     hosts: routers
     connection: network_cli
     gather_facts: no
   
     tasks:
       - <mark>name: gather ios_facts</mark>
         ios_facts:
         register: version
   
       - debug:
           msg: "{{version}}"
   
       - <mark>name: Backup configuration</mark>
         ios_config:
           backup: yes
</code></pre>




# Host Selector

<pre><code data-noescape>

   ---
   - name: backup router configurations
     <mark>hosts: routers</mark>
     connection: network_cli
     gather_facts: no
   
     tasks:
       - name: gather ios_facts
         ios_facts:
         register: version
   
       - debug:
           msg: "{{version}}"
   
       - name: Backup configuration
         ios_config:
            backup: yes
</code></pre>




# Tasks
 <pre><code data-noescape>
 
---
- name: backup router configurations
  hosts: routers
  connection: network_cli
  gather_facts: no

  tasks:
    - name: gather ios_facts
      <mark>ios_facts:</mark>
      <mark>register: version</mark>

    - <mark>debug:</mark>
        <mark>msg: "{{version}}"</mark>

    - name: Backup configuration
      <mark>ios_config:</mark>
        <mark>backup: yes</mark>
</code></pre>




<section data-state="title alt">
# Demo Time:
# Exercise 1.2 - Backing up Configurations




<section data-state="title alt">
# Workshop: 
# Exercise 1.2 - Backing up Configurations




# Variables - Recap
- **host vars** - variable specific to one host
- **group vars** - variables for all hosts within the group
It is possible, but not required, to configure variables in the inventory file.




# Inventory ini file

``` ini
[junos]
vsrx01 ansible_host=an-vsrx-01.rhdemo.io private_ip=172.16.1.1
vsrx02 ansible_host=an-vsrx-02.rhdemo.io private_ip=172.17.1.1

[junos:vars]
ansible_network_os=junos
ansible_password=Ansible

[ios]
ios01 ansible_host=an-ios-01.rhdemo.io

[ios:vars]
ansible_network_os=ios
ansible_become=yes
ansible_become_method=enable
ansible_become_pass=cisco
```



# Host Variables - hostvars
<pre><code data-noescape>
[junos]
vsrx01 ansible_host=an-vsrx-01.rhdemo.io <mark>private_ip=172.16.1.1</mark>
vsrx02 ansible_host=an-vsrx-02.rhdemo.io <mark>private_ip=172.17.1.1</mark>

[junos:vars]
ansible_network_os=junos
ansible_password=Ansible

[ios]
ios01 ansible_host=an-ios-01.rhdemo.io

[ios:vars]
ansible_network_os=ios
ansible_become=yes
ansible_become_method=enable
ansible_become_pass=cisco
</pre></code>




# Group Variables - groupvars
<pre><code data-noescape>
[junos]
vsrx01 ansible_host=an-vsrx-01.rhdemo.io private_ip=172.16.1.1
vsrx02 ansible_host=an-vsrx-02.rhdemo.io private_ip=172.17.1.1

[junos:vars]
<mark>ansible_network_os=junos
ansible_password=Ansible</mark>

[ios]
ios01 ansible_host=an-ios-01.rhdemo.io

[ios:vars]
<mark>ansible_network_os=ios
ansible_become=yes
ansible_become_method=enable
ansible_become_pass=cisco</mark>
</pre></code>




# Conditionals
Ansible supports the conditional execution of a task based on the run-time evaluation of variable, fact, or previous task result.

<pre><code data-noescape>
- name: configure interface settings
  ios_config:
    lines:
      - description shutdown by Ansible
      - shutdown
    parents: interface GigabitEthernet2
  <mark>when: ansible_network_os == "ios"</mark>
</code></pre>



# Multi-Platform Playbooks

``` yaml

   - name: run on eos
     include_tasks: tasks/eos.yml
     when: ansible_network_os == eos

   - name: run on ios
     include_tasks: tasks/ios.yml
     when: ansible_network_os == ios

   - name: run on junos
     include_tasks: tasks/junos.yml
     when: ansible_network_os == junos

   - name: run on nxos
     include_tasks: tasks/nxos.yml
     when: ansible_network_os == iosxr
     
```




# Using a config module
Manage configuration on a network platform

```
- name: configure top level configuration
  ios_config:
    lines: hostname {{ inventory_hostname }}

- name: configure interface settings
  ios_config:
    lines:
      - description test interface
      - ip address 172.31.1.1 255.255.255.0
    parents: interface Ethernet1

- name: configure from a jinja2 template
  ios_config:
    src: config.j2
        
```




# Exercise 1.3 - Network Diagram
As a lab precursor look at the network diagram
<img src="images/gre_diagram.png">




<section data-state="title alt">
# Demo Time: 
# Exercise 1.3 - Creating a GRE Tunnel




<section data-state="title alt">
# Workshop: 
# Exercise 1.3 - Creating a GRE Tunnel




# Doing More with Playbooks
Here are some more essential playbook features that you can apply:

- Templates
- Loops
- Conditionals
- Tags
- Blocks



# Templates
Ansible embeds the [Jinja2 templating engine](http://jinja.pocoo.org/docs/) that can be used to dynamically:

- Set and modify play variables
- Conditional logic
- Generate files such as configurations from variables



# Loops
Loops can do one task on multiple things, such as create a lot of users, install a lot of packages, or repeat a polling step until a certain result is reached.
  
 <pre><code data-noescape>

---
- hosts: cisco
connection: local
tasks:
  - nxos_snmp_user:
      user: "{{item.user}}"
      group: network-admin
      authentication: sha
      pwd: "{{item.password}}"
    <mark>with_items:</mark>
      <mark>- { user: 'exampleuser', password: 'testPASS123' }</mark>
      <mark>- { user: 'gerald', password: 'testPASS456' }</mark>
      <mark>- { user: 'sean', password: 'testPASS789' }</mark>
      <mark>- { user: 'andrius', password: 'vTECH1234' }</mark>
</code></pre>




# Tags
Tags are useful to be able to run a subset of a playbook on-demand.

<pre><code data-noescape>

tasks:
- name: gather ios_facts
  ios_facts:
  register: version
  <mark>tags: debug</mark>

- debug:
    msg: "{{version}}"
  <mark>tags: debug</mark>

- name: Backup configuration
  ios_config:
    backup: yes
  <mark>tags: </mark>
    <mark>- backup</mark>
</code></pre>




# Blocks
Blocks cut down on repetitive task directives, allow for logical grouping of tasks and even in play error handling.

<pre><code data-noescape>
- name: Configure Hostname and DNS
  <mark>block:</mark>
  - ios_config:
      lines: hostname {{ inventory_hostname }}

  - name: configure name servers
    ios_system:
      name_servers:
        - 8.8.8.8
        - 8.8.4.4
  when: ansible_network_os == "ios"
</code></pre>




<section data-state="title alt">
# Demo Time: 
# Exercise 1.4 - Additional router configurations




<section data-state="title alt">
# Workshop: 
# Exercise 1.4 - Additional router configurations




# Roles
Roles are a packages of closely related Ansible content that can be shared more easily than plays alone.

- Improves readability and maintainability of complex plays
- Eases sharing, reuse and standardization of automation processes
- Enables Ansible content to exist independently of playbooks, projects -- even organizations
- Provides functional conveniences such as file path resolution and default values




# Project with Embedded Roles Example

``` bash
site.yml
roles/
   common/
     files/
     templates/
     tasks/
     handlers/
     vars/
     defaults/
     meta/
   ospf/
     files/
     templates/
     tasks/
     handlers/
     vars/
     defaults/
     meta/
```



# Project with Embedded Roles Example

``` yaml

# site.yml
---
- hosts: routers
  roles:
     - common
     - ospf
```



# Ansible Galaxy

**http://galaxy.ansible.com**

Ansible Galaxy is a hub for finding, reusing and sharing Ansible content.

Jump-start your automation project with content contributed and reviewed by the Ansible community.




<section data-state="title alt">
# Demo Time: 
# A Playbook Using Roles




# Next Steps
- **It's easy to get started**

   ansible.com/get-started
- **Join the Ansible community**

   ansible.com/community
- **Would you like to learn a lot more?**

   redhat.com/en/services/training/do407-automation-ansible
