<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%def name="title()">
  tagger - ${_('Link')}
</%def>

${c.w_object_title(obj=link, tg=tg, lang=lang) | n}

<div>
    ${link.description[lang]}
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

