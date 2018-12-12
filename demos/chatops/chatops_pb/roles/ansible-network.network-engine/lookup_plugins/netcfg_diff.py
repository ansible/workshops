# (c) 2018 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
lookup: netcfg_diff
author: Ansible Network
version_added: "2.5"
short_description: Generates a text configuration difference between two configuration
                   mainly used with network devices.
description:
  - This plugin lookups will generate a difference between two text configuration that
    is supported by Network OS. This difference can be used to identify the
    exact change that is required to be pushed to remote host.
options:
  _terms:
    description:
      - Specifies the wanted text configuration. Theis is usually
        the text configuration that is expected to be present on remote host.
    required: True
  have:
    description:
      - Specifies the text configuration. The C(have) is usually
        the text configuration that is active on remote host.
    required: True
  match:
    description:
      - Instructs the module on the way to perform the matching of
        the set of text commands between C(want) and C(have).
        If match is set to I(line), commands are matched line by line.  If
        match is set to I(strict), command lines are matched with respect
        to position.  If match is set to I(exact), command lines
        must be an equal match.
    default: line
    choices: ['line', 'strict', 'exact']
  replace:
    description:
      - Instructs the module on the way to perform the configuration
        diff.  If the replace argument is set to I(line) then
        the modified lines are pushed in the generated diff. If the replace argument
        is set to I(block) then the entire command block is pushed in the generated
        diff if any line is not correct.
    default: line
    choices: ['line', 'block']
  indent:
    description:
      - Specifies the indentation used for the block in text configuration. The value of C(indent)
        is specific on network platform to which the text configuration in C(want) and C(have)
        conforms to.
    default: 1
    type: int
  ignore_lines:
    description:
      - This specifies the lines to be ignored while generating diff. The value of C(ignore_lines) can
        also be a python regex.

"""

EXAMPLES = """
- name: generate diff between two text configuration
  debug: msg="{{ lookup('netcfg_diff', want, have=have) }}
"""

RETURN = """
_raw:
   description: The text difference between values of want and have with want as base reference
"""

from ansible.plugins.lookup import LookupBase
from ansible.module_utils.network.common.config import NetworkConfig, dumps
from ansible.errors import AnsibleError


MATCH_CHOICES = ('line', 'strict', 'exact')
REPLACE_CHOICES = ('line', 'block')


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        ret = []

        try:
            want = terms[0]
        except IndexError:
            raise AnsibleError("value of 'want' must be specified")

        try:
            have = kwargs['have']
        except KeyError:
            raise AnsibleError("value of 'have' must be specified")

        match = kwargs.get('match', 'line')
        if match not in MATCH_CHOICES:
            choices_str = ", ".join(MATCH_CHOICES)
            raise AnsibleError("value of match must be one of: %s, got: %s" % (choices_str, match))

        replace = kwargs.get('replace', 'line')
        if replace not in REPLACE_CHOICES:
            choices_str = ", ".join(REPLACE_CHOICES)
            raise AnsibleError("value of replace must be one of: %s, got: %s" % (choices_str, replace))

        indent = int(kwargs.get('indent', 1))
        ignore_lines = kwargs.get('ignore_lines')

        running_obj = NetworkConfig(indent=indent, contents=have, ignore_lines=ignore_lines)
        candidate_obj = NetworkConfig(indent=indent, contents=want, ignore_lines=ignore_lines)

        configobjs = candidate_obj.difference(running_obj, match=match, replace=replace)

        diff = dumps(configobjs, output='commands')
        ret.append(diff)

        return ret
