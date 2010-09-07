<%!
    import tg
    from tagger.model.helpers import get_page
%>

<%
    page = get_page(pageid)
%>

% if page:
    <a href="${tg.url('/page/%s/%s/%s' % (page.article.id, page.string_id, lang))}">
        ${label or page.name[lang]}
    </a>
% else:
    <span class="not_found" title="${_('page not found')}">
        ${label or page.name[lang]}
    </span>
% endif

