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
"""Admin Controller"""

from tg import expose, flash, require, url, request, redirect, tmpl_context
from tg import validate, app_globals as G
from tg.exceptions import HTTPBadRequest
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from sqlalchemy import desc
from tagger.lib.base import BaseController
from tagger.model import DBSession, metadata, Language, Tag, Category
from tagger.model import Article, Media, Link, Comment, Setting
from tagger.lib.widgets import FormSettings

import logging
log = logging.getLogger(__name__)

__all__ = ['RootController']

f_settings = FormSettings(action=url('/admin/settings_set'))

class Controller(BaseController):
    """The admin controller for the tagger application."""
    allow_only = has_permission('manage')

    @expose('tagger.templates.admin.index')
    def index(self):
        """Handle the front-page."""
        return dict(path=('admin', ''))

    @expose('json')
    @expose('tagger.templates.admin.language')
    def language(self):
        """Return the list of all languages for administration"""
        languages = DBSession.query(Language).all()
        return dict(languages=languages, path=('admin', 'languages'))

    @expose('json')
    @expose('tagger.templates.admin.tag')
    def tag(self):
        """Return the list of all tags for administration"""
        tags = DBSession.query(Tag).all()
        return dict(tags=tags, path=('admin', 'tags'))

    @expose('json')
    @expose('tagger.templates.admin.category')
    def category(self):
        """Return the list of all categories for administration"""
        categories = DBSession.query(Category).all()
        return dict(categories=categories, path=('admin', 'categories'))

    @expose('json')
    @expose('tagger.templates.admin.article')
    def article(self):
        """Return the list of all articles for administration"""
        articles = DBSession.query(Article).order_by(desc('created')).all()
        return dict(articles=articles, path=('admin', 'articles'))

    @expose('json')
    @expose('tagger.templates.admin.media')
    def media(self,):
        """Return the list of all media for administration"""
        media = DBSession.query(Media).all()
        return dict(media=media, path=('admin', 'media'))

    @expose('json')
    @expose('tagger.templates.admin.link')
    def link(self):
        """Return the list of all links for administration"""
        links = DBSession.query(Link).all()
        return dict(links=links, path=('admin', 'links'))

    @expose('json')
    @expose('tagger.templates.admin.comment')
    def comment(self):
        """Return the list of all comments for administration"""
        comments = DBSession.query(Comment).order_by(desc('created')).all()
        return dict(comments=comments, path=('admin', 'comments'))

    @expose('json')
    @expose('tagger.templates.admin.settings')
    def settings(self):
        """Return a form to edit settings"""
        tmpl_context.f_settings = f_settings
        lang = tmpl_context.lang

        query = DBSession.query(Setting)
        settings = dict([('v_%s' % s.id, s.value) for s in query])
        fargs = settings

        querymedia = DBSession.query(Media).filter_by(type=u'image')
        media_list = [('', '')]
        media_list.extend([(m.id, m.name[lang]) for m in querymedia])
        link_list = [('', '')]
        link_list.extend([(l.id, l.name[lang]) for l in DBSession.query(Link)])
        cc_list = [
            ('', ''),
            ('cc by', 'CC Attribution'),
            ('cc by-sa', 'CC Attribution Share Alike'),
            ('cc by-nd', 'CC Attribution No Derivatives'),
            ('cc by-nc', 'CC Attribution Non-Commercial'),
            ('cc by-nc-sa', 'CC Attribution Non-Commercial Share Alike'),
            ('cc by-nc-nd', 'CC Attribution Non-Commercial No Derivatives'),
        ]
        fcargs = dict(v_banner_media=dict(options=media_list),
                      v_banner_link=dict(options=link_list),
                      v_theme = dict(options=G.themes),
                      v_cc = dict(options=cc_list),
                     )
        return dict(args=fargs, child_args=fcargs, path=('admin', 'settings'))

    @expose()
    @validate(f_settings, error_handler=settings)
    def settings_set(self, name=None, value=None):
        """Set settings values"""
        query = DBSession.query(Setting)
        settings = dict([(s.id, s) for s in query])
        if not len(name) == len(value):
            raise HTTPBadRequest("names and values don't match")

        modified = False
        for n, v in zip(name, value):
            if n in settings:
                if not settings[n].value == v:
                    settings[n].value = v
                    modified = True
            else:
                DBSession.add(Setting(n, v))
                modified = True

        if modified:
            flash(_('Updated Settings'), 'ok')
        else:
            flash(_('Settings are unchanged'), 'info')
        redirect(url('/admin/settings/'))

