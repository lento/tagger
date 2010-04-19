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

from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission

from tagger.lib.base import BaseController
from tagger.model import DBSession, metadata, Language, Tag, Category
from tagger.model import Article, Media, Link

__all__ = ['RootController']


class Controller(BaseController):
    """The admin controller for the tagger application."""
    allow_only = has_permission('manage')

    @expose('tagger.templates.admin.index')
    def index(self):
        """Handle the front-page."""
        return dict(page=('admin', ''))

    @expose('json')
    @expose('tagger.templates.admin.language')
    def language(self):
        """Return a list of languages"""
        languages = DBSession.query(Language).all()
        return dict(languages=languages, page=('admin', 'languages'))

    @expose('json')
    @expose('tagger.templates.admin.tag')
    def tag(self):
        """Return a list of tags"""
        tags = DBSession.query(Tag).all()
        return dict(tags=tags, page=('admin', 'tags'))

    @expose('json')
    @expose('tagger.templates.admin.category')
    def category(self):
        """Return list of categories"""
        categories = DBSession.query(Category).all()
        return dict(categories=categories, page=('admin', 'categories'))

    @expose('json')
    @expose('tagger.templates.admin.media')
    def media(self,):
        """Return the list of all media for administration"""
        media = DBSession.query(Media).all()
        return dict(media=media, page=('admin', 'media'))

    @expose('json')
    @expose('tagger.templates.admin.link')
    def link(self):
        """Return a list of links"""
        links = DBSession.query(Link).all()
        return dict(links=links, page=('admin', 'links'))


