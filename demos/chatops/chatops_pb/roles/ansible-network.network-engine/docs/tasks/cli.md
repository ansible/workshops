# Task cli
The ```cli``` task provides an implementation for running CLI commands on
network devices that is platform agnostic. The ```cli``` task accepts a
command and will attempt to execute that command on the remote device returning
the command ouput.

If the ```parser``` argument is provided, the output from the command will be
passed through the parser and returned as JSON facts using the ```engine```
argument.


## Requirements
The following is the list of requirements for using the this task:

* Ansible 2.5 or later
* Connection ```network_cli```
* ansible_network_os

## Arguments
The following are the list of required and optional arguments supported by this
task.

### command
This argument specifies the command to be executed on the remote device. The
```command``` argument is a required value.

### parser
This argument specifies the location of the parser to pass the output from the command to
in order to generate JSON data. The ```parser``` argument is an optional value, but required
when ```engine``` is used.

### engine
The ```engine``` argument is used to define which parsing engine to use when parsing the output
of the CLI commands. This argument uses the file specified to ```parser``` for parsing output to
JSON facts. This argument requires ```parser``` argument to be specified.

This action currently supports two different parsers:

* ```command_parser```
* ```textfsm_parser```

The default value is ```command_parser```.

## How to use
This section describes how to use the ```cli``` task in a playbook.


The following example runs CLI command on the network node.
```yaml

---
- hosts: ios01
  connection: network_cli

  tasks:
  - name: run cli command with cli task
    import_role:
      name: ansible-network.network-engine
      tasks_from: cli
    vars:
      ansible_network_os: ios
      command: show version

```

When run with verbose mode, the output returned is as follows:

```

ok: [ios01] => {
    "changed": false,
    "json": null,
    "stdout": "Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.6(2)T, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2016 by Cisco Systems, Inc.\nCompiled Tue 22-Mar-16 16:19 by prod_rel_team\n\n\nROM: Bootstrap program is IOSv\n\nan-ios-01 uptime is 19 weeks, 5 days, 19 hours, 14 minutes\nSystem returned to ROM by reload\nSystem image file is \"flash0:/vios-adventerprisek9-m\"\nLast reload reason: Unknown reason\n\n\n\nThis product contains cryptographic features and is subject to United\nStates and local country laws governing import, export, transfer and\nuse. Delivery of Cisco cryptographic products does not imply\nthird-party authority to import, export, distribute or use encryption.\nImporters, exporters, distributors and users are responsible for\ncompliance with U.S. and local country laws. By using this product you\nagree to comply with applicable laws and regulations. If you are unable\nto comply with U.S. and local laws, return this product immediately.\n\nA summary of U.S. laws governing Cisco cryptographic products may be found at:\nhttp://www.cisco.com/wwl/export/crypto/tool/stqrg.html\n\nIf you require further assistance please contact us by sending email to\nexport@cisco.com.\n\nCisco IOSv (revision 1.0) with  with 460033K/62464K bytes of memory.\nProcessor board ID 92O0KON393UV5P77JRKZ5\n4 Gigabit Ethernet interfaces\nDRAM configuration is 72 bits wide with parity disabled.\n256K bytes of non-volatile configuration memory.\n2097152K bytes of ATA System CompactFlash 0 (Read/Write)\n0K bytes of ATA CompactFlash 1 (Read/Write)\n0K bytes of ATA CompactFlash 2 (Read/Write)\n10080K bytes of ATA CompactFlash 3 (Read/Write)\n\n\n\nConfiguration register is 0x0"
}

```

The following example runs cli command and parse output to JSON facts.
```yaml

---
- hosts: ios01
  connection: network_cli

  tasks:
  - name: run cli command and parse output to JSON facts
    import_role:
      name: ansible-network.network-engine
      tasks_from: cli
    vars:
      ansible_network_os: ios
      command: show version
      parser: parser_templates/ios/show_version.yaml
      engine: command_parser

```

When run with verbose mode, the output returned is as follows:

```

ok: [ios01] => {
    "ansible_facts": {
        "system_facts": {
            "image_file": "\"flash0:/vios-adventerprisek9-m\"",
            "memory": {
                "free": "62464K",
                "total": "460033K"
            },
            "model": "IOSv",
            "uptime": "19 weeks, 5 days, 19 hours, 34 minutes",
            "version": "15.6(2)T"
        }
    },
    "changed": false,
    "included": [
        "parser_templates/ios/show_version.yaml"
    ],
    "json": null,
    "stdout": "Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.6(2)T, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2016 by Cisco Systems, Inc.\nCompiled Tue 22-Mar-16 16:19 by prod_rel_team\n\n\nROM: Bootstrap program is IOSv\n\nan-ios-01 uptime is 19 weeks, 5 days, 19 hours, 34 minutes\nSystem returned to ROM by reload\nSystem image file is \"flash0:/vios-adventerprisek9-m\"\nLast reload reason: Unknown reason\n\n\n\nThis product contains cryptographic features and is subject to United\nStates and local country laws governing import, export, transfer and\nuse. Delivery of Cisco cryptographic products does not imply\nthird-party authority to import, export, distribute or use encryption.\nImporters, exporters, distributors and users are responsible for\ncompliance with U.S. and local country laws. By using this product you\nagree to comply with applicable laws and regulations. If you are unable\nto comply with U.S. and local laws, return this product immediately.\n\nA summary of U.S. laws governing Cisco cryptographic products may be found at:\nhttp://www.cisco.com/wwl/export/crypto/tool/stqrg.html\n\nIf you require further assistance please contact us by sending email to\nexport@cisco.com.\n\nCisco IOSv (revision 1.0) with  with 460033K/62464K bytes of memory.\nProcessor board ID 92O0KON393UV5P77JRKZ5\n4 Gigabit Ethernet interfaces\nDRAM configuration is 72 bits wide with parity disabled.\n256K bytes of non-volatile configuration memory.\n2097152K bytes of ATA System CompactFlash 0 (Read/Write)\n0K bytes of ATA CompactFlash 1 (Read/Write)\n0K bytes of ATA CompactFlash 2 (Read/Write)\n10080K bytes of ATA CompactFlash 3 (Read/Write)\n\n\n\nConfiguration register is 0x0"
}

```

To know how to write a parser for ```command_parser``` or ```textfsm_parser``` engine, please follow the user guide [here](https://github.com/ansible-network/network-engine/blob/devel/docs/user_guide/README.md).
