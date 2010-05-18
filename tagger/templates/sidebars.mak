<%def name="side_admin()">
    <div>
        <ul>
            <li class="settings"><div><a href="${tg.url('/admin/settings/')}">${_('settings')}</a></div></li>
            <li class="languages"><div><a href="${tg.url('/admin/language/')}">${_('languages')}</a></div></li>
            <li class="tags"><div><a href="${tg.url('/admin/tag/')}">${_('tags')}</a></div></li>
            <li class="categories"><div><a href="${tg.url('/admin/category/')}">${_('categories')}</a></div></li>
            <li class="articles"><div><a href="${tg.url('/admin/article/')}">${_('articles')}</a></div></li>
            <li class="media"><div><a href="${tg.url('/admin/media/')}">${_('media')}</a></div></li>
            <li class="links"><div><a href="${tg.url('/admin/link/')}">${_('links')}</a></div></li>
            <li class="comments"><div><a href="${tg.url('/admin/comment/')}">${_('comments')}</a></div></li>
        </ul>
    </div>
</%def>

<%def name="side_related()">
    % if related:
        <div>
            <h1>${_('related stuff')}</h1>
            <ul>
                % for assoc, numtags in related:
                    <li class="related ${assoc.type}">
                        % if assoc.type in c.w_sideobj:
                            ${c.w_sideobj[assoc.type](obj=assoc.associated) | n}
                        % endif
                    </li>
                % endfor
            </ul>
        </div>
    % endif
</%def>

<%def name="side_recent()">
    % if recent:
        <div>
            <h1>${_('recent stuff')}</h1>
            <ul>
                % for assoc in recent:
                    <li class="related ${assoc.type}">
                        % if assoc.type in c.w_sideobj:
                            ${c.w_sideobj[assoc.type](obj=assoc.associated) | n}
                        % endif
                    </li>
                % endfor
            </ul>
        </div>
    % endif
</%def>

