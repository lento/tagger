<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Comment')}
</%def>

<div>${comment.id}</div>
<div>${comment.to}</div>
<div>${comment.name}</div>
<div>${comment.email}</div>
<div>${comment.status}</div>

