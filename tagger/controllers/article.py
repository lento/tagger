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

from tg import expose, url, tmpl_context, validate, require, flash
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

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.article.get_all')
    def get_all(self):
        """Return a list of articles"""
        articles = DBSession.query(Article).all()
        return dict(articles=articles, page=('admin', 'articles'))

    @expose('json')
    @expose('tagger.templates.article.get_one')
    def get_one(self, articleid, languageid=None):
        """Return a single article"""
        article = DBSession.query(Article).get(articleid.decode())
        if languageid:
            lang = languageid
        elif tmpl_context.lang:
            lang = tmpl_context.lang
        else:
            lang = article.language_id

        return dict(article=article, lang=lang)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new
        lang = tmpl_context.lang

        fargs = dict()
        
        cat_list = [(c.id, c.name[lang]) for c in DBSession.query(Category)]
        lang_list = [(l.id, l.name) for l in DBSession.query(Language)]
        fcargs = dict(categoryid=dict(options=cat_list),
                                            languageid=dict(options=lang_list))
        return dict(title=_('Create a new Article'),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_new, error_handler=new)
    def post(self, title, categoryid, languageid, text):
        """create a new Article"""
        user = tmpl_context.user
        category = DBSession.query(Category).get(categoryid)
        DBSession.add(Article(title, category, languageid, user, text))
        flash(_('Created Article "%s"') % title, 'ok')
        return dict(redirect_to=url('/article/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.article.edit')
    def edit(self, articleid, **kwargs):
        """Return a page to edit an article and all its pages"""
        tmpl_context.f_edit = f_edit
        lang = tmpl_context.lang
        article = DBSession.query(Article).get(articleid.decode())

        categories = [(c.id, c.name[lang]) for c in DBSession.query(Category)]
        languages = [(l.id, l.name) for l in DBSession.query(Language)]
        fargs = dict(articleid=article.id,
                     id_=article.id,
                     categoryid=article.category_id,
                     languageid=article.language_id,
                     title=article.title[''],
                     text=article.text[''],
                    )
        fcargs = dict(categoryid=dict(options=categories),
                      languageid=dict(options=languages),
                     )
        return dict(article=article, page=('admin', None), args=fargs,
                                                            child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, articleid, title, categoryid, languageid, text=None):
        """Edit a article"""
        article = DBSession.query(Article).get(articleid.decode())

        modified = False
        if article.title[languageid] != title:
            article.title[languageid] = title
            modified = True
            log.debug('article.put title: %s - %s' % (article.title[languageid], title))

        if article.category_id != categoryid:
            article.category_id = categoryid
            modified = True
            log.debug('article.put category: %s - %s' % (article.category_id, categoryid))

        if article.text[languageid] != text:
            article.text[languageid] = text
            modified = True
            log.debug('article.put text: %s - %s' % (article.text[languageid], text))

        if modified:
            flash(_('updated article "%s"') % articleid, 'ok')
        else:
            flash(_('article "%s" unchanged') % articleid, 'info')
        return dict(redirect_to=url('/article/%s/edit' % article.id))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, articleid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        article = DBSession.query(Article).get(articleid.decode())

        fargs = dict(articleid=article.id,
                     id_=article.id,
                     title_=article.title[''],
                    )
        fcargs = dict()
        warning = _('This will delete the article and all its pages')
        return dict(
                title=_('Are you sure you want to delete Article "%s"?') %
                                                            article.title[''],
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, articleid):
        """Delete a Article"""
        article = DBSession.query(Article).get(articleid.decode())

        for page in article.pages:
            for pagedata in page.data:
                DBSession.delete(pagedata)
            DBSession.delete(page)
        DBSession.delete(article)
        flash(_('Deleted Article "%s"') % article.id, 'ok')
        return dict(redirect_to=url('/article/'))


    # REST-like methods
    _custom_actions = ['translation']
    
    @expose('json')
    def translation(self, articleid, value):
        """Return a article translation"""
        log.debug('article.translation: %s %s' % (articleid, value))
        article = DBSession.query(Article).get(articleid.decode())

        title = article.title[value]
        text = article.text[value]
        
        return dict(title=title, text=text)


