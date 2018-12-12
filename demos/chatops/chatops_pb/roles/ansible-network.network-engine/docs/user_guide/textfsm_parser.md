# textfsm_parser

The [textfsm_parser](https://github.com/ansible-network/network-engine/blob/devel/library/textfsm_parser.py)
module is based on [Google TextFSM](https://github.com/google/textfsm/wiki/TextFSM) definitions. 
This module iterates over matching rules defined in TextFSM format, extracts data from structured ASCII text based on those rules,
and returns Ansible facts in a JSON data structure that can be added to inventory host facts and/or consumed by Ansible tasks and templates.

The `textfsm_parser` module requires two inputs:
- the output of commands run on the network device, passed to the `content` parameter
- the parser template that defines the rules for parsing the output, passed to either the `file` or the `src` parameter

## content

The `content` parameter for `textfsm_parser` must point to the ASCII text output of commands run on network devices. The text output can be in a variable or in a file.

## file

The `file` parameter for `textfsm_parser` must point to a parser template that contains a TextFSM rule for each data field you want to extract from your network devices. 

Parser templates for the `textfsm_parser` module in the Network Engine role use TextFSM notation.

### name

The `name` parameter for `textfsm_parser` names the variable in which Ansible will store the JSON data structure. If name is not set, the JSON facts from parsing will not be displayed/exported.

### src

The `src` parameter for `textfsm_parser` loads your parser template from an external source, usually a URL.

## Sample Parser Templates

Here is a sample TextFSM parser template:

`parser_templates/ios/show_interfaces`
```

Value Required name (\S+)
Value type ([\w ]+)
Value description (.*)
Value mtu (\d+)

Start
  ^${name} is up
  ^\s+Hardware is ${type} -> Continue
  ^\s+Description: ${description}
  ^\s+MTU ${mtu} bytes, -> Record

```

## Sample Playbooks

To extract the data defined in your parser template, create a playbook that includes the Network Engine role and references the `content` and `file` parameters of the `command_parser` module. 

The example playbook below runs a show command, imports the Network Engine role, extracts data from the text output of the command by matching it against the rules defined
in your parser template, and stores the results in a variable. To view the content of that final variable, add it to the `name` parameter as shown in the example and run the playbook in `verbose` mode: `ansible-playbook -v`.

Make sure the `hosts` definition in the playbook matches a host group in your inventory - in these examples, the playbook expects a group called `ios`.

The example below parses the output of the `show interfaces` command on IOS and creates facts from that output:

```yaml

---

# ~/my-playbooks/textfsm-gather-interface-info.yml

- hosts: ios
  connection: network_cli

  tasks:
  - name: Collect interface information from device
    ios_command:
      commands: "show interfaces"
    register: ios_interface_output

  - name: Generate interface facts as JSON
    textfsm_parser:
      file: "parser_templates/ios/show_interfaces"
      content: "{{ ios_interface_output.stdout.0 }}"
      name: interface_facts

```
