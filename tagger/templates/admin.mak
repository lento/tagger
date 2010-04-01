<%inherit file="local:templates.master"/>

admin

<%def name="side()">
    <ul>
        <li class="languages"><a href="${tg.url('/language')}">languages</a></li>
        <li class="categories"><a href="${tg.url('/category')}">categories</a></li>
    </ul>
</%def>

