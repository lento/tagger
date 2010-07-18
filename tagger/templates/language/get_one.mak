<%inherit file="local:templates.master"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Language')
%>

<div>${language.id}</div>
<div>${language.name}</div>

