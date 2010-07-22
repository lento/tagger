<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Link')
%>

<div class="object">
    ${c.w_object_title(obj=link, lang=lang) | n}

    <div class="object_body">
        % if link.description[lang]:
            <div>
                ${link.description[lang]}
            </div>
            <br/>
        % endif
        <div class="document">
            ${c.w_link(linkid=link.id, lang=lang) | n}
        </div>
    </div>
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

