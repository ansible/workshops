# -*- coding: utf-8 -*-

# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
lookup: network_template
author: Ansible Network
version_added: "2.5"
short_description: template device configuration
description:
  - This plugin will lookup the file and template it into a network
    configuration.
options:
  _terms:
    description: list of files to template
"""

EXAMPLES = """
- name: show config template results
  debug: msg="{{ lookup('network_template', './config_template.j2') }}
"""

RETURN = """
_raw:
   description: file(s) content after templating
"""


import collections

from ansible.plugins.lookup import LookupBase, display
from ansible.module_utils.network.common.utils import to_list
from ansible.module_utils.six import iteritems, string_types
from ansible.module_utils._text import to_text, to_bytes
from ansible.errors import AnsibleError, AnsibleUndefinedVariable


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):
        self.ds = variables.copy()

        config_lines = list()

        for term in to_list(terms[0]):
            display.debug("File lookup term: %s" % term)

            lookupfile = self.find_file_in_search_path(variables, 'templates', term)
            display.vvvv("File lookup using %s as file" % lookupfile)

            if lookupfile:
                with open(to_bytes(lookupfile, errors='surrogate_or_strict'), 'rb'):
                    tasks = self._loader.load_from_file(lookupfile)

                    for task in tasks:
                        task.pop('name', None)

                        register = task.pop('register', None)

                        when = task.pop('when', None)
                        if when is not None:
                            if not self._check_conditional(when, self.ds):
                                display.vvv('skipping task due to conditional check failure')
                                continue

                        loop = task.pop('loop', None)

                        if loop:
                            loop = self.template(loop, self.ds)
                            loop_result = list()

                            if isinstance(loop, collections.Mapping):
                                for loop_key, loop_value in iteritems(loop):
                                    self.ds['item'] = {'key': loop_key, 'value': loop_value}
                                    res = self._process_directive(task)
                                    if res:
                                        loop_result.extend(to_list(res))

                            elif isinstance(loop, collections.Iterable) and not isinstance(loop, string_types):
                                for loop_item in loop:
                                    self.ds['item'] = loop_item
                                    res = self._process_directive(task)
                                    if res:
                                        loop_result.extend(to_list(res))

                            config_lines.extend(loop_result)

                            if register:
                                self.ds[register] = loop_result

                        else:
                            res = self._process_directive(task)
                            if res:
                                config_lines.extend(to_list(res))
                                if register:
                                    self.ds[register] = res

            else:
                raise AnsibleError("the template file %s could not be found for the lookup" % term)

        return [to_text('\n'.join(config_lines)).strip()]

    def do_context(self, block):

        results = list()

        for entry in block:
            task = entry.copy()

            when = task.pop('when', None)
            if when is not None:
                if not self._check_conditional(when, self.ds):
                    display.vvv('skipping context due to conditional check failure')
                    continue

            loop = task.pop('loop', None)
            if loop:
                loop = self.template(loop, self.ds)

            if 'context' in task:
                res = self.do_context(task['context'])
                if res:
                    results.extend(res)

            elif isinstance(loop, collections.Mapping):
                loop_result = list()
                for loop_key, loop_value in iteritems(loop):
                    self.ds['item'] = {'key': loop_key, 'value': loop_value}
                    loop_result.extend(to_list(self._process_directive(task)))
                results.extend(loop_result)

            elif isinstance(loop, collections.Iterable) and not isinstance(loop, string_types):
                loop_result = list()
                for loop_item in loop:
                    self.ds['item'] = loop_item
                    loop_result.extend(to_list(self._process_directive(task)))
                results.extend(loop_result)

            else:
                res = self._process_directive(task)
                if res:
                    results.extend(to_list(res))

        return results

    def _process_directive(self, task):
        for directive, args in iteritems(task):
            if directive == 'context':
                meth = getattr(self, 'do_%s' % directive)
                if meth:
                    return meth(args)
            else:
                meth = getattr(self, 'do_%s' % directive)
                if meth:
                    return meth(**args)

    def do_lines_template(self, template, join=False, when=None, required=False):
        templated_lines = list()
        _processed = list()

        if when is not None:
            if not self._check_conditional(when, self.ds):
                display.vvv("skipping due to conditional failure")
                return templated_lines

        for line in to_list(template):
            res = self.template(line, self.ds)
            if res:
                _processed.append(res)
            elif not res and join:
                break

        if required and not _processed:
            raise AnsibleError('unabled to templated required line')
        elif _processed and join:
            templated_lines.append(' '.join(_processed))
        elif _processed:
            templated_lines.extend(_processed)

        return templated_lines

    def _process_include(self, item, variables):
        name = item.get('name')
        include = item['include']

        src = self.template(include, variables)
        source = self._find_needle('templates', src)

        when = item.get('when')

        if when:
            conditional = "{%% if %s %%}True{%% else %%}False{%% endif %%}"
            if not self.template(conditional % when, variables, fail_on_undefined=False):
                display.vvvvv("include '%s' skipped due to conditional check failure" % name)
                return []

        display.display('including file %s' % source)
        include_data = self._loader.load_from_file(source)

        template_data = item.copy()

        # replace include directive with block directive and contents of
        # included file.  this will preserve other values such as loop,
        # loop_control, etc
        template_data.pop('include')
        template_data['block'] = include_data

        return self.build([template_data], variables)

    def template(self, data, variables, convert_bare=False):

        if isinstance(data, collections.Mapping):
            templated_data = {}
            for key, value in iteritems(data):
                templated_key = self.template(key, variables, convert_bare=convert_bare)
                templated_data[templated_key] = self.template(value, variables, convert_bare=convert_bare)
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
        return value

    def _check_conditional(self, when, variables):
        conditional = "{%% if %s %%}True{%% else %%}False{%% endif %%}"
        return self.template(conditional % when, variables)
