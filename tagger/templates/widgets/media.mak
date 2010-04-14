<%!
    from tagger.model import DBSession, Media
%>

<%
    media = DBSession.query(Media).get(mediaid)
%>

% if media.type == 'image':
    <img src="${extra.url(media.uri)}"
        alt="${label or media.uri}"
        title="${media.description[extra.lang]}"
        % if width:
            width="${width}"
        % endif
        % if height:
            height="${height}"
        % endif
    />
% elif media.type == 'video':
    <video src="${extra.url(media.uri)}"
        title="${media.description[extra.lang]}"
        controls
        % if width:
            width="${width}"
        % endif
        % if height:
            height="${height}"
        % endif
    />
% elif media.type == 'youtube':
    <object width="${width or '480'}" height="${height or '385'}">
        <param name="movie" value="http://www.youtube.com/v/${media.uri}&hl=en_US&fs=1&"></param>
        <param name="allowFullScreen" value="true"></param>
        <param name="allowscriptaccess" value="always"></param>
        <embed src="http://www.youtube.com/v/${media.uri}&hl=en_US&fs=1&"
            type="application/x-shockwave-flash"
            allowscriptaccess="always"
            allowfullscreen="true"
            width="${width or '480'}"
            height="385">
        </embed>
    </object>
% elif media.type == 'vimeo':
    <object width="${width or '400'}" height="${height or '220'}">
        <param name="allowfullscreen" value="true" />
        <param name="allowscriptaccess" value="always" />
        <param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=${media.uri}&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" />
        <embed src="http://vimeo.com/moogaloop.swf?clip_id=${media.uri}&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1"
            type="application/x-shockwave-flash"
            allowfullscreen="true"
            allowscriptaccess="always"
            width="${width or '400'}"
            height="${height or '220'}">
        </embed>
    </object>
% endif

