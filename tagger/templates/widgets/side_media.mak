<%!
    from tg import tmpl_context as c, url
%>

<a href="${url('/media/%s' % obj.id)}">
    <div class="icon ${obj.type}"></div>
    <div>
        <div class="title" title="${obj.description[c.lang] or ''}">${obj.name[c.lang]}</div>
        ${c.w_media(mediaid=obj.id, lang=c.lang, width=80)}
    </div>
</a>

