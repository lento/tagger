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
"""reStructuredText render module"""

from docutils.core import publish_parts
from mako.template import Template
from tagger.lib.render import widgets

def render_rst(text):
    return publish_parts(text, writer_name='html')['html_body']

def render_mak(text):
    template = Template(text, default_filters=['trim'])
    return template.render(**widgets)

def render_text(text):
    text = render_rst(text)
    text = render_mak(text)
    return text

