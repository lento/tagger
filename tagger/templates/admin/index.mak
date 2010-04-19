<%inherit file="local:templates.master"/>

admin

<%def name="side()">
    <ul>
        <li class="languages"><a href="${tg.url('/admin/language/')}">languages</a></li>
        <li class="tags"><a href="${tg.url('/admin/tag/')}">tags</a></li>
        <li class="categories"><a href="${tg.url('/admin/category/')}">categories</a></li>
        <li class="articles"><a href="${tg.url('/admin/article/')}">articles</a></li>
        <li class="media"><a href="${tg.url('/admin/media/')}">media</a></li>
        <li class="links"><a href="${tg.url('/admin/link/')}">links</a></li>
    </ul>
</%def>

