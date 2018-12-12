# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys
import collections

from ansible import constants as C
from ansible.plugins.action import ActionBase
from ansible.module_utils.six import iteritems, string_types
from ansible.module_utils._text import to_text
from ansible.errors import AnsibleError

try:
    from ansible.module_utils.network.common.utils import to_list
except ImportError:
    # keep role compatible with Ansible 2.4
    from ansible.module_utils.network_common import to_list

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir, 'lib'))
from network_engine.plugins import template_loader, parser_loader
from network_engine.utils import dict_merge


try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


def warning(msg):
    if C.ACTION_WARNINGS:
        display.warning(msg)


class ActionModule(ActionBase):

    VALID_FILE_EXTENSIONS = ('.yaml', '.yml', '.json')
    VALID_GROUP_DIRECTIVES = ('pattern_group', 'block')
    VALID_ACTION_DIRECTIVES = ('parser_metadata', 'pattern_match', 'set_vars', 'json_template')
    VALID_DIRECTIVES = VALID_GROUP_DIRECTIVES + VALID_ACTION_DIRECTIVES
    VALID_EXPORT_AS = ('list', 'elements', 'dict', 'object', 'hash')

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            source_dir = self._task.args.get('dir')
            source_file = self._task.args.get('file')
            content = self._task.args['content']
        except KeyError as exc:
            return {'failed': True, 'msg': 'missing required argument: %s' % exc}

        if source_dir and source_file:
            return {'failed': True, 'msg': '`dir` and `file` are mutually exclusive arguments'}

        if source_dir:
            sources = self.get_files(to_list(source_dir))
        else:
            if source_file:
                sources = to_list(source_file)
            else:
                searchpath = []
                searchpath = task_vars.get('ansible_search_path', [])
                if not searchpath:
                    searchpath.append(self._loader._basedir)

                if 'parser_templates' in os.listdir(searchpath[0]):
                    subdir_searchpath = os.path.join(searchpath[0], 'parser_templates')

                    # parser in {{ playbook_dir }}/parser_templates/{{ ansible_network_os }}
                    if task_vars['ansible_network_os'] in os.listdir(subdir_searchpath):
                        newsearchpath = os.path.join(subdir_searchpath, task_vars['ansible_network_os'])
                        sources = self.get_parser(path=newsearchpath)

                    # parser in {{ playbook_dir }}/parser_templates
                    else:
                        sources = self.get_parser(path=subdir_searchpath)

                # parser in {{ playbook_dir }}
                else:
                    sources = self.get_parser(path=searchpath[0])

        facts = {}

        self.template = template_loader.get('json_template', self._templar)

        for src in sources:
            src_path = os.path.expanduser(src)
            if not os.path.exists(src_path) and not os.path.isfile(src_path):
                raise AnsibleError("src [%s] is either missing or invalid" % src_path)

            tasks = self._loader.load_from_file(src)

            self.ds = {'content': content}
            self.ds.update(task_vars)

            for task in tasks:
                name = task.pop('name', None)
                display.vvvv('processing directive: %s' % name)

                register = task.pop('register', None)
                extend = task.pop('extend', None)
                if extend:
                    extend = self.template(extend, self.ds)

                export = task.pop('export', False)
                export_as = task.pop('export_as', 'list')
                export_as = self.template(export_as, self.ds)
                if export_as not in self.VALID_EXPORT_AS:
                    raise AnsibleError('invalid value for export_as, got %s' % export_as)

                if 'export_facts' in task:
                    task['set_vars'] = task.pop('export_facts')
                    export = True
                elif 'set_vars' not in task:
                    if export and not register:
                        warning('entry will not be exported due to missing register option')

                when = task.pop('when', None)
                if when is not None:
                    if not self._check_conditional(when, self.ds):
                        display.vvv('command_parser: skipping task [%s] due to conditional check' % name)
                        continue

                loop = task.pop('loop', None)
                loop_var = task.pop('loop_control', {}).get('loop_var') or 'item'

                if loop is not None:
                    loop = self.template(loop, self.ds)
                    if not loop:
                        display.vvv('command_parser: loop option was defined but no loop data found')
                    res = list()

                    if loop:
                        # loop is a hash so break out key and value
                        if isinstance(loop, collections.Mapping):
                            for loop_key, loop_value in iteritems(loop):
                                self.ds[loop_var] = {'key': loop_key, 'value': loop_value}
                                resp = self._process_directive(task)
                                res.append(resp)

                        # loop is either a list or a string
                        else:
                            for loop_item in loop:
                                self.ds[loop_var] = loop_item
                                resp = self._process_directive(task)
                                res.append(resp)

                        if 'set_vars' in task:
                            if register:
                                self.ds[register] = res
                                if export:
                                    if extend:
                                        facts.update(self.merge_facts(task_vars, extend, register, res))
                                    else:
                                        facts[register] = res
                            else:
                                self.ds.update(res)
                                if export:
                                    facts.update(res)
                        elif register:
                            self.ds[register] = res
                            if export:
                                if export_as in ('dict', 'hash', 'object'):
                                    if extend:
                                        facts.update(self.merge_facts(task_vars, extend, register, res, expand=True))
                                    else:
                                        if register not in facts:
                                            facts[register] = {}
                                        for item in res:
                                            facts[register] = self.rec_update(facts[register], item)
                                else:
                                    if extend:
                                        facts.update(self.merge_facts(task_vars, extend, register, res))
                                    else:
                                        facts[register] = res
                else:
                    res = self._process_directive(task)
                    if 'set_vars' in task:
                        if register:
                            self.ds[register] = res
                            if export:
                                if extend:
                                    facts.update(self.merge_facts(task_vars, extend, register, res))
                                else:
                                    facts[register] = res
                        else:
                            self.ds.update(res)
                            if export:
                                facts.update(res)
                    elif res and register:
                        self.ds[register] = res
                        if export:
                            if register:
                                if extend:
                                    facts.update(self.merge_facts(task_vars, extend, register, res))
                                else:
                                    facts[register] = res
                            else:
                                for r in to_list(res):
                                    for k, v in iteritems(r):
                                        facts.update({to_text(k): v})

                task_vars.update(facts)

        result.update({
            'ansible_facts': facts,
            'included': sources
        })

        return result

    def merge_facts(self, task_vars, extend, register, res, expand=False):
        update = self.build_update(extend, register, res, expand)
        root = extend.split('.')[0]
        current = {root: task_vars.get(root, {})}
        return dict_merge(current, update)

    def build_update(self, path, child, value, expand=False):
        """Build an update based on the current results

        This method will take the current results and build a nested dict
        object.  The keys for the nested dict object are identified by
        path.

        :param path: The path of the nest keys

        :param child: The child key name to assign the value to

        :param value: The value to assign to the child key

        :param expand: When set to True, this will iterate over the value

        :returns: A nest dict object
        """
        update_set = dict()
        working_set = update_set

        if expand is True:
            for key in path.split('.'):
                working_set[key] = dict()
                working_set = working_set[key]
            working_set[child] = {}
            for item in value:
                working_set[child] = self.rec_update(working_set[child], item)
        else:
            for key in path.split('.'):
                working_set[key] = dict()
                working_set = working_set[key]
            working_set[child] = value

        return update_set

    def get_parser(self, path):
        sources = list()
        src_file = list()

        for i in os.listdir(path):
            if i.startswith('show_'):
                f, ext = os.path.splitext(i)
                if ext in self.VALID_FILE_EXTENSIONS:
                    src_file.append(i)

        if len(src_file) == 1:
            sources.append(os.path.join(path, src_file[0]))
        elif len(src_file) == 0:
            raise AnsibleError("no parser file found in {0}, please create a parser".format(path))
        else:
            raise AnsibleError("too many files in {0}, please use `file` or `dir` parameter".format(path))

        return sources

    def get_files(self, source_dirs):
        include_files = list()
        _processed = set()

        for source_dir in source_dirs:
            if not os.path.isdir(source_dir):
                raise AnsibleError('%s does not appear to be a valid directory' % source_dir)

            for filename in os.listdir(source_dir):
                fn, fext = os.path.splitext(filename)
                if fn not in _processed:
                    _processed.add(fn)

                    filename = os.path.join(source_dir, filename)

                    if not os.path.isfile(filename) or fext not in self.VALID_FILE_EXTENSIONS:
                        continue
                    else:
                        include_files.append(filename)

        return include_files

    def rec_update(self, d, u):
        for k, v in iteritems(u):
            if isinstance(v, collections.Mapping):
                d[k] = self.rec_update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def do_pattern_group(self, block):

        results = list()
        registers = {}

        for entry in block:
            task = entry.copy()

            name = task.pop('name', None)
            display.vvv("command_parser: starting pattern_match [%s] in pattern_group" % name)

            register = task.pop('register', None)

            when = task.pop('when', None)
            if when is not None:
                if not self._check_conditional(when, self.ds):
                    warning('skipping task due to conditional check failure')
                    continue

            loop = task.pop('loop', None)
            if loop:
                loop = self.template(loop, self.ds)

            loop_var = task.pop('loop_control', {}).get('loop_var') or 'item'
            display.vvvv('command_parser: loop_var is %s' % loop_var)

            if not set(task).issubset(('pattern_group', 'pattern_match')):
                raise AnsibleError('invalid directive specified')

            if 'pattern_group' in task:
                if loop and isinstance(loop, collections.Iterable) and not isinstance(loop, string_types):
                    res = list()
                    for loop_item in loop:
                        self.ds[loop_var] = loop_item
                        res.append(self.do_pattern_group(task['pattern_group']))
                else:
                    res = self.do_pattern_group(task['pattern_group'])

                if res:
                    results.append(res)
                if register:
                    registers[register] = res

            elif isinstance(loop, collections.Iterable) and not isinstance(loop, string_types):
                loop_result = list()

                for loop_item in loop:
                    self.ds[loop_var] = loop_item
                    loop_result.append(self._process_directive(task))

                results.append(loop_result)

                if register:
                    registers[register] = loop_result

            else:
                res = self._process_directive(task)
                if res:
                    results.append(res)
                if register:
                    registers[register] = res

        return registers

    def _process_directive(self, task):
        for directive, args in iteritems(task):
            if directive == 'block':
                display.deprecated('`block` is not longer supported, use `pattern_group` instead')
                directive = 'pattern_group'

            if directive not in self.VALID_DIRECTIVES:
                raise AnsibleError('invalid directive in parser: %s' % directive)

            meth = getattr(self, 'do_%s' % directive)

            if meth:
                if directive in self.VALID_GROUP_DIRECTIVES:
                    return meth(args)
                elif directive in self.VALID_ACTION_DIRECTIVES:
                    return meth(**args)
            else:
                raise AnsibleError('invalid directive: %s' % directive)

    def do_parser_metadata(self, version=None, command=None, network_os=None):
        if version:
            display.vvv('command_parser: using parser version %s' % version)

        if network_os not in (None, self.ds['ansible_network_os']):
            raise AnsibleError('parser expected %s, got %s' % (network_os, self.ds['ansible_network_os']))

    def do_pattern_match(self, regex, content=None, match_all=None, match_until=None, match_greedy=None):
        content = self.template(content, self.ds) or self.template("{{ content }}", self.ds)
        regex = self.template(regex, self.ds)
        parser = parser_loader.get('pattern_match', content)
        return parser.match(regex, match_all, match_until, match_greedy)

    def do_json_template(self, template):
        return self.template.run(template, self.ds)

    def do_set_vars(self, **kwargs):
        return self.template(kwargs, self.ds)

    def _check_conditional(self, when, variables):
        conditional = "{%% if %s %%}True{%% else %%}False{%% endif %%}"
        return self.template(conditional % when, variables)
