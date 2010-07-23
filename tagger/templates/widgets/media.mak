<%!
    import os.path
    from tg import app_globals as G, tmpl_context as c, url
    from tagger.model import DBSession, Media
    from tagger.lib.base import flowplayer_js
%>

<%
    media = DBSession.query(Media).get(mediaid)
    mediaurl = media and url('/%s/%s' % (G.upload_prefix, media.uri))
%>

% if media:
    % if media.type == 'image':
        <img src="${mediaurl}"
            alt="${label or media.uri}"
            title="${media.description[lang] or ''}"
            width="${width or 'auto'}"
            height="${height or 'auto'}"
        />
    % elif media.type == 'video':
        <video src="${mediaurl}"
            title="${media.description[lang] or ''}"
            controls=""
            width="${width or 'auto'}"
            height="${height or 'auto'}"
            onerror="alert('Can\'t load video');">
                ${flowplayer_js.render() | n}
                <%
                    filename, ext = os.path.splitext(mediaurl)
                    fallbackurl = '%s.flv' % filename
                %>
                <a id="flowplayer_${media.id}"
                    href="${fallbackurl}"
                    style="display:block;width:${width or 'auto'}px;height:${height or 'auto'}px;">
                </a>
                <script type="text/javascript">
                    flowplayer(
                        "flowplayer_${media.id}",
                        "${url('/swf/flowplayer-3.1.5.swf')}",
                        {
                            clip: {
                                scaling: "orig",
                            }
                        }
                    );
                </script>
        </video>
    % elif media.type == 'youtube':
        <object width="${width or '480'}" height="${height or width and int(width*0.8) or '385'}">
            <param name="movie" value="http://www.youtube.com/v/${media.uri}&hl=en_US&fs=1&"></param>
            <param name="allowFullScreen" value="true"></param>
            <param name="allowscriptaccess" value="always"></param>
            <embed src="http://www.youtube.com/v/${media.uri}&hl=en_US&fs=1&"
                type="application/x-shockwave-flash"
                allowscriptaccess="always"
                allowfullscreen="true"
                width="${width or '480'}"
                height="${height or width and int(width*0.8) or '385'}">
            </embed>
        </object>
    % elif media.type == 'vimeo':
        <object width="${width or '480'}" height="${height or width and int(width*0.55) or '264'}">
            <param name="allowfullscreen" value="true" />
            <param name="allowscriptaccess" value="always" />
            <param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=${media.uri}&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" />
            <embed src="http://vimeo.com/moogaloop.swf?clip_id=${media.uri}&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1"
                type="application/x-shockwave-flash"
                allowfullscreen="true"
                allowscriptaccess="always"
                width="${width or '480'}"
                height="${height or width and int(width*0.55) or '264'}">
            </embed>
        </object>
    % endif
% else:
    <span class="not_found" title="${_('media not found')}">${mediaid}</span>
% endif
