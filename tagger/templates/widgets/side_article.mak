<%!
    from tg import tmpl_context as c, url
%>

<div class="icon article"></div>
<div class="title">
    <a href="${url('/%s/%s' % (obj.category_id, obj.id))}">
        ${obj.title[c.lang]}
    </a>
</div>
