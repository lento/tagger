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
"""Page render module"""

import cgi
from docutils.core import publish_parts
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from mako.template import Template
from tagger.lib.widgets import LinkWidget

w_link = LinkWidget()


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

        text = '${w_link(linkid=%s, label="%s")}' % (linkid, label)
        link_node = nodes.raw(rawsource='', text=text, format='html')
        return [link_node]

directives.register_directive('link', LinkDirective)


def render_rst(text):
    return publish_parts(text, writer_name='html')['html_body']

def render_mak(text):
    template = Template(text, default_filters=['trim'])
    widgets = dict(w_link=w_link)
    return template.render(**widgets)

def render_text(text):
    text = render_rst(text)
    text = render_mak(text)
    return text

