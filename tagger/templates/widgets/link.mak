<%!
    from tagger.model import DBSession, Link
%>

<%
    link = DBSession.query(Link).get(linkid)
%>

<a href="${link.uri}" title="${link.description[extra.lang]}">${label or link.uri}</a>
