#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of Ansible
#
# Copyright 2018, Jimmy Conner <jconner@redhat.com>
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

# this is a windows documentation stub.  actual code lives in the .ps1
# file of the same name

DOCUMENTATION = '''
---
module: win_ad_dnsrecord
version_added: "2.6"
short_description: Manages DNS A Record on Windows DNS Server
description:
     - Manages DNS A Record on Windows DNS Server
options:
  hostname:
    description: Specifies a host name
    required: yes
  zone:
    description: Specifies the name of a DNS zone
    required: yes
  ipaddr:
    description: Specifies an IPv4 address (required if state = present)
    required: no
  timetolive:
    description: Specifies the Time to Live (TTL) value, in seconds, for a resource record. Specified in Time Format ex: 01:00:00
    required: no
    default: 01:00:00
  state:
    description: If present then a DNS record is created. If absent the DNS record is deleted
    choices: ['present', 'absent']
    default: 'present'
author: Jimmy Conner (jconner@redhat.com)
'''

EXAMPLES = r'''
- name: Create / Update DNS A Record
  win_ad_dnsrecord:
    hostname: myserver1
    zone: mydomain.pvt
    ipaddr: 192.168.0.2
    timetolive: 01:00:00
    state: present

- name: Remove DNS A Record
  win_ad_dnsrecord:
    hostname: myserver1
    zone: mydomain.pvt
    state: absent
'''