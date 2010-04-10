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
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect, response
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates

from tagger.lib.base import BaseController
from tagger.controllers.error import ErrorController
from tagger.controllers import admin, language, category, article, link
from tagger.model import DBSession, Language, Category, Article

__all__ = ['RootController']


class RootController(BaseController):
    """The root controller for the tagger application."""
    admin = admin.Controller()
    error = ErrorController()
    category = category.Controller()
    language = language.Controller()
    article = article.Controller()
    link = link.Controller()

    @expose('tagger.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('tagger.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from='/'):
        """Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.
        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """Redirect the user to the root page on logout and say
        goodbye as well."""
        flash(_('We hope to see you soon!'))
        redirect(url('/'))

    @expose('tagger.templates.article.get_one')
    def _default(self, categoryname, stringid, language_id=None):
        category = DBSession.query(Category).filter_by(
                                            name=categoryname.decode()).one()
        article = DBSession.query(Article).filter_by(
                    category_id=category.id, string_id=stringid.decode()).one()
        return self.article.get_one(article.id, language_id)

    @expose()
    def set_language(self, languageid, came_from=url('/')):
        """Set language cookie"""
        language = DBSession.query(Language).get(languageid.decode())
        response.set_cookie('lang', language.id)
        flash('%s %s' % (_('Preferred language set to'), language.name))
        redirect(came_from)

    @expose()
    def unset_language(self, came_from=url('/')):
        """Delete language cookie"""
        response.delete_cookie('lang')
        flash(_('No preferred language'))
        redirect(came_from)


