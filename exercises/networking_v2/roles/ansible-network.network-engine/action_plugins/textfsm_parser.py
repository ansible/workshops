# -*- coding: utf-8 -*-

# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.six import StringIO, string_types

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError

try:
    import textfsm
    HAS_TEXTFSM = True
except ImportError:
    HAS_TEXTFSM = False


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        ''' handler for textfsm action '''

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        try:
            if not HAS_TEXTFSM:
                raise AnsibleError('textfsm_parser engine requires the TextFSM library to be installed')

            try:
                filename = self._task.args.get('file')
                src = self._task.args.get('src')
                content = self._task.args['content']
                name = self._task.args.get('name')
            except KeyError as exc:
                raise AnsibleError('missing required argument: %s' % exc)

            if src and filename:
                raise AnsibleError('`src` and `file` are mutually exclusive arguments')

            if not isinstance(content, string_types):
                return {'failed': True, 'msg': '`content` must be of type str, got %s' % type(content)}

            if filename:
                tmpl = open(filename)
            else:
                tmpl = StringIO()
                tmpl.write(src.strip())
                tmpl.seek(0)

            try:
                re_table = textfsm.TextFSM(tmpl)
                fsm_results = re_table.ParseText(content)

            except Exception as exc:
                raise AnsibleError(str(exc))

            final_facts = []
            for item in fsm_results:
                facts = {}
                facts.update(dict(zip(re_table.header, item)))
                final_facts.append(facts)

            if name:
                result['ansible_facts'] = {name: final_facts}
            else:
                result['ansible_facts'] = {}

        finally:
            self._remove_tmp_path(self._connection._shell.tmpdir)

        return result
