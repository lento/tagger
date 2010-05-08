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
"""Settings model"""

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from tagger.model import DeclarativeBase, metadata

import logging
log = logging.getLogger(__name__)


############################################################
# Settings
############################################################
class Setting(DeclarativeBase):
    __tablename__ = 'settings'

    # Columns
    id = Column(Unicode(255), primary_key=True)
    value = Column(Unicode(255))

    # Special methods
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __repr__(self):
        return '<Setting: id=%s value=%s>' % (self.id, self.value)

