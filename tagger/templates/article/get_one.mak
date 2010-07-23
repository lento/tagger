<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tagger.lib.render.rst import render_text
%>

<%def name="title()">
    ${c.title}
    ${c.title and article and ' - '}
    ${article.title[lang]}
</%def>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

<div class="object">
    ${c.w_object_title(obj=article, tg=tg, lang=lang) | n}

    <div class="object_body">
        ${render_text(article.text[lang], lang) | n}
    </div>
</div>

