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
"""Language controller"""

from tg import expose, url, tmpl_context, validate, require, flash
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tagger.model import DBSession, Language
from tagger.lib.widgets import FormLanguageNew, FormLanguageEdit
from tagger.lib.widgets import FormLanguageDelete
from repoze.what.predicates import has_permission

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormLanguageNew(action=url('/language/'))
f_edit = FormLanguageEdit(action=url('/language/'))
f_delete = FormLanguageDelete(action=url('/language/'))


class Controller(RestController):
    """REST controller for managing languages"""

    @expose('json')
    @expose('tagger.templates.language.get_all')
    def get_all(self):
        """Return a list of languages"""
        languages = DBSession.query(Language).all()
        return dict(languages=languages)

    @expose('json')
    @expose('tagger.templates.language.get_one')
    def get_one(self, languageid):
        """Return a single language"""
        language = DBSession.query(Language).get(languageid.decode())
        return dict(language=language)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new

        fargs = dict()
        fcargs = dict()
        return dict(title=_('Create a new Language'),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_new, error_handler=new)
    def post(self, languageid, name):
        """create a new Language"""
        language = Language(languageid, name)
        DBSession.add(language)
        flash('%s %s' % (_('Created Language:'), language.id), 'ok')
        return dict(redirect_to=url('/admin/language/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, languageid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        language = DBSession.query(Language).get(languageid.decode())
        fargs = dict(languageid=language.id, id_=language.id,
                     name=language.name)
        fcargs = dict()
        return dict(title='%s %s' % (_('Edit Language:'), language.id),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, languageid, name):
        """Edit a language"""
        language = DBSession.query(Language).get(languageid.decode())

        modified = False
        if language.name != name:
            language.name = name
            modified = True

        if modified:
            flash('%s %s' % (_('Updated Language:'), language.id), 'ok')
        else:
            flash('%s %s' % (_('Language is unchanged:'), language.id), 'info')
        return dict(redirect_to=url('/admin/language/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, languageid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        language = DBSession.query(Language).get(languageid.decode())
        fargs = dict(languageid=language.id,
                     id_=language.id,
                     name_=language.name,
                    )
        fcargs = dict()
        warning = _('This will delete the Language from the database')
        return dict(
                title='%s %s ?' % (
                    _('Are you sure you want to delete Language:'),
                    language.name),
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, languageid):
        """Delete a Language"""
        language = DBSession.query(Language).get(languageid.decode())

        DBSession.delete(language)
        flash('%s %s' % (_('Deleted Language:'), language.id), 'ok')
        return dict(redirect_to=url('/admin/language/'))

