<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Admin')
%>

<%def name="side()">
    ${sidebars.side_admin()}
</%def>

