### Section 2: Writing your first playbook

Now that you have a fundamental grasp of the inventory file and the group/host variables, this section will walk you through building a playbook.

> This section will help you understand the components of a playbook while giving you an immediate baseline for using it within your own production environment!

#### Step 1:

Using your favorite text editor (`vim` and `nano` are available on the control host) create a new file called `gather_eos_data.yml`.

>Alternately, you can create it using sublimetext or any GUI editor on your laptop and scp it over)


>Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format)

#### Step 2:
```
[vagrant@ansible linklight]$ nano gather_eos_data.yml
```

Enter the following play definition into `gather_eos_data.yml`:

>Press the letter "i" to enter insert mode*
``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: network
  gather_facts: no
```

`---` indicates that this is a YAML file. We are running this playbook against the group `network`, that was defined earlier in the inventory file. Playbooks related to network devices should use the connection plugin called `network_cli`. Ansible has different connection plugins that handle different connection interfaces.


#### Step 3

Next, add the first `task`. This task will use the `ios_facts` module to gather facts about each device in the group `network`.


``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: network
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:
```

>A play is a list of tasks. Modules are pre-written code that perform the task.



#### Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

>Use the write/quit method in vim to save your playbook, i.e. Esc :wq!


```
[vagrant@ansible linklight]$ ansible-playbook gather_eos_facts.yml
```

The output should look as follows.

```
[vagrant@ansible linklight]$ ansible-playbook gather_eos_facts.yml

PLAY [GATHER INFORMATION FROM SWITCHES] *******************************************************************************************************************************************

TASK [GATHER SWITCH FACTS] *******************************************************************************************************************************************************
ok: [leaf01]
ok: [spine02]
ok: [spine01]
ok: [leaf02]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=1    changed=0    unreachable=0    failed=0
leaf02                     : ok=1    changed=0    unreachable=0    failed=0
spine01                    : ok=1    changed=0    unreachable=0    failed=0
spine02                    : ok=1    changed=0    unreachable=0    failed=0
```


#### Step 5


The play ran successfully and executed against the 4 switches. But where is the output?! Re-run the playbook using the `-v` flag.

> Note: Ansible has increasing level of verbosity. You can use up to 4 "v's", -vvvv.


```
[vagrant@ansible linklight]$ ansible-playbook gather_eos_facts.yml -v
Using /home/vagrant/.ansible.cfg as config file

PLAY [GATHER INFORMATION FROM SWITCHES] *******************************************************************************************************************************************

TASK [GATHER SWITCH FACTS] *******************************************************************************************************************************************************
ok: [spine02] => {"ansible_facts": {"ansible_net_all_ipv4_addresses": ["10.0.2.15", "192.168.0.11"], "ansible_net_all_ipv6_addresses": [], "ansible_net_filesystems": ["file:", "flash:", "system:"], "ansible_net_fqdn": "localhost", "ansible_net_gather_subset": ["hardware", "default", "interfaces"], "ansible_net_hostname": "localhost", "ansible_net_image": "flash:/vEOS-lab.swi", "ansible_net_interfaces": {"Ethernet1": {"bandwidth": 0, "description": "", "duplex": "duplexFull", "ipv4": {"address": "192.168.0.11", "masklen": 24}, "lineprotocol": "up", "macaddress": "08:00:27:d4:98:b9", "mtu": 1500, "operstatus": "connected", "type": "routed"}, "Ethernet2": {"bandwidth": 0, "description": "", "duplex": "duplexFull", "ipv4": {}, "lineprotocol": "up", "macaddress": "08:00:27:91:59:ea", "mtu": 9214, "operstatus": "connected", "type": "bridged"}, "Ethernet3": {"bandwidth": 0, "description": "", "duplex": "duplexFull", "ipv4": {}, "lineprotocol": "up", "macaddress": "08:00:27:dc:63:fd", "mtu": 9214, "operstatus": "connected", "type": "bridged"}, "Ethernet4": {"bandwidth": 0, "description": "", "duplex": "duplexFull", "ipv4": {}, "lineprotocol": "up", "macaddress": "08:00:27:bb:e5:26", "mtu": 9214, "operstatus": "connected", "type": "bridged"}, "Ethernet5": {"bandwidth": 0, "description": "", "duplex": "duplexFull", "ipv4": {}, "lineprotocol": "up", "macaddress": "08:00:27:3b:9c:99", "mtu": 9214, "operstatus": "connected", "type": "bridged"}, "Management1": {"bandwidth": 1000000000,

.
.
.
.
.
<output truncated for readability>
```


> Note: The output returns key-value pairs that can then be used within the playbook for subsequent tasks. Also note that all variables that start with **ansible_** are automatically available for subsequent tasks within the play.


#### Step 6

Ansible allows you to limit the playbook execution to a subset of the devices declared in the group, against which the play is running against. This can be done using the `--limit` flag. Rerun the above task, limiting it first to `leaf01` and then to both `leaf01` and `spine02`


```
[vagrant@ansible linklight]$ ansible-playbook gather_eos_data.yml  -v --limit leaf01
```


```
[vagrant@ansible linklight]$ ansible-playbook gather_eos_data.yml  -v --limit leaf01,spine02
```





#### Step 7

Running a playbook in verbose mode is a good option to validate the output from a task. To work with the variables within a playbook you can use the `debug` module.

Write 2 tasks that display the switches' OS version and serial number.


``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: network
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The EOS version is: {{ ansible_net_version }}"

    - name: DISPLAY SERIAL NUMBER
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"
```

#### Step 8

Now re-run the playbook but this time do not use the `verbose` flag and run it against all hosts.

```
[vagrant@ansible linklight]$ ansible-playbook gather_eos_facts.yml

PLAY [GATHER INFORMATION FROM SWITCHES] *******************************************************************************************************************************************

TASK [GATHER SWITCH FACTS] *******************************************************************************************************************************************************
ok: [leaf01]
ok: [spine01]
ok: [spine02]
ok: [leaf02]

TASK [DISPLAY VERSION] ***********************************************************************************************************************************************************
ok: [leaf01] => {
    "msg": "The IOS version is: 4.20.1F"
}
ok: [spine02] => {
    "msg": "The IOS version is: 4.20.1F"
}
ok: [spine01] => {
    "msg": "The IOS version is: 4.20.1F"
}
ok: [leaf02] => {
    "msg": "The IOS version is: 4.20.1F"
}

TASK [DISPLAY SERIAL NUMBER] *****************************************************************************************************************************************************
ok: [leaf01] => {
    "msg": "The serial number is:"
}
ok: [spine02] => {
    "msg": "The serial number is:"
}
ok: [spine01] => {
    "msg": "The serial number is:"
}
ok: [leaf02] => {
    "msg": "The serial number is:"
}

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=3    changed=0    unreachable=0    failed=0
leaf02                     : ok=3    changed=0    unreachable=0    failed=0
spine01                    : ok=3    changed=0    unreachable=0    failed=0
spine02                    : ok=3    changed=0    unreachable=0    failed=0

```


Using less than 20 lines of "code" you have just automated version and serial number collection. Imagine if you were running this against your production network! You have actionable data in hand that does not go out of date.  

**NOTE**: depending on vendor implementation their virtual instance might be blank for serial number

## Complete
You have completed Exercise 02.

[Return to training-course](../README.md)
