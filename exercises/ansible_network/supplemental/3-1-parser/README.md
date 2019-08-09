# Exercise 3.1 - Building dynamic documentation using the command parser

Most CLI based network devices support `show` commands. The output of the commands are "pretty" formatted, in the sense that they are very human readable. However, in the context of automation, where the objective is for a machine(code) to interpret this output, it needs to be transformed into "structured" data. In other words data-types that the code/machine can interpret and navigate. Examples would be lists, dictionaries, arrays and so on.

The Ansible [network-engine](https://github.com/ansible-network/network-engine) is a [role](https://docs.ansible.com/ansible/2.5/user_guide/playbooks_reuse_roles.html) that supports 2 such "translators" - `command_parser` and `textfsm_parser`. These are modules built into the `network-engine` role that takes a raw text input (pretty formatted) and converts it into structured data. You will work with each of these to generate dynamic reports in the following sections:


# Unstructured command output from network devices

Here is how the output of a `show interfaces` command looks like on a Cisco IOS device:

``` shell
rtr2#show interfaces
GigabitEthernet1 is up, line protocol is up
  Hardware is CSR vNIC, address is 0e56.1bf5.5ee2 (bia 0e56.1bf5.5ee2)
  Internet address is 172.17.16.140/16
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full Duplex, 1000Mbps, link type is auto, media type is Virtual
  output flow-control is unsupported, input flow-control is unsupported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output 00:00:00, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 1000 bits/sec, 1 packets/sec
  5 minute output rate 1000 bits/sec, 1 packets/sec
     208488 packets input, 22368304 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 0 multicast, 0 pause input
     250975 packets output, 40333671 bytes, 0 underruns
     0 output errors, 0 collisions, 1 interface resets
     0 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier, 0 pause output
     0 output buffer failures, 0 output buffers swapped out
Loopback0 is up, line protocol is up
  Hardware is Loopback
  Internet address is 192.168.2.102/24
  MTU 1514 bytes, BW 8000000 Kbit/sec, DLY 5000 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation LOOPBACK, loopback not set
  Keepalive set (10 sec)

.
.
.
.
.
<output omitted for brevity>
```


Let's say your task is to prepare a list of interfaces that are currently **up**, the MTU setting, the type and description on the interface. You could log into each device, execute the above command and collect this information. Now imagine if you had to repeat this for 150 devices in your network. That is a lot of man-hours on a relatively boring task!

In this lab, we will learn how to automate this exact scenario using Ansible.

#### Step 1

Start by creating a new playbook called `interface_report.yml` and add the following play definition:

``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli


```

#### Step 2

Next add the `ansible-network.network-engine` role into the playbook. Roles are nothing but a higher level playbook abstraction. Think of them as pre-written playbooks that handle repeated, specific tasks. For this we will need to first install the role. Execute the following command on the control node to install this role:

``` bash
[student1@ansible networking-workshop]$ ansible-galaxy install ansible-network.network-engine

```

The `ansible-network.network-engine` role specifically makes available the `command_parser` module, among other things, which you can then use in subsequent tasks inside your own playbook.


``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine
```


#### Step 3

Now we can begin adding our tasks. Add the first task to run the `show interfaces` command against all the routers and register the output into a variable.



``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      ios_command:
        commands:
          - show interfaces
      register: output



```
> Feel free to run this playbook in verbose mode to view the output returned from the devices.

#### Step 4

The next task is to send the raw data returned in the previous task to the `command_parser` module. This module takes the raw content as one of the inputs along with the name of the parser file.

> Note: The parser file is a YAML file that has a similar structure to Ansible playbooks.


Add this to your playbook:


``` yaml
{%raw%}
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      ios_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

{%endraw%}
```

Let's understand this task in a little more depth. The `command_parser` is referencing a file called `show_interfaces.yaml` within the `parsers` directory. For this lab, the parser has been pre-populated for you. The parsers are written to handle the output from standard show commands on various network platforms.


> More parsers are being made available in the public domain so you will only have to build them if a specific use case has not been handled.

Feel free to view the contents of the parser file. You will notice how it uses regular expressions to capture relevant data from the show command and return it as a variable called `interface_facts`



#### Step 5

Add a new task to view the contents being returned by the `command_parser`

``` yaml
{%raw%}
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      ios_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

    - name: DISPLAY THE PARSED DATA
      debug:
        var: interface_facts
{%endraw%}
```


#### Step 6

Go ahead and run this playbook. Since our objective is to simply view the returned data, limit your playbook run to a single router.


``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts interface_report.yml --limit rtr1

PLAY [GENERATE INTERFACE REPORT] ************************************************************************************************************************************************************

TASK [CAPTURE SHOW INTERFACES] **************************************************************************************************************************************************************
ok: [rtr1]

TASK [PARSE THE RAW OUTPUT] *****************************************************************************************************************************************************************
ok: [rtr1]

TASK [DISPLAY THE PARSED DATA] **************************************************************************************************************************************************************
ok: [rtr1] => {
    "interface_facts": [
        {
            "GigabitEthernet1": {
                "config": {
                    "description": null,
                    "mtu": 1500,
                    "name": "GigabitEthernet1",
                    "type": "CSR"
                }
            }
        },
        {
            "Loopback0": {
                "config": {
                    "description": null,
                    "mtu": 1514,
                    "name": "Loopback0",
                    "type": "Loopback"
                }
            }
        },
        {
            "Loopback1": {
                "config": {
                    "description": null,
                    "mtu": 1514,
                    "name": "Loopback1",
                    "type": "Loopback"
                }
            }
        },
        {
            "Tunnel0": {
                "config": {
                    "description": null,
                    "mtu": 9976,
                    "name": "Tunnel0",
                    "type": "Tunnel"
                }
            }
        },
        {
            "Tunnel1": {
                "config": {
                    "description": null,
                    "mtu": 9976,
                    "name": "Tunnel1",
                    "type": "Tunnel"
                }
            }
        },
        {
            "VirtualPortGroup0": {
                "config": {
                    "description": null,
                    "mtu": 1500,
                    "name": "VirtualPortGroup0",
                    "type": "Virtual"
                }
            }
        }
    ]
}

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=3    changed=0    unreachable=0    failed=0   

[student1@ansible networking-workshop]$
```


How cool is that! Your playbook now converted all that raw text output into structured data: a list of dictionaries where each dictionary describes the elements you need to build your report.









#### Step 7
Next create a directory to hold the per device report:

``` shell

[student1@ansible networking-workshop]$ mkdir intf_reports
[student1@ansible networking-workshop]$

```

#### Step 8
Our next step is to use the template module to generate a report from the above data. Use the same technique you learned in the previous lab to generate the reports per device and then consolidate them using the assemble module.


``` yaml
{%raw%}
---
- name: GENERATE INTERFACE REPORT
  hosts: cisco
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      ios_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

    #- name: DISPLAY THE PARSED DATA
    #  debug:
    #    var: interface_facts

    - name: GENERATE REPORT FRAGMENTS
      template:
        src: interface_facts.j2
        dest: intf_reports/{{inventory_hostname}}_intf_report.md

    - name: GENERATE A CONSOLIDATED REPORT
      assemble:
        src: intf_reports/
        dest: interfaces_report.md
      delegate_to: localhost
      run_once: yes

{%endraw%}
```

> Note: For this lab the  Jinja2 template has been pre-populated for you. Feel free to look at the file **interface_facts.j2** in the **templates** directory.

> Note: The debug task has been commented out so that display is concise

#### Step 9

Run the playbook:



``` shell
[student1@ansible networking-workshop]$ ansible-playbook -i lab_inventory/hosts interface_report.yml

PLAY [GENERATE INTERFACE REPORT] ************************************************************************************************************************************************************

TASK [CAPTURE SHOW INTERFACES] **************************************************************************************************************************************************************
ok: [rtr1]
ok: [rtr3]
ok: [rtr4]
ok: [rtr2]

TASK [PARSE THE RAW OUTPUT] *****************************************************************************************************************************************************************
ok: [rtr3]
ok: [rtr2]
ok: [rtr1]
ok: [rtr4]

TASK [GENERATE REPORT FRAGMENTS] ************************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr2]
changed: [rtr3]
changed: [rtr1]

TASK [GENERATE A CONSOLIDATED REPORT] *******************************************************************************************************************************************************
changed: [rtr3]
ok: [rtr1]
ok: [rtr4]
ok: [rtr2]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=4    changed=1    unreachable=0    failed=0   
rtr2                       : ok=4    changed=1    unreachable=0    failed=0   
rtr3                       : ok=4    changed=2    unreachable=0    failed=0   
rtr4                       : ok=4    changed=1    unreachable=0    failed=0   

[student1@ansible networking-workshop]$

```


#### Step 10


Use the `cat` command to view the contents of the final report:


``` shell
[student1@ansible networking-workshop]$ cat interfaces_report.md
RTR1
----
GigabitEthernet1:
  Description:
  Name: GigabitEthernet1
  MTU: 1500

Loopback0:
  Description:
  Name: Loopback0
  MTU: 1514

Loopback1:
  Description:
  Name: Loopback1
  MTU: 1514

Tunnel0:
  Description:
  Name: Tunnel0
  MTU: 9976

Tunnel1:
  Description:
  Name: Tunnel1
  MTU: 9976

VirtualPortGroup0:
  Description:
  Name: VirtualPortGroup0
  MTU: 1500

RTR2
----
GigabitEthernet1:
  Description:
  Name: GigabitEthernet1
  MTU: 1500

Loopback0:
  Description:
  Name: Loopback0
  MTU: 1514

Loopback1:
  Description:
  Name: Loopback1
  MTU: 1514
.
.
.
.
.
<output omitted for brevity>
```

# Complete

You have completed lab exercise 3.1

---
[Click Here to return to the Ansible Linklight - Networking Workshop](../../README.md)
