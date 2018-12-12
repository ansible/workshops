# Copyright (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible.module_utils.six import string_types
from ansible.errors import AnsibleFilterError


def interface_split(interface, key=None):
    match = re.match(r'([A-Za-z\-]*)(.+)', interface)
    if not match:
        raise AnsibleFilterError('unable to parse interface %s' % interface)
    obj = {'name': match.group(1), 'index': match.group(2)}
    if key:
        return obj[key]
    else:
        return obj


def interface_range(interface):
    if not isinstance(interface, string_types):
        raise AnsibleFilterError('value must be of type string, got %s' % type(interface))

    parts = interface.rpartition('/')
    if parts[1]:
        prefix = '%s/' % parts[0]
        index = parts[2]
    else:
        match = re.match(r'([A-Za-z]*)(.+)', interface)
        if not match:
            raise AnsibleFilterError('unable to parse interface %s' % interface)
        prefix = match.group(1)
        index = match.group(2)

    indicies = list()

    for item in index.split(','):
        tokens = item.split('-')

        if len(tokens) == 1:
            indicies.append(tokens[0])

        elif len(tokens) == 2:
            start, end = tokens
            for i in range(int(start), int(end) + 1):
                indicies.append(i)
                i += 1

    return ['%s%s' % (prefix, index) for index in indicies]


def _gen_ranges(vlan):
    s = e = None
    for i in sorted(vlan):
        if s is None:
            s = e = i
        elif i == e or i == e + 1:
            e = i
        else:
            yield (s, e)
            s = e = i
    if s is not None:
        yield (s, e)


def vlan_compress(vlan):
    if not isinstance(vlan, list):
        raise AnsibleFilterError('value must be of type list, got %s' % type(vlan))

    return (','.join(['%d' % s if s == e else '%d-%d' % (s, e) for (s, e) in _gen_ranges(vlan)]))


def vlan_expand(vlan):
    if not isinstance(vlan, string_types):
        raise AnsibleFilterError('value must be of type string, got %s' % type(vlan))

    match = re.match(r'([A-Za-z]*)(.+)', vlan)
    if not match:
        raise AnsibleFilterError('unable to parse vlan %s' % vlan)

    index = match.group(2)
    indices = list()

    for item in index.split(','):
        tokens = item.split('-')

        if len(tokens) == 1:
            indices.append(int(tokens[0]))

        elif len(tokens) == 2:
            start, end = tokens
            for i in range(int(start), int(end) + 1):
                indices.append(i)
                i += 1

    return ['%d' % int(index) for index in indices]


def to_lines(value):
    if isinstance(value, (list, set, tuple)):
        return value
    elif isinstance(value, string_types):
        return value.split('\n')
    raise AnsibleFilterError('cannot convert value to lines')


class FilterModule(object):
    ''' Network interface filter '''

    def filters(self):
        return {
            'interface_split': interface_split,
            'interface_range': interface_range,
            'vlan_compress': vlan_compress,
            'vlan_expand': vlan_expand,
            'to_lines': to_lines
        }
