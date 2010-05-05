<%def name="side_admin()">
    <ul>
        <li class="banner"><a href="${tg.url('/admin/banner/')}">${_('banner')}</a></li>
        <li class="languages"><a href="${tg.url('/admin/language/')}">${_('languages')}</a></li>
        <li class="tags"><a href="${tg.url('/admin/tag/')}">${_('tags')}</a></li>
        <li class="categories"><a href="${tg.url('/admin/category/')}">${_('categories')}</a></li>
        <li class="articles"><a href="${tg.url('/admin/article/')}">${_('articles')}</a></li>
        <li class="media"><a href="${tg.url('/admin/media/')}">${_('media')}</a></li>
        <li class="links"><a href="${tg.url('/admin/link/')}">${_('links')}</a></li>
        <li class="comments"><a href="${tg.url('/admin/comment/')}">${_('comments')}</a></li>
    </ul>
</%def>

<%def name="side_related()">
    <ul>
        % for assoc, numtags in related:
            <li class="related ${assoc.type}">
                % if assoc.type in c.w_sideobj:
                    ${c.w_sideobj[assoc.type](obj=assoc.associated) | n}
                % endif
            </li>
        % endfor
    </ul>
</%def>

<%def name="side_recent()">
    <ul>
        % for assoc in recent:
            <li class="related ${assoc.type}">
                % if assoc.type in c.w_sideobj:
                    ${c.w_sideobj[assoc.type](obj=assoc.associated) | n}
                % endif
            </li>
        % endfor
    </ul>
</%def>

