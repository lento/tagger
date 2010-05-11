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
from tg import tmpl_context, override_template
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates
from tg.exceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound

from tagger.lib.base import BaseController
from tagger.lib.widgets import FormLogin
from tagger.controllers.error import ErrorController
from tagger.controllers import admin, language, category, article, link, media
from tagger.controllers import tag, comment, page
from tagger.model import DBSession, Language, Category, Article

__all__ = ['RootController']

f_login = FormLogin(action=url('/login_handler'))


class RootController(BaseController):
    """The root controller for the tagger application."""
    admin = admin.Controller()
    error = ErrorController()
    category = category.Controller()
    language = language.Controller()
    article = article.Controller()
    link = link.Controller()
    media = media.Controller()
    tag = tag.Controller()
    comment = comment.Controller()
    page = page.Controller()

    @expose('tagger.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(path=('home', ''))

    @expose('tagger.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        tmpl_context.f_login = f_login

        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        fargs = dict(came_from=came_from, logins=str(login_counter))
        return dict(page='login', fargs=fargs)

    @expose()
    def post_login(self, came_from='/'):
        """Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.
        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash('%s, %s!' % (_('Welcome back'), userid))
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """Redirect the user to the root page on logout and say
        goodbye as well."""
        flash(_('We hope to see you soon!'))
        redirect('/')

    @expose()
    def set_language(self, languageid, came_from=url('/')):
        """Set language cookie"""
        language = DBSession.query(Language).get(languageid.decode())
        response.set_cookie('lang', language.id)
        flash('%s %s' % (_('Preferred language set to:'), language.name))
        redirect(came_from)

    @expose()
    def unset_language(self, came_from=url('/')):
        """Delete language cookie"""
        response.delete_cookie('lang')
        flash(_('No preferred language'))
        redirect(came_from)

    @expose()
    def _default(self, *args, **kwargs):
        """Catch requests for "/<category>" or "/<category>/<article>" and
        serve them through the article controller, otherwise rise a "Not Found"
        error"""
        if len(args) > 0:
            categoryid = args[0]
            category = DBSession.query(Category).get(categoryid.decode())
        else:
            category = None

        if len(args) > 1:
            articleid = args[1]
            article = DBSession.query(Article).get(articleid.decode())
        else:
            article = None

        if len(args) > 2:
            languageid = args[2]
        else:
            languageid = None

        tag = kwargs.get('tag', None)
        mode = kwargs.get('mode', 'all')

        if article:
            override_template(self._default,
                                        'mako:tagger.templates.article.get_one')
            result = self.article.get_one(article.id, languageid)
            result.update(path=(category.id, ''))
            return result
        elif category:
            override_template(self._default,
                                        'mako:tagger.templates.article.get_all')
            result = self.article.get_all(categoryid=category.id, tag=tag,
                                                                    mode=mode)
            result.update(path=(category.id, ''))
            return result
        else:
            raise HTTPNotFound


