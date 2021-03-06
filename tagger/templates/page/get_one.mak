<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tagger.lib.render.rst import render_text
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Article')
%>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

<div class="object">
    ${c.w_object_title(obj=article, tg=tg, lang=lang) | n}

    <div class="object_body">
        ${render_text(page.text[lang], lang) | n}
    </div>
</div>

