<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%def name="title()">
  tagger - ${_('Link')}
</%def>

<div class="object">
    ${c.w_object_title(obj=link, lang=lang) | n}

    % if link.description[lang]:
        <div>
            ${link.description[lang]}
        </div>
        <br/>
    % endif
    <div>
        ${c.w_link(linkid=link.id, lang=lang) | n}
    </div>
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

