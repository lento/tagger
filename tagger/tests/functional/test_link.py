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
"""Functional test suite for the link controller"""

import transaction
from nose.tools import assert_true, assert_false, eq_
from tagger.tests import TestController
from tagger.model import DBSession, User, Language, Link, LinkData


class TestLinkController(TestController):
    """Tests for the methods in the link controller."""

    def _fill_db(self):
        tadm = DBSession.query(User).filter_by(user_name=u'test_admin').one()
        language = Language(u'xx', u'test_langugage')
        DBSession.add(language)
        link = Link(u'test link', u'http://example.com', tadm, u'xx',
                                                                u'random text')
        DBSession.add(link)
        DBSession.flush()
        languageid = language.id
        linkid = link.id
        transaction.commit()
        return languageid, linkid.encode()

    def test_get_all(self):
        """controllers.link.Controller.get_all is working properly"""
        languageid, linkid = self._fill_db()
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/link/', extra_environ=environ, status=200)

        tr = response.html.table('tr')[1]
        eq_(str(tr('td')[0]), '<td>%s</td>' % linkid)
        eq_(str(tr('td')[1]), '<td>test link</td>')
        eq_(str(tr('td')[2]), '<td>http://example.com</td>')
        eq_(str(tr('td')[3]), '<td>%s</td>' % languageid)
        actions = tr('td')[4]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_get_one(self):
        """controllers.link.Controller.get_one is working"""
        languageid, linkid = self._fill_db()

        response = self.app.get('/link/%s' % linkid)

        expected = ('<div id="content_with_side">\n'
                    '<div>%s</div>\n'
                    '<div>test link</div>\n'
                    '<div>http://example.com</div>\n'
                    '<div>random text</div>\n'
                    '</div>' % linkid
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_new(self):
        """controllers.link.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/link/new', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/link/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('select', {'id': 'languageid'}),
                                        '"languageid" input element not found')
        assert_true(response.html.find('input', {'id': 'uri'}),
                                    '"uri" input element not found')
        assert_true(response.html.find('input', {'id': 'name'}),
                                    '"name" input element not found')
        assert_true(response.html.find('textarea', {'id': 'description'}),
                                    '"description" textarea element not found')

    def test_post(self):
        """controllers.link.Controller.post is working properly"""
        languageid, linkid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/link/', dict(name='another link',
                                                uri='http://example.com',
                                                languageid=languageid,
                                                description='random text',
                                               ),
                                            extra_environ=environ, status=200)
        assert_true('parent.location = /link/;' in response.body,
                            'should be redirected to "/link/" via javascript')

        link = DBSession().query(Link).get(u'another-link')
        eq_(link.name[''], u'another link')
        eq_(link.description[''], u'random text')
        eq_(link.language_ids, set([languageid]))
        eq_(link.user.user_name, 'test_admin')

    def test_edit(self):
        """controllers.link.Controller.edit is working"""
        languageid, linkid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/link/%s/edit' % linkid,
                                            extra_environ=environ, status=200)

        eq_(response.html.form['action'], u'/link/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                {'name': 'linkid', 'value': linkid}),
                                'wrong link_id')
        elem_languageid = response.html.find('select', {'id': 'languageid'})
        assert_true(elem_languageid, '"languageid" input element not found')
        eq_(elem_languageid.find('option', {'selected': 'selected'})['value'],
                                                            languageid)
        eq_(response.html.find('input', {'id': 'uri'})['value'],
                                                        u'http://example.com')
        eq_(response.html.find('input', {'id': 'name'})['value'],
                                                        u'test link')
        eq_(response.html.find('textarea', {'id': 'description'}).string,
                                                        u'random text')

    def test_put(self):
        """controllers.link.Controller.put is working properly"""
        languageid, linkid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.put('/link/%s' % linkid,
                                            dict(name='changed',
                                                 uri='changed',
                                                 languageid=languageid,
                                                 description='Changed',
                                                ),
                                            extra_environ=environ, status=200)
        assert_true('parent.location = /link/;' in response.body,
                            'should be redirected to "/link/" via javascript')

        link = DBSession.query(Link).get(u'changed')
        eq_(link.uri, 'changed')
        eq_(link.name[languageid], 'changed')
        eq_(link.description[languageid], 'Changed')

    def test_get_delete(self):
        """controllers.link.Controller.get_delete is working properly"""
        languageid, linkid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/link/%s/delete' % linkid,
                                           extra_environ=environ, status=200)

        eq_(response.html.form['action'], u'/link/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                {'name': '_method', 'value': 'DELETE'}),
                                '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                                {'name': 'linkid', 'value': linkid}),
                                'wrong link_id')

    def test_post_delete(self):
        """controllers.link.Controller.post_delete is working properly"""
        languageid, linkid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.delete('/link?linkid=%s' % linkid,
                                            extra_environ=environ, status=200)
        assert_true('parent.location = /link/;' in response.body,
                            'should be redirected to "/link/" via javascript')

        link = DBSession.query(Link).get(linkid.decode())
        assert_true(link is None,
                            'Link "1" should have been deleted from the db')
        linkdata = DBSession.query(LinkData).filter_by(parent_id=None).all()
        assert_false(linkdata,
                    'orphaned LinkData should have been deleted from the db')

    def test_translation(self):
        """controllers.link.Controller.translation is working properly"""
        languageid, linkid = self._fill_db()

        response = self.app.post('/link/', dict(linkid=linkid,
                                               value=languageid,
                                               _method='TRANSLATION',
                                              )
                                )

        expected = '{"name": "test link", "description": "random text"}'
        eq_(response.body, expected)

