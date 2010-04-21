<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Articles')}
</%def>

<ul>
    % for article in articles:
        <li>
            <div>${article.title[c.lang]}</div>
        </li>
    % endfor
</ul>
