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
from tagger.model import DBSession, User, Link, LinkData


class TestLinkController(TestController):
    """Tests for the methods in the link controller."""

    def _fill_db(self):
        user = DBSession.query(User).get(1)
        link = Link(u'http://example.com', user, u'en', u'random text')
        DBSession.add(link)
        transaction.commit()

    def test_get_all(self):
        """controllers.link.Controller.get_all is working properly"""
        self._fill_db()
        
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/link/', extra_environ=environ, status=200)

        tr = response.html.table('tr')[1]
        eq_(str(tr('td')[0]), '<td>1</td>')
        eq_(str(tr('td')[1]), '<td>http://example.com</td>')
        eq_(str(tr('td')[2]), '<td>en</td>')
        eq_(str(tr('td')[3]), '<td>random text</td>')
        actions = tr('td')[4]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_get_one(self):
        """controllers.link.Controller.get_one is working"""
        self._fill_db()

        response = self.app.get('/link/1')

        expected = ('<div id="content_with_side">\n'
                    '<div>1</div>\n'
                    '<div>http://example.com</div>\n'
                    '<div>random text</div>\n'
                    '</div>'
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_new(self):
        """controllers.link.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/link/new', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/link/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('select', {'id': 'languageid'}),
                                        '"languageid" input element not found')
        assert_true(response.html.find('input', {'id': 'url'}),
                                    '"url" input element not found')
        assert_true(response.html.find('textarea', {'id': 'description'}),
                                    '"description" textarea element not found')

    def test_post(self):
        """controllers.link.Controller.post is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.post('/link/', dict(url='http://example.com',
                                                languageid='en',
                                                description='random text',
                                               ),
                                            extra_environ=environ, status=302)
        redirected = self.app.get(response.location,
                                            extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        link = DBSession().query(Link).get(1)
        eq_(link.url, u'http://example.com')
        eq_(link.description[''], u'random text')
        eq_(link.language_ids, set([u'en']))
        eq_(link.user.user_name, 'admin')

    def test_edit(self):
        """controllers.link.Controller.edit is working"""
        self._fill_db()

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/link/1/edit', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/link/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                        {'name': 'linkid', 'value': '1'}),
                                        'wrong link_id')
        languageid = response.html.find('select', {'id': 'languageid'})
        assert_true(languageid, '"languageid" input element not found')
        eq_(languageid.find('option', {'selected': 'selected'})['value'],
                                                            u'en')
        eq_(response.html.find('input', {'id': 'url'})['value'],
                                                        u'http://example.com')
        eq_(response.html.find('textarea', {'id': 'description'}).string,
                                                        u'random text')

    def test_put(self):
        """controllers.link.Controller.put is working properly"""
        self._fill_db()

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.put('/link/1', dict(url='changed',
                                                languageid='en',
                                                description='Changed',
                                               ),
                                            extra_environ=environ, status=302)
        redirected = self.app.get(response.location,
                                            extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        link = DBSession.query(Link).get(1)
        eq_(link.url, 'changed')
        eq_(link.description['en'], 'Changed')

    def test_get_delete(self):
        """controllers.link.Controller.get_delete is working properly"""
        self._fill_db()

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/link/1/delete', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/link/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'DELETE'}),
                                        '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                                        {'name': 'linkid', 'value': '1'}),
                                        'wrong link_id')

    def test_post_delete(self):
        """controllers.link.Controller.post_delete is working properly"""
        self._fill_db()

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.delete('/link?linkid=1',
                                            extra_environ=environ, status=302)
        redirected = self.app.get(response.location,
                                            extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        link = DBSession.query(Link).get(1)
        assert_true(link is None,
                            'Link "1" should have been deleted from the db')
        linkdata = DBSession.query(LinkData).all()
        assert_false(linkdata,
                    'orphaned LinkData should have been deleted from the db')

    def test_translation(self):
        """controllers.link.Controller.translation is working properly"""
        self._fill_db()

        response = self.app.post('/link/', dict(linkid='1',
                                               value='en',
                                               _method='TRANSLATION',
                                              )
                                )

        expected = '{"description": "random text"}'
        eq_(response.body, expected)

