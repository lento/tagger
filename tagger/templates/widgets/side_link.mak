<%!
    from tg import tmpl_context as c, url
%>

<div>
    <a href="${url('/link/%s' % obj.id)}">
        <h2>${obj.name[c.lang]}</h2>
        <div>
            <span class="icon link"></span>
            <span class="type">${_('link')}</span>
            <span class="date">${obj.created}</span>
            <span class="user">${obj.user.user_name}</span>
        </div>
    </a>
</div>

