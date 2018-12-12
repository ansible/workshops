#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2018 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}

DOCUMENTATION = '''
---
module: textfsm_parser
author: Ansible Network Team
short_description: Parses text into JSON facts using TextFSM
description:
  - Provides textfsm rule based templates to parse data from text.
    The template acting as parser will iterate of the rules and parse
    the output of structured ASCII text into a JSON data structure
    that can be added to the inventory host facts.
requirements:
  - textfsm
version_added: "2.5"
options:
  file:
    description:
      - Path to the TextFSM parser to use to parse the output from a command.
        The C(file) argument accepts either a relative or absolute path
        to the TextFSM file.
    default: null
  src:
    description:
      - The C(src) argument can be used to load the content of a TextFSM
        parser file.  This argument allow the TextFSM parser to be loaded
        from an external source.  See EXAMPLES.
    default: null
  content:
    description:
      - The output of the command to parse using the rules in the TextFSM
        file.  The content should be a text string.
    required: true
  name:
    description:
      - The C(name) argument is used to define the top-level fact name to
        hold the output of the parser.  If this argument is not provided,
        the output from parsing will not be exported.
    default: null
'''

EXAMPLES = '''
- name: parse the content of a command
  textfsm_parser:
    file: files/parser_templates/show_interface.yaml
    content: "{{ lookup('file', 'output/show_interfaces.txt') }}"

- name: store returned facts into a key call output
  textfsm_parser:
    file: files/parser_templates/show_interface.yaml
    content: "{{ lookup('file', 'output/show_interfaces.txt') }}"
    name: output

- name: read the parser from an url
  textfsm_parser:
    src: "{{ lookup('url', 'http://server/path/to/parser') }}"
    content: "{{ lookup('file', 'output/show_interfaces.txt') }}"
'''
