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
"""Media render module"""

import cgi
from tw.api import Widget
from docutils.parsers.rst import directives, Directive
from docutils import nodes

media_types = ['image', 'video', 'youtube', 'vimeo']


############################################################
# render widgets
############################################################
class MediaWidget(Widget):
    """Render a Media object"""
    params = ['mediaid', 'lang', 'label']
    template = 'mako:tagger.templates.widgets.media'

    lang = None
    label = None


############################################################
# reStructuredText directives
############################################################
class MediaDirective(Directive):
    """Return a MediaWidget invocation"""
    required_arguments = 1
    optional_arguments = 1
    option_spec = {'width': directives.nonnegative_int,
                   'height': directives.nonnegative_int,
                  }
    has_content = False

    def run(self):
        mediaid = self.arguments[0]
        if len(self.arguments) > 1:
            label = self.arguments[1]
        elif isinstance(self.state.parent, nodes.substitution_definition):
            label = self.state.parent['names'][0]
        else:
            label = ''
        label = cgi.escape(label)

        width = self.options.get('width', None)
        height = self.options.get('height', None)

        text = ('${w_media(mediaid="%s", '
                          'label="%s", '
                          'width=%s, '
                          'height=%s, '
                          'lang=lang)}' % (mediaid, label, width, height))
        media_node = nodes.raw(rawsource='', text=text, format='html')
        return [media_node]



