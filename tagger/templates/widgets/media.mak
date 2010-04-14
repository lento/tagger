<%!
    from tagger.model import DBSession, Media
%>

<%
    media = DBSession.query(Media).get(mediaid)
%>

% if media.type == 'image':
    <img src="${extra.url(media.uri)}" alt="${label or media.uri}"  title="${media.description[extra.lang]}"/>
% endif

