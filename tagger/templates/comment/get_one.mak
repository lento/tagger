<%inherit file="local:templates.master"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Comment')
%>

<div>${comment.id}</div>
<div>${comment.to}</div>
<div>${comment.name}</div>
<div>${comment.email}</div>
<div>${comment.status}</div>

