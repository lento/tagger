<%inherit file="local:templates.admin"/>

<%def name="title()">
  tagger - ${_('Articles')}
</%def>

${c.f_edit(args, child_args=child_args) | n}

