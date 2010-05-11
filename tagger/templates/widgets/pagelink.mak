<%!
    import tg
    from tagger.model import DBSession, Page
%>

<%
    if pageid.isdigit():
        page = DBSession.query(Page).get(pageid)
    else:
        page = DBSession.query(Page).filter_by(string_id=pageid).one()
%>

<a href="${tg.url('/page/%s/%s/%s' % (page.article.id, page.string_id, lang))}">
    ${label or page.name[lang]}
</a>

