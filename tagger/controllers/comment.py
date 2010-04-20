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
"""Comment controller"""

from tg import expose, tmpl_context, validate, require, flash, url, redirect
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tagger.model import DBSession, Comment, Associable
from tagger.lib.widgets import FormCommentNew, FormCommentEdit
from tagger.lib.widgets import FormCommentDelete
from repoze.what.predicates import has_permission

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormCommentNew(action=url('/comment/'))
f_edit = FormCommentEdit(action=url('/comment/'))
f_delete = FormCommentDelete(action=url('/comment/'))


class Controller(RestController):
    """REST controller for managing comments"""

    @expose('json')
    @expose('tagger.templates.comment.get_all')
    def get_all(self):
        """Return a list of comments"""
        comments = DBSession.query(Comment).all()
        return dict(comments=comments)

    @expose('json')
    @expose('tagger.templates.comment.get_one')
    def get_one(self, commentid, languageid=None):
        """Return a single comment"""
        comment = DBSession.query(Comment).get(commentid)
        return dict(comment=comment, lang=languageid)

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def new(self, associableid, came_from='/', **kwargs):
        """Display a NEW form."""
        tmpl_context.form = f_new

        fargs = dict(associableid=associableid,
                     came_from=came_from)
        fcargs = dict()
        return dict(title=_('Create a new Comment'),
                                                args=fargs, child_args=fcargs)

    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_new, error_handler=new)
    def post(self, associableid, name, email, text, came_from='/'):
        """create a new Comment"""
        associable = DBSession.query(Associable).get(associableid)
        comment = Comment(name, email, text)
        associable.comments.append(comment)
        flash('%s %s' % (_('Created Comment:'), comment.header), 'ok')
        return dict(redirect_to=url(came_from))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def edit(self, commentid, **kwargs):
        """Display a EDIT form."""
        tmpl_context.form = f_edit
        comment = DBSession.query(Comment).get(commentid)
        fargs = dict(commentid=comment.id, id_=comment.id,
                     date_=comment.created,
                     to_=comment.to,
                     name=comment.name,
                     email=comment.email,
                     text=comment.text,
                    )
        fcargs = dict()
        return dict(title='%s %s' % (_('Edit comment:'), comment.id),
                                                args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_edit, error_handler=edit)
    def put(self, commentid, name, email, text):
        """Edit a comment"""
        comment = DBSession.query(Comment).get(commentid)

        modified = False
        if comment.name != name:
            comment.name = name
            modified = True

        if comment.email != email:
            comment.email = email
            modified = True

        if comment.text != text:
            comment.text = text
            modified = True

        if modified:
            flash('%s %s' % (_('Updated Comment:'), comment.id), 'ok')
        else:
            flash('%s %s' % (_('Comment is unchanged:'), comment.id), 'info')
        return dict(redirect_to=url('/admin/comment/'))

    @require(has_permission('manage'))
    @expose('tagger.templates.forms.form')
    def get_delete(self, commentid, **kwargs):
        """Display a DELETE confirmation form."""
        tmpl_context.form = f_delete
        comment = DBSession.query(Comment).get(commentid)
        fargs = dict(commentid=comment.id,
                     id_=comment.id,
                     date_=comment.created,
                     to_=comment.to,
                     name_=comment.name,
                     text_=comment.text,
                    )
        fcargs = dict()
        warning = _('This will delete the Comment from the database')
        return dict(
                title='%s %s ?' % (
                    _('Are you sure you want to delete Comment:'),
                    comment.id),
                warning=warning, args=fargs, child_args=fcargs)

    @require(has_permission('manage'))
    @expose('json')
    @expose('tagger.templates.redirect_parent')
    @validate(f_delete, error_handler=get_delete)
    def post_delete(self, commentid):
        """Delete a Comment"""
        comment = DBSession.query(Comment).get(commentid)

        DBSession.delete(comment)
        flash('%s %s' % (_('Deleted Comment:'), comment.id), 'ok')
        return dict(redirect_to=url('/admin/comment/'))

    # REST-like methods
    _custom_actions = ['approve', 'revoke', 'spam', 'unspam']
    
    @expose()
    def approve(self, commentid):
        """Approve a comment and make it visible"""
        comment = DBSession.query(Comment).get(commentid)

        comment.status = 'approved'
        flash('%s %s' % (_('Approved Comment:'), comment.id), 'ok')
        redirect(url('/admin/comment'))

    @expose()
    def revoke(self, commentid):
        """Revoke comment approval and make it invisible"""
        comment = DBSession.query(Comment).get(commentid)

        comment.status = 'waiting'
        flash('%s %s' % (_('Revoked approval for Comment:'), comment.id), 'ok')
        redirect(url('/admin/comment'))

    @expose()
    def spam(self, commentid):
        """Mark a comment as spam"""
        comment = DBSession.query(Comment).get(commentid)

        comment.status = 'spam'
        flash('%s %s' % (_('Comment marked as spam:'), comment.id), 'ok')
        redirect(url('/admin/comment'))

    @expose()
    def unspam(self, commentid):
        """Remove the spam mark from a comment"""
        comment = DBSession.query(Comment).get(commentid)

        comment.status = 'waiting'
        flash('%s %s' % (_('Removed spam mark from Comment:'), comment.id),
                                                                        'ok')
        redirect(url('/admin/comment'))


