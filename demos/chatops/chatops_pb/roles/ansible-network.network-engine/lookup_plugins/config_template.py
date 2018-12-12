# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2012-17 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
lookup: config_template
author: Peter Sprygada (privateip)
version_added: "2.7"
short_description: retrieve contents of file after templating with Jinja2
description:
  - This lookup plugin implements the standard template plugin with a slight
    twist in that it supports using default(omit) to remove an entire line
options:
  _terms:
    description: list of files to template
"""

EXAMPLES = """
- name: show templating results
  debug: msg="{{ lookup('config_template', './some_template.j2') }}
"""

RETURN = """
_raw:
   description: file(s) content after templating
"""
from ansible.plugins.lookup.template import LookupModule as LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        ret = super(LookupModule, self).run(terms, variables, **kwargs)

        omit = variables['omit']
        filtered = list()

        for line in ret[0].split('\n'):
            if all((line, omit not in line, not line.startswith('!'))):
                filtered.append(line)

        return [filtered]
