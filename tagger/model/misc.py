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
"""Miscellaneous model"""

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from tagger.model import DeclarativeBase, metadata

import logging
log = logging.getLogger(__name__)


############################################################
# Banner Content
############################################################
class BannerContent(DeclarativeBase):
    __tablename__ = 'banner_content'
    
    # Columns
    id = Column(Integer, primary_key=True)
    media_id = Column(Unicode(255), ForeignKey('media.id'))
    link_id = Column(Unicode(255), ForeignKey('links.id'))

    # Relations
    media = relation('Media')
    link = relation('Link')

    # Special methods
    def __init__(self, media=None, link=None):
        self.media = media
        self.link = link

    def __repr__(self):
        return '<BannerContent: media=%s link=%s>' % (self.media_id,
                                                                self.link_id)

