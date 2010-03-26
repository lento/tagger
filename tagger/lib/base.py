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

        request.identity = request.environ.get('repoze.who.identity')
        tmpl_context.identity = request.identity

        # set theme and title
        tmpl_context.theme = config.get('theme', 'default')
        tmpl_context.title = config.get(
                                    'title', 'Welcome to Tagger!').strip('\"')

        # add categories list to template context (used in the header)
        tmpl_context.categories = DBSession.query(Category).all()

        return TGController.__call__(self, environ, start_response)
