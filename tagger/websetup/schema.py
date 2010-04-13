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
"""Setup the tagger application"""

import transaction
from tg import config
from paste.deploy.converters import asbool

import logging
log = logging.getLogger(__name__)

def setup_schema(command, conf, vars):
    """Place any commands to setup tagger here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from tagger import model
    # <websetup.websetup.schema.after.model.import>

    
    # <websetup.websetup.schema.before.metadata.create_all>
    engine = config['pylons.app_globals'].sa_engine

    create_triggers = asbool(config.get('sql_create_triggers', 'true'))
    if not create_triggers:
        log.debug('removing triggers creation from metadata')
        model.utils.TriggerRemover().traverse(model.metadata)

    log.debug('Creating tables')
    model.metadata.create_all(bind=engine)
    # <websetup.websetup.schema.after.metadata.create_all>
    transaction.commit()
