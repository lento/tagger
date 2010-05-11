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
from tg import url
from tagger.lib.render import widgets

defaults = {'file_insertion_enabled': 0,
            'raw_enabled': 0,
            'report_level': 4,
            '_disable_config': 1,
           }

def render_rst(text):
    rst = publish_parts(text, writer_name='html', settings_overrides=defaults)
    return rst['html_body']

def render_rst_summary(text):
    rst = publish_parts(text, writer_name='html', settings_overrides=defaults)
    text = rst['html_body']
    short, moretag, rest = text.partition('<!-- more -->')
    has_more = not rest == ''
    return short, has_more

def render_mak(text, lang=None):
    template = Template(text, default_filters=['trim'])
    return template.render_unicode(lang=lang or '', **widgets)

def render_text(text, lang=''):
    text = render_rst(text)
    text = render_mak(text, lang)
    return text

def render_summary(text, lang=''):
    text, has_more = render_rst_summary(text)
    text = render_mak(text, lang)
    return text, has_more

