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
"""Functional test suite for the category controller"""

import transaction
from nose.tools import assert_true, eq_
from tagger.tests import TestController
from tagger.model import DBSession, Category


class TestCategoryController(TestController):
    """Tests for the methods in the category controller."""

    def test_get_all(self):
        """controllers.category.Controller.get_all is working properly"""
        response = self.app.get('/category')
        
        expected = ('<tr>\n'
                    '<td>1</td>\n'
                    '<td>blog</td>\n'
                    '<td>Web log</td>\n'
                    '<td>\n'
                    '</td>\n'
                    '</tr>'
                   )

        eq_(str(response.html.table.tr), expected)

    def test_get_one(self):
        """controllers.category.Controller.get_one is working properly"""
        response = self.app.get('/category/1')
        
        expected = ('<div id="content">\n'
                    '<div>1</div>\n'
                    '<div>blog</div>\n'
                    '<div>Web log</div>\n'
                    '</div>'
                   )

        eq_(str(response.html.find(id='content')), expected)

    def test_new(self):
        """controllers.category.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/category/new', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/category/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input', {'id': 'name'}),
                                            '"name" input element not found')
        assert_true(response.html.find('textarea', {'id': 'description'}),
                                    '"description" textarea element not found')

    def test_post(self):
        """controllers.category.Controller.post is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.post('/category?name=test&description=Test',
                                            extra_environ=environ, status=200)
        
        assert_true(response.html.find('div', 'result success'),
                            'result div should have a "result success" class')

        cat = DBSession().query(Category).filter_by(name=u'test').one()
        eq_(cat.description, 'Test')

    def test_edit(self):
        """controllers.category.Controller.edit is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/category/1/edit', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/category/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                        {'name': 'category_id', 'value': '1'}),
                                        'wrong category_id')
        eq_(response.html.find('input', {'id': 'name'})['value'],
                                                            u'blog')
        eq_(response.html.find('textarea', {'id': 'description'}).string,
                                                            u'Web log')

    def test_put(self):
        """controllers.category.Controller.put is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.put('/category/1?name=test&description=Test',
                                            extra_environ=environ, status=200)
        
        assert_true(response.html.find('div', 'result success'),
                            'result div should have a "result success" class')

        cat = DBSession.query(Category).get(1)
        eq_(cat.name, 'test')
        eq_(cat.description, 'Test')

    def test_get_delete(self):
        """controllers.category.Controller.get_delete is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/category/1/delete', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/category/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'DELETE'}),
                                        '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                                        {'name': 'category_id', 'value': '1'}),
                                        'wrong category_id')

    def test_post_delete(self):
        """controllers.category.Controller.post_delete is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.delete('/category?category_id=1',
                                            extra_environ=environ, status=200)
        
        assert_true(response.html.find('div', 'result success'),
                            'result div should have a "result success" class')

        cat = DBSession.query(Category).get(1)
        assert_true(cat is None,
                            'Category "1" should have been deleted from the db')

