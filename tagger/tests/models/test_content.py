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
"""Test suite for the TG app's models"""

from nose.tools import eq_, assert_true, assert_equals

from tagger.model import DBSession, auth, content
from tagger.tests.models import ModelTest

class TestAssociable(ModelTest):
    """Unit test case for the ``Associable`` model."""
    klass = content.Associable
    attrs = dict(
        association_type = u"test_association_type",
        )

    def test_obj_creation(self):
        """model.content.Associable objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Associable objects can be queried"""
        self._obj_query()

    def test_obj_creation_association_type(self):
        """model.content.Associable constructor must set the association_type right"""
        eq_(self.obj.association_type, u"test_association_type")


class TestTag(ModelTest):
    """Unit test case for the ``Tag`` model."""
    klass = content.Tag
    attrs = dict(
        id = u"test_tag",
        )

    def test_obj_creation(self):
        """model.content.Tag objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Tag objects can be queried"""
        self._obj_query()

    def test_obj_creation_id(self):
        """model.content.Tag constructor must set the id right"""
        eq_(self.obj.id, u"test_tag")


class TestCategory(ModelTest):
    """Unit test case for the ``Category`` model."""
    klass = content.Category
    attrs = dict(
        name = u"test category",
        description = u"Test Category"
        )

    def do_get_dependencies(self):
        try:
            self.language = content.Language(id=u'xx', name=u'test_lang')
            DBSession.add(self.language)
            DBSession.flush()
            return dict(lang=self.language.id,
                       )
        except:
            DBSession.rollback()
            raise

    def test_obj_creation(self):
        """model.content.Category objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Category objects can be queried"""
        obj = DBSession.query(self.klass).get(u"test-category")
        assert_true(obj, 'Category not found')

    def test_obj_creation_id(self):
        """model.content.Category constructor must set the name right"""
        eq_(self.obj.id, u"test-category")

    def test_obj_creation_description(self):
        """model.content.Category constructor must set the description right"""
        eq_(self.obj.description[''], u"Test Category")

    def test_obj_property_language_id_get(self):
        """model.content.Category property "language_id" can get value"""
        eq_(self.obj.language_id, self.language.id)

    def test_obj_property_language_ids_get(self):
        """model.content.Category property "language_ids" can get value"""
        eq_(self.obj.language_ids, set([self.language.id]))

    def test_obj_property_languages_get(self):
        """model.content.Category property "languages" can get value"""
        eq_(self.obj.languages, set([self.language]))

    def test_obj_property_name_get(self):
        """model.content.Category property "name" can get value"""
        expected = u'test category'
        assert_equals(self.obj.name[''], expected,
                'Category.name[""] should be "%s", not "%s"' % 
                (expected, self.obj.name['']))
        assert_equals(self.obj.name[u'xx'], expected,
                'Category.name["xx"] should be "%s", not "%s"' % 
                (expected, self.obj.name[u'xx']))

    def test_obj_property_name_set(self):
        """model.content.Category property "name" can set value"""
        expected = u'changed name'
        self.obj.name[''] = expected
        assert_equals(self.obj.data[0].name, expected,
                'Category.data[0].name should be "%s", not "%s"' % 
                (expected, self.obj.data[0].name))

    def test_obj_property_description_get(self):
        """model.content.Category property "description" can get value"""
        expected = u'Test Category'
        assert_equals(self.obj.description[''], expected,
                'Category.description[""] should be "%s", not "%s"' % 
                (expected, self.obj.description['']))
        assert_equals(self.obj.description[u'xx'], expected,
                'Category.description["xx"] should be "%s", not "%s"' % 
                (expected, self.obj.description[u'xx']))

    def test_obj_property_description_set(self):
        """model.content.Category property "description" can set value"""
        expected = u'changed text'
        self.obj.description[''] = expected
        assert_equals(self.obj.data[0].description, expected,
                'Category.data[0].description should be "%s", not "%s"' % 
                (expected, self.obj.data[0].description))


