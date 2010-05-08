# -*- coding: utf-8 -*-

"""The base Controller API."""

from tg import TGController, tmpl_context, config, i18n, url
from tg.render import render
from tg import request
from pylons.i18n import _, ungettext, N_
from tw.api import WidgetBunch, JSLink
from tagger.model import DBSession, Language, Category, Setting
from tagger.lib.render import LinkWidget, MediaWidget
from tagger.lib.widgets import SideArticle, SideMedia, SideLink

__all__ = ['BaseController']

w_link = LinkWidget()
w_media = MediaWidget()
w_sideobj = dict(
    article=SideArticle(),
    media=SideMedia(),
    link=SideLink(),
    )

# JQuery and plugins
jquery_js = JSLink(link=url('/js/jquery.js'))
jquery_tools_js = JSLink(link=url('/js/jquery.tools.js'))

# tagger
tagger_js = JSLink(link=url('/js/tagger.js'))

# FlowPlayer - don't load this at startup, its a fallback for browsers not
# supporting HTML5 <video> tag
flowplayer_js = JSLink(link=url('/js/flowplayer.js'))


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

        # load javascripts
        jquery_js.inject()
        jquery_tools_js.inject()
        tagger_js.inject()

        # add languages and categories to template context (used in the header)
        tmpl_context.languages = DBSession.query(Language)
        tmpl_context.categories = DBSession.query(Category)

        # set language
        if 'lang' in request.cookies:
            tmpl_context.lang = request.cookies['lang']
            i18n.set_lang(tmpl_context.lang)
        else:
            tmpl_context.lang = config.get('lang', None)
            i18n.set_lang(None)

        # add current url to template context
        tmpl_context.current_url = request.url

        # set banner link and content
        tmpl_context.w_link = w_link
        tmpl_context.w_media = w_media
        banner_media = DBSession.query(Setting).get(u'banner_media')
        banner_link = DBSession.query(Setting).get(u'banner_link')
        tmpl_context.banner_mediaid = banner_media and banner_media.value
        tmpl_context.banner_linkid = banner_link and banner_link.value

        # add Sidebar widgets
        tmpl_context.w_sideobj = w_sideobj

        return TGController.__call__(self, environ, start_response)
