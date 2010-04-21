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

from tagger.model import DBSession, auth, content, misc
from tagger.tests.models import ModelTest

class TestBannerContent(ModelTest):
    """Unit test case for the ``BannerContent`` model."""
    klass = misc.BannerContent
    attrs = dict(
        )

    def do_get_dependencies(self):
        try:
            user = auth.User(user_name=u'test_user')
            DBSession.add(user)
            language = content.Language(id=u'xx', name=u'test_lang')
            DBSession.add(language)
            self.media = content.Media(u'image', u'test_image', u'test.png',
                                                                    user, u'xx')
            DBSession.add(self.media)
            self.link = content.Link(u'test_link', u'http://example.com',
                                                                    user, u'xx')
            DBSession.add(self.link)
            DBSession.flush()
            return dict(media=self.media,
                        link=self.link,
                       )
        except:
            DBSession.rollback()
            raise

    def test_obj_creation(self):
        """model.misc.BannerContent objects can be created"""
        self._obj_creation()

    def test_obj_query(self):
        """model.misc.BannerContent objects can be queried"""
        self._obj_query()

    def test_obj_creation_media(self):
        """model.misc.BannerContent constructor must set the media right"""
        eq_(self.obj.media, self.media)

    def test_obj_creation_link(self):
        """model.misc.BannerContent constructor must set the link right"""
        eq_(self.obj.link, self.link)


