<%inherit file="local:templates.admin.index"/>

<%def name="title()">
  tagger - ${_('Settings')}
</%def>

${c.f_settings(args, child_args=child_args) | n}

