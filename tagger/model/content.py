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

from sqlalchemy import Table, ForeignKey, Column, UniqueConstraint, desc
from sqlalchemy.types import Unicode, UnicodeText, Integer, DateTime
from sqlalchemy.types import TIMESTAMP, Boolean, Enum
from sqlalchemy.orm import relation, backref, synonym
from sqlalchemy.ext.declarative import synonym_for

from tagger.model import DeclarativeBase, metadata
from tagger.model.utils import mapped_scalar, dict_property
from tagger.model.utils import add_language_props, add_version_props
from tagger.model.auth import User
from tagger.model.utils import make_id
from tagger.model.history_meta import VersionedMeta

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
    _created = Column('created', DateTime)
    published = Column(Boolean, default=True)
    
    # Properties
    @property
    def associated(self):
        return getattr(self, 'associated_%s' % self.association_type)

    @property
    def type(self):
        return self.association_type

    @synonym_for('_created')
    @property
    def created(self):
        return self._created

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


# Association table for the many-to-many relationship associables-tags.
associables_tags_table = Table('__associables_tags', metadata,
    Column('associable_id', Integer, ForeignKey('associables.id',
                                    onupdate='CASCADE', ondelete='CASCADE')),
    Column('tag_id', Unicode(50), ForeignKey('tags.id',
                                    onupdate='CASCADE', ondelete='CASCADE')),
)

############################################################
# Tag
############################################################
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
    def __init__(self, name, lang):
        self.id = make_id(name)
        self.data.append(TagData(name, lang))

    def __repr__(self):
        return '<Tag: %s>' % self.id

    def __json__(self):
        return dict(id=self.id)

add_language_props(Tag,
    [('name', lambda obj, lang, val: TagData(val, lang)),
    ])


