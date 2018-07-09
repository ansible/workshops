# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.loader import PluginLoader

template_loader = PluginLoader(
    'TemplateEngine',
    'network_engine.plugins.template',
    None,
    'template_plugins',
    required_base_class='TemplateBase'
)

parser_loader = PluginLoader(
    'ParserEngine',
    'network_engine.plugins.parser',
    None,
    'parser_plugins',
    # required_base_class='ParserBase'
)
