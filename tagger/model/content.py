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
"""Content model"""

from datetime import datetime

from sqlalchemy import Table, ForeignKey, Column, DDL
from sqlalchemy.types import Unicode, UnicodeText, Integer, DateTime
from sqlalchemy.orm import relation, backref

from tagger.model import DeclarativeBase, metadata
from tagger.model.auth import User

import logging
log = logging.getLogger(__name__)

############################################################
# Associations
############################################################
class Associable(DeclarativeBase):
    __tablename__ = 'associables'
    
    # Columns
    id = Column(Integer, primary_key=True)
    association_type = Column(Unicode(50))
    
    # Properties
    @property
    def associated(self):
        return getattr(self, 'associated_%s' % self.association_type)
    
    # Methods
    def has_tags(self, tag_ids):
        find = set(tag_ids)
        tags = set([t.id for t in self.tags])
        return find.issubset(tags)
        
    # Special methods
    def __init__(self, association_type):
        self.association_type = association_type

    def __repr__(self):
        return '<Associable: %s (%s)>' % (self.id or 0, self.association_type)

associable_delete_trigger = (
    'CREATE TRIGGER delete_orphaned_%(table)s_associable DELETE ON %(table)s '
    'BEGIN '
        'DELETE FROM associables WHERE id=old.id; '
    'END;')


# Association table for the many-to-many relationship associables-tags.
associables_tags_table = Table('__associables_tags', metadata,
    Column('associable_id', Integer, ForeignKey('associables.id',
                                    onupdate='CASCADE', ondelete='CASCADE')),
    Column('tag_id', Unicode(50), ForeignKey('tags.id',
                                    onupdate='CASCADE', ondelete='CASCADE')),
)

class Tag(DeclarativeBase):
    __tablename__ = 'tags'
    
    # Columns
    id = Column(Unicode(50), primary_key=True)
    
    # Relations
    associables = relation(Associable, secondary=associables_tags_table,
                                backref=backref('tags', order_by='Tag.id'))
    
    # Properties
    @property
    def tagged(self):
        return [t.associated for t in self.associables]
    
    # Special methods
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Tag: %s>' % self.id

    def __json__(self):
        return dict(id=self.id)


############################################################
# Article
############################################################
class Category(DeclarativeBase):
    """Article categories"""
    __tablename__ = 'categories'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True)
    description = Column(Unicode(255))

    # Special methods
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Category: %s "%s">' % (self.id or 0, self.name)


class Article(DeclarativeBase):
    """Article definition"""
    __tablename__ = 'articles'

    # Columns
    id = Column(Integer, primary_key=True)
    associable_id = Column(Integer, ForeignKey('associables.id'))
    title = Column(Unicode(255), unique=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    text = Column(UnicodeText)

    # Relations
    associable = relation('Associable', backref=backref('associated_article',
                                                                uselist=False))
    user = relation('User', backref='articles')
    category = relation('Category', backref='articles')

    # Properties
    @property
    def tags(self):
        return self.associable.tags

    # Special methods
    def __init__(self, title, category, user, text):
        self.title = title
        self.category = category
        self.user = user
        self.text = text
        self.associable = Associable(u'article')

    def __repr__(self):
        return '<Article: %s "%s">' % (self.id or 0, self.title)

DDL(associable_delete_trigger).execute_at('after-create', Article.__table__)

