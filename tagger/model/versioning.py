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
"""Schema migration functions for the database."""

from tg import config
from migrate.versioning import api as migrate_api
from migrate.versioning.exceptions import DatabaseAlreadyControlledError
from tagger.model import DBSession

import logging
log = logging.getLogger(__name__)

# DB versioning
def db_init(version=None):
    """Init the database and put it under ``migrate`` control."""
    try:
        migrate_api.version_control(config.sqlalchemy.url, config.migrate_repo)
    except DatabaseAlreadyControlledError:
        log.debug('database already under migrate control')
    migrate_api.upgrade(config.sqlalchemy.url, config.migrate_repo, version)

def migraterepo_get_version():
    """Get the ``migrate`` repository current version."""
    return migrate_api.version(config.migrate_repo)

def db_get_version():
    """Get the ``migrate`` schema version for the database."""
    sess = DBSession()
    engine = sess.bind
    result = engine.execute('SELECT version FROM migrate_version')
    version = result.fetchone()[0]
    return version

def db_upgrade(version=None):
    """Upgrade the database schema."""
    migrate_api.upgrade(config.sqlalchemy.url, config.migrate_repo, version)
    
def db_downgrade(version):
    """Downgrade the database schema."""
    migrate_api.downgrade(config.sqlalchemy.url, config.migrate_repo, version)
    

