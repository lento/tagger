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
"""Media controller"""

import os.path, shutil
from tg import expose, tmpl_context, validate, require, flash, url, config
from tg.controllers import RestController
from tg.exceptions import HTTPClientError
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from tagger.model import DBSession, Media, Language
from tagger.lib.widgets import FormMediaNew, FormMediaEdit, FormMediaDelete
from tagger.lib.utils import make_id

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormMediaNew(action=url('/media/'))
f_edit = FormMediaEdit(action=url('/media/'))
f_delete = FormMediaDelete(action=url('/media/'))


class Controller(RestController):
    """REST controller for managing media"""

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.media.get_all')
    def get_all(self):
        """Return a list of media"""
        media = DBSession.query(Media).all()
        return dict(media=media, page=('admin', 'media'))

    @expose('json')
    @expose('tagger.templates.media.get_one')
    def get_one(self, mediaid, languageid=None):
        """Return a single media"""
        media = DBSession.query(Media).get(mediaid.decode())
        return dict(media=media, lang=languageid)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new

        fargs = dict()
        lang_list = [(l.id, l.name) for l in DBSession.query(Language).all()]
        fcargs = dict(languageid=dict(options=lang_list))
        return dict(title=_('Create a new Media'),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_new, error_handler=new)
    def post(self, mediatype, languageid, name, uri=None, uploadfile=None,
                                        fallbackfile=None, description=None):
        """create a new Media"""
        user = tmpl_context.user
        upload_dir = config.get('upload_dir', '%s/upload' % config['cache.dir'])
        upload_prefix = config.get('upload_prefix', 'upload')

        # TODO: redirect to "new" with errors instead of raising an exception
        if mediatype == 'image':
            if uploadfile is None:
                raise HTTPClientError(_('No image uploaded'))
            origname, ext = os.path.splitext(uploadfile.filename)
            filename = '%s%s' % (make_id(name), ext)
            tmpf = open(os.path.join(upload_dir, filename), 'w+b')
            shutil.copyfileobj(uploadfile.file, tmpf)
            tmpf.close()
            uri = '/%s/%s' % (upload_prefix, filename)
        elif mediatype == 'video':
            if uploadfile is None or fallbackfile is None:
                raise HTTPClientError(_('No video or no fallback uploaded'))
            # copy video file in the upload area
            origname, ext = os.path.splitext(uploadfile.filename)
            filename = '%s%s' % (make_id(name), ext)
            tmpf = open(os.path.join(upload_dir, filename), 'w+b')
            shutil.copyfileobj(uploadfile.file, tmpf)
            tmpf.close()

            # copy fallback video file in the upload area
            origname, fallbackext = os.path.splitext(fallbackfile.filename)
            fallbackname = '%s%s' % (make_id(name), fallbackext)
            fallbacktmpf = open(os.path.join(upload_dir, fallbackname), 'w+b')
            shutil.copyfileobj(fallbackfile.file, fallbacktmpf)
            fallbacktmpf.close()

            uri = '/%s/%s' % (upload_prefix, filename)
        elif mediatype == 'youtube':
            if not uri:
                raise HTTPClientError(_('No video id'))
        elif mediatype == 'vimeo':
            if not uri:
                raise HTTPClientError(_('No video id'))

        media = Media(mediatype, name, uri, user, languageid, description)
        DBSession.add(media)
        flash(_('Created Media "%s"') % media.id, 'ok')
        return dict(redirect_to=url('/media/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, mediaid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        media = DBSession.query(Media).get(mediaid.decode())
        fargs = dict(mediaid=media.id, id_=media.id,
                     mediatype_=media.type,
                     uri=media.uri,
                     languageid=media.language_id,
                     name=media.name[''],
                     description=media.description[''])
        languages = [(l.id, l.name) for l in DBSession.query(Language)]
        fcargs = dict(languageid=dict(options=languages))
        return dict(title='Edit media "%s"' % media.id, args=fargs,
                                                            child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, mediaid, uri, languageid, name, description=None):
        """Edit a media"""
        media = DBSession.query(Media).get(mediaid.decode())

        modified = False
        if media.uri != uri:
            media.uri = uri
            modified = True

        if media.name[languageid] != name:
            media.name[languageid] = name
            modified = True

        if media.description[languageid] != description:
            media.description[languageid] = description
            modified = True

        if modified:
            flash(_('updated media "%s"') % mediaid, 'ok')
        else:
            flash(_('media "%s" unchanged') % mediaid, 'info')

        return dict(redirect_to=url('/media/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, mediaid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        media = DBSession.query(Media).get(mediaid.decode())
        fargs = dict(mediaid=media.id,
                     id_=media.id,
                     mediatype_=media.type,
                     uri_=media.uri,
                    )
        fcargs = dict()
        warning = _('This will delete the media entry in the database')
        return dict(
                title=_('Are you sure you want to delete Media "%s"?') %
                                                                media.id,
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, mediaid):
        """Delete a Media"""
        media = DBSession.query(Media).get(mediaid.decode())

        for mediadata in media.data:
            DBSession.delete(mediadata)
        DBSession.delete(media)
        flash(_('Deleted Media "%s"') % media.id, 'ok')
        return dict(redirect_to=url('/media/'))

    # REST-like methods
    _custom_actions = ['translation']
    
    @expose('json')
    def translation(self, mediaid, value):
        """Return a media translation"""
        media = DBSession.query(Media).get(mediaid)

        name = media.name[value]
        description = media.description[value]
        
        return dict(name=name, description=description)

