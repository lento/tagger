<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tg import tmpl_context as c
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Media')
%>

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

<ul>
    % for m in media:
        <li class="object summary">
            ${c.w_object_title(obj=m, lang=c.lang, add_link=True) | n}
            <div class="object_body">
                % if m.description[c.lang]:
                    <div>
                        ${m.description[c.lang]}
                    </div>
                    <br/>
                % endif
                <div>
                    ${c.w_media(mediaid=m.id, lang=c.lang, width=240) | n}
                </div>
            </div>
        </li>
    % endfor
</ul>

% if more_results:
    <div class="more_results">
        ${'%s %s' % (more_results, _('more media'))}
        <a href="${tg.url('/media?max_results=0')}">
            ${_('view all')}
        </a>
    </div>
% endif

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