class TestArticle(ModelTest):
    """Unit test case for the ``Article`` model."""
    
    klass = content.Article
    attrs = dict()

    def do_get_dependencies(self):
        try:
            self.user = auth.User(user_name=u'test_user')
            DBSession.add(self.user)
            self.language = content.Language(id=u'xx', name=u'test_lang')
            DBSession.add(self.language)
            self.category = content.Category(u'test category', u'xx')
            DBSession.add(self.category)
            DBSession.flush()
            return dict(title=u"A test article!",
                        category=self.category,
                        user=self.user,
                        #language=self.language,
                        lang=self.language.id,
                        text = u"random text"
                       )
        except:
            DBSession.rollback()
            raise

    def test_obj_creation(self):
        """model.content.Article objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Article objects can be queried"""
        self._obj_query()

    def test_obj_creation_id(self):
        """model.content.Article constructor must set the id right"""
        eq_(self.obj.id, u'a-test-article')

    def test_obj_creation_default_page(self):
        """model.content.Article constructor must create a default page"""
        assert_true(len(self.obj.pages), 'Article.pages is empty')

    def test_obj_creation_user(self):
        """model.content.Article constructor must set the user right"""
        eq_(self.obj.user, self.user)

    def test_obj_creation_category(self):
        """model.content.Article constructor must set the category right"""
        eq_(self.obj.category, self.category)

    def test_obj_property_language_id_get(self):
        """model.content.Article property "language_id" can get value"""
        eq_(self.obj.language_id, self.language.id)

    def test_obj_property_language_ids_get(self):
        """model.content.Article property "language_ids" can get value"""
        eq_(self.obj.language_ids, set([self.language.id]))

    def test_obj_property_languages_get(self):
        """model.content.Article property "languages" can get value"""
        eq_(self.obj.languages, set([self.language]))

    def test_obj_property_title_get(self):
        """model.content.Article property "title" can get value"""
        expected = u'A test article!'
        assert_equals(self.obj.title[''], expected,
                'Article.title[""] should be "%s", not "%s"' % 
                (expected, self.obj.title['']))
        assert_equals(self.obj.title[u'xx'], expected,
                'Article.title["xx"] should be "%s", not "%s"' % 
                (expected, self.obj.title[u'xx']))

    def test_obj_property_title_set(self):
        """model.content.Article property "title" can set value"""
        expected = u'changed title'
        self.obj.title[''] = expected
        assert_equals(self.obj.pages['default'].name[''], expected,
                'Article.pages["default"].name[""] should be "%s", not "%s"' % 
                (expected, self.obj.pages['default'].name['']))
        assert_equals(self.obj.pages['default'].name[u'xx'], expected,
                'Article.pages["default"].name["xx"] should be "%s", not "%s"' % 
                (expected, self.obj.pages['default'].name[u'xx']))

    def test_obj_property_text_get(self):
        """model.content.Article property "text" can get value"""
        expected = u'random text'
        assert_equals(self.obj.text[''], expected,
                'Article.text[""] should be "%s", not "%s"' % 
                (expected, self.obj.text['']))
        assert_equals(self.obj.text[u'xx'], expected,
                'Article.text["xx"] should be "%s", not "%s"' % 
                (expected, self.obj.text[u'xx']))

    def test_obj_property_text_set(self):
        """model.content.Article property "text" can set value"""
        expected = u'changed text'
        self.obj.text[''] = expected
        assert_equals(self.obj.pages['default'].text[''], expected,
                'Article.pages["default"].text[""] should be "%s", not "%s"' % 
                (expected, self.obj.pages['default'].text['']))
        assert_equals(self.obj.pages['default'].text[u'xx'], expected,
                'Article.pages["default"].text["xx"] should be "%s", not "%s"' % 
                (expected, self.obj.pages['default'].text[u'xx']))

    def test_is_taggable(self):
        """model.content.Article objects are taggable"""
        tag = content.Tag(id=u'test_tag')
        self.obj.tags.append(tag)
        DBSession.flush()
        eq_(self.obj.tags[0], tag) 


