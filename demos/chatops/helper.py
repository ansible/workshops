#!/usr/bin/env python

import netaddr

def validate_network(net):
    pass

def get_ipmask(net):
  try:
     ip, mask = net.split("/")
  except ValueError:
     net = net + "/32"
  ip, mask = net.split("/")
  network = netaddr.IPNetwork(net)
  result = dict(ip_address=ip, ip_mask=str(network.netmask))
  return result

def validate_input(user_input):
    #{u'protocol': u'tcp', u'source_network': u'10.3.3.3', u'destination_network': u'10.0.0.0/24', u'port': u'2222'}
    result = {}
    result['protocol'] = user_input['protocol']
    result['dst_port'] = user_input['port']
    result['action'] = user_input['action']
    result['src_network'] = get_ipmask(user_input['source_network']).get('ip_address')
    result['src_mask'] =  get_ipmask(user_input['source_network']).get('ip_mask')
    result['dst_network'] = get_ipmask(user_input['destination_network']).get('ip_address')
    result['dst_mask'] =  get_ipmask(user_input['destination_network']).get('ip_mask')
    return result
