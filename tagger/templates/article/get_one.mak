<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tagger.lib.render.rst import render_text
%>

<%def name="title()">
  tagger - ${_('Article')}
</%def>

${c.w_object_title(obj=article, tg=tg, lang=lang) | n}

<div>
    ${render_text(article.text[lang], lang) | n}
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

