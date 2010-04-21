<%inherit file="local:templates.admin.index"/>

<%def name="title()">
  tagger - ${_('Banner')}
</%def>

${c.f_banner(args, child_args=child_args) | n}

