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
"""Category controller"""

from tg import expose, url, tmpl_context, validate, require, flash
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tagger.model import DBSession, Language, Category
from tagger.lib.widgets import FormCategoryNew, FormCategoryEdit
from tagger.lib.widgets import FormCategoryDelete
from repoze.what.predicates import has_permission

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormCategoryNew(action=url('/category/'))
f_edit = FormCategoryEdit(action=url('/category/'))
f_delete = FormCategoryDelete(action=url('/category/'))


class Controller(RestController):
    """REST controller for managing categories"""
    
    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.category.get_all')
    def get_all(self):
        """Return list of categories"""
        categories = DBSession.query(Category).all()
        return dict(categories=categories, page=('admin', 'categories'))

    @expose('json')
    @expose('tagger.templates.category.get_one')
    def get_one(self, categoryid):
        """Return a single category"""
        category = DBSession.query(Category).get(categoryid.decode())
        return dict(category=category)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new
        
        fargs = dict()
        lang_list = [(l.id, l.name) for l in DBSession.query(Language).all()]
        fcargs = dict(languageid=dict(options=lang_list))
        return dict(title=_('Create a new Category'),
                                                args=fargs, child_args=fcargs)
    
    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_new, error_handler=new)
    def post(self, name, languageid, description):
        """create a new Category"""
        DBSession.add(Category(name, languageid, description))
        flash(_('Created Category "%s"') % name, 'ok')
        return dict(redirect_to=url('/category/'))
    
    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, categoryid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        lang = tmpl_context.lang
        category = DBSession.query(Category).get(categoryid.decode())
        fargs = dict(categoryid=category.id, id_=category.id,
                     languageid=category.language_id,
                     name=category.name[lang],
                     description=category.description[lang])
        languages = [(l.id, l.name) for l in DBSession.query(Language)]
        fcargs = dict(languageid=dict(options=languages))
        return dict(title='Edit category "%s"' % category.id, args=fargs,
                                                            child_args=fcargs)
        
    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, categoryid, name, languageid, description=None):
        """Edit a category"""
        category = DBSession.query(Category).get(categoryid.decode())
        
        modified = False
        if category.name[languageid] != name:
            category.name[languageid] = name
            modified = True
        
        if category.description[languageid] != description:
            category.description[languageid] = description
            modified = True
        
        if modified:
            flash(_('updated category "%s"') % category.id, 'ok')
        else:
            flash(_('category "%s" unchanged') % category.id, 'info')
        return dict(redirect_to=url('/category/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, categoryid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        lang = tmpl_context.lang
        category = DBSession.query(Category).get(categoryid.decode())
        fargs = dict(categoryid=category.id,
                     id_=category.id,
                     name_=category.name[lang],
                    )
        fcargs = dict()
        warning = _('This will delete the category entry in the database')
        return dict(
                title=_('Are you sure you want to delete Category "%s"?') %
                                                                category.id,
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, categoryid):
        """Delete a Category"""
        category = DBSession.query(Category).get(categoryid.decode())
        
        for categorydata in category.data:
            DBSession.delete(categorydata)
        DBSession.delete(category)
        flash(_('Deleted Category "%s"') % category.id, 'ok')
        return dict(redirect_to=url('/category/'))

    # REST-like methods
    _custom_actions = ['translation']
    
    @expose('json')
    def translation(self, categoryid, value):
        """Return a category translation"""
        category = DBSession.query(Category).get(categoryid.decode())

        name = category.name[value]
        description = category.description[value]
        
        return dict(name=name, description=description)

