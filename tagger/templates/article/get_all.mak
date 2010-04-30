<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

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

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

