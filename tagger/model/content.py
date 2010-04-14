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

from sqlalchemy import Table, ForeignKey, Column, DDL, UniqueConstraint
from sqlalchemy.types import Unicode, UnicodeText, Integer, DateTime
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relation, backref, synonym

from tagger.model import DeclarativeBase, metadata
from tagger.model.utils import mapped_scalar, dict_property, add_language_props
from tagger.model.auth import User
from tagger.lib.utils import make_id

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

orphaned_associable_trigger = (
    #'DROP TRIGGER IF EXISTS delete_orphaned_%(table)s_associable; '
    'CREATE TRIGGER delete_orphaned_%(table)s_associable '
    'AFTER DELETE '
    'ON %(table)s '
    'FOR EACH ROW '
        'DELETE FROM associables WHERE id=old.associable_id; '
    )


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
# Language
############################################################
class Language(DeclarativeBase):
    __tablename__ = 'languages'

    # Columns
    id = Column(Unicode(3), primary_key=True)
    name = Column(Unicode(50), unique=True)

    # Special methods
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Language: %s %s>' % (self.id, self.name)


############################################################
# Category
############################################################
class Category(DeclarativeBase):
    """Article categories"""
    __tablename__ = 'categories'

    # Columns
    id = Column(Unicode(50), primary_key=True)

    # Special methods
    def __init__(self, name, lang, description=None):
        self.id = make_id(name)
        self.data.append(CategoryData(name, lang, description))

    def __repr__(self):
        return '<Category: %s %s>' % (self.id or 0, self.name)

add_language_props(Category,
    [('name', lambda obj, lang, val: CategoryData(val, lang, None)),
     ('description', lambda obj, lang, val: CategoryData(
                                                    obj.name[''], lang, val)),
    ])


