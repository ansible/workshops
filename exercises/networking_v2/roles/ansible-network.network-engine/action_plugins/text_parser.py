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
        display.deprecated(msg='the `text_parser` module has been deprecated, please use `command_parser` instead',
                           version='2.6',
                           removed=False)

        del tmp # tmp no longer has any effect

        if task_vars is None:
            task_vars = dict()

        new_task = self._task.copy()
        new_task.args = {
            'dir': self._task.args.get('dir'),
            'file': self._task.args.get('file'),
            'content': self._task.args['content']
        }

        kwargs = {
            'task': new_task,
            'connection': self._connection,
            'play_context': self._play_context,
            'loader': self._loader,
            'templar': self._templar,
            'shared_loader_obj': self._shared_loader_obj
        }

        text_parser_action = self._shared_loader_obj.action_loader.get('command_parser', **kwargs)
        result = text_parser_action.run(task_vars=task_vars)

        return result
