# (c) 2018 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
lookup: json_template
author: Ansible Network
version_added: "2.5"
short_description: retrieve and template device configuration
description:
  - This plugin lookups the content(key-value pair) of a JSON file
    and returns network configuration in JSON format.
options:
  _terms:
    description: File for lookup
"""

EXAMPLES = """
- name: show interface lookup result
  debug: msg="{{ lookup('json_template', './show_interface.json') }}
"""

RETURN = """
_raw:
   description: JSON file content
"""

import json
import os
import sys

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase, display
from ansible.module_utils._text import to_bytes

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir, 'lib'))
from network_engine.plugins import template_loader


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        ret = list()

        self.ds = variables.copy()
        self.template = template_loader.get('json_template', self._templar)

        display.debug("File lookup term: %s" % terms[0])

        lookupfile = self.find_file_in_search_path(variables, 'files', terms[0])
        display.vvvv("File lookup using %s as file" % lookupfile)
        try:
            if lookupfile:
                with open(to_bytes(lookupfile, errors='surrogate_or_strict'), 'rb') as f:
                    json_data = list()
                    json_data.append(json.load(f))
                    ret.append(self.template.run(json_data, self.ds))
            else:
                raise AnsibleParserError()
        except AnsibleParserError:
            raise AnsibleError("could not locate file in lookup: %s" % terms[0])

        return ret
