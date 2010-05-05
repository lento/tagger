<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%def name="title()">
  tagger - ${_('Media')}
</%def>

${c.w_object_title(obj=media, tg=tg, lang=lang) | n}

<div>
    ${media.description[lang]}
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

