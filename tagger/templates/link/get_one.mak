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
  tagger - ${_('Link')}
</%def>

<div class="object">
    ${c.w_object_title(obj=link, tg=tg, lang=lang) | n}

    % if link.description[lang]:
        <div>
            ${link.description[lang]}
        </div>
        <br/>
    % endif
    <div>
        ${c.w_link(linkid=link.id, extra=extra) | n}
    </div>
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

