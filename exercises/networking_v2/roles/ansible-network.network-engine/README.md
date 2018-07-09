# network-engine

[![network-engine Ansible Galaxy Role](https://img.shields.io/ansible/role/25206.svg)](https://galaxy.ansible.com/ansible-network/network-engine/)

This role provides the foundation for building network roles by providing
modules and plugins that are common to all Ansible Network roles. The role
is platform-agnostic - all of the artifacts in this role can be used on any
Ansible-managed network platform.

To install this role: `ansible-galaxy install ansible-network.network-engine`

To see the version of this role you currently have installed: `ansible-galaxy list | grep network-engine` 

To ensure you have the latest version available: `ansible-galaxy install -f ansible-network.network-engine`

To use this role, follow the [User Guide](https://github.com/ansible-network/network-engine/blob/devel/docs/user_guide/README.md).

To find other roles maintained by the Ansible Network team, see our [Galaxy Profile](https://galaxy.ansible.com/ansible-network/). 

Any open bugs and/or feature requests are tracked in [GitHub issues](https://github.com/ansible-network/network-engine/issues).

Interested in contributing to this role? Check out [CONTRIBUTING](https://github.com/ansible-network/network-engine/blob/devel/CONTRIBUTING.md) before submitting a pull request.

## Documentation

* User guide:
    - [How to use](https://github.com/ansible-network/network-engine/blob/devel/docs/user_guide/README.md)
    - [Parser Directives](https://github.com/ansible-network/network-engine/blob/devel/docs/directives/parser_directives.md)
* Development guide: [How to test](https://github.com/ansible-network/network-engine/blob/devel/docs/tests/test_guide.md)

For module documentation see the [modules](#modules) section below.

## Requirements

* Ansible 2.5.0 (or higher)

## Tasks

The following are the available tasks provided by this role for use in
playbooks.

None

## Variables

The following are the list of variables this role accepts

None

## Modules

The following is a list of modules that are provided by this role, which include documentation & examples:

* `cli` [source](https://github.com/ansible-network/network-engine/blob/devel/action_plugins/cli.py)
* `command_parser` [source](https://github.com/ansible-network/network-engine/blob/devel/library/command_parser.py)
* `textfsm_parser` [source](https://github.com/ansible-network/network-engine/blob/devel/library/textfsm_parser.py)

## Plugins

The following is a list of plugins that are provided by this role.

None

## Dependencies

The following is the list of dependencies on other roles this role requires.

None

## License

GPLv3

## Author Information

Ansible Network Engineering Team
