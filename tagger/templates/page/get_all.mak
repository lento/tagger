<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tagger.lib.render.rst import render_summary
%>

<%def name="title()">
  tagger - ${_('Pages')}
</%def>

<ul>
    % for page in pages:
        <li>
            ${page.name[c.lang]}
        </li>
    % endfor
</ul>

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

