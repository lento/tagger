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
  tagger - ${_('Links')}
</%def>

<ul>
    % for link in links:
        <li class="object summary">
            ${c.w_object_title(obj=link, tg=tg, lang=c.lang, add_link=True) | n}
            % if link.description[lang]:
                <div>
                    ${link.description[c.lang]}
                </div>
                <br/>
            % endif
            <div>
                ${c.w_link(linkid=link.id, extra=extra) | n}
            </div>
        </li>
    % endfor
</ul>
<%def name="side()">
    ${sidebars.side_recent()}
</%def>

