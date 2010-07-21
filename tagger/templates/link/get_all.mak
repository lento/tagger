<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tg import tmpl_context as c
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Links')
%>

<ul>
    % for link in links:
        <li class="object summary">
            ${c.w_object_title(obj=link, lang=c.lang, add_link=True) | n}
            % if link.description[c.lang]:
                <div>
                    ${link.description[c.lang]}
                </div>
                <br/>
            % endif
            <div class="document">
                ${c.w_link(linkid=link.id, lang=c.lang) | n}
            </div>
        </li>
    % endfor
</ul>

% if more_results:
    <div class="more_results">
        ${'%s %s' % (more_results, _('more links'))}
        <a href="${tg.url('/link?max_results=0')}">
            ${_('view all')}
        </a>
    </div>
% endif

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

