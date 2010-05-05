<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

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
        </li>
    % endfor
</ul>

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

