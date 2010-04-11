<%inherit file="local:templates.master"/>

<%!
    from tagger.lib.render import render_text
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
    <div>
        % for language in article.languages:
            <a class="language ${language.id == lang and 'active' or ''}" title="${language.name}"
               href="${tg.url('/%s/%s/%s' % (article.category.id, article.string_id, language.id))}">
                ${language.name}
            </a>
        % endfor
    </div>
</div>

<div>
    ${render_text(article.text[lang]) | n}
</div>

