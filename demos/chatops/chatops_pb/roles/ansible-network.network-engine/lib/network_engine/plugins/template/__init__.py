# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections

from ansible.module_utils.six import iteritems, string_types
from ansible.errors import AnsibleUndefinedVariable


class TemplateBase(object):

    def __init__(self, templar):
        self._templar = templar

    def __call__(self, data, variables, convert_bare=False):
        return self.template(data, variables, convert_bare)

    def run(self, template, variables):
        pass

    def template(self, data, variables, convert_bare=False):

        if isinstance(data, collections.Mapping):
            templated_data = {}
            for key, value in iteritems(data):
                templated_key = self.template(key, variables, convert_bare=convert_bare)
                templated_value = self.template(value, variables, convert_bare=convert_bare)
                templated_data[templated_key] = templated_value
            return templated_data

        elif isinstance(data, collections.Iterable) and not isinstance(data, string_types):
            return [self.template(i, variables, convert_bare=convert_bare) for i in data]

        else:
            data = data or {}
            tmp_avail_vars = self._templar._available_variables
            self._templar.set_available_variables(variables)
            try:
                resp = self._templar.template(data, convert_bare=convert_bare)
                resp = self._coerce_to_native(resp)
            except AnsibleUndefinedVariable:
                resp = None
                pass
            finally:
                self._templar.set_available_variables(tmp_avail_vars)
            return resp

    def _coerce_to_native(self, value):
        if not isinstance(value, bool):
            try:
                value = int(value)
            except Exception:
                if value is None or len(value) == 0:
                    return None
                pass
        return value

    def _update(self, d, u):
        for k, v in iteritems(u):
            if isinstance(v, collections.Mapping):
                d[k] = self._update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def _check_conditional(self, when, variables):
        conditional = "{%% if %s %%}True{%% else %%}False{%% endif %%}"
        return self.template(conditional % when, variables)
