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

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

<ul>
    % for m in media:
        <li class="object summary">
            ${c.w_object_title(obj=m, tg=tg, lang=c.lang, add_link=True) | n}
            <div>
                ${m.description[c.lang]}
            </div>
            <div>
                ${c.w_media(mediaid=m.id, extra=extra, width=120) | n}
            </div>
        </li>
    % endfor
</ul>

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

