#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
---
module: net_facts
version_added: "2.7"
short_description: Collect device capabilities from Network devices
description:
  - Collect basic fact capabilities from Network devices and return
    the capabilities as Ansible facts.

author:
  - Trishna Guha (@trishnaguha)
options: {}
"""

EXAMPLES = """
- facts:
"""

RETURN = """
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def main():
    """ main entry point for Ansible module
    """
    argument_spec = {}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    connection = Connection(module._socket_path)
    facts = connection.get_capabilities()
    facts = module.from_json(facts)
    result = {
        'changed': False,
        'ansible_facts': {'ansible_network_facts': {'capabilities': facts['device_info']}}
    }
    module.exit_json(**result)


if __name__ == '__main__':
    main()
