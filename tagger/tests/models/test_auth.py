# -*- coding: utf-8 -*-
"""Test suite for the TG app's models"""
from nose.tools import eq_

from tagger import model
from tagger.tests.models import ModelTest

class TestGroup(ModelTest):
    """Unit test case for the ``Group`` model."""
    klass = model.Group
    attrs = dict(
        group_name = u"test_group",
        display_name = u"Test Group"
        )

    def test_obj_creation(self):
        """model.Group objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.Group objects can be queried"""
        self._obj_query()

    def test_obj_creation_groupname(self):
        """model.Group constructor must set the user name right"""
        eq_(self.obj.group_name, u"test_group")

    def test_obj_creation_displayname(self):
        """model.Group constructor must set the display name right"""
        eq_(self.obj.display_name, u"Test Group")


class TestUser(ModelTest):
    """Unit test case for the ``User`` model."""
    
    klass = model.User
    attrs = dict(
        user_name = u"ignucius",
        email_address = u"ignucius@example.org"
        )

    def test_obj_creation(self):
        """model.User objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.User objects can be queried"""
        self._obj_query()

    def test_obj_creation_username(self):
        """model.User constructor must set the user name right"""
        eq_(self.obj.user_name, u"ignucius")

    def test_obj_creation_email(self):
        """model.User constructor must set the email right"""
        eq_(self.obj.email_address, u"ignucius@example.org")

    def test_no_permissions_by_default(self):
        """model.User objects should have no permission by default."""
        eq_(len(self.obj.permissions), 0)

    def test_getting_by_email(self):
        """model.User Users should be fetcheable by their email addresses"""
        him = model.User.by_email_address(u"ignucius@example.org")
        eq_(him, self.obj)


class TestPermission(ModelTest):
    """Unit test case for the ``Permission`` model."""
    
    klass = model.Permission
    attrs = dict(
        permission_name = u"test_permission",
        description = u"This is a test Description"
        )

    def test_obj_creation(self):
        """model.Permission objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.Permission objects can be queried"""
        self._obj_query()

    def test_obj_creation_email(self):
        """model.Permission constructor must set the name right"""
        eq_(self.obj.permission_name, u"test_permission")

    def test_obj_creation_email(self):
        """model.Permission constructor must set the description right"""
        eq_(self.obj.description, u"This is a test Description")

