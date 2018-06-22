# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action.cli import ActionModule as ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        self._display.deprecated('the `cli_get` module has been deprecated, please use `cli` instead')
        return super(ActionModule, self).run(tmp, task_vars)
