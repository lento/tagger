<%!
    from tg import tmpl_context as c, url
%>

<div>
    <a href="${url('/%s/%s' % (obj.category_id, obj.id))}">
        <h2>${obj.title[c.lang]}</h2>
        <div class="info">
            <span class="icon article"></span>
            <span class="type">${obj.category.name[c.lang]}</span>
            <span class="date">${obj.created}</span>
            <span class="user">${obj.user.user_name}</span>
        </div>
    </a>
</div>

