# -*- coding: utf-8 -*-

"""The application's Globals object"""

import os
from tg import config

import logging
log = logging.getLogger(__name__)

__all__ = ['Globals']


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """

    def __init__(self):
        """Initialize global variables"""
        here = config.get('here', '')
        cache_dir = config.get('cache.dir', '')
        self.upload_dir = config.get('upload_dir', '%s/upload' % cache_dir)
        self.upload_prefix = config.get('upload_prefix', 'upload')
        themes_dir = os.path.join(here, 'tagger', 'public', 'themes')
        self.themes = [d for d in os.listdir(themes_dir)]