class TestPage(ModelTest):
    """Unit test case for the ``Page`` model."""

    klass = content.Page
    attrs = dict()

    def do_get_dependencies(self):
        try:
            self.language = content.Language(id=u'xx', name=u'test_lang')
            DBSession.add(self.language)
            DBSession.flush()
            return dict(name=u"A test page!",
                        lang=self.language.id,
                        text=u"random text",
                       )
        except:
            DBSession.rollback()
            raise

    def test_obj_creation(self):
        """model.content.Page objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Page objects can be queried"""
        self._obj_query()

    def test_obj_creation_string_id(self):
        """model.content.Page constructor must set the string_id right"""
        eq_(self.obj.string_id, u'a-test-page')

    def test_obj_creation_page_data(self):
        """model.content.Page constructor must create a PageData"""
        assert_true(len(self.obj.data), 'Page.data is empty')

    def test_obj_creation_page_data_title(self):
        """model.content.PageData constructor must set the name right"""
        eq_(self.obj.data[0].name, u'A test page!')

    def test_obj_creation_page_data_language(self):
        """model.content.PageData constructor must set the language right"""
        eq_(self.obj.data[0].language, self.language)

    def test_obj_creation_text(self):
        """model.content.PageData constructor must set the text right"""
        eq_(self.obj.data[0].text, u"random text")

    def test_obj_property_language_id_get(self):
        """model.content.Page property "language_id" can get value"""
        eq_(self.obj.language_id, self.language.id)

    def test_obj_property_language_ids_get(self):
        """model.content.Page property "language_ids" can get value"""
        eq_(self.obj.language_ids, set([self.language.id]))

    def test_obj_property_languages_get(self):
        """model.content.Page property "languages" can get value"""
        eq_(self.obj.languages, set([self.language]))

    def test_obj_property_name_get(self):
        """model.content.Page property "name" can get value"""
        expected = u'A test page!'
        assert_equals(self.obj.name[''], expected,
                        'Page.name[""] should be "%s", not "%s"' %
                        (expected, self.obj.name['']))
        assert_equals(self.obj.name[u'xx'], expected,
                        'Page.name[u"xx"] should be "%s", not "%s"' %
                        (expected, self.obj.name[u'xx']))

    def test_obj_property_name_set(self):
        """model.content.Page property "name" can set value"""
        expected = u'changed name (default lang)'
        self.obj.name[''] = expected
        assert_equals(self.obj.name[''], expected,
                        'Page.name[""] should be "%s", not "%s"' %
                        (expected, self.obj.name['']))

        expected = u'changed name (specific lang)'
        self.obj.name[u'xx'] = expected
        assert_equals(self.obj.name[u'xx'], expected,
                        'Page.name[u"xx"] should be "%s", not "%s"' %
                        (expected, self.obj.name[u'xx']))

    def test_obj_property_text_get(self):
        """model.content.Page property "text" can get value"""
        expected = u'random text'
        assert_equals(self.obj.text[''], expected,
                        'Page.text[""] should be "%s", not "%s"' %
                        (expected, self.obj.text['']))
        assert_equals(self.obj.text[u'xx'], expected,
                        'Page.text[u"xx"] should be "%s", not "%s"' %
                        (expected, self.obj.text[u'xx']))

    def test_obj_property_text_set(self):
        """model.content.Page property "text" can set value"""
        expected = u'changed text (default lang)'
        self.obj.text[''] = expected
        assert_equals(self.obj.text[''], expected,
                        'Page.text[""] should be "%s", not "%s"' %
                        (expected, self.obj.text['']))

        expected = u'changed text (specific lang)'
        self.obj.text[u'xx'] = expected
        assert_equals(self.obj.text[u'xx'], expected,
                        'Page.text[u"xx"] should be "%s", not "%s"' %
                        (expected, self.obj.text[u'xx']))


