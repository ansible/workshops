# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections

from ansible.module_utils.six import string_types

from network_engine.plugins.template import TemplateBase


class TemplateEngine(TemplateBase):

    def run(self, template, variables=None):

        templated_items = {}

        for item in template:
            key = self.template(item['key'], variables)

            # FIXME moving to the plugin system breaks this
            when = item.get('when')
            if when is not None:
                if not self._check_conditional(when, variables):
                    continue

            if 'value' in item:
                value = item.get('value')
                items = None
                item_type = None

            elif 'object' in item:
                items = item.get('object')
                item_type = 'dict'

            elif 'elements' in item:
                items = item.get('elements')
                item_type = 'list'

            loop = item.get('repeat_for')
            loop_data = self.template(loop, variables) if loop else None
            loop_var = item.get('repeat_var', 'item')

            if items:
                if loop:
                    if isinstance(loop_data, collections.Iterable) and not isinstance(loop_data, string_types):
                        templated_value = list()

                        for loop_item in loop_data:
                            variables[loop_var] = loop_item
                            if isinstance(items, string_types):
                                templated_value.append(self.template(items, variables))
                            else:
                                templated_value.append(self.run(items, variables))

                        if item_type == 'list':
                            templated_items[key] = templated_value

                        elif item_type == 'dict':
                            if key not in templated_items:
                                templated_items[key] = {}

                            for t in templated_value:
                                templated_items[key] = self._update(templated_items[key], t)
                    else:
                        templated_items[key] = []

                else:
                    val = self.run(items, variables)

                    if item_type == 'list':
                        templated_value = [val]
                    else:
                        templated_value = val

                    templated_items[key] = templated_value

            else:
                templated_value = self.template(value, variables)
                templated_items[key] = templated_value

        return templated_items
