# -*- coding: utf-8 -*-

"""The base Controller API."""

from tg import TGController, tmpl_context, config
from tg.render import render
from tg import request
from pylons.i18n import _, ungettext, N_
from tw.api import WidgetBunch
from tagger.model import DBSession, Category

__all__ = ['BaseController']

class BaseController(TGController):
    """
    Base class for the controllers in the application.

    Your web application should have one of these. The root of
    your application is used to compute URLs used by your app.

    """

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # TGController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        identity = request.environ.get('repoze.who.identity')
        request.identity = identity
        tmpl_context.identity = identity
        tmpl_context.user = identity and identity['user'] or False

        # set theme, title and copyright notice
        tmpl_context.theme = config.get('theme', 'default')
        tmpl_context.title = config.get(
                                    'title', 'Welcome to Tagger!').strip('\"')
        tmpl_context.copyright = config.get('copyright', '').strip('\"')

        # add categories list to template context (used in the header)
        tmpl_context.categories = DBSession.query(Category).all()

        return TGController.__call__(self, environ, start_response)
