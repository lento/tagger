<%inherit file="local:templates.admin.index"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Settings')
%>

${c.f_settings(args, child_args=child_args) | n}

