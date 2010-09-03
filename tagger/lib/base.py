# -*- coding: utf-8 -*-

"""The base Controller API."""

from tg import TGController, tmpl_context, config, i18n, url, app_globals as G
from tg.render import render
from tg import request
from pylons.i18n import _, ungettext, N_
from tw.api import WidgetBunch, JSLink
from tagger.model import DBSession, Language, Category, Setting, Media
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

# springs
mjs_js = JSLink(link=url('/js/extern/mjs.js'))
springs_js = JSLink(link=url('/js/springs.js'))

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

        # get settings from the db
        settings = dict([(s.id, s.value) for s in DBSession.query(Setting)])

        # set theme, title and copyright notice
        tmpl_context.theme = (settings.get('theme') or
                              config.get('theme') or
                              'default'
                             )
        tmpl_context.title = (settings.get('title') or
                              config.get('title', '').strip('\"') or
                              ''
                             )
        tmpl_context.copyright = (settings.get('copyright') or
                                  config.get('copyright', '').strip('\"') or
                                  ''
                                 )
        tmpl_context.cc = (settings.get('cc') or
                           config.get('cc', '').strip('\"') or
                           ''
                          )

        # load javascripts
        jquery_js.inject()
        jquery_tools_js.inject()
        tagger_js.inject()
        springs_js.inject()
        mjs_js.inject()

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

        # set logo
        l_mediaid = settings.get(u'logo_media', None)
        l_media = l_mediaid and DBSession.query(Media).get(l_mediaid)
        l_mediaurl = l_media and url('/%s/%s' % (G.upload_prefix, l_media.uri))
        tmpl_context.logo_mediaurl = l_mediaurl

        # set banner link and background image
        tmpl_context.w_link = w_link
        tmpl_context.w_media = w_media
        tmpl_context.banner_linkid = settings.get(u'banner_link', None)
        b_mediaid = settings.get(u'banner_media', None)
        b_media = b_mediaid and DBSession.query(Media).get(b_mediaid)
        b_mediaurl = b_media and url('/%s/%s' % (G.upload_prefix, b_media.uri))
        tmpl_context.banner_mediaurl = b_mediaurl

        # add Sidebar widgets
        tmpl_context.w_sideobj = w_sideobj

        return TGController.__call__(self, environ, start_response)
