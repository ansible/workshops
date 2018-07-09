### Section 3 - Module documentation, Registering output & tags

In the previous section you learned to use the `eos_facts` and the `debug` modules. The `debug` module had an input parameter called `msg` whereas the `eos_facts` module had no input parameters. As someone just starting out how would you know what these parameters were for a module?

There are 2 options.

- 1. Point your browser to https://docs.ansible.com > Network Modules and read the documentation

- 2. From the command line, issue the `ansible-doc <module-name>` to read the documentation on the control host.

#### Step 1
On the control host read the documentation about the `eos_facts` module and the `debug` module.


```
[vagrant@ansible linklight]$ ansible-doc debug

```

What happens when you use `debug` without specifying any parameter?

```
[vagrant@ansible linklight]$ ansible-doc eos_facts

```

How can you limit the facts collected ?



#### Step 2
In the previous section, you learned how to use the `eos_facts` module to collect device details. What if you wanted to collect the output of a `show` command that was not provided as a part of `eos_facts` ?

The `eos_command` module allows you to do that. Go ahead and add another task to the playbook to collect the output of 2 _show_ commands to collect the **hostname** and the output of the `show ip interface brief` commands:

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: network
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      eos_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The EOS version is: {{ ansible_net_version }}"

    - name: DISPLAY SERIAL NUMBER
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"


    - name: COLLECT OUTPUT OF SHOW COMMANDS
      eos_command:
        commands:
          - show run | i hostname
          - show ip interface brief
```

> Note: **commands** is a parameter required by the **eos_module**. The input to this parameter is a "list" of EOS commands.

#### Step 3

Before running the playbook, add a `tag` to the last task. Name it "show"

> Tags can be added to tasks, plays or roles within a playbook. You can assign one or more tags to any given task/play/role. Tags allow you to selectively run parts of the playbook.

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: network
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      eos_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The EOS version is: {{ ansible_net_version }}"

    - name: DISPLAY SERIAL NUMBER
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"

    - name: COLLECT OUTPUT OF SHOW COMMANDS
      eos_command:
        commands:
          - show run | i hostname
          - show ip interface brief
      tags: show
```


#### Step 4

Selectively run the last task within the playbook using the `--tags` option:

```
[vagrant@ansible linklight]$ ansible-playbook gather_eos_data.yml --tags=show

PLAY [GATHER INFORMATION FROM SWITCHES] *******************************************************************************************************************************************

TASK [COLLECT OUTPUT OF SHOW COMMANDS] *******************************************************************************************************************************************
ok: [spine01]
ok: [leaf01]
ok: [spine02]
ok: [leaf02]

PLAY RECAP ***********************************************************************************************************************************************************************
leaf01                     : ok=1    changed=0    unreachable=0    failed=0
leaf02                     : ok=1    changed=0    unreachable=0    failed=0
spine01                    : ok=1    changed=0    unreachable=0    failed=0
spine02                    : ok=1    changed=0    unreachable=0    failed=0
```

Note 2 important points here.

1. Only a single task was executed during the playbook run (You no longer can see the serial number and EOS version being displayed)

2. The output of the show commands is not being displayed.


#### Step 5

Re-run the playbook using the `-v` verbose flag to see the output coming back from the switches.

```
[student1@ip-172-16-101-121 networking-workshop]$ ansible-playbook gather_eos_data.yml --tags=show -v

```

#### Step 6

With the `eos_facts` module, the output was automatically assigned to the `ansible_*` variables. For any of the ad-hoc commands we run against remote devices, the output has to be "registered" to a variable in order to use it within the playbook. Go ahead and add the `register` directive to collect the output of the show commands into a variable called `show_output`:


``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: network
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      eos_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The EOS version is: {{ ansible_net_version }}"

    - name: DISPLAY SERIAL NUMBER
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"

    - name: COLLECT OUTPUT OF SHOW COMMANDS
      eos_command:
        commands:
          - show run | i hostname
          - show ip interface brief
      tags: show
      register: show_output
