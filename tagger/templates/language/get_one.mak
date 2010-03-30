<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Language')}
</%def>

<div>${language.id}</div>
<div>${language.name}</div>

