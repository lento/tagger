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
        """controllers.category.Controller.get_all page is working properly"""
        DBSession.add(Category(u'test_category', u'A Test Category'))
        transaction.commit()
        
        response = self.app.get('/category')
        
        expected = ('<tr>\n'
                    '<td>1</td>\n'
                    '<td>test_category</td>\n'
                    '<td>A Test Category</td>\n'
                    '<td>\n'
                    '</td>\n'
                    '</tr>'
                   )

        eq_(str(response.html.table.tr), expected)

    def test_get_one(self):
        """controllers.category.Controller.get_one page is working properly"""
        DBSession.add(Category(u'test_category', u'A Test Category'))
        transaction.commit()
        
        response = self.app.get('/category/1')
        
        expected = ('<div id="content">\n'
                    '<div>1</div>\n'
                    '<div>test_category</div>\n'
                    '<div>A Test Category</div>\n'
                    '</div>'
                   )

        eq_(str(response.html.find(id='content')), expected)

    def test_new(self):
        """controllers.category.Controller.new page is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/category/new', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/category/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input', {'id': 'name'}),
                                            '"name" input element not found')
        assert_true(response.html.find('textarea', {'id': 'description'}),
                                    '"description" textarea element not found')


