<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Article')}
</%def>

<div>${article.id}</div>
<div>${article.title['']}</div>
<div>${article.category.name}</div>
<div>${', '.join(article.languages)}</div>

