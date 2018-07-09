# -*- coding: utf-8 -*-

# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        ''' handler for textfsm action '''
        display.deprecated(msg='the `textfsm` module has been deprecated, please use `textfsm_parser` instead',
                           version='2.6',
                           removed=False)

        if task_vars is None:
            task_vars = dict()

        del tmp  # tmp no longer has any effect

        new_task = self._task.copy()
        new_task.args = {
            'file': self._task.args.get('file'),
            'src': self._task.args.get('src'),
            'content': self._task.args['content'],
            'name': self._task.args.get('name')
        }

        kwargs = {
            'task': new_task,
            'connection': self._connection,
            'play_context': self._play_context,
            'loader': self._loader,
            'templar': self._templar,
            'shared_loader_obj': self._shared_loader_obj
        }

        textfsm_action = self._shared_loader_obj.action_loader.get('textfsm_parser', **kwargs)
        result = textfsm_action.run(task_vars=task_vars)

        return result
