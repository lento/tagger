<%inherit file="local:templates.master"/>

<%!
    from tagger.lib.render.rst import render_text
%>

<%def name="title()">
  tagger - ${_('Article')}
</%def>

<div class="article_title">
    <h1>${article.title[lang]}</h1>
    <div>
        <span class="date">${article.created}</span>
        <span class="user">${article.user.user_name}</span>
    </div>
    <div class="tags">
        % for tag in article.tags:
            <a class="tag" href="">
                ${tag.name[lang]}
            </a>
        % endfor
    </div>
    <div class="languages">
        % for language in article.languages:
            <a class="language ${language.id == lang and 'active' or ''}"
                title="${language.name}"
                href="${tg.url('/%s/%s/%s' % (article.category.id, article.id, language.id))}">
                    ${language.name}
            </a>
        % endfor
    </div>
</div>

<div>
    ${render_text(article.text[lang], lang) | n}
</div>

<%def name="side()">
    ${parent.side_related()}
</%def>

