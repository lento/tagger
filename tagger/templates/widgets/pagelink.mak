<%!
    import tg
    from tagger.model import DBSession, Page
    from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
%>

<%
    try:
        if pageid.isdigit():
            page = DBSession.query(Page).get(pageid)
        else:
            page = DBSession.query(Page).filter_by(string_id=pageid).one()
    except NoResultFound, MultipleResultsFound:
        page = None
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

