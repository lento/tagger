<%!
    from tg import tmpl_context as c, url
%>

<a href="${url('/link/%s' % obj.id)}">
    <div class="icon link"></div>
    <div>${obj.name[c.lang]}</div>
</a>

