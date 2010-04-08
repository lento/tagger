<%!
    from tagger.model import DBSession, Link
%>

<%
    link = DBSession.query(Link).get(linkid)
%>

<a href="${link.url}" title="${link.description[languageid]}">${label or link.url}</a>