class TestLink(ModelTest):
    """Unit test case for the ``Link`` model."""
    klass = content.Link
    attrs = dict(
        uri = u"http://example.com",
        name = u'test link',
        description = u"Test Link"
        )

    def do_get_dependencies(self):
        try:
            self.user = auth.User(user_name=u'test_user')
            DBSession.add(self.user)
            self.language = content.Language(id=u'xx', name=u'test_lang')
            DBSession.add(self.language)
            DBSession.flush()
            return dict(lang=self.language.id,
                        user=self.user,
                       )
        except:
            DBSession.rollback()
            raise

    def test_obj_creation(self):
        """model.content.Link objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Link objects can be queried"""
        obj = DBSession.query(self.klass).get(u'test-link')
        assert_true(obj, 'Link not found')
        eq_(obj.uri, self.attrs['uri'])

    def test_obj_creation_id(self):
        """model.content.Link constructor must set the id right"""
        eq_(self.obj.id, u'test-link')

    def test_obj_creation_name(self):
        """model.content.Link constructor must set the name right"""
        eq_(self.obj.name[''], u'test link')

    def test_obj_creation_uri(self):
        """model.content.Link constructor must set the uri right"""
        eq_(self.obj.uri, u"http://example.com")

    def test_obj_creation_user(self):
        """model.content.Link constructor must set the user right"""
        eq_(self.obj.user, self.user)

    def test_obj_creation_description(self):
        """model.content.Link constructor must set the description right"""
        eq_(self.obj.description[''], u"Test Link")

    def test_obj_property_language_id_get(self):
        """model.content.Link property "language_id" can get value"""
        eq_(self.obj.language_id, self.language.id)

    def test_obj_property_language_ids_get(self):
        """model.content.Link property "language_ids" can get value"""
        eq_(self.obj.language_ids, set([self.language.id]))

    def test_obj_property_languages_get(self):
        """model.content.Link property "languages" can get value"""
        eq_(self.obj.languages, set([self.language]))

    def test_obj_property_name_get(self):
        """model.content.Link property "name" can get value"""
        expected = u'test link'
        assert_equals(self.obj.name[''], expected,
                        'Link.name[""] should be "%s", not "%s"' %
                        (expected, self.obj.name['']))
        assert_equals(self.obj.name[u'xx'], expected,
                        'Link.name[u"xx"] should be "%s", not "%s"' %
                        (expected, self.obj.name[u'xx']))

    def test_obj_property_name_set(self):
        """model.content.Link property "name" can set value"""
        expected = u'changed name (default lang)'
        self.obj.name[''] = expected
        assert_equals(self.obj.name[''], expected,
                        'Link.name[""] should be "%s", not "%s"' %
                        (expected, self.obj.name['']))

        expected = u'changed name (specific lang)'
        self.obj.name[u'xx'] = expected
        assert_equals(self.obj.name[u'xx'], expected,
                        'Link.name[u"xx"] should be "%s", not "%s"' %
                        (expected, self.obj.name[u'xx']))

    def test_obj_property_description_get(self):
        """model.content.Link property "description" can get value"""
        expected = u'Test Link'
        assert_equals(self.obj.description[''], expected,
                'Link.description[""] should be "%s", not "%s"' %
                (expected, self.obj.description['']))
        assert_equals(self.obj.description[u'xx'], expected,
                'Link.description["xx"] should be "%s", not "%s"' %
                (expected, self.obj.description[u'xx']))

    def test_obj_property_description_set(self):
        """model.content.Link property "description" can set value"""
        expected = u'changed text'
        self.obj.description[''] = expected
        assert_equals(self.obj.data[0].description, expected,
                'Link.data[0].description should be "%s", not "%s"' %
                (expected, self.obj.data[0].description))


