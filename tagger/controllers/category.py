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

from tg import expose, url, tmpl_context, redirect, validate, require
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tagger.model import DBSession, Category
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
    
    @expose('json')
    @expose('tagger.templates.category.get_all')
    def get_all(self):
        """Return list of categories"""
        categories = DBSession.query(Category).all()
        return dict(categories=categories)

    @expose('json')
    @expose('tagger.templates.category.get_one')
    def get_one(self, category_id):
        """Return a single category"""
        category = DBSession.query(Category).get(category_id)
        return dict(category=category)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new
        
        fargs = dict()
        fcargs = dict()
        return dict(title=_('Create a new Category'),
                                                args=fargs, child_args=fcargs)
    
    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.forms.result')
    @validate(f_new, error_handler=new)
    def post(self, name, description):
        """create a new Category"""
        DBSession.add(Category(name, description))
        return dict(msg=_('Created Category "%s"') % name, result='success')
    
    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, category_id, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        category = DBSession.query(Category).get(category_id)
        fargs = dict(category_id=category.id,
                     id_=category.id,
                     name_=category.name,
                    )
        fcargs = dict()
        warning = _('This will delete the category entry in the database')
        return dict(
                title=_('Are you sure you want to delete Category "%s"?') %
                                                                category.name,
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.forms.result')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, category_id):
        """Delete a Category"""
        category = DBSession.query(Category).get(category_id)
        
        DBSession.delete(category)
        return dict(msg='Deleted Category "%s"' % category.id, result='success')

