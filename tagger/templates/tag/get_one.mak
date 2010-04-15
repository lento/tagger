<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Tag')}
</%def>

<div>${tag.id}</div>
<div>${tag.name[lang]}</div>

