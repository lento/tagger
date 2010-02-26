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
from datetime import datetime
from hashlib import sha1
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

metadata = MetaData()
DeclarativeBase = declarative_base(bind=migrate_engine, metadata=metadata)

# This is the association table for the many-to-many relationship between
# groups and permissions. This is required by repoze.what.
groups_permissions_table = Table('__group_permission', metadata,
    Column('group_id', Integer, ForeignKey('auth_groups.group_id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('permission_id', Integer, ForeignKey('auth_permissions.permission_id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships. It's required by repoze.what.
users_groups_table = Table('__user_group', metadata,
    Column('user_id', Integer, ForeignKey('auth_users.user_id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('group_id', Integer, ForeignKey('auth_groups.group_id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)


class Group(DeclarativeBase):
    """Group definition for :mod:`repoze.what`.

    Only the ``group_name`` column is required by :mod:`repoze.what`.
    """
    __tablename__ = 'auth_groups'

    # Columns
    group_id = Column(Integer, autoincrement=True, primary_key=True)
    group_name = Column(Unicode(16), unique=True, nullable=False)
    display_name = Column(Unicode(255))
    created = Column(DateTime, default=datetime.now)


class User(DeclarativeBase):
    """User definition.

    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.
    """
    __tablename__ = 'auth_users'

    # Columns
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(Unicode(16), unique=True, nullable=False)
    email_address = Column(Unicode(255), unique=True, nullable=False,
                           info={'rum': {'field':'Email'}})
    display_name = Column(Unicode(255))
    _password = Column('password', Unicode(80),
                       info={'rum': {'field':'Password'}})
    created = Column(DateTime, default=datetime.now)


class Permission(DeclarativeBase):
    """Permission definition for :mod:`repoze.what`.

    Only the ``permission_name`` column is required by :mod:`repoze.what`.
    """
    __tablename__ = 'auth_permissions'

    # Columns
    permission_id = Column(Integer, autoincrement=True, primary_key=True)
    permission_name = Column(Unicode(63), unique=True, nullable=False)
    description = Column(Unicode(255))


def upgrade():
    # Upgrade operations go here. Don't create your own engine; use the engine
    # named 'migrate_engine' imported from migrate.
    Group.__table__.create()
    User.__table__.create()
    Permission.__table__.create()
    groups_permissions_table.create()
    users_groups_table.create()
    
def downgrade():
    # Operations to reverse the above upgrade go here.
    users_groups_table.drop()
    groups_permissions_table.drop()
    Permission.__table__.drop()
    User.__table__.drop()
    Group.__table__.drop()

