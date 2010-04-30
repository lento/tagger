<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%def name="title()">
  tagger - ${_('Media')}
</%def>

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

