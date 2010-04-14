<%inherit file="local:templates.master"/>

admin

<%def name="side()">
    <ul>
        <li class="languages"><a href="${tg.url('/language/')}">languages</a></li>
        <li class="categories"><a href="${tg.url('/category/')}">categories</a></li>
        <li class="articles"><a href="${tg.url('/article/')}">articles</a></li>
        <li class="links"><a href="${tg.url('/link/')}">links</a></li>
        <li class="media"><a href="${tg.url('/media/')}">media</a></li>
    </ul>
</%def>

