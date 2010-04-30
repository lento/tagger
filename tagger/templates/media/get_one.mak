<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%def name="title()">
  tagger - ${_('Media')}
</%def>

<div>${media.id}</div>
<div>${media.type}</div>
<div>${media.name[lang]}</div>
<div>${media.uri}</div>
<div>${media.description[lang]}</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

