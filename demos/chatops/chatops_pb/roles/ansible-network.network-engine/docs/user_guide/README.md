Using the Network Engine Role
----------------------------------

The Network Engine role is supported as a dependency of other Roles. The Network Engine Role extracts data about your network devices as Ansible facts in a JSON data structure, ready to be added to your inventory host facts and/or consumed by Ansible tasks and templates. You define the data elements you want to extract from each network OS command in parser templates, using either YAML or Google TextFSM syntax. The matching rules may be different on each network platform, but by defining the same variable names for the output on all platforms, you can normalize similar data across platforms. That's how the Network Engine Role supports truly platform-agnostic network automation.

The Network Engine role can also be used directly, though direct usage is not supported with your Red Hat subscription.

The initial release of the Network Engine role includes two parser modules:
* [command_parser](https://github.com/ansible-network/network-engine/blob/devel/docs/user_guide/command_parser.md) accepts YAML input, uses an internally maintained, loosely defined parsing language based on Ansible playbook directives
* [textfsm_parser](https://github.com/ansible-network/network-engine/blob/devel/docs/user_guide/textfsm_parser.md) accepts Google TextFSM input, uses Google TextFSM parsing language

Both modules iterate over the data definitions in your parser templates, parse command output from your network devices (structured ASCII text) to find matches, and then convert the matches into Ansible facts in a JSON data structure.

The task ```cli``` provided by the role, can also be directly implemented in your playbook. The documentation can be found here [tasks/cli](https://github.com/ansible-network/network-engine/blob/devel/docs/tasks/cli.md).

To manage multiple interfaces and vlans, the Network Engine role also offers [filter_plugins](https://github.com/ansible-network/network-engine/blob/devel/docs/plugins/filter_plugins.md) that turn lists of Interfaces or VLANs into ranges and vice versa.

Modules:
--------
- `command_parser`
- `textfsm_parser`
- `net_facts`

To use the Network Engine Role:
----------------------------------------
1. Install the role from Ansible Galaxy
`ansible-galaxy install ansible-network.network-engine` will copy the Network Engine role to `~/.ansible/roles/`.
1. Select the parser engine you prefer
For YAML formatting, use `command_parser`; for TextFSM formatting, use `textfsm_parser`. The parser docs include
examples of how to define your data and create your tasks.
1. Define the data you want to extract (or use a pre-existing parser template)
See the parser_template sections of the command_parser and textfsm_parser docs for examples.
1. Create a playbook to extract the data you've defined
See the Playbook sections of the command_parser and textfsm_parser docs for examples.
1. Run the playbook with `ansible-playbook -i /path/to/your/inventory -u my_user -k /path/to/your/playbook`
1. Consume the JSON-formatted Ansible facts about your device(s) in inventory, templates, and tasks.

Additional Resources
-------------------------------------

* [README](https://galaxy.ansible.com/ansible-network/network-engine/#readme)
* [command_parser tests](https://github.com/ansible-network/network-engine/tree/devel/tests/command_parser)
* [textfsm_parser tests](https://github.com/ansible-network/network-engine/tree/devel/tests/textfsm_parser)
* [Full changelog diff](https://github.com/ansible-network/network-engine/blob/devel/CHANGELOG.rst)

Contributing and Reporting Feedback
-------------------------------------
[Review issues](https://github.com/ansible-network/network-engine/issues)
