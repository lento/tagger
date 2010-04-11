<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Category')}
</%def>

<div>${category.id}</div>
<div>${category.name[c.lang]}</div>
<div>${category.description[c.lang]}</div>

