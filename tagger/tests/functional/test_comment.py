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
"""Functional test suite for the comment controller"""

import transaction
from nose.tools import assert_true, assert_false, eq_
from tagger.tests import TestController
from tagger.model import DBSession, User, Language, Link, Comment


class TestCommentController(TestController):
    """Tests for the methods in the comment controller."""

    def _fill_db(self):
        tadm = DBSession.query(User).filter_by(user_name=u'test_admin').one()
        language = Language(u'xx', u'test_langugage')
        DBSession.add(language)
        link = Link(u'test link', u'http://example.com', tadm, u'xx',
                                                                u'random text')
        DBSession.add(link)
        comment = Comment(u'anonymous', u'anonym@example.com', u'test comment')
        DBSession.add(comment)
        link.comments.append(comment)
        DBSession.flush()
        associableid = link.associable.id
        commentid = comment.id
        transaction.commit()
        return associableid, commentid

    def test_get_all(self):
        """controllers.comment.Controller.get_all is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/comment/', extra_environ=environ, status=200)

    def test_get_one(self):
        """controllers.comment.Controller.get_one is working properly"""
        associableid, commentid = self._fill_db()

        response = self.app.get('/comment/%s' % commentid)
        
        expected = ('<div id="content_with_side">\n'
                    '<div>%s</div>\n'
                    '<div>link/test-link</div>\n'
                    '<div>anonymous</div>\n'
                    '<div>anonym@example.com</div>\n'
                    '<div>waiting</div>\n'
                    '</div>' % commentid
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_new(self):
        """controllers.comment.Controller.new is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/comment/%s/new' % associableid,
                                            extra_environ=environ, status=200)
        
        eq_(response.html.form['action'], u'/comment/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input', {'id': 'came_from'}),
                                    '"came_from" input element not found')
        assert_true(response.html.find('input', {'id': 'associableid'}),
                                    '"associableid" input element not found')
        assert_true(response.html.find('input', {'id': 'name'}),
                                    '"name" input element not found')
        assert_true(response.html.find('input', {'id': 'email'}),
                                    '"email" input element not found')
        assert_true(response.html.find('textarea', {'id': 'text'}),
                                    '"text" textarea element not found')

    def test_post(self):
        """controllers.comment.Controller.post is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/comment/',
                                            dict(associableid=associableid,
                                                 came_from='/admin/comment/',
                                                 name='anonymous',
                                                 email='anonym@example.com',
                                                 text='another comment',
                                                ),
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/comment/";' in response.body,
                    'should be redirected to "/admin/comment/" via javascript')

        query = DBSession().query(Comment)
        comment = query.filter_by(text=u'another comment').one()
        eq_(comment.name, 'anonymous')
        eq_(comment.email, 'anonym@example.com')

    def test_edit(self):
        """controllers.comment.Controller.edit is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/comment/%s/edit' % commentid,
                                            extra_environ=environ, status=200)
        
        eq_(response.html.form['action'], u'/comment/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                    {'name': 'commentid', 'value': commentid}),
                                    'wrong commentid')
        eq_(response.html.find('input', {'id': 'name'})['value'],
                                                        u'anonymous')
        eq_(response.html.find('input', {'id': 'email'})['value'],
                                                        u'anonym@example.com')
        eq_(response.html.find('textarea', {'id': 'text'}).string,
                                                            u'test comment')

    def test_put(self):
        """controllers.comment.Controller.put is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.put('/comment/%s' % commentid,
                                            dict(name='changed',
                                                 email='changed@example.com',
                                                 text='Changed',
                                                ),
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/comment/";' in response.body,
                    'should be redirected to "/admin/comment/" via javascript')

        comment = DBSession.query(Comment).get(commentid)
        eq_(comment.name, 'changed')
        eq_(comment.email, 'changed@example.com')
        eq_(comment.text, 'Changed')

    def test_get_delete(self):
        """controllers.comment.Controller.get_delete is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/comment/%s/delete' % commentid,
                                            extra_environ=environ, status=200)
        
        eq_(response.html.form['action'], u'/comment/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'DELETE'}),
                                        '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                            {'name': 'commentid', 'value': commentid}),
                            'wrong commentid')

    def test_post_delete(self):
        """controllers.comment.Controller.post_delete is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.delete('/comment?commentid=%s' % commentid,
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/comment/";' in response.body,
                    'should be redirected to "/admin/comment/" via javascript')

        comment = DBSession.query(Comment).get(commentid)
        assert_true(comment is None,
                            'Comment should have been deleted from the db')

    def test_approve(self):
        """controllers.comment.Controller.approve is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/comment/',
                                            dict(commentid=commentid,
                                                 _method='APPROVE',
                                                ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        comment = DBSession.query(Comment).get(commentid)
        eq_(comment.status, 'approved')

    def test_revoke(self):
        """controllers.comment.Controller.revoke is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/comment/',
                                            dict(commentid=commentid,
                                                 _method='REVOKE',
                                                ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        comment = DBSession.query(Comment).get(commentid)
        eq_(comment.status, 'waiting')

    def test_spam(self):
        """controllers.comment.Controller.spam is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/comment/',
                                            dict(commentid=commentid,
                                                 _method='SPAM',
                                                ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        comment = DBSession.query(Comment).get(commentid)
        eq_(comment.status, 'spam')

    def test_unspam(self):
        """controllers.comment.Controller.unspam is working properly"""
        associableid, commentid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/comment/',
                                            dict(commentid=commentid,
                                                 _method='UNSPAM',
                                                ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        comment = DBSession.query(Comment).get(commentid)
        eq_(comment.status, 'waiting')


