<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tagger.lib.render.rst import render_summary
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Pages')
%>

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

