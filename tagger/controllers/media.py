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

import os.path, shutil, datetime
from tg import expose, tmpl_context, validate, require, flash, url, redirect
from tg import app_globals as G
from tg.controllers import RestController
from tg.exceptions import HTTPClientError
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from sqlalchemy import desc
from tagger.model import DBSession, Media, Language, Setting
from tagger.model.helpers import tags_from_string
from tagger.model.utils import make_id
from tagger.lib.widgets import FormMediaNew, FormMediaEdit, FormMediaDelete
from tagger.lib.widgets import ObjectTitle
from tagger.lib.render import MediaWidget
from tagger.lib.utils import find_related, find_recent

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormMediaNew(action=url('/media/'))
f_edit = FormMediaEdit(action=url('/media/'))
f_delete = FormMediaDelete(action=url('/media/'))

w_object_title = ObjectTitle()
w_media = MediaWidget()

class Controller(RestController):
    """REST controller for managing media"""

    @expose('json')
    @expose('tagger.templates.media.get_all')
    def get_all(self, tag=[], max_results=None, mode='all'):
        """Return a list of media"""
        settings = dict([(s.id, s.value) for s in DBSession.query(Setting)])
        if max_results is None:
            max_results = int(settings.get('max_results', 0))
        else:
            max_results = int(max_results)

        tmpl_context.w_object_title = w_object_title
        tmpl_context.w_media = w_media
        query = DBSession.query(Media)
        query = query.join(Media.associable).filter_by(published=True)
        query = query.order_by(desc(Media.created))

        tot_results = query.count()
        if max_results:
            media = query[0:max_results]
            more_results = max(tot_results - max_results, 0)
        else:
            media = query.all()
            more_results = False

        if tag:
            tagids = isinstance(tag, list) and tag or [tag]
            tagstring = ', '.join(tagids)
            tags = set(tags_from_string(tagstring, create=False))
            if mode == 'all':
                media = [obj for obj in media if set(obj.tags) >= (tags)]
            elif mode == 'any':
                media = [obj for obj in media if set(obj.tags) & (tags)]

        return dict(media=media, recent=find_recent(), path=('media', ''),
                                                    more_results=more_results)

    @expose('json')
    @expose('tagger.templates.media.get_one')
    def get_one(self, mediaid, languageid=None):
        """Return a single media"""
        tmpl_context.w_object_title = w_object_title
        tmpl_context.w_media = w_media
        media = DBSession.query(Media).get(mediaid.decode())

        if languageid:
            lang = languageid
        elif tmpl_context.lang:
            lang = tmpl_context.lang
        else:
            lang = media.language_id

        return dict(media=media, lang=lang, related=find_related(obj=media))

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
                            fallbackfile=None, description=None, tagids=None):
        """create a new Media"""
        user = tmpl_context.user
        lang = tmpl_context.lang or DBSession.query(Language).first().id

        # TODO: redirect to "new" with errors instead of raising an exception
        if mediatype == 'image':
            if uploadfile is None:
                raise HTTPClientError(_('No image uploaded'))
            origname, ext = os.path.splitext(uploadfile.filename)
            filename = '%s%s' % (make_id(name), ext)
            tmpf = open(os.path.join(G.upload_dir, filename), 'w+b')
            shutil.copyfileobj(uploadfile.file, tmpf)
            tmpf.close()
            uri = filename
        elif mediatype == 'video':
            if uploadfile is None or fallbackfile is None:
                raise HTTPClientError(_('No video or no fallback uploaded'))
            # copy video file in the upload area
            origname, ext = os.path.splitext(uploadfile.filename)
            filename = '%s%s' % (make_id(name), ext)
            tmpf = open(os.path.join(G.upload_dir, filename), 'w+b')
            shutil.copyfileobj(uploadfile.file, tmpf)
            tmpf.close()

            # copy fallback video file in the upload area
            origname, fallbackext = os.path.splitext(fallbackfile.filename)
            fallbackname = '%s%s' % (make_id(name), fallbackext)
            fallbacktmpf = open(os.path.join(G.upload_dir, fallbackname), 'w+b')
            shutil.copyfileobj(fallbackfile.file, fallbacktmpf)
            fallbacktmpf.close()

            uri = filename
        elif mediatype == 'youtube':
            if not uri:
                raise HTTPClientError(_('No video id'))
        elif mediatype == 'vimeo':
            if not uri:
                raise HTTPClientError(_('No video id'))

        media = Media(mediatype, name, uri, user, languageid, description)
        DBSession.add(media)

        tags = tags_from_string(tagids, lang=lang)
        media.tags[:] = tags

        flash('%s %s' % (_('Created Media:'), media.id), 'ok')
        return dict(redirect_to=url('/admin/media/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, mediaid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        lang = tmpl_context.lang
        media = DBSession.query(Media).get(mediaid.decode())

        tags = ', '.join([t.name[lang] for t in media.tags])
        fargs = dict(mediaid=media.id, id_=media.id,
                     mediatype_=media.type,
                     uri=media.uri,
                     languageid=media.language_id,
                     version=media.version,
                     modified=media.data[0].modified,
                     name=media.name[''],
                     description=media.description[''],
                     tagids=tags,
                    )

        languages = [(l.id, l.name) for l in DBSession.query(Language)]

        data = media.data[0]
        DataHistory = data.__history_mapper__.class_
        query = DBSession.query(DataHistory).filter_by(id=data.id)
        versions = range(query.count(), 0, -1)
        versions.insert(0, int(data.version))

        fcargs = dict(
            languageid=dict(options=languages),
            version=dict(options=versions),
            )
        return dict(title='%s %s' % (_('Edit media:'), media.id),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, mediaid, uri, languageid, name, description=None,
                                    tagids=None, version=None, modified=None):
        """Edit a media"""
        lang = tmpl_context.lang or DBSession.query(Language).first().id
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

        tags = tags_from_string(tagids, lang=lang)
        if media.tags != tags:
            media.tags[:] = tags
            modified = True

        if modified:
            media.data[languageid].modified = datetime.datetime.now()
            flash('%s %s' % (_('Updated Media:'), media.id), 'ok')
        else:
            flash('%s %s' % (_('Media is unchanged:'), media.id), 'info')

        return dict(redirect_to=url('/admin/media/'))

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
        warning = _('This will delete the Media from the database '\
                    'and all related files from the upload area')
        return dict(
                title='%s %s ?' % (
                    _('Are you sure you want to delete Media:'),
                    media.id),
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, mediaid):
        """Delete a Media"""
        media = DBSession.query(Media).get(mediaid.decode())

        if media.type == 'image':
            mediaurl = os.path.join(G.upload_dir, media.uri)
            try:
                os.remove(mediaurl)
            except OSError as error:
                if error.errno == 2:
                    log.debug('file "%s" not found' % mediaurl)
                else:
                    raise
        elif media.type == 'video':
            mediaurl = os.path.join(G.upload_dir, media.uri)
            filename, ext = os.path.splitext(mediaurl)
            try:
                os.remove(mediaurl)
            except OSError as error:
                if error.errno == 2:
                    log.debug('file "%s" not found' % mediaurl)
                else:
                    raise
            try:
                os.remove('%s.flv' % filename)
            except OSError:
                if error.errno == 2:
                    log.debug('file "%s.flv" not found' % filename)
                else:
                    raise

        for mediadata in media.data:
            DBSession.delete(mediadata)
        DBSession.delete(media.associable)
        DBSession.delete(media)
        flash('%s %s' % (_('Deleted Media:'), media.id), 'ok')
        return dict(redirect_to=url('/admin/media/'))

    # REST-like methods
    _custom_actions = ['translation', 'version', 'publish', 'unpublish']
    
    @expose('json')
    def translation(self, mediaid, value):
        """Return a media translation"""
        media = DBSession.query(Media).get(mediaid)
        data = media.data[value]

        if data:
            DataHistory = data.__history_mapper__.class_
            query = DBSession.query(DataHistory).filter_by(id=data.id)
            versions = range(query.count(), 0, -1)
            versions.insert(0, int(data.version))
            modified = data.modified
        else:
            versions = [0]
            modified = _('(new translation)')

        name = media.name[value]
        description = media.description[value]
        
        return dict(version=versions, modified=modified, name=name,
                                                        description=description)

    @expose('json')
    def version(self, mediaid, languageid, value):
        """Return a media version"""
        media = DBSession.query(Media).get(mediaid)
        data = media.data[languageid]

        if int(value) == data.version:
            modified = data.modified
            name = data.name
            description = data.description
        else:
            DataHistory = data.__history_mapper__.class_
            query = DBSession.query(DataHistory).filter_by(id=data.id)
            ver = query.filter_by(version=value).one()

            modified = ver.modified
            name = ver.name
            description = ver.description

        return dict(modified=modified, name=name, description=description)

    @require(has_permission('manage'))
    @expose()
    def publish(self, mediaid):
        """Make media visible to users"""
        media = DBSession.query(Media).get(mediaid.decode())

        if media.published:
            flash('%s %s' % (_('Media is already published:'), mediaid), 'info')
        else:
            media.published = True
            flash('%s %s' % (_('Published Media:'), mediaid), 'ok')

        redirect(url('/admin/media/'))

    @require(has_permission('manage'))
    @expose()
    def unpublish(self, mediaid):
        """Revert media publication and making it invisible to user"""
        media = DBSession.query(Media).get(mediaid.decode())

        if media.published:
            media.published = False
            flash('%s %s' % (_('Unpublished Media:'), mediaid), 'ok')
        else:
            flash('%s %s' % (_('Media is not published:'), mediaid), 'info')

        redirect(url('/admin/media/'))

