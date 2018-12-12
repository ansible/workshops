# network-engine

[![network-engine Ansible Galaxy Role](https://img.shields.io/ansible/role/25206.svg)](https://galaxy.ansible.com/ansible-network/network-engine/)

This role provides the foundation for building network roles by providing
modules and plugins that are common to all Ansible Network roles.  Typically
this role should not be directly invoked in a playbook.

To install this role: `ansible-galaxy install ansible-network.network-engine`

To see the version of this role you currently have installed: `ansible-galaxy info ansible-network.network-engine`

To ensure you have the latest version available: `ansible-galaxy install -f ansible-network.network-engine`

To find other roles maintained by the Ansible Network team, see our [Galaxy Profile](https://galaxy.ansible.com/ansible-network/). 

Any open bugs and/or feature requests are tracked in [GitHub issues](https://github.com/ansible-network/network-engine/issues).

Interested in contributing to this role? Check out [CONTRIBUTING](https://github.com/ansible-network/network-engine/blob/devel/CONTRIBUTING.md) before submitting a pull request.


## Functions

This section provides a list of the available functions that are included in
this role.  Any of the provided functions can be implemented in Ansible
playbooks directly.  To use a particular function, please see the `docs` link
associated with the function.

* `cli` [[source]](https://github.com/ansible-network/network-engine/blob/devel/tasks/cli.yaml) [[docs]](https://github.com/ansible-network/network-engine/blob/devel/docs/tasks/cli.md).

## Developer Guide

- [How to use](https://github.com/ansible-network/network-engine/blob/devel/docs/user_guide/README.md)
- [Parser Directives](https://github.com/ansible-network/network-engine/blob/devel/docs/directives/parser_directives.md)
- [Filter Plugins](https://github.com/ansible-network/network-engine/blob/devel/docs/plugins/filter_plugins.md)
- [How to test](https://github.com/ansible-network/network-engine/blob/devel/docs/tests/test_guide.md)


## License

GPLv3

## Author Information

Ansible Network Community (ansible-network)
