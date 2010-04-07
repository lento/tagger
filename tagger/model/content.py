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
from sqlalchemy.orm import relation, backref

from tagger.model import DeclarativeBase, metadata, mapped_scalar, dict_property
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
        return '<Category: %s %s>' % (self.id or 0, self.name)


class Article(DeclarativeBase):
    """Article definition"""
    __tablename__ = 'articles'

    # Columns
    id = Column(Integer, primary_key=True)
    string_id = Column(Unicode(255))
    associable_id = Column(Integer, ForeignKey('associables.id'))
    user_id = Column(Integer, ForeignKey('auth_users.user_id'))
    category_id = Column(Integer, ForeignKey('categories.id',
                                        onupdate='CASCADE', ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)

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

    def _title_get(self, lang):
        return self.pages['default'].name[lang]

    def _title_set(self, lang, value):
        self.pages['default'].name[lang] = value

    title = dict_property(_title_get, _title_set)

    def _text_get(self, lang):
        return self.pages['default'].text[lang]

    def _text_set(self, lang, value):
        self.pages['default'].text[lang] = value

    text = dict_property(_text_get, _text_set)

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
    def language_id(self):
        return self.data[0].language_id

    @property
    def language_ids(self):
        return set([data.language_id for data in self.data])

    @property
    def languages(self):
        return set([data.language for data in self.data])

    def _name_get(self, lang):
        if lang and lang in self.language_ids:
            return self.data[lang].name
        return self.data[0].name

    def _name_set(self, lang, value):
        if not lang:
            self.data[0].name = value
        elif lang in self.language_ids:
            self.data[lang].name = value
        else:
            self.data.append(PageData(value, lang, None))

    name = dict_property(_name_get, _name_set)

    def _text_get(self, lang):
        if lang and lang in self.language_ids:
            return self.data[lang].text
        return self.data[0].text

    def _text_set(self, lang, value):
        if not lang:
            self.data[0].text = value
        elif lang in self.language_ids:
            self.data[lang].text = value
        else:
            self.data.append(PageData(self.name[''], lang, value))

    text = dict_property(_text_get, _text_set)

    # Special methods
    def __init__(self, name, lang, text=None, string_id=None):
        self.string_id = string_id or make_id(name)
        self.data.append(PageData(name, lang, text))

    def __repr__(self):
        return '<Page: [%s] %s %s>' % (self.article_id, self.id, self.string_id)


class PageData(DeclarativeBase):
    """Language specific Page data"""
    __tablename__ = 'pages_data'

    # Columns
    page_id = Column(Integer, ForeignKey('pages.id',
                    onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    language_id = Column(Unicode(50), ForeignKey('languages.id',
                    onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    name = Column(Unicode(255))
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    text = Column(UnicodeText)

    # Relations
    page = relation('Page', backref=backref('data',
                                collection_class=mapped_scalar('language_id')))
    language = relation('Language', backref=backref('pages_data'))

    # Special methods
    def __init__(self, name, lang, text=None):
        self.name = name
        self.language_id = lang
        self.text = text

    def __repr__(self):
        return '<PageData: %s (%s) %s>' % (self.page_id, self.language_id,
                                                                    self.name)


