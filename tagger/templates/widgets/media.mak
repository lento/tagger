<%!
    import os.path
    from tg import app_globals as G
    from tagger.model import DBSession, Media
    from tagger.lib.base import flowplayer_js
%>

<%
    media = DBSession.query(Media).get(mediaid)
    mediaurl = extra.url('/%s/%s' % (G.upload_prefix, media.uri))
%>

% if media.type == 'image':
    <img src="${mediaurl}"
        alt="${label or media.uri}"
        title="${media.description[extra.lang] or ''}"
        width="${width or '480'}"
        height="${height or '270'}"
    />
% elif media.type == 'video':
    <video src="${mediaurl}"
        title="${media.description[extra.lang] or ''}"
        controls
        width="${width or '480'}"
        height="${height or '270'}"
        onerror="alert('Can\'t load video');">
            ${flowplayer_js.render() | n}
            <%
                filename, ext = os.path.splitext(mediaurl)
                fallbackurl = '%s.flv' % filename
            %>
            <a id="flowplayer_${media.id}"
                href="${fallbackurl}"
                style="display:block;width:${width or '480'}px;height:${height or '270'}px;">
            </a>
            <script type="text/javascript">
                flowplayer(
                    "flowplayer_${media.id}",
                    "${extra.url('/swf/flowplayer-3.1.5.swf')}",
                    {
                        clip: {
                            scaling: "orig",
                        }
                    }
                );
            </script>
    </video>
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
    <object width="${width or '480'}" height="${height or '264'}">
        <param name="allowfullscreen" value="true" />
        <param name="allowscriptaccess" value="always" />
        <param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=${media.uri}&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" />
        <embed src="http://vimeo.com/moogaloop.swf?clip_id=${media.uri}&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1"
            type="application/x-shockwave-flash"
            allowfullscreen="true"
            allowscriptaccess="always"
            width="${width or '480'}"
            height="${height or '264'}">
        </embed>
    </object>
% endif

