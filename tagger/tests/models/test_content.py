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

from nose.tools import eq_

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
        name = u"test_category",
        description = u"Test Category"
        )

    def test_obj_creation(self):
        """model.content.Category objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Category objects can be queried"""
        self._obj_query()

    def test_obj_creation_name(self):
        """model.content.Category constructor must set the name right"""
        eq_(self.obj.name, u"test_category")

    def test_obj_creation_description(self):
        """model.content.Category constructor must set the description right"""
        eq_(self.obj.description, u"Test Category")


class TestArticle(ModelTest):
    """Unit test case for the ``Article`` model."""
    
    klass = content.Article
    attrs = dict(
        title = u"A test article",
        text = u"random text",
        )

    def do_get_dependencies(self):
        try:
            self.user = auth.User(user_name=u'test_user')
            DBSession.add(self.user)
            self.category = content.Category(name=u'test_category')
            DBSession.add(self.category)
            DBSession.flush()
            return dict(user=self.user, category=self.category)
        except:
            DBSession.rollback()
            raise

    def test_obj_creation(self):
        """model.content.Article objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.content.Article objects can be queried"""
        self._obj_query()

    def test_obj_creation_title(self):
        """model.content.Article constructor must set the title right"""
        eq_(self.obj.title, u"A test article")

    def test_obj_creation_text(self):
        """model.content.Article constructor must set the text right"""
        eq_(self.obj.text, u"random text")

    def test_obj_creation_user(self):
        """model.content.Article constructor must set the user right"""
        eq_(self.obj.user, self.user)

    def test_obj_creation_category(self):
        """model.content.Article constructor must set the category right"""
        eq_(self.obj.category, self.category)

    def test_is_taggable(self):
        """model.content.Article objects are taggable"""
        tag = content.Tag(id=u'test_tag')
        self.obj.tags.append(tag)
        DBSession.flush()
        eq_(self.obj.tags[0], tag) 

