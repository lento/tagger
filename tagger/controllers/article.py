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
"""Article controller"""

from tg import expose, url, tmpl_context, redirect, validate, require
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tagger.model import DBSession, Language, Category, Article
from tagger.lib.widgets import FormArticleNew, FormArticleEdit
from tagger.lib.widgets import FormArticleDelete
from repoze.what.predicates import has_permission

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormArticleNew(action=url('/article/'))
f_edit = FormArticleEdit(action=url('/article/'))
f_delete = FormArticleDelete(action=url('/article/'))


class Controller(RestController):
    """REST controller for managing articles"""

    @expose('json')
    @expose('tagger.templates.article.get_all')
    def get_all(self):
        """Return a list of articles"""
        articles = DBSession.query(Article).all()
        return dict(articles=articles)

    @expose('json')
    @expose('tagger.templates.article.get_one')
    def get_one(self, article_id):
        """Return a single article"""
        query = DBSession.query(Article)
        if article_id.isdigit():
            article = query.get(int(article_id))
        else:
            article = query.filter_by(string_id=article_id.decode()).one()

        return dict(article=article)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new

        fargs = dict()
        
        cat_list = [(c.id, c.name) for c in DBSession.query(Category).all()]
        lang_list = [(l.id, l.name) for l in DBSession.query(Language).all()]
        fcargs = dict(category_id=dict(options=cat_list),
                                            language_id=dict(options=lang_list))
        return dict(title=_('Create a new Article'),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.forms.result')
    @validate(f_new, error_handler=new)
    def post(self, title, category_id, language_id, text):
        """create a new Article"""
        user = tmpl_context.user
        category = DBSession.query(Category).get(category_id)
        DBSession.add(Article(title, category, language_id, user, text))
        return dict(msg=_('Created Article "%s"') % title, result='success')

    # TODO: how do we edit articles and pages?
    '''
    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, article_id, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        article = DBSession.query(Article).get(article_id)
        fargs = dict(article_id=article.id, id_=article.id,
                     name=article.name)
        fcargs = dict()
        return dict(title='Edit category "%s"' % article.id, args=fargs,
                                                            child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.forms.result')
    @validate(f_edit, error_handler=edit)
    def put(self, article_id, name):
        """Edit a article"""
        article = DBSession.query(Article).get(article_id.decode())

        modified = False
        if article.name != name:
            article.name = name
            modified = True

        if modified:
            return dict(msg='updated article "%s"' %
                                                article_id, result='success')
        return dict(msg='article "%s" unchanged' %
                                                article_id, result='success')
    '''

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, article_id, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        query = DBSession.query(Article)
        if article_id.isdigit():
            article = query.get(int(article_id))
        else:
            article = query.filter_by(string_id=article_id.decode()).one()

        fargs = dict(article_id=article.id,
                     id_=article.id,
                     title_=article.title[''],
                    )
        fcargs = dict()
        warning = _('This will delete the article entry in the database')
        return dict(
                title=_('Are you sure you want to delete Article "%s"?') %
                                                            article.title[''],
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.forms.result')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, article_id):
        """Delete a Article"""
        query = DBSession.query(Article)
        if article_id.isdigit():
            article = query.get(int(article_id))
        else:
            article = query.filter_by(string_id=article_id.decode()).one()

        DBSession.delete(article)
        return dict(msg='Deleted Article "%s"' % article.id, result='success')