class CategoryData(DeclarativeBase):
    """Language specific Category data"""
    __tablename__ = 'categories_data'
    __table_args__ = (UniqueConstraint('parent_id', 'language_id'),
                      {})

    # Columns
    id = Column(Integer, primary_key=True)
    parent_id = Column(Unicode(50), ForeignKey('categories.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    language_id = Column(Unicode(50), ForeignKey('languages.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    _name = Column('name', Unicode(255))
    description = Column(Unicode(255))

    # Relations
    parent = relation('Category', backref=backref('data',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('categories_data'))

    # Properties
    def _get_name(self):
        return self._name

    def _set_name(self, val):
        if self.parent.language_id == self.language_id:
            self.parent.id = make_id(val)
        self._name = val

    name = synonym('_name', descriptor=property(_get_name, _set_name))

    # Special methods
    def __init__(self, name, lang, description=None):
        self._name = name
        self.language_id = lang
        self.description = description

    def __repr__(self):
        return '<CategoryData: %s (%s) %s>' % (self.parent_id,
                                                    self.language_id, self.name)


############################################################
# Article
############################################################
class Article(DeclarativeBase):
    """Article definition"""
    __tablename__ = 'articles'

    # Columns
    id = Column(Integer, primary_key=True)
    string_id = Column(Unicode(255))
    associable_id = Column(Integer, ForeignKey('associables.id'))
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    category_id = Column(Unicode(50), ForeignKey('categories.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.now)

    # Relations
    associable = relation('Associable', backref=backref('associated_article',
                                                                uselist=False))
    user = relation('User', backref='articles')
    category = relation('Category', backref='articles')

    # Properties
    @property
    def tags(self):
        return self.associable.tags

    @property
    def language_id(self):
        return self.pages['default'].language_id

    @property
    def language_ids(self):
        langs = set()
        for p in self.pages:
            langs |= p.language_ids
        return langs

    @property
    def languages(self):
        langs = set()
        for p in self.pages:
            langs |= p.languages
        return langs

    @property
    def title(self):
        return self.pages['default'].name

    @property
    def text(self):
        return self.pages['default'].text

    @property
    def modified(self):
        return max([p.modified for p in self.pages])

    # Special methods
    def __init__(self, title, category, lang, user, text=None):
        self.string_id = make_id(title)
        self.category = category
        self.user = user
        self.associable = Associable(u'article')
        self.pages.append(Page(title, lang, text=text,
                                                        string_id=u'default'))

    def __repr__(self):
        return '<Article: %s %s>' % (self.id, self.string_id)

DDL(orphaned_associable_trigger).execute_at('after-create', Article.__table__)


############################################################
# Page
############################################################
class Page(DeclarativeBase):
    """Article page"""
    __tablename__ = 'pages'
    __table_args__ = [UniqueConstraint(['string_id', 'article_id']),
                      {}
                     ]

    # Columns
    id = Column(Integer, primary_key=True)
    string_id = Column(Unicode(255))
    article_id = Column(Integer, ForeignKey('articles.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))

    # Relations
    article = relation('Article', backref=backref('pages',
                                collection_class=mapped_scalar('string_id')))

    # Properties
    @property
    def modified(self):
        return max([d.modified for d in self.data])

    # Special methods
    def __init__(self, name, lang, text=None, string_id=None):
        self.string_id = string_id or make_id(name)
        self.data.append(PageData(name, lang, text))

    def __repr__(self):
        return '<Page: [%s] %s %s>' % (self.article_id, self.id, self.string_id)

add_language_props(Page,
    [('name', lambda obj, lang, val: PageData(val, lang, None)),
     ('text', lambda obj, lang, val: CategoryData(obj.name[''], lang, val)),
    ])


class PageData(DeclarativeBase):
    """Language specific Page data"""
    __tablename__ = 'pages_data'
    __table_args__ = (UniqueConstraint('parent_id', 'language_id'),
                      {})

    # Columns
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('pages.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    language_id = Column(Unicode(50), ForeignKey('languages.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    _name = Column('name', Unicode(255))
    created = Column(DateTime, default=datetime.now)
    modified = Column(TIMESTAMP, default=datetime.now)
    text = Column(UnicodeText)

    # Relations
    parent = relation('Page', backref=backref('data',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('pages_data'))

    # Properties
    def _get_name(self):
        return self._name

    def _set_name(self, val):
        if self.parent.language_id == self.language_id:
            if self.parent.string_id == 'default':
                self.parent.article.string_id = make_id(val)
            else:
                self.parent.string_id = make_id(val)
        self._name = val

    name = synonym('_name', descriptor=property(_get_name, _set_name))

    # Special methods
    def __init__(self, name, lang, text=None):
        self._name = name
        self.language_id = lang
        self.text = text

    def __repr__(self):
        return '<PageData: %s (%s) %s>' % (self.parent_id, self.language_id,
                                                                    self.name)


############################################################
# Link
############################################################
class Link(DeclarativeBase):
    """Link definition"""
    __tablename__ = 'links'

    # Columns
    id = Column(Integer, primary_key=True)
    associable_id = Column(Integer, ForeignKey('associables.id'))
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    created = Column(DateTime, default=datetime.now)
    uri = Column(Unicode(255))

    # Relations
    associable = relation('Associable', backref=backref('associated_link',
                                                                uselist=False))
    user = relation('User', backref='links')

    # Properties
    @property
    def modified(self):
        return max([d.modified for d in self.data])

    # Special methods
    def __init__(self, uri, user, lang, description=None):
        self.uri = uri
        self.user = user
        self.data.append(LinkData(lang, description))

    def __repr__(self):
        return '<Link: %s %s>' % (self.id, self.uri)

DDL(orphaned_associable_trigger).execute_at('after-create', Link.__table__)
add_language_props(Link, 
            [('description', lambda obj, lang, val: LinkData(lang, val))])


class LinkData(DeclarativeBase):
    """Language specific Link data"""
    __tablename__ = 'links_data'
    __table_args__ = (UniqueConstraint('parent_id', 'language_id'),
                      {})

    # Columns
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('links.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    language_id = Column(Unicode(50), ForeignKey('languages.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    description = Column(Unicode(255))
    modified = Column(TIMESTAMP, default=datetime.now)

    # Relations
    parent = relation('Link', backref=backref('data',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('links_data'))

    # Special methods
    def __init__(self, lang, description=None):
        self.language_id = lang
        self.description = description

    def __repr__(self):
        return '<linkData: %s (%s)>' % (self.parent_id, self.language_id)


############################################################
# Media
############################################################
class Media(DeclarativeBase):
    """Media definition"""
    __tablename__ = 'media'

    # Columns
    id = Column(Integer, primary_key=True)
    associable_id = Column(Integer, ForeignKey('associables.id'))
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    created = Column(DateTime, default=datetime.now)
    type = Column(Unicode(50))
    uri = Column(Unicode(255))

    # Relations
    associable = relation('Associable', backref=backref('associated_media',
                                                                uselist=False))
    user = relation('User', backref='media')

    # Properties
    @property
    def modified(self):
        return max([d.modified for d in self.data])

    # Special methods
    def __init__(self, type, uri, user, lang, description=None):
        self.type = type
        self.uri = uri
        self.user = user
        self.data.append(MediaData(lang, description))

    def __repr__(self):
        return '<Media: %s %s %s>' % (self.id, self, type, self.uri)

DDL(orphaned_associable_trigger).execute_at('after-create', Media.__table__)
add_language_props(Media, 
            [('description', lambda obj, lang, val: MediaData(lang, val))])


class MediaData(DeclarativeBase):
    """Language specific Media data"""
    __tablename__ = 'media_data'
    __table_args__ = (UniqueConstraint('parent_id', 'language_id'),
                      {})

    # Columns
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('media.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    language_id = Column(Unicode(50), ForeignKey('languages.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    description = Column(Unicode(255))
    modified = Column(TIMESTAMP, default=datetime.now)

    # Relations
    parent = relation('Media', backref=backref('data',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('media_data'))

    # Special methods
    def __init__(self, lang, description=None):
        self.language_id = lang
        self.description = description

    def __repr__(self):
        return '<MediaData: %s (%s)>' % (self.parent_id, self.language_id)

