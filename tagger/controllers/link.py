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
"""Link controller"""

import tg
from tg import expose, tmpl_context, redirect, validate, require, flash
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tagger.model import DBSession, Link, Language
from tagger.lib.widgets import FormLinkNew, FormLinkEdit, FormLinkDelete
from repoze.what.predicates import has_permission

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormLinkNew(action=tg.url('/link/'))
f_edit = FormLinkEdit(action=tg.url('/link/'))
f_delete = FormLinkDelete(action=tg.url('/link/'))


class Controller(RestController):
    """REST controller for managing links"""

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.link.get_all')
    def get_all(self):
        """Return a list of links"""
        links = DBSession.query(Link).all()
        return dict(links=links, page=('admin', 'links'))

    @expose('json')
    @expose('tagger.templates.link.get_one')
    def get_one(self, linkid, languageid=None):
        """Return a single link"""
        link = DBSession.query(Link).get(linkid.decode())
        return dict(link=link, lang=languageid)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new

        fargs = dict()
        lang_list = [(l.id, l.name) for l in DBSession.query(Language).all()]
        fcargs = dict(languageid=dict(options=lang_list))
        return dict(title=_('Create a new Link'),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.forms.result')
    @validate(f_new, error_handler=new)
    def post(self, url, languageid, description):
        """create a new Link"""
        user = tmpl_context.user
        DBSession.add(Link(url, user, languageid, description))
        flash(_('Created Link "%s"') % url, 'ok')
        redirect(tg.url('/link/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, linkid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        link = DBSession.query(Link).get(linkid.decode())
        fargs = dict(linkid=link.id, id_=link.id,
                     url=link.url,
                     languageid=link.language_id,
                     description=link.description[''])
        languages = [(l.id, l.name) for l in DBSession.query(Language)]
        fcargs = dict(languageid=dict(options=languages))
        return dict(title='Edit link "%s"' % link.id, args=fargs,
                                                            child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.forms.result')
    @validate(f_edit, error_handler=edit)
    def put(self, linkid, url, languageid, description=None):
        """Edit a link"""
        link = DBSession.query(Link).get(linkid.decode())

        modified = False
        if link.url != url:
            link.url = url
            modified = True

        if link.description[languageid] != description:
            link.description[languageid] = description
            modified = True

        if modified:
            flash(_('updated link "%s"') % linkid, 'ok')
        else:
            flash(_('link "%s" unchanged') % linkid, 'info')
        redirect(tg.url('/link/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, linkid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        link = DBSession.query(Link).get(linkid.decode())
        fargs = dict(linkid=link.id,
                     id_=link.id,
                     url_=link.url,
                    )
        fcargs = dict()
        warning = _('This will delete the link entry in the database')
        return dict(
                title=_('Are you sure you want to delete Link "%s"?') %
                                                                link.id,
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.forms.result')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, linkid):
        """Delete a Link"""
        link = DBSession.query(Link).get(linkid.decode())

        for linkdata in link.data:
            DBSession.delete(linkdata)
        DBSession.delete(link)
        flash(_('Deleted Link "%s"') % link.id, 'ok')
        redirect(tg.url('/link/'))

    # REST-like methods
    _custom_actions = ['translation']
    
    @expose('json')
    def translation(self, linkid, value):
        """Return a link translation"""
        link = DBSession.query(Link).get(linkid)

        description = link.description[value]
        
        return dict(description=description)

