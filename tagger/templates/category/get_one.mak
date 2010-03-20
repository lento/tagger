<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Category')}
</%def>

<div>${category.id}</div>
<div>${category.name}</div>
<div>${category.description}</div>

