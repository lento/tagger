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
"""Functional test suite for the tag controller"""

import transaction
from nose.tools import assert_true, assert_false, eq_
from tagger.tests import TestController
from tagger.model import DBSession, User, Language, Tag, TagData


class TestTagController(TestController):
    """Tests for the methods in the tag controller."""

    def _fill_db(self):
        language = Language(u'xx', u'test_langugage')
        DBSession.add(language)
        tag = Tag(u'test tag', u'xx')
        DBSession.add(tag)
        DBSession.flush()
        languageid = language.id
        tagid = tag.id
        transaction.commit()
        return languageid, tagid.encode()

    def test_get_all(self):
        """controllers.tag.Controller.get_all is working properly"""
        languageid, tagid = self._fill_db()
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/tag/', extra_environ=environ, status=200)

    def test_get_one(self):
        """controllers.tag.Controller.get_one is working"""
        languageid, tagid = self._fill_db()

        response = self.app.get('/tag/%s' % tagid)

        expected = ('<div id="content_with_side">\n'
                    '<div>%s</div>\n'
                    '<div>test tag</div>\n'
                    '</div>' % tagid
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_new(self):
        """controllers.tag.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/tag/new', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/tag/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('select', {'id': 'languageid'}),
                                        '"languageid" input element not found')
        assert_true(response.html.find('input', {'id': 'name'}),
                                    '"name" input element not found')

    def test_post(self):
        """controllers.tag.Controller.post is working properly"""
        languageid, tagid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/tag/', dict(name='another tag',
                                               languageid=languageid,
                                              ),
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/tag/";' in response.body,
                        'should be redirected to "/admin/tag/" via javascript')

        tag = DBSession().query(Tag).get(u'another-tag')
        eq_(tag.name[''], u'another tag')
        eq_(tag.language_ids, set([languageid]))

    def test_edit(self):
        """controllers.tag.Controller.edit is working"""
        languageid, tagid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/tag/%s/edit' % tagid,
                                            extra_environ=environ, status=200)

        eq_(response.html.form['action'], u'/tag/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                {'name': 'tagid', 'value': tagid}),
                                'wrong tag_id')
        elem_languageid = response.html.find('select', {'id': 'languageid'})
        assert_true(elem_languageid, '"languageid" input element not found')
        eq_(elem_languageid.find('option', {'selected': 'selected'})['value'],
                                                            languageid)
        eq_(response.html.find('input', {'id': 'name'})['value'],
                                                        u'test tag')

    def test_put(self):
        """controllers.tag.Controller.put is working properly"""
        languageid, tagid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.put('/tag/%s' % tagid,
                                            dict(name='changed',
                                                 languageid=languageid,
                                                ),
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/tag/";' in response.body,
                        'should be redirected to "/admin/tag/" via javascript')

        tag = DBSession.query(Tag).get(u'changed')
        eq_(tag.name[languageid], 'changed')

    def test_get_delete(self):
        """controllers.tag.Controller.get_delete is working properly"""
        languageid, tagid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/tag/%s/delete' % tagid,
                                           extra_environ=environ, status=200)

        eq_(response.html.form['action'], u'/tag/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                {'name': '_method', 'value': 'DELETE'}),
                                '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                                {'name': 'tagid', 'value': tagid}),
                                'wrong tag_id')

    def test_post_delete(self):
        """controllers.tag.Controller.post_delete is working properly"""
        languageid, tagid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.delete('/tag?tagid=%s' % tagid,
                                            extra_environ=environ, status=200)
        assert_true('parent.location = "/admin/tag/";' in response.body,
                        'should be redirected to "/admin/tag/" via javascript')

        tag = DBSession.query(Tag).get(tagid.decode())
        assert_true(tag is None,
                            'Tag should have been deleted from the db')
        tagdata = DBSession.query(TagData).filter_by(parent_id=None).all()
        assert_false(tagdata,
                    'orphaned TagData should have been deleted from the db')

    def test_translation(self):
        """controllers.tag.Controller.translation is working properly"""
        languageid, tagid = self._fill_db()

        response = self.app.post('/tag/', dict(tagid=tagid,
                                               value=languageid,
                                               _method='TRANSLATION',
                                              )
                                )

        expected = '{"name": "test tag"}'
        eq_(response.body, expected)