```

#### Step 7

Add a task to use the `debug` module to display the content's of the `show_output` variable. Tag this task as "show" as well.

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: network
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      eos_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The EOS version is: {{ ansible_net_version }}"

    - name: DISPLAY SERIAL NUMBER
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"

    - name: COLLECT OUTPUT OF SHOW COMMANDS
      eos_command:
        commands:
          - show run | i hostname
          - show ip interface brief
      tags: show
      register: show_output

    - name: DISPLAY THE COMMAND OUTPUT
      debug:
        var: show_output
      tags: show
```

> Note the use of **var** vs **msg** for the debug module.

#### Step 8

Re-run the playbook to execute only the tasks that have been tagged. This time run the playbook without the `-v` flag.


```
[vagrant@ansible linklight]$ ansible-playbook gather_eos_data.yml --tags=show

PLAY [GATHER INFORMATION FROM SWITCHES] *******************************************************************************************************************************************

TASK [COLLECT OUTPUT OF SHOW COMMANDS] *******************************************************************************************************************************************
ok: [spine02]
ok: [spine01]
ok: [leaf01]
ok: [leaf02]

TASK [DISPLAY THE COMMAND OUTPUT] ************************************************************************************************************************************************
ok: [leaf02] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "",
            "Interface              IP Address         Status     Protocol         MTU\nEthernet1              192.168.0.15/24    up         up              1500\nManagement1            10.0.2.15/24       up         up              1500"
        ],
        "stdout_lines": [
            [
                ""
            ],
            [
                "Interface              IP Address         Status     Protocol         MTU",
                "Ethernet1              192.168.0.15/24    up         up              1500",
                "Management1            10.0.2.15/24       up         up              1500"
            ]
        ]
    }
}
.
.
.
.
.
<output omitted for brevity>
```
#### Step 9

The `show_output` variable can now be parsed just like a `Python` dictionary. It contains a "key" called `stdout`. `stdout` is a list object, and will contain exactly as many elements as were in the input to the `commands` parameter of the `eos_command` task. This means `show_output.stdout[0]` will contain the output of the `show running | i hostname` command and `show_output.stdout[1]` will contain the output of `show ip interface brief`.

Write a new task to display only the hostname using a debug command:

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: network
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER ROUTER FACTS
      eos_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The EOS version is: {{ ansible_net_version }}"

    - name: DISPLAY SERIAL NUMBER
      debug:
        msg: "The serial number is:{{ ansible_net_serialnum }}"

    - name: COLLECT OUTPUT OF SHOW COMMANDS
      eos_command:
        commands:
          - show run | i hostname
          - show ip interface brief
      tags: show
      register: show_output

    - name: DISPLAY THE COMMAND OUTPUT
      debug:
        var: show_output
      tags: show

    - name: DISPLAY THE HOSTNAME
      debug:
        msg: "The hostname is {{ show_output.stdout[0] }}"
      tags: show
```

#### Step 10

Re-run the playbook.


``` yaml
[student1@ip-172-16-101-121 networking-workshop]$ ansible-playbook gather_eos_data.yml --tags=show

PLAY [GATHER INFORMATION FROM SWITCHES] **************************************************************************

TASK [COLLECT OUTPUT OF SHOW COMMANDS] **************************************************************************
ok: [rtr2]
ok: [rtr4]
ok: [rtr1]
ok: [rtr3]

TASK [DISPLAY THE COMMAND OUTPUT] *******************************************************************************
ok: [rtr2] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
.
.
.
.
.
<output omitted for brevity>
.
.
.
TASK [DISPLAY THE HOSTNAME] ******************************************************************************************************************************************************
ok: [spine01] => {
    "msg": "The hostname is hostname spine01"
}
ok: [leaf01] => {
    "msg": "The hostname is hostname leaf01"
}
ok: [leaf02] => {
    "msg": "The hostname is hostname leaf02 "
}
ok: [spine02] => {
    "msg": "The hostname is hostname spine02"
}


PLAY RECAP ******************************************************************************************************
rtr1                       : ok=3    changed=0    unreachable=0    failed=0   
rtr2                       : ok=3    changed=0    unreachable=0    failed=0   
rtr3                       : ok=3    changed=0    unreachable=0    failed=0   
rtr4                       : ok=3    changed=0    unreachable=0    failed=0   
```

## Complete
You have completed Exercise 03.

[Return to training-course](../README.md)
