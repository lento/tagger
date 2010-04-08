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
"""Functional test suite for the root controller"""

from nose.tools import assert_true

from tagger.tests import TestController


class TestAdminController(TestController):
    """Tests for the method in the admin controller."""

    def test_index(self):
        """controllers.admin.Controller.index is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin', extra_environ=environ, status=200)

        msg = 'admin'
        # You can look for specific strings:
        assert_true(msg in response)

