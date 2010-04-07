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
from tagger import model

import logging
log = logging.getLogger(__name__)


def bootstrap(command, conf, vars):
    """Place any commands to setup tagger here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = u'admin'
        u.display_name = u'Admin'
        u.email_address = u''
        u.password = u'none'

        model.DBSession.add(u)

        # admin for automated tests with a password that can't be matched to
        # prevent interactive login
        tadm = model.User()
        tadm.user_name = u'test_admin'
        tadm.display_name = u'Test Admin'
        tadm.email_address = u''
        tadm._password = u'*'

        model.DBSession.add(tadm)

        # user for automated tests with a password that can't be matched to
        # prevent interactive login
        tuser = model.User()
        tuser.user_name = u'test_user'
        tuser.display_name = u'Test User'
        tuser.email_address = u''
        tuser._password = u'*'

        model.DBSession.add(tuser)

        g = model.Group()
        g.group_name = u'admins'
        g.display_name = u'Administrators Group'

        g.users.append(u)
        g.users.append(tadm)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = u'manage'
        p.description = u'This permission give an administrative right to the bearer'
        p.groups.append(g)

        model.DBSession.add(p)

        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        log.debug('Warning, there was a problem adding your auth data, '
                  'it may have already been added:')
        import traceback
        log.debug(traceback.format_exc())
        transaction.abort()
        log.debug('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>

    # languages
    try:
        en = model.Language(u'en', u'english')
        model.DBSession.add(en)

        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        log.debug('Warning, there was a problem adding your Category data, '
                  'it may have already been added:')
        import traceback
        log.debug(traceback.format_exc())
        transaction.abort()
        log.debug('Continuing with bootstrapping...')

    # categories
    try:
        blog = model.Category(u'blog', u'Web log')
        model.DBSession.add(blog)

        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        log.debug('Warning, there was a problem adding your Category data, '
                  'it may have already been added:')
        import traceback
        log.debug(traceback.format_exc())
        transaction.abort()
        log.debug('Continuing with bootstrapping...')

