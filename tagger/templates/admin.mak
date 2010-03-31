<%inherit file="local:templates.master"/>

admin

<%def name="side()">
    <ul>
        <li><a href="${tg.url('/language')}">languages</a></li>
        <li><a href="${tg.url('/category')}">categories</a></li>
    </ul>
</%def>

