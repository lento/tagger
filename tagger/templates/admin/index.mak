<%inherit file="local:templates.master"/>

admin

<%def name="side()">
    <ul>
        <li class="languages"><a href="${tg.url('/admin/language/')}">${_('languages')}</a></li>
        <li class="tags"><a href="${tg.url('/admin/tag/')}">${_('tags')}</a></li>
        <li class="categories"><a href="${tg.url('/admin/category/')}">${_('categories')}</a></li>
        <li class="articles"><a href="${tg.url('/admin/article/')}">${_('articles')}</a></li>
        <li class="media"><a href="${tg.url('/admin/media/')}">${_('media')}</a></li>
        <li class="links"><a href="${tg.url('/admin/link/')}">${_('links')}</a></li>
    </ul>
</%def>

