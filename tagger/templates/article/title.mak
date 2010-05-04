<div class="article_title">
    <h1>
        % if add_link:
            <a href="${tg.url('/%s/%s' % (article.category.id, article.id))}">
        % endif
                ${article.title[lang]}
        % if add_link:
            </a>
        % endif
    </h1>
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

