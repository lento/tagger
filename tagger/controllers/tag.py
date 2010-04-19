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
"""Tag controller"""

from tg import expose, tmpl_context, validate, require, flash, url
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tagger.model import DBSession, Tag, Language
from tagger.lib.widgets import FormTagNew, FormTagEdit, FormTagDelete
from repoze.what.predicates import has_permission

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormTagNew(action=url('/tag/'))
f_edit = FormTagEdit(action=url('/tag/'))
f_delete = FormTagDelete(action=url('/tag/'))


class Controller(RestController):
    """REST controller for managing tags"""

    @expose('json')
    @expose('tagger.templates.tag.get_all')
    def get_all(self):
        """Return a list of tags"""
        tags = DBSession.query(Tag).all()
        return dict(tags=tags)

    @expose('json')
    @expose('tagger.templates.tag.get_one')
    def get_one(self, tagid, languageid=None):
        """Return a single tag"""
        tag = DBSession.query(Tag).get(tagid.decode())
        return dict(tag=tag, lang=languageid)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new

        fargs = dict()
        lang_list = [(l.id, l.name) for l in DBSession.query(Language).all()]
        fcargs = dict(languageid=dict(options=lang_list))
        return dict(title=_('Create a new Tag'),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_new, error_handler=new)
    def post(self, name, languageid):
        """create a new Tag"""
        user = tmpl_context.user
        tag = Tag(name, languageid)
        DBSession.add(tag)
        flash(_('Created Tag "%s"') % tag.id, 'ok')
        return dict(redirect_to=url('/admin/tag/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, tagid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        tag = DBSession.query(Tag).get(tagid.decode())
        fargs = dict(tagid=tag.id, id_=tag.id,
                     languageid=tag.language_id,
                     name=tag.name[''],
                    )
        languages = [(l.id, l.name) for l in DBSession.query(Language)]
        fcargs = dict(languageid=dict(options=languages))
        return dict(title='Edit tag "%s"' % tag.id, args=fargs,
                                                            child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, tagid, name, languageid):
        """Edit a tag"""
        tag = DBSession.query(Tag).get(tagid.decode())

        modified = False
        if tag.name[languageid] != name:
            tag.name[languageid] = name
            modified = True

        if modified:
            flash(_('updated tag "%s"') % tagid, 'ok')
        else:
            flash(_('tag "%s" unchanged') % tagid, 'info')
        return dict(redirect_to=url('/admin/tag/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, tagid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        tag = DBSession.query(Tag).get(tagid.decode())
        fargs = dict(tagid=tag.id,
                     id_=tag.id,
                    )
        fcargs = dict()
        warning = _('This will delete the tag entry in the database')
        return dict(
                title=_('Are you sure you want to delete Tag "%s"?') %
                                                                tag.id,
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, tagid):
        """Delete a Tag"""
        tag = DBSession.query(Tag).get(tagid.decode())

        for tagdata in tag.data:
            DBSession.delete(tagdata)
        DBSession.delete(tag)
        flash(_('Deleted Tag "%s"') % tag.id, 'ok')
        return dict(redirect_to=url('/admin/tag/'))

    # REST-like methods
    _custom_actions = ['translation']
    
    @expose('json')
    def translation(self, tagid, value):
        """Return a tag translation"""
        tag = DBSession.query(Tag).get(tagid.decode())

        name = tag.name[value]
        
        return dict(name=name)

