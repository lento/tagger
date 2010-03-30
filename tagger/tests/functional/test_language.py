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

    def test_get_all(self):
        """controllers.language.Controller.get_all is working properly"""
        response = self.app.get('/language')
        
        expected = ('<tr>\n'
                    '<td>en</td>\n'
                    '<td>english</td>\n'
                    '<td>\n'
                    '</td>\n'
                    '</tr>'
                   )

        eq_(str(response.html.table.tr), expected)

    def test_get_one(self):
        """controllers.language.Controller.get_one is working properly"""
        response = self.app.get('/language/en')
        
        expected = ('<div id="content">\n'
                    '<div>en</div>\n'
                    '<div>english</div>\n'
                    '</div>'
                   )

        eq_(str(response.html.find(id='content')), expected)

    def test_new(self):
        """controllers.language.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/language/new', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/language/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input', {'id': 'language_id'}),
                                        '"language_id" input element not found')
        assert_true(response.html.find('input', {'id': 'name'}),
                                        '"name" input element not found')

    def test_post(self):
        """controllers.language.Controller.post is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.post('/language?language_id=xx&name=test_language&',
                                            extra_environ=environ, status=200)
        
        assert_true(response.html.find('div', 'result success'),
                            'result div should have a "result success" class')

        cat = DBSession().query(Language).get(u'xx')
        eq_(cat.name, 'test_language')

    def test_edit(self):
        """controllers.language.Controller.edit is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/language/en/edit', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/language/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                        {'name': 'language_id', 'value': 'en'}),
                                        'wrong language_id')
        eq_(response.html.find('input', {'id': 'name'})['value'],
                                                            u'english')

    def test_put(self):
        """controllers.language.Controller.put is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.put('/language/en?name=test_language',
                                            extra_environ=environ, status=200)
        
        assert_true(response.html.find('div', 'result success'),
                            'result div should have a "result success" class')

        cat = DBSession.query(Language).get(u'en')
        eq_(cat.name, 'test_language')

    def test_get_delete(self):
        """controllers.language.Controller.get_delete is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/language/en/delete', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/language/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'DELETE'}),
                                        '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                                        {'name': 'language_id', 'value': 'en'}),
                                        'wrong language_id')

    def test_post_delete(self):
        """controllers.language.Controller.post_delete is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.delete('/language?language_id=en',
                                            extra_environ=environ, status=200)
        
        assert_true(response.html.find('div', 'result success'),
                            'result div should have a "result success" class')

        result = DBSession.query(Language).get(u'en')
        assert_true(result is None,
                        'Language "en" should have been deleted from the db')

