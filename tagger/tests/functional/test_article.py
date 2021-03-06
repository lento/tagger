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
from nose.tools import assert_true, assert_false, eq_
from tagger.tests import TestController
from tagger.model import DBSession, User, Language, Category, Article, Tag
from tagger.model import Page, PageData


class TestCategoryController(TestController):
    """Tests for the methods in the article controller."""

    def _fill_db(self):
        tadm = DBSession.query(User).filter_by(user_name=u'test_admin').one()
        language = Language(u'xx', u'test_langugage')
        DBSession.add(language)
        cat = Category(u'test_category', u'xx')
        DBSession.add(cat)
        tag = Tag(u'test_tag', u'xx')
        DBSession.add(tag)
        article = Article(u'A Test Article!', cat, u'xx', tadm, u'random text')
        article.tags.append(tag)
        DBSession.add(article)
        DBSession.flush()
        categoryid = cat.id
        articleid = article.id
        languageid = language.id
        transaction.commit()
        return languageid, categoryid, articleid.encode()

    def test_get_all(self):
        """controllers.article.Controller.get_all is working properly"""
        languageid, categoryid, articleid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/article/', extra_environ=environ,
                                                                    status=200)

    def test_get_one(self):
        """controllers.article.Controller.get_one is working"""
        languageid, categoryid, articleid = self._fill_db()

        response = self.app.get('/article/%s' % articleid)

        assert_true(str(response.html.find(id='content_with_side')),
                                'content should have class "content_with_side"')
        title = response.html.find('div', 'article_title')
        eq_(str(title.h1), '<h1>A Test Article!</h1>')
        eq_(str(title.find('span', 'user')),
                                        '<span class="user">test_admin</span>')

    def test_new(self):
        """controllers.article.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
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
        assert_true(response.html.find('input', {'id': 'tagids'}),
                                        '"tagids" input element not found')

    def test_post(self):
        """controllers.article.Controller.post is working properly"""
        languageid, categoryid, articleid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/article/', dict(title='test',
                                                   categoryid=categoryid,
                                                   languageid=languageid,
                                                   text='random text',
                                                   tagids='test_tag',
                                                  ),
                                            extra_environ=environ, status=200)
        print(response.body)
        assert_true('parent.location = "/admin/article/";' in response.body,
                    'should be redirected to "/admin/article/" via javascript')

        article = DBSession().query(Article).get(u'test')
        eq_(article.category.id, 'test_category')
        eq_(article.language_ids, set([u'%s' % languageid]))
        eq_(article.user.user_name, 'test_admin')
        eq_(article.tags[0].id, u'test_tag')

    def test_edit(self):
        """controllers.article.Controller.edit is working"""
        languageid, categoryid, articleid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/article/%s/edit' % articleid,
                                            extra_environ=environ, status=200)

        eq_(response.html.form['action'], u'/article/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                {'name': '_method', 'value': 'PUT'}),
                                '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                {'name': 'articleid', 'value': articleid}),
                                'wrong article_id')
        elem_categoryid = response.html.find('select', {'id': 'categoryid'})
        assert_true(elem_categoryid, '"categoryid" input element not found')
        eq_(elem_categoryid.find('option', {'selected': 'selected'})['value'],
                                                            str(categoryid))
        elem_languageid = response.html.find('select', {'id': 'languageid'})
        assert_true(elem_languageid, '"languageid" input element not found')
        eq_(elem_languageid.find('option', {'selected': 'selected'})['value'],
                                                            languageid)
        eq_(response.html.find('input', {'id': 'title'})['value'],
                                                            u'A Test Article!')
        eq_(response.html.find('textarea', {'id': 'text'}).string,
                                                            u'random text')
        eq_(response.html.find('input', {'id': 'tagids'})['value'],
                                                            u'test_tag')

    def test_put(self):
        """controllers.article.Controller.put is working properly"""
        languageid, categoryid, articleid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.put('/article/%s' % articleid,
                                            dict(title='test',
                                                 categoryid=categoryid,
                                                 languageid=languageid,
                                                 text='Test',
                                                 tagids='another_tag',
                                                ),
                                            extra_environ=environ, status=200)
        print(response.body)
        assert_true(
            'parent.location = "/article/test/edit";' in response.body,
            'should be redirected to "/article/<id>/edit" via javascript')

        article = DBSession().query(Article).get(u'test')
        eq_(article.title[''], 'test')
        eq_(article.text[''], 'Test')
        eq_(article.tags[0].id, 'another_tag')

    def test_get_delete(self):
        """controllers.article.Controller.get_delete is working properly"""
        languageid, categoryid, articleid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/article/%s/delete' % articleid,
                                            extra_environ=environ, status=200)

        eq_(response.html.form['action'], u'/article/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                {'name': '_method', 'value': 'DELETE'}),
                                '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                                {'name': 'articleid', 'value': articleid}),
                                'wrong article_id')

    def test_post_delete(self):
        """controllers.article.Controller.post_delete is working properly"""
        languageid, categoryid, articleid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.delete('/article?articleid=%s' % articleid,
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/article/";' in response.body,
                    'should be redirected to "/admin/article/" via javascript')

        article = DBSession().query(Article).get(articleid.decode())
        assert_true(article is None,
                            'the article should have been deleted from the db')
        pages = DBSession.query(Page).filter_by(article_id=None).all()
        assert_false(pages,
                    'orphaned Pages should have been deleted from the db')
        pagedata = DBSession.query(PageData).filter_by(parent_id=None).all()
        assert_false(pagedata,
                    'orphaned PageData should have been deleted from the db')

    def test_translation(self):
        """controllers.article.Controller.translation is working properly"""
        languageid, categoryid, articleid = self._fill_db()

        response = self.app.post('/article', dict(articleid=articleid,
                                                  value=languageid,
                                                  _method='TRANSLATION',
                                                 )
                                )

        expected = '{"text": "random text", "title": "A Test Article!"}'
        eq_(response.body, expected)

    def test_publish(self):
        """controllers.article.Controller.publish is working properly"""
        languageid, categoryid, articleid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/article', dict(articleid=articleid,
                                                  _method='PUBLISH',
                                                 ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        article = DBSession().query(Article).get(articleid.decode())
        eq_(article.published, True)

    def test_unpublish(self):
        """controllers.article.Controller.unpublish is working properly"""
        languageid, categoryid, articleid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/article', dict(articleid=articleid,
                                                  _method='UNPUBLISH',
                                                 ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        article = DBSession().query(Article).get(articleid.decode())
        eq_(article.published, False)

