<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Link')}
</%def>

<div>${link.id}</div>
<div>${link.name[lang]}</div>
<div>${link.uri}</div>
<div>${link.description[lang]}</div>

