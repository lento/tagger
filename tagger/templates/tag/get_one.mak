<%inherit file="local:templates.master"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Tag')
%>

<div>${tag.id}</div>
<div>${tag.name[lang]}</div>

