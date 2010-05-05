<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%def name="title()">
  tagger - ${_('Links')}
</%def>

<ul>
    % for link in links:
        <li class="object summary">
            ${c.w_object_title(obj=link, tg=tg, lang=c.lang, add_link=True) | n}
            <div>
                ${link.description[c.lang]}
            </div>
        </li>
    % endfor
</ul>
<%def name="side()">
    ${sidebars.side_recent()}
</%def>

