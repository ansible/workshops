# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


from ansible.errors import AnsibleFilterError
from ansible.utils import helpers
from copy import deepcopy


def routeinfo_filter(route_list, alias='routeinfo_filter'):

    # Initialize empty  dict
    # This should result in route_type = { 'static': [ { 'network':
    # 1.1.1.1, nexthop: 2.2.2.2 }, { 'network': 101.1.1.1, nexthop:
    # 2.2.2.2}], 'bgp': [{' network': x.x.x.x, etc}], 'ospf': [] etc}
    route_type = {}
    static_routes = []
    bgp_routes = []
    ospf_routes = []
    connected_routes = []
    local_routes = []
    other_routes = []
    for route in route_list:
        if route.get('PROTOCOL') == 'S':
            static_routes.append(route)
        elif route.get('PROTOCOL') == 'B':
            bgp_routes.append(route)
        elif route.get('PROTOCOL') == 'O':
            ospf_routes.append(route)
        elif route.get('PROTOCOL') == 'C':
            connected_routes.append(route)
        elif route.get('PROTOCOL') == 'L':
            local_routes.append(route)
        else:
            other_routes.append(route)

    route_type['static'] = static_routes
    route_type['bgp'] = bgp_routes
    route_type['ospf'] = ospf_routes
    route_type['connected'] = connected_routes
    route_type['local'] = local_routes
    route_type['other'] = other_routes

    return route_type


# ---- Ansible filters ----
class FilterModule(object):
    ''' Route info  filter '''

    def filters(self):
        return {
            'sort_routes': routeinfo_filter
        }
