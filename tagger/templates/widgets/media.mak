<%!
    from tagger.model import DBSession, Media
%>

<%
    link = DBSession.query(Media).get(mediaid)
%>

<a href="${media.uri}" title="${media.description[lang]}">${label or media.uri}</a>
