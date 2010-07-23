<%!
    from tagger.model import DBSession, Link
%>

<%
    link = DBSession.query(Link).get(linkid)
%>

% if link:
    <a href="${link.uri}" title="${link.description[lang]}">${label or link.uri}</a>
% else:
    <span class="not_found" title="${_('link not found')}">${linkid}</span>
% endif