class TagData(DeclarativeBase):
    """Language specific Tag data"""
    __tablename__ = 'tags_data'
    __table_args__ = (UniqueConstraint('parent_id', 'language_id'),
                      {})

    # Columns
    id = Column(Integer, primary_key=True)
    parent_id = Column(Unicode(50), ForeignKey('tags.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    language_id = Column(Unicode(50), ForeignKey('languages.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    _name = Column('name', Unicode(255))

    # Relations
    parent = relation('Tag', backref=backref('data',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('tags_data'))

    # Properties
    def _get_name(self):
        return self._name

    def _set_name(self, val):
        if self.parent.language_id == self.language_id:
            self.parent.id = make_id(val)
        self._name = val

    name = synonym('_name', descriptor=property(_get_name, _set_name))

    # Special methods
    def __init__(self, name, lang):
        self._name = name
        self.language_id = lang

    def __repr__(self):
        return '<TagData: %s (%s) %s>' % (self.parent_id,
                                                    self.language_id, self.name)


############################################################
# Comments
############################################################
class Comment(DeclarativeBase):
    __tablename__ = 'comments'
    
    # Columns
    id = Column(Integer, primary_key=True)
    associable_id = Column(Integer, ForeignKey('associables.id'))
    name = Column(Unicode(255))
    email = Column(Unicode(255))
    text = Column(UnicodeText)
    created = Column(DateTime, default=datetime.now)
    status = Column(Enum('waiting', 'approved', 'spam'), default='waiting')

    # Relations
    associable = relation(Associable, backref=backref('comments',
                                                    order_by=(desc('created'))))
    
    # Properties
    @property
    def commented(self):
        return self.associable and self.associable.associated or None

    @property
    def to(self):
        if isinstance(self.commented, Article):
            return '%s/%s' % (self.commented.category.id, self.commented.id)
        elif isinstance(self.commented, Media):
            return 'media/%s' % self.commented.id
        elif isinstance(self.commented, Link):
            return 'link/%s' % self.commented.id
        else:
            return ''

    @property
    def header(self):
        return '%s at %s' %(self.name, self.created)
    
    @property
    def summary(self):
        characters = 75
        summary = self.text[0:characters]
        if len(self.text) > characters:
            summary = '%s[...]' % summary
        return summary
    
    @property
    def lines(self):
        return [dict(line=l) for l in self.text.split('\n')]
    
    # Special methods
    def __init__(self, name, email, text):
        self.name = name
        self.email = email
        self.text = text

    def __repr__(self):
        return '<Comment: by %s at %s "%s">' % (self.name, self.created,
                                                                self.summary)


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
    id = Column(Unicode(255), primary_key=True)
    associable_id = Column(Integer, ForeignKey('associables.id'))
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    category_id = Column(Unicode(50), ForeignKey('categories.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    _created = Column('created', DateTime)

    # Relations
    associable = relation('Associable', backref=backref('associated_article',
                                                                uselist=False))
    user = relation('User', backref='articles')
    category = relation('Category', backref='articles')

    # Properties
    @synonym_for('_created')
    @property
    def created(self):
        return self._created

    @property
    def tags(self):
        return self.associable.tags

    @property
    def comments(self):
        return self.associable.comments

    @property
    def language_id(self):
        return self.pages['default'].language_id

    @property
    def language_ids(self):
        langs = []
        for p in self.pages:
            for l in p.language_ids:
                if l not in langs:
                    langs.append(l)
        return langs

    @property
    def languages(self):
        langs = []
        for p in self.pages:
            for l in p.languages:
                if l not in langs:
                    langs.append(l)
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
    
    published = property(
        lambda self: self.associable.published,
        lambda self, val: setattr(self.associable, 'published', val)
    )

    # Special methods
    def __init__(self, title, category, lang, user, text=None):
        self.id = make_id(title)
        self.category = category
        self.user = user
        self.pages.append(Page(title, lang, user, text=text, is_default=True))
        self.associable = Associable(u'article')
        now = datetime.now()
        self._created = now
        self.associable._created = now
        self.published = False

    def __repr__(self):
        return '<Article: %s>' % self.id


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
    article_id = Column(Unicode(255), ForeignKey('articles.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    _created = Column('created', DateTime)

    # Relations
    article = relation('Article', backref=backref('pages',
                                collection_class=mapped_scalar('string_id')))
    user = relation('User', backref='pages')

    # Properties
    @synonym_for('_created')
    @property
    def created(self):
        return self._created

    @property
    def modified(self):
        return max([d.modified for d in self.data])

    # Special methods
    def __init__(self, name, lang, user, text=None, is_default=False):
        self.string_id = is_default and u'default' or make_id(name)
        self.data.append(PageData(name, lang, text))
        self.user = user
        now = datetime.now()
        self._created = now        

    def __repr__(self):
        return '<Page: [%s] %s %s>' % (self.article_id, self.id, self.string_id)

add_language_props(Page,
    [('name', lambda obj, lang, val: PageData(val, lang, None)),
     ('text', lambda obj, lang, val: PageData(obj.name[''], lang, val)),
    ])
add_version_props(Page)


class PageData(DeclarativeBase):
    """Language specific Page data"""
    __metaclass__ = VersionedMeta
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
                                order_by='PageData.created',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('pages_data'))

    # Properties
    def _get_name(self):
        return self._name

    def _set_name(self, val):
        if self.parent.language_id == self.language_id:
            if self.parent.string_id == 'default':
                self.parent.article.id = make_id(val)
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
    id = Column(Unicode(255), primary_key=True)
    associable_id = Column(Integer, ForeignKey('associables.id'))
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    _created = Column('created', DateTime)
    uri = Column(Unicode(255))

    # Relations
    associable = relation('Associable', backref=backref('associated_link',
                                                                uselist=False))
    user = relation('User', backref='links')

    # Properties
    @synonym_for('_created')
    @property
    def created(self):
        return self._created

    @property
    def tags(self):
        return self.associable.tags

    @property
    def comments(self):
        return self.associable.comments

    @property
    def modified(self):
        return max([d.modified for d in self.data])

    published = property(
        lambda self: self.associable.published,
        lambda self, val: setattr(self.associable, 'published', val)
    )

    # Special methods
    def __init__(self, name, uri, user, lang, description=None):
        self.id = make_id(name)
        self.uri = uri
        self.user = user
        self.data.append(LinkData(name, lang, description))
        self.associable = Associable(u'link')
        now = datetime.now()
        self._created = now        
        self.associable._created = now

    def __repr__(self):
        return '<Link: %s %s>' % (self.id, self.uri)

add_language_props(Link, 
    [('name', lambda obj, lang, val: LinkData(val, lang, None)),
     ('description', lambda obj, lang, val: LinkData(obj.name[''], lang, val)),
    ])
add_version_props(Link)


class LinkData(DeclarativeBase):
    """Language specific Link data"""
    __metaclass__ = VersionedMeta
    __tablename__ = 'links_data'
    __table_args__ = (UniqueConstraint('parent_id', 'language_id'),
                      {})

    # Columns
    id = Column(Integer, primary_key=True)
    parent_id = Column(Unicode(255), ForeignKey('links.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    language_id = Column(Unicode(50), ForeignKey('languages.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    _name = Column('name', Unicode(255))
    description = Column(UnicodeText)
    created = Column(DateTime, default=datetime.now)
    modified = Column(TIMESTAMP, default=datetime.now)

    # Relations
    parent = relation('Link', backref=backref('data',
                                order_by='LinkData.created',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('links_data'))

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
        return '<linkData: %s (%s)>' % (self.parent_id, self.language_id)


############################################################
# Media
############################################################
class Media(DeclarativeBase):
    """Media definition"""
    __tablename__ = 'media'

    # Columns
    id = Column(Unicode(255), primary_key=True)
    associable_id = Column(Integer, ForeignKey('associables.id'))
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    _created = Column('created', DateTime)
    type = Column(Unicode(50))
    uri = Column(Unicode(255))

    # Relations
    associable = relation('Associable', backref=backref('associated_media',
                                                                uselist=False))
    user = relation('User', backref='media')

    # Properties
    @synonym_for('_created')
    @property
    def created(self):
        return self._created

    @property
    def tags(self):
        return self.associable.tags

    @property
    def comments(self):
        return self.associable.comments

    @property
    def modified(self):
        return max([d.modified for d in self.data])

    published = property(
        lambda self: self.associable.published,
        lambda self, val: setattr(self.associable, 'published', val)
    )

    # Special methods
    def __init__(self, type, name, uri, user, lang, description=None):
        self.id = make_id(name)
        self.type = type
        self.uri = uri
        self.user = user
        self.data.append(MediaData(name, lang, description))
        self.associable = Associable(u'media')
        now = datetime.now()
        self._created = now
        self.associable._created = now

    def __repr__(self):
        return '<Media: %s %s %s>' % (self.id, self.type, self.uri)

add_language_props(Media, 
    [('name', lambda obj, lang, val: MediaData(val, lang, None)),
     ('description', lambda obj, lang, val: MediaData(obj.name[''],lang, val)),
    ])
add_version_props(Media)


class MediaData(DeclarativeBase):
    """Language specific Media data"""
    __metaclass__ = VersionedMeta
    __tablename__ = 'media_data'
    __table_args__ = (UniqueConstraint('parent_id', 'language_id'),
                      {})

    # Columns
    id = Column(Integer, primary_key=True)
    parent_id = Column(Unicode(255), ForeignKey('media.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    language_id = Column(Unicode(50), ForeignKey('languages.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    _name = Column('name', Unicode(255))
    description = Column(UnicodeText)
    created = Column(DateTime, default=datetime.now)
    modified = Column(TIMESTAMP, default=datetime.now)

    # Relations
    parent = relation('Media', backref=backref('data',
                                order_by='MediaData.created',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('media_data'))

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
        return '<MediaData: %s (%s)>' % (self.parent_id, self.language_id)

