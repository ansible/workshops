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
module: cli
author: Ansible Network Team
short_description: Runs the specific command and returns the output
description:
  - The command specified in C(command) will be executed on the remote
    device and its output will be returned to the module.  This module
    requires that the device is supported using the C(network_cli)
    connection plugin and has a valid C(cliconf) plugin to work correctly.
version_added: "2.5"
options:
  command:
    description:
      - The command to be executed on the remote node.  The value for this
        argument will be passed unchanged to the network device and the
        output returned.
    required: yes
    default: null
  parser:
    description:
      - The parser file to pass the output from the command through to
        generate Ansible facts.  If this argument is specified, the output
        from the command will be parsed based on the rules in the
        specified parser.
    default: null
  engine:
    description:
      - Defines the engine to use when parsing the output.  This argument
        accepts one of two valid values, C(command_parser) or C(textfsm_parser).
    default: command_parser
    choices:
      - command_parser
      - textfsm_parser
"""

EXAMPLES = """
- name: return show version
  cli:
    command: show version

- name: return parsed command output
  cli:
    command: show version
    parser: parser_templates/show_version.yaml
"""

RETURN = """
stdout:
  description: returns the output from the command
  returned: always
  type: dict
json:
  description: the output converted from json to a hash
  returned: always
  type: dict
"""

import json

from ansible.plugins.action import ActionBase
from ansible.module_utils.connection import Connection, ConnectionError
from ansible.module_utils._text import to_text
from ansible.errors import AnsibleError

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        ''' handler for cli operations '''

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        try:
            command = self._task.args['command']
            parser = self._task.args.get('parser')
            engine = self._task.args.get('engine', 'command_parser')
        except KeyError as exc:
            raise AnsibleError(to_text(exc))

        socket_path = getattr(self._connection, 'socket_path') or task_vars.get('ansible_socket')
        connection = Connection(socket_path)

        # make command a required argument
        if not command:
            raise AnsibleError('missing required argument `command`')

        try:
            output = connection.get(command)
        except ConnectionError as exc:
            raise AnsibleError(to_text(exc))

        result['stdout'] = output

        # try to convert the cli output to native json
        try:
            json_data = json.loads(output)
        except:
            json_data = None

        result['json'] = json_data

        if parser:
            if engine not in ('command_parser', 'textfsm_parser'):
                raise AnsibleError('missing or invalid value for argument engine')

            new_task = self._task.copy()
            new_task.args = {
                'file': parser,
                'content': (json_data or output)
            }

            kwargs = {
                'task': new_task,
                'connection': self._connection,
                'play_context': self._play_context,
                'loader': self._loader,
                'templar': self._templar,
                'shared_loader_obj': self._shared_loader_obj
            }

            task_parser = self._shared_loader_obj.action_loader.get(engine, **kwargs)
            result.update(task_parser.run(task_vars=task_vars))

        self._remove_tmp_path(self._connection._shell.tmpdir)

        # this is needed so the strategy plugin can identify the connection as
        # a persistent connection and track it, otherwise the connection will
        # not be closed at the end of the play
        socket_path = getattr(self._connection, 'socket_path') or task_vars.get('ansible_socket')
        self._task.args['_ansible_socket'] = socket_path

        return result
