from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1267209135.4607329
_template_filename='/home/lorenzo/dev/tagger/tagger/templates/master.mak'
_template_uri='/home/lorenzo/dev/tagger/tagger/templates/master.mak'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['footer', 'header', 'meta', 'content_wrapper', 'title']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        tg = context.get('tg', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html>\n<head>\n    ')
        # SOURCE LINE 5
        __M_writer(escape(self.meta()))
        __M_writer(u'\n    <title>')
        # SOURCE LINE 6
        __M_writer(escape(self.title()))
        __M_writer(u'</title>\n    <link rel="stylesheet" type="text/css" media="screen" href="')
        # SOURCE LINE 7
        __M_writer(escape(tg.url('/css/style.css')))
        __M_writer(u'" />\n</head>\n<body>\n  ')
        # SOURCE LINE 10
        __M_writer(escape(self.header()))
        __M_writer(u'\n  ')
        # SOURCE LINE 11
        __M_writer(escape(self.content_wrapper()))
        __M_writer(u'\n  ')
        # SOURCE LINE 12
        __M_writer(escape(self.footer()))
        __M_writer(u'\n</body>\n\n')
        # SOURCE LINE 19
        __M_writer(u'\n\n')
        # SOURCE LINE 23
        __M_writer(u'\n\n')
        # SOURCE LINE 25
        __M_writer(u'\n\n')
        # SOURCE LINE 30
        __M_writer(u'\n\n')
        # SOURCE LINE 35
        __M_writer(u'\n\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 32
        __M_writer(u'\n  <div id="footer">\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 27
        __M_writer(u'\n  <div id="header">\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_meta(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 21
        __M_writer(u'\n  <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content_wrapper(context):
    context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 15
        __M_writer(u'\n    <div id="content">\n      ')
        # SOURCE LINE 17
        __M_writer(escape(self.body()))
        __M_writer(u'\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


