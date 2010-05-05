<%
    from tagger.model import Article, Media, Link
    if isinstance(obj, Article):
        name = obj.title[lang]
        link = '/%s/%s' % (obj.category.id, obj.id)
    elif isinstance(obj, Media):
        name = obj.name[lang]
        link = '/media/%s' % obj.id
    elif isinstance(obj, Link):
        name = obj.name[lang]
        link = '/link/%s' % obj.id
    else:
        name = None
        link = None
%>

<div class="object_title">
    <h1>
        % if add_link:
            <a href="${tg.url(link)}">
        % endif
                ${name}
        % if add_link:
            </a>
        % endif
    </h1>
    <div>
        <span class="date">${obj.created}</span>
        <span class="user">${obj.user.user_name}</span>
    </div>
    <div class="tags">
        % for tag in obj.tags:
            <a class="tag" href="">
                ${tag.name[lang]}
            </a>
        % endfor
    </div>
    <div class="languages">
        % for language in obj.languages:
            <a class="language ${language.id == lang and 'active' or ''}"
                title="${language.name}"
                href="${tg.url('%s/%s' % (link, language.id))}"
                >
                    ${language.name}
            </a>
        % endfor
    </div>
</div>

