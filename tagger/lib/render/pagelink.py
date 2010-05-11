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
"""Page link render module"""

import cgi
from tw.api import Widget
from docutils.parsers.rst import Directive
from docutils import nodes


############################################################
# render widgets
############################################################
class PageLinkWidget(Widget):
    """Render a PageLink object"""
    params = ['pageid', 'lang', 'label']
    template = 'mako:tagger.templates.widgets.pagelink'

    lang = ''
    label = None


############################################################
# reStructuredText directives
############################################################
class PageLinkDirective(Directive):
    """Return a PageLinkWidget invocation"""
    required_arguments = 1
    optional_arguments = 1
    option_spec = {}
    has_content = False

    def run(self):
        pageid = self.arguments[0]
        if len(self.arguments) > 1:
            label = self.arguments[1]
        elif isinstance(self.state.parent, nodes.substitution_definition):
            label = self.state.parent['names'][0]
        else:
            label = ''
        label = cgi.escape(label)

        text = '${w_pagelink(pageid="%s", label="%s", lang=lang)}' % (
                                                                pageid, label)
        pagelink_node = nodes.raw(rawsource='', text=text, format='html')
        return [pagelink_node]

