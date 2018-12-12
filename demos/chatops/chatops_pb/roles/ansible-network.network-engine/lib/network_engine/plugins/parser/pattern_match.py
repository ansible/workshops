# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible.module_utils.six import iteritems


def get_value(m, i):
    return m.group(i) if m else None


class ParserEngine(object):

    def __init__(self, text):
        self.text = text

    def match(self, regex, match_all=None, match_until=None, match_greedy=None):
        """ Perform the regular expression match against the content

        :args regex: The regular expression pattern to use
        :args content: The content to run the pattern against
        :args match_all: Specifies if all matches of pattern should be returned
            or just the first occurrence

        :returns: list object of matches or None if there where no matches found
        """
        content = self.text

        if match_greedy:
            return self._match_greedy(content, regex, end=match_until, match_all=match_all)
        elif match_all:
            return self._match_all(content, regex)
        else:
            return self._match(content, regex)

    def _match_all(self, content, pattern):
        match = self.re_matchall(pattern, content)
        if match:
            return match

    def _match(self, content, pattern):
        match = self.re_search(pattern, content)
        return match

    def _match_greedy(self, content, start, end=None, match_all=None):
        """ Filter a section of the content text for matching

        :args content: The content to match against
        :args start: The start of the section data
        :args end: The end of the section data
        :args match_all: Whether or not to match all of the instances

        :returns: a list object of all matches
        """
        section_data = list()

        if match_all:
            while True:
                section_range = self._get_section_range(content, start, end)
                if not section_range:
                    break

                sidx, eidx = section_range

                if eidx is not None:
                    section_data.append(content[sidx: eidx])
                    content = content[eidx:]
                else:
                    section_data.append(content[sidx:])
                    break

        else:
            section_data.append(content)

        return section_data

    def _get_section_range(self, content, start, end=None):

        context_start_re = re.compile(start, re.M)
        if end:
            context_end_re = re.compile(end, re.M)
            include_end = True
        else:
            context_end_re = context_start_re
            include_end = False

        context_start = re.search(context_start_re, content)
        if not context_start:
            return

        string_start = context_start.start()
        end = context_start.end() + 1

        context_end = re.search(context_end_re, content[end:])
        if not context_end:
            return (string_start, None)

        if include_end:
            string_end = end + context_end.end()
        else:
            string_end = end + context_end.start()

        return (string_start, string_end)

    def _get_context_data(self, entry, content):
        name = entry['name']

        context = entry.get('context', {})
        context_data = list()

        if context:
            while True:
                context_range = self._get_context_range(name, context, content)

                if not context_range:
                    break

                start, end = context_range

                if end is not None:
                    context_data.append(content[start: end])
                    content = content[end:]
                else:
                    context_data.append(content[start:])
                    break

        else:
            context_data.append(content)

        return context_data

    def re_search(self, regex, value):
        obj = {'matches': []}
        regex = re.compile(regex, re.M)
        match = regex.search(value)
        if match:
            items = list(match.groups())
            if regex.groupindex:
                for name, index in iteritems(regex.groupindex):
                    obj[name] = items[index - 1]
            obj['matches'] = items
        return obj

    def re_matchall(self, regex, value):
        objects = list()
        regex = re.compile(regex)
        for match in re.findall(regex.pattern, value, re.M):
            obj = {}
            obj['matches'] = match
            if regex.groupindex:
                for name, index in iteritems(regex.groupindex):
                    if len(regex.groupindex) == 1:
                        obj[name] = match
                    else:
                        obj[name] = match[index - 1]
            objects.append(obj)
        return objects
