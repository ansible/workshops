# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}

DOCUMENTATION = """
---
module: validate_role_spec
author: Ansible Network Team
short_description: Validate required arguments are set from facts
description:
  - This module will accept an external argument spec file that will be used to
    validate arguments have been configured and set properly in order to allow
    the role to proceed.  This validate specification file provides the
    equivalent of the Ansible module argument spec.
version_added: "2.7"
options:
  spec:
    description:
      - Relative or absolute path to the arugment specification file to use to
        validate arguments are properly set for role execution.
    required: yes
"""

EXAMPLES = """
- name: use spec file for role validation
  validate_role_spec:
    spec: args.yaml
"""

RETURN = """
"""
import os
import json

from ansible.plugins.action import ActionBase
from ansible.module_utils._text import to_text, to_bytes
from ansible.module_utils.six import iteritems, string_types
from ansible.module_utils import basic
from ansible.errors import AnsibleModuleError

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(ActionBase):

    VALID_MODULE_KWARGS = (
        'argument_spec', 'mutually_exclusive', 'required_if',
        'required_one_of', 'required_together'
    )

    def run(self, tmp=None, task_vars=None):
        ''' handler for cli operations '''

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        try:
            spec = self._task.args['spec']
        except KeyError as exc:
            raise AnsibleModuleError(to_text(exc))

        if not spec:
            raise AnsibleModuleError('missing required argument: spec')

        spec_fp = os.path.join(task_vars['role_path'], 'meta/%s' % spec)
        display.vvv('using role spec %s' % spec_fp)
        spec = self._loader.load_from_file(spec_fp)

        argument_spec = spec.get('argument_spec') or {}

        args = {}
        for key, attrs in iteritems(argument_spec):
            if attrs is None:
                argument_spec[key] = {'type': 'str'}
            if key in task_vars:
                if isinstance(task_vars[key], string_types):
                    value = self._templar.do_template(task_vars[key])
                    if value:
                        args[key] = value
                else:
                    args[key] = task_vars[key]
            elif attrs:
                if 'aliases' in attrs:
                    for item in attrs['aliases']:
                        if item in task_vars:
                            args[key] = self._templar.do_template(task_vars[key])
                elif 'default' in attrs and key not in args:
                    args[key] = attrs['default']

        basic._ANSIBLE_ARGS = to_bytes(json.dumps({'ANSIBLE_MODULE_ARGS': args}))
        basic.AnsibleModule.fail_json = self.fail_json

        spec = dict([(k, v) for k, v in iteritems(spec) if k in self.VALID_MODULE_KWARGS])
        basic.AnsibleModule(**spec)

        self._remove_tmp_path(self._connection._shell.tmpdir)

        return result

    def fail_json(self, msg):
        raise AnsibleModuleError(msg)
