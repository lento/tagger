<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tg import tmpl_context as c
%>

<%def name="title()">
  tagger - ${_('Links')}
</%def>

<ul>
    % for link in links:
        <li class="object summary">
            ${c.w_object_title(obj=link, lang=c.lang, add_link=True) | n}
            % if link.description[c.lang]:
                <div>
                    ${link.description[c.lang]}
                </div>
                <br/>
            % endif
            <div>
                ${c.w_link(linkid=link.id, lang=c.lang) | n}
            </div>
        </li>
    % endfor
</ul>
<%def name="side()">
    ${sidebars.side_recent()}
</%def>

