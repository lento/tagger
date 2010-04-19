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
"""Functional test suite for the language controller"""

import transaction
from nose.tools import assert_true, eq_
from tagger.tests import TestController
from tagger.model import DBSession, Language


class TestLanguageController(TestController):
    """Tests for the methods in the language controller."""

    def _fill_db(self):
        language = Language(u'xx', u'test language')
        DBSession.add(language)
        DBSession.flush()
        languageid = language.id
        transaction.commit()
        return languageid.encode()

    def test_get_all(self):
        """controllers.language.Controller.get_all is working properly"""
        languageid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/language', extra_environ=environ, status=200)

    def test_get_one(self):
        """controllers.language.Controller.get_one is working properly"""
        languageid = self._fill_db()

        response = self.app.get('/language/%s' % languageid)
        
        expected = ('<div id="content_with_side">\n'
                    '<div>xx</div>\n'
                    '<div>test language</div>\n'
                    '</div>'
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_new(self):
        """controllers.language.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/language/new',
                                            extra_environ=environ, status=200)
        
        eq_(response.html.form['action'], u'/language/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input', {'id': 'languageid'}),
                                        '"language_id" input element not found')
        assert_true(response.html.find('input', {'id': 'name'}),
                                        '"name" input element not found')

    def test_post(self):
        """controllers.language.Controller.post is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/language/',
                                            dict(languageid='xx',
                                                 name='test language',
                                                ),
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/language/";' in response.body,
                        'should be redirected to "/admin/language/" via javascript')

        cat = DBSession().query(Language).get(u'xx')
        eq_(cat.name, 'test language')

    def test_edit(self):
        """controllers.language.Controller.edit is working properly"""
        languageid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/language/%s/edit' % languageid,
                                            extra_environ=environ, status=200)
        
        eq_(response.html.form['action'], u'/language/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                            {'name': '_method', 'value': 'PUT'}),
                            '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                            {'name': 'languageid', 'value': languageid}),
                            'wrong language_id')
        eq_(response.html.find('input', {'id': 'name'})['value'],
                                                            u'test language')

    def test_put(self):
        """controllers.language.Controller.put is working properly"""
        languageid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.put('/language/%s' % languageid,
                                            dict(name='changed'),
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/language/";' in response.body,
                        'should be redirected to "/admin/language/" via javascript')

        cat = DBSession.query(Language).get(languageid.decode())
        eq_(cat.name, 'changed')

    def test_get_delete(self):
        """controllers.language.Controller.get_delete is working properly"""
        languageid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/language/%s/delete' % languageid,
                                            extra_environ=environ, status=200)
        
        eq_(response.html.form['action'], u'/language/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                            {'name': '_method', 'value': 'DELETE'}),
                            '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                            {'name': 'languageid', 'value': languageid}),
                            'wrong language_id')

    def test_post_delete(self):
        """controllers.language.Controller.post_delete is working properly"""
        languageid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.delete('/language?languageid=%s' % languageid,
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/language/";' in response.body,
                        'should be redirected to "/admin/language/" via javascript')

        result = DBSession.query(Language).get(languageid.decode())
        assert_true(result is None,
                        'Language should have been deleted from the db')

