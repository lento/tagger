from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1267209135.587707
_template_filename='/home/lorenzo/dev/tagger/tagger/templates/error.mak'
_template_uri='/home/lorenzo/dev/tagger/tagger/templates/error.mak'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        message = context.get('message', UNDEFINED)
        code = context.get('code', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html>\n\n<head>\n  <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="\'\'"/>\n  <title>A ')
        # SOURCE LINE 7
        __M_writer(escape(code))
        __M_writer(u' Error has Occurred </title>\n</head>\n\n<body>\n<h1>Error ')
        # SOURCE LINE 11
        __M_writer(escape(code))
        __M_writer(u'</h1>\n\n<div>')
        # SOURCE LINE 13
        __M_writer(message )
        __M_writer(u'</div>\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


