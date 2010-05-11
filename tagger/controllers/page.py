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
"""Page controller"""

from tg import expose, tmpl_context, validate, require, flash, url
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from tagger.model import DBSession, Page, Language, Article
from tagger.model.helpers import tags_from_string
from tagger.lib.widgets import FormPageNew, FormPageEdit, FormPageDelete
from tagger.lib.widgets import ObjectTitle
from tagger.lib.utils import find_related, find_recent

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormPageNew(action=url('/page/'))
f_edit = FormPageEdit(action=url('/page/'))
f_delete = FormPageDelete(action=url('/page/'))

w_object_title = ObjectTitle()

class Controller(RestController):
    """REST controller for managing pages"""

    @expose('json')
    @expose('tagger.templates.page.get_all')
    def get_all(self, articleid=None):
        """Return a list of pages"""
        tmpl_context.w_object_title = w_object_title
        article = DBSession.query(Article).get(articleid.decode())

        return dict(pages=article.pages, recent=find_recent())

    @expose('json')
    @expose('tagger.templates.page.get_one')
    def get_one(self, articleid, pagestringid, languageid=None):
        """Return a single page"""
        tmpl_context.w_object_title = w_object_title
        article = DBSession.query(Article).get(articleid.decode())
        page = article.pages[pagestringid]

        if languageid:
            lang = languageid
        elif tmpl_context.lang:
            lang = tmpl_context.lang
        else:
            lang = page.language_id

        return dict(article=article, page=page, lang=lang,
                                            related=find_related(obj=article))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, articleid, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new
        article = DBSession.query(Article).get(articleid.decode())

        fargs = dict(articleid=article.id)
        lang_list = [(l.id, l.name) for l in DBSession.query(Language)]
        fcargs = dict(languageid=dict(options=lang_list))
        return dict(title=_('Create a new Page'), args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_new, error_handler=new)
    def post(self, articleid, name, languageid, text=None):
        """create a new Page"""
        user = tmpl_context.user
        article = DBSession.query(Article).get(articleid.decode())
        page = Page(name, languageid, user, text)
        article.pages.append(page)
        DBSession.flush()

        flash('%s %s' % (_('Created Page:'), page.string_id), 'ok')
        return dict(redirect_to=url('/article/%s/edit' % article.id))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, articleid, pagestringid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        article = DBSession.query(Article).get(articleid.decode())
        page = article.pages[pagestringid]

        fargs = dict(pageid=page.id, id_=page.id,
                     languageid=page.language_id,
                     name=page.name[''],
                     text=page.text[''],
                    )

        languages = [(l.id, l.name) for l in DBSession.query(Language)]
        fcargs = dict(languageid=dict(options=languages))
        return dict(title='%s %s' % (_('Edit page:'), page.string_id),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, pageid, name, languageid, text=None):
        """Edit a page"""
        lang = tmpl_context.lang or DBSession.query(Language).first().id
        page = DBSession.query(Page).get(pageid)

        modified = False
        if page.name[languageid] != name:
            page.name[languageid] = name
            modified = True

        if page.text[languageid] != text:
            page.text[languageid] = text
            modified = True

        if modified:
            flash('%s %s' % (_('Updated Page:'), page.string_id), 'ok')
        else:
            flash('%s %s' % (_('Page is unchanged:'), page.string_id), 'info')
        return dict(redirect_to=url('/article/%s/edit' % page.article.id))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, articleid, pagestringid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        article = DBSession.query(Article).get(articleid.decode())
        page = article.pages[pagestringid]

        fargs = dict(pageid=page.id,
                     id_=page.id,
                     stringid_=page.string_id,
                    )
        fcargs = dict()
        warning = _('This will delete the Page from the database')
        return dict(
                title='%s %s ?' % (
                    _('Are you sure you want to delete Page:'),
                    page.string_id),
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, pageid):
        """Delete a Page"""
        page = DBSession.query(Page).get(pageid)

        for pagedata in page.data:
            DBSession.delete(pagedata)
        DBSession.delete(page)
        flash('%s %s' % (_('Deleted Page:'), page.string_id), 'ok')
        return dict(redirect_to=url('/article/%s/edit' % page.article.id))

    # REST-like methods
    _custom_actions = ['translation']
    
    @expose('json')
    def translation(self, pageid, value):
        """Return a page translation"""
        page = DBSession.query(Page).get(pageid)

        name = page.name[value]
        text = page.text[value]
        
        return dict(name=name, text=text)

