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

from tg import expose, tmpl_context, validate, require, flash, url
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from tagger.model import DBSession, Link, Language
from tagger.model.helpers import tags_from_string
from tagger.lib.widgets import FormLinkNew, FormLinkEdit, FormLinkDelete
from tagger.lib.widgets import ObjectTitle
from tagger.lib.utils import find_related, find_recent

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormLinkNew(action=url('/link/'))
f_edit = FormLinkEdit(action=url('/link/'))
f_delete = FormLinkDelete(action=url('/link/'))

w_object_title = ObjectTitle()

class Controller(RestController):
    """REST controller for managing links"""

    @expose('json')
    @expose('tagger.templates.link.get_all')
    def get_all(self, tag=[], mode='all'):
        """Return a list of links"""
        tmpl_context.w_object_title = w_object_title
        links = DBSession.query(Link).all()

        if tag:
            tagids = isinstance(tag, list) and tag or [tag]
            tagstring = ', '.join(tagids)
            tags = set(tags_from_string(tagstring, create=False))
            if mode == 'all':
                links = [obj for obj in links if set(obj.tags) >= (tags)]
            elif mode == 'any':
                links = [obj for obj in links if set(obj.tags) & (tags)]

        return dict(links=links, recent=find_recent(), page=('links', ''))

    @expose('json')
    @expose('tagger.templates.link.get_one')
    def get_one(self, linkid, languageid=None):
        """Return a single link"""
        tmpl_context.w_object_title = w_object_title
        link = DBSession.query(Link).get(linkid.decode())

        if languageid:
            lang = languageid
        elif tmpl_context.lang:
            lang = tmpl_context.lang
        else:
            lang = link.language_id

        return dict(link=link, lang=lang, related=find_related(obj=link))

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
    @expose('tagger.templates.redirect_parent')
    @validate(f_new, error_handler=new)
    def post(self, name, uri, languageid, description=None, tagids=None):
        """create a new Link"""
        user = tmpl_context.user
        lang = tmpl_context.lang or DBSession.query(Language).first().id
        link = Link(name, uri, user, languageid, description)
        DBSession.add(link)

        tags = tags_from_string(tagids, lang=lang)
        link.tags[:] = tags

        flash('%s %s' % (_('Created Link:'), link.id), 'ok')
        return dict(redirect_to=url('/admin/link/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, linkid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        lang = tmpl_context.lang
        link = DBSession.query(Link).get(linkid.decode())

        tags = ', '.join([t.name[lang] for t in link.tags])
        fargs = dict(linkid=link.id, id_=link.id,
                     uri=link.uri,
                     languageid=link.language_id,
                     name=link.name[''],
                     description=link.description[''],
                     tagids=tags,
                    )

        languages = [(l.id, l.name) for l in DBSession.query(Language)]
        fcargs = dict(languageid=dict(options=languages))
        return dict(title='%s %s' % (_('Edit link:'), link.id),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, linkid, name, uri, languageid, description=None, tagids=None):
        """Edit a link"""
        lang = tmpl_context.lang or DBSession.query(Language).first().id
        link = DBSession.query(Link).get(linkid.decode())

        modified = False
        if link.uri != uri:
            link.uri = uri
            modified = True

        if link.name[languageid] != name:
            link.name[languageid] = name
            modified = True

        if link.description[languageid] != description:
            link.description[languageid] = description
            modified = True

        tags = tags_from_string(tagids, lang=lang)
        if link.tags != tags:
            link.tags[:] = tags
            modified = True

        if modified:
            flash('%s %s' % (_('Updated Link:'), link.id), 'ok')
        else:
            flash('%s %s' % (_('Link is unchanged:'), link.id), 'info')
        return dict(redirect_to=url('/admin/link/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, linkid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        link = DBSession.query(Link).get(linkid.decode())
        fargs = dict(linkid=link.id,
                     id_=link.id,
                     uri_=link.uri,
                    )
        fcargs = dict()
        warning = _('This will delete the Link from the database')
        return dict(
                title='%s %s ?' % (
                    _('Are you sure you want to delete Link:'),
                    link.id),
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, linkid):
        """Delete a Link"""
        link = DBSession.query(Link).get(linkid.decode())

        for linkdata in link.data:
            DBSession.delete(linkdata)
        DBSession.delete(link)
        flash('%s %s' % (_('Deleted Link:'), link.id), 'ok')
        return dict(redirect_to=url('/admin/link/'))

    # REST-like methods
    _custom_actions = ['translation']
    
    @expose('json')
    def translation(self, linkid, value):
        """Return a link translation"""
        link = DBSession.query(Link).get(linkid.decode())

        name = link.name[value]
        description = link.description[value]
        
        return dict(name=name, description=description)

