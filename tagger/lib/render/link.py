# -*- coding: utf-8 -*-
#
# This file is part of Tagger.
#
# Tagger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tagger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tagger.  If not, see <http://www.gnu.org/licenses/>.
#
# Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
# Contributor(s): 
#
"""Link render module"""

import cgi
from tw.api import Widget
from docutils.parsers.rst import Directive
from docutils import nodes


############################################################
# render widgets
############################################################
class LinkWidget(Widget):
    """Render a Link object"""
    params = ['linkid', 'lang', 'label']
    template = 'mako:tagger.templates.widgets.link'

    lang = None
    label = None


############################################################
# reStructuredText directives
############################################################
class LinkDirective(Directive):
    """Return a LinkWidget invocation"""
    required_arguments = 1
    optional_arguments = 1
    option_spec = {}
    has_content = False

    def run(self):
        linkid = int(self.arguments[0])
        if len(self.arguments) > 1:
            label = self.arguments[1]
        elif isinstance(self.state.parent, nodes.substitution_definition):
            label = self.state.parent['names'][0]
        else:
            label = ''
        label = cgi.escape(label)

        text = '${w_link(linkid=%s, label="%s", lang=lang)}' % (linkid, label)
        link_node = nodes.raw(rawsource='', text=text, format='html')
        return [link_node]