class TestMedia(ModelTest):
    """Unit test case for the ``Media`` model."""
    klass = content.Media
    attrs = dict(
        type = u'image',
        name = u'test image',
        uri = u"/test.png",
        description = u"Test Media",
        )

    def do_get_dependencies(self):
        try:
            self.user = auth.User(user_name=u'test_user')
            DBSession.add(self.user)
            self.language = content.Language(id=u'xx', name=u'test_lang')
            DBSession.add(self.language)
            DBSession.flush()
            return dict(lang=self.language.id,
                        user=self.user,
                       )
        except:
            DBSession.rollback()
            raise

    def test_obj_creation(self):
        """model.content.Media objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Media objects can be queried"""
        obj = DBSession.query(self.klass).get(u'test-image')
        assert_true(obj, 'Media not found')
        eq_(obj.uri, self.attrs['uri'])

    def test_obj_creation_type(self):
        """model.content.Media constructor must set the type right"""
        eq_(self.obj.type, u'image')

    def test_obj_creation_id(self):
        """model.content.Media constructor must set the id right"""
        eq_(self.obj.id, u'test-image')

    def test_obj_creation_name(self):
        """model.content.Media constructor must set the name right"""
        eq_(self.obj.name[''], u'test image')

    def test_obj_creation_uri(self):
        """model.content.Media constructor must set the uri right"""
        eq_(self.obj.uri, u'/test.png')

    def test_obj_creation_user(self):
        """model.content.Media constructor must set the user right"""
        eq_(self.obj.user, self.user)

    def test_obj_creation_description(self):
        """model.content.Media constructor must set the description right"""
        eq_(self.obj.description[''], u"Test Media")

    def test_obj_property_language_id_get(self):
        """model.content.Media property "language_id" can get value"""
        eq_(self.obj.language_id, self.language.id)

    def test_obj_property_language_ids_get(self):
        """model.content.Media property "language_ids" can get value"""
        eq_(self.obj.language_ids, set([self.language.id]))

    def test_obj_property_languages_get(self):
        """model.content.Media property "languages" can get value"""
        eq_(self.obj.languages, set([self.language]))

    def test_obj_property_name_get(self):
        """model.content.Media property "name" can get value"""
        expected = u'test image'
        assert_equals(self.obj.name[''], expected,
                        'Media.name[""] should be "%s", not "%s"' %
                        (expected, self.obj.name['']))
        assert_equals(self.obj.name[u'xx'], expected,
                        'Media.name[u"xx"] should be "%s", not "%s"' %
                        (expected, self.obj.name[u'xx']))

    def test_obj_property_name_set(self):
        """model.content.Media property "name" can set value"""
        expected = u'changed name (default lang)'
        self.obj.name[''] = expected
        assert_equals(self.obj.name[''], expected,
                        'Media.name[""] should be "%s", not "%s"' %
                        (expected, self.obj.name['']))

        expected = u'changed name (specific lang)'
        self.obj.name[u'xx'] = expected
        assert_equals(self.obj.name[u'xx'], expected,
                        'Media.name[u"xx"] should be "%s", not "%s"' %
                        (expected, self.obj.name[u'xx']))

    def test_obj_property_description_get(self):
        """model.content.Media property "description" can get value"""
        expected = u'Test Media'
        assert_equals(self.obj.description[''], expected,
                'Media.description[""] should be "%s", not "%s"' %
                (expected, self.obj.description['']))
        assert_equals(self.obj.description[u'xx'], expected,
                'Media.description["xx"] should be "%s", not "%s"' %
                (expected, self.obj.description[u'xx']))

    def test_obj_property_description_set(self):
        """model.content.Media property "description" can set value"""
        expected = u'changed text'
        self.obj.description[''] = expected
        assert_equals(self.obj.data[0].description, expected,
                'Media.data[0].description should be "%s", not "%s"' %
                (expected, self.obj.data[0].description))


