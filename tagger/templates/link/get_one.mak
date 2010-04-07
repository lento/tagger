<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Link')}
</%def>

<div>${link.id}</div>
<div>${link.url}</div>
<div>${link.description[lang]}</div>

