# -*- coding: utf-8 -*-

"""The application's Globals object"""

from tg import config

__all__ = ['Globals']


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """

    def __init__(self):
        """Initialize global variables"""
        cache_dir = config.get('cache.dir', '')
        self.upload_dir = config.get('upload_dir', '%s/upload' % cache_dir)
        self.upload_prefix = config.get('upload_prefix', 'upload')

