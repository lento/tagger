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
"""Functional test suite for the article controller"""

import transaction
from nose.tools import assert_true, eq_
from tagger.tests import TestController
from tagger.model import DBSession, User, Category, Article


class TestCategoryController(TestController):
    """Tests for the methods in the article controller."""

    def test_get_all(self):
        """controllers.article.Controller.get_all is working properly"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        response = self.app.get('/article')
        
        expected = ('<tr>\n'
                    '<td>1</td>\n'
                    '<td>A Test Article!</td>\n'
                    '<td>blog</td>\n'
                    '<td>en</td>\n'
                    '<td>\n'
                    '</td>\n'
                    '</tr>'
                   )

        eq_(str(response.html.table('tr')[1]), expected)

    def test_get_one_id(self):
        """controllers.article.Controller.get_one is working with id"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        response = self.app.get('/article/1')
        
        expected = ('<div id="content_with_side">\n'
                    '<div>1</div>\n'
                    '<div>A Test Article!</div>\n'
                    '<div>blog</div>\n'
                    '<div>en</div>\n'
                    '</div>'
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_get_one_string_id(self):
        """controllers.article.Controller.get_one is working with string_id"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        response = self.app.get('/article/a_test_article')
        
        expected = ('<div id="content_with_side">\n'
                    '<div>1</div>\n'
                    '<div>A Test Article!</div>\n'
                    '<div>blog</div>\n'
                    '<div>en</div>\n'
                    '</div>'
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_new(self):
        """controllers.article.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/article/new', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/article/')
        eq_(response.html.form['method'], u'post')
        # TODO: check category element
        # TODO: check language element
        assert_true(response.html.find('input', {'id': 'title'}),
                                            '"title" input element not found')
        assert_true(response.html.find('textarea', {'id': 'text'}),
                                            '"text" textarea element not found')

    def test_post(self):
        """controllers.article.Controller.post is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.post('/article?title=test&category_id=1&'
                                            'language_id=en&text=RandomText',
                                            extra_environ=environ, status=200)
        
        assert_true(response.html.find('div', 'result success'),
                            'result div should have a "result success" class')

        article = DBSession().query(Article).get(1)
        eq_(article.string_id, 'test')
        eq_(article.category.name, 'blog')
        eq_(article.languages, set([u'en']))
        eq_(article.user.user_name, 'admin')

    # TODO: fix test
    '''
    def test_edit_id(self):
        """controllers.article.Controller.edit is working with id"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/article/1/edit', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/article/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                        {'name': 'article_id', 'value': '1'}),
                                        'wrong article_id')
        eq_(response.html.find('input', {'id': 'category'})['value'],
                                                            u'blog')
        eq_(response.html.find('input', {'id': 'language'})['value'],
                                                            u'en')
        eq_(response.html.find('input', {'id': 'user'})['value'],
                                                            u'admin')
        eq_(response.html.find('textarea', {'id': 'text'}).string,
                                                            u'random text')
    '''

    # TODO: add test_edit_string_id

    # TODO: fix test
    '''
    def test_put(self):
        """controllers.article.Controller.put is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.put('/article/1?title=test&description=Test',
                                            extra_environ=environ, status=200)
        
        assert_true(response.html.find('div', 'result success'),
                            'result div should have a "result success" class')

        cat = DBSession.query(Category).get(1)
        eq_(cat.name, 'test')
        eq_(cat.description, 'Test')
    '''

    # TODO: fix test
    '''
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
    '''

    # TODO: fix test
    '''
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
    '''

