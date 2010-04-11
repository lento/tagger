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
from nose.tools import assert_true, assert_false, eq_
from tagger.tests import TestController
from tagger.model import DBSession, Language, Category, CategoryData


class TestCategoryController(TestController):
    """Tests for the methods in the category controller."""

    def _fill_db(self):
        language = Language(u'xx', u'test_langugage')
        DBSession.add(language)
        cat = Category(u'test category', u'xx', u'a test category')
        DBSession.add(cat)
        DBSession.flush()
        languageid = language.id
        categoryid = cat.id
        transaction.commit()
        return languageid, categoryid.encode()

    def test_get_all(self):
        """controllers.category.Controller.get_all is working properly"""
        languageid, categoryid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/category/', extra_environ=environ, status=200)
        
        tr = response.html.table.find('tr', categoryid)
        eq_(str(tr('td')[0]), '<td>%s</td>' % categoryid)
        eq_(str(tr('td')[1]), '<td>test category</td>')
        eq_(str(tr('td')[2]), '<td>a test category</td>')
        eq_(str(tr('td')[3]), '<td>%s</td>' % languageid)
        actions = tr('td')[4]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_get_one(self):
        """controllers.category.Controller.get_one is working properly"""
        languageid, categoryid = self._fill_db()

        response = self.app.get('/category/%s' % categoryid)
        
        expected = ('<div id="content_with_side">\n'
                    '<div>%s</div>\n'
                    '<div>test category</div>\n'
                    '<div>a test category</div>\n'
                    '</div>' % categoryid
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_new(self):
        """controllers.category.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/category/new', extra_environ=environ,
                                                                    status=200)
        
        eq_(response.html.form['action'], u'/category/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('select', {'id': 'languageid'}),
                                        '"languageid" input element not found')
        assert_true(response.html.find('input', {'id': 'name'}),
                                            '"name" input element not found')
        assert_true(response.html.find('textarea', {'id': 'description'}),
                                    '"description" textarea element not found')

    def test_post(self):
        """controllers.category.Controller.post is working properly"""
        languageid, categoryid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/category/',
                                            dict(name='test',
                                                languageid=languageid,
                                                 description='Test',
                                                ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)
        
        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        cat = DBSession().query(Category).get(u'test')
        eq_(cat.language_ids, set([languageid]))
        eq_(cat.description[languageid], 'Test')

    def test_edit(self):
        """controllers.category.Controller.edit is working properly"""
        languageid, categoryid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/category/%s/edit' % categoryid,
                                            extra_environ=environ, status=200)
        
        eq_(response.html.form['action'], u'/category/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                            {'name': 'categoryid', 'value': categoryid}),
                            'wrong categoryid')
        elem_languageid = response.html.find('select', {'id': 'languageid'})
        assert_true(elem_languageid, '"languageid" input element not found')
        eq_(elem_languageid.find('option', {'selected': 'selected'})['value'],
                                                            languageid)
        eq_(response.html.find('input', {'id': 'name'})['value'],
                                                            u'test category')
        eq_(response.html.find('textarea', {'id': 'description'}).string,
                                                            u'a test category')

    def test_put(self):
        """controllers.category.Controller.put is working properly"""
        languageid, categoryid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.put('/category/%s' % categoryid,
                                            dict(name='changed',
                                                 languageid=languageid,
                                                 description='Changed',
                                                ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)
        
        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        cat = DBSession.query(Category).get(u'changed')
        eq_(cat.name[languageid], 'changed')
        eq_(cat.description[languageid], 'Changed')

    def test_get_delete(self):
        """controllers.category.Controller.get_delete is working properly"""
        languageid, categoryid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/category/%s/delete' % categoryid,
                                            extra_environ=environ, status=200)
        
        eq_(response.html.form['action'], u'/category/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'DELETE'}),
                                        '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                            {'name': 'categoryid', 'value': categoryid}),
                            'wrong categoryid')

    def test_post_delete(self):
        """controllers.category.Controller.post_delete is working properly"""
        languageid, categoryid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.delete('/category?categoryid=%s' % categoryid,
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)
        
        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        cat = DBSession.query(Category).get(categoryid.decode())
        assert_true(cat is None,
                            'Category should have been deleted from the db')
        query = DBSession.query(CategoryData)
        categorydata = query.filter_by(category_id=None).all()
        assert_false(categorydata,
                'orphaned CategoryData should have been deleted from the db')

