#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
---
module: ios_check_match
version_added: "2.7"
short_description: Check if user input matches existing ACLs on an IOS device
description:
  - Checks if the user input matches existing ACLS. Supports subnets, sub protocols etc. TODO - source ports, ranges
author:
  - Ajay Chenampara(@termlen0)
options: {}
"""

EXAMPLES = """
- check_ios_match:
    protocol: 'udp'
    action: 'deny'
    src_network: '10.1.1.2'
    src_mask: '255.255.255.255'
    dst_network: '172.17.33.128'
    dst_mask: '255.255.255.128'
    dst_port: '2223'
    device_acl: "{{ output.stdout[0] }}

"""

RETURN = """
"""
from ansible.module_utils.basic import AnsibleModule
import netaddr


def check_network(network_to_check=None, network_from_device=None):
    def wildcard_conversion(wildcard):
        subnet = []
        for x in wildcard.split('.'):
            component = 255 - int(x)
            subnet.append(str(component))
        subnet = '.'.join(subnet)
        return subnet
    # Clean up the data returned from the device
    if network_from_device != 'any':
        param1, param2 = network_from_device.split()
    # First check if device allows any
    if network_from_device == 'any':
        return True
    # Next, check if device is permitting a host and requested rule check is
    # also a host
    elif param1 == 'host':
        if network_to_check['mask'] == '255.255.255.255' and \
           network_to_check['network'] == param2:
            return True
    elif "host" in network_from_device.split():
        _, configured_src = network_from_device.split()
    # Finally, check whether requested network is a subnetwork of configured
    # network
    else:
        subnet_mask = netaddr.IPAddress(wildcard_conversion(param2))
        device_ip = netaddr.IPNetwork(param1 + '/' +
                                      str(subnet_mask.netmask_bits()))
        device_network = netaddr.IPSet(device_ip)
        input_mask = str(netaddr.IPAddress(
            network_to_check['mask']).netmask_bits())
        input_nw = netaddr.IPNetwork(network_to_check['network'] + '/' +
                                     input_mask)
        return input_nw 


def check_port(input_dict=None, device_dict=None):
    input_port = str(input_dict.get('port')).strip()
    device_port = str(device_dict.get('dst_port')).strip()
    device_protocol = device_dict.get('protocol')
    if input_port == device_port:
        return True
    if device_port == 'any':
        return True
    # Check for 'permit ip host 192.168.0.1 host 172.16.0.1; with user input
    # for a specific TCP/UDP port
    if device_port == 'None' or not device_port:
        if device_protocol == 'ip':
            return True
    return False


def check_match(input_action, input_protocol, src_dict, dst_dict, device_acls):
    result = []
    for acl in device_acls:
        details = list(acl.values())
        for ace in details[0]['data']:
            protocol_match = False
            action_match = False
            src_match = False
            dst_match = False
            dst_port_match = False
            if ace['action'] == input_action:
                action_match = True
            if action_match:
                if ace['protocol'] in ['ip', input_protocol]:
                    protocol_match = True
            if protocol_match:
                src_match = check_network(src_dict, ace['src_network'])
            if src_match:
                dst_match = check_network(dst_dict, ace['dst_network'])
            if dst_match:
                dst_port_match = check_port(dst_dict, ace)
            if dst_port_match:
                # match = f"{ace['src_network']} -> {ace['dst_network']}:{ace.get('dst_port')}"
                match = "{} -> {}:{}".format(ace['src_network'],
                                             ace['dst_network'],
                                             ace.get('dst_port'))
                result.append({'ace_name': list(acl.keys())[0],
                               'ace_action': ace['action'],
                               'ace_number': ace['ace_num'],
                               'rule_match': match})
    if result:
        output = {"result": result}
        return output
    else:
        return {"result": "No match found"}


# def gather_input():
#     src = {'network': '10.1.1.1'}
#     dest = {'dst_network': '172.17.1.1', 'dst_port': '8080'}
#     protocol = 8080
#     pass


# if __name__ == "__main__":
#     #gather_input()
#     # Test data
#     src = {'network': '10.1.1.2', 'mask': '255.255.255.255'}
#     dest = {'network': '172.17.33.128', 'mask': '255.255.255.128',
#             'port': '2223'}
#     protocol = 'udp'
#     action = 'deny'
#     
#     print(result)


def main():
    """ main entry point for Ansible module
    """
    argument_spec = dict(
        protocol=dict(type='str', required=True,
                      choices=['ip', 'tcp', 'udp']),
        action=dict(type='str', required=True, choices=['permit', 'deny']),
        src_network=dict(type='str', required=True),
        src_mask=dict(type='str'),
        dst_network=dict(type='str', required=True),
        dst_mask=dict(type='str'),
        dst_port=dict(type='str'),
        device_acl=dict(type='list', required=True)
        )

    
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    protocol = module.params['protocol']
    action = module.params['action']
    src_network = module.params['src_network']
    src_mask = module.params['src_mask']
    dst_network= module.params['dst_network']
    dst_mask = module.params['dst_mask']
    dst_port = module.params['dst_port']
    device_acl = module.params['device_acl']

    src = dict(network=src_network, mask=src_mask)
    dest = dict(network=dst_network, mask=dst_mask, port=dst_port)
    result = check_match(action, protocol, src, dest, device_acl)

    result.update({'changed': False})
    # result = {
    #     'changed': False,
    #     #'ansible_facts': {'cisco_ios': {'capabilities': facts['device_info']}}
    #     'out': test 
    # }
    module.exit_json(**result)


if __name__ == '__main__':
    main()






