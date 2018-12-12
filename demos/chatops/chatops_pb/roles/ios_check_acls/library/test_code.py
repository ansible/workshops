#!/usr/bin/env python
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


if __name__ == "__main__":
    #gather_input()
    # Test data
    src = {'network': '10.1.1.2', 'mask': '255.255.255.255'}
    dest = {'network': '172.17.33.128', 'mask': '255.255.255.128',
            'port': '2223'}
    protocol = 'udp'
    action = 'deny'
    print(result)
