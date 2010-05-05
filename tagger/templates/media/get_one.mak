<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tg import url
    from tg.configuration import Bunch
%>
<%
    extra = Bunch(lang=c.lang, url=tg.url)
%>

<%def name="title()">
  tagger - ${_('Media')}
</%def>

${c.w_object_title(obj=media, tg=tg, lang=lang) | n}

<div>
    ${media.description[lang]}
</div>
<div>
    ${c.w_media(mediaid=media.id, extra=extra) | n}
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

