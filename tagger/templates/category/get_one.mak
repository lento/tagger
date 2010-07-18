<%inherit file="local:templates.master"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Category')
%>

<div>${category.id}</div>
<div>${category.name[c.lang]}</div>
<div>${category.description[c.lang]}</div>

