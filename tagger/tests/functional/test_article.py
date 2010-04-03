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

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/article/', extra_environ=environ,
                                                                    status=200)

        tr = response.html.table('tr')[1]
        eq_(str(tr('td')[0]), '<td>1</td>')
        eq_(str(tr('td')[1]), '<td>A Test Article!</td>')
        eq_(str(tr('td')[2]), '<td>blog</td>')
        eq_(str(tr('td')[3]), '<td>en</td>')
        actions = tr('td')[4]
        eq_(str(actions('a')[0]['class']), 'icon edit')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_get_one(self):
        """controllers.article.Controller.get_one is working"""
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

    def test_new(self):
        """controllers.article.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/article/new', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/article/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('select', {'id': 'categoryid'}),
                                        '"categoryid" input element not found')
        assert_true(response.html.find('select', {'id': 'languageid'}),
                                        '"languageid" input element not found')
        assert_true(response.html.find('input', {'id': 'title'}),
                                        '"title" input element not found')
        assert_true(response.html.find('textarea', {'id': 'text'}),
                                        '"text" textarea element not found')

    def test_post(self):
        """controllers.article.Controller.post is working properly"""
        environ = {'REMOTE_USER': 'admin'}
        response = self.app.post('/article?title=test&categoryid=1&'
                                            'languageid=en&text=RandomText',
                                            extra_environ=environ, status=302)
        redirected = self.app.get(response.location,
                                            extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        article = DBSession().query(Article).get(1)
        eq_(article.string_id, 'test')
        eq_(article.category.name, 'blog')
        eq_(article.languages, set([u'en']))
        eq_(article.user.user_name, 'admin')

    def test_edit(self):
        """controllers.article.Controller.edit is working"""
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
                                        {'name': 'articleid', 'value': '1'}),
                                        'wrong article_id')
        categoryid = response.html.find('select', {'id': 'categoryid'})
        assert_true(categoryid, '"categoryid" input element not found')
        eq_(categoryid.find('option', {'selected': 'selected'})['value'],
                                                            u'1')
        languageid = response.html.find('select', {'id': 'languageid'})
        assert_true(languageid, '"languageid" input element not found')
        eq_(languageid.find('option', {'selected': 'selected'})['value'],
                                                            u'en')
        eq_(response.html.find('input', {'id': 'title'})['value'],
                                                            u'A Test Article!')
        eq_(response.html.find('textarea', {'id': 'text'}).string,
                                                            u'random text')

    def test_put(self):
        """controllers.article.Controller.put is working properly"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.put(
                '/article/1?title=test&categoryid=1&languageid=en&text=Test',
                extra_environ=environ, status=302)
        redirected = self.app.get(response.location,
                                            extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        article = DBSession.query(Article).get(1)
        eq_(article.title[''], 'test')
        eq_(article.text[''], 'Test')

    def test_get_delete(self):
        """controllers.article.Controller.get_delete is working properly"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.get('/article/1/delete', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/article/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'DELETE'}),
                                        '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                                        {'name': 'articleid', 'value': '1'}),
                                        'wrong article_id')

    def test_post_delete(self):
        """controllers.category.Controller.post_delete is working properly"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        environ = {'REMOTE_USER': 'admin'}
        response = self.app.delete('/article?articleid=1',
                                            extra_environ=environ, status=302)
        redirected = self.app.get(response.location,
                                            extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        article = DBSession.query(Article).get(1)
        assert_true(article is None,
                            'Article "1" should have been deleted from the db')

    def test_translation(self):
        """controllers.category.Controller.translation is working properly"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        response = self.app.post('/article', dict(articleid=1,
                                                  value='en',
                                                  _method='TRANSLATION',
                                                 )
                                )

        expected = '{"text": "random text", "title": "A Test Article!"}'
        eq_(response.body, expected)

