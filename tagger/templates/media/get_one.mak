<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Media')
%>

<div class="object">
    ${c.w_object_title(obj=media, lang=lang) | n}

    % if media.description[lang]:
        <div>
            ${media.description[lang]}
        </div>
        <br/>
    % endif
    <div>
        ${c.w_media(mediaid=media.id, lang=lang) | n}
    </div>
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

