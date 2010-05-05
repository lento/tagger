<%!
    from tg import tmpl_context as c, url
%>

<a href="${url('/%s/%s' % (obj.category_id, obj.id))}">
    <div class="icon article"></div>
    <div>
        <span class="category">${obj.category.name[c.lang]}</span>
        <span class="title">${obj.title[c.lang]}</span>
    </div>
</a>

