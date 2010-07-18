<%inherit file="local:templates.admin.index"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Articles')
%>

<div class="content_title">
    <h1>${_('Articles')}</h1>
    <a class="button overlay" href="${tg.url('/article/new')}" rel="#overlay">${_('add new')}</a>
</div>

<table>
    <tr class="table_header">
        <th>${_('Date')}</th>
        <th>${_('Category')}</th>
        <th>${_('ID')}</th>
        <th>${_('Title')}</th>
        <th>${_('Tags')}</th>
        <th>${_('Languages')}</th>
        <th>${_('Status')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for article in articles:
    <tr class="${article.id}">
        <td>${article.created}</td>
        <td>${article.category.name[c.lang]}</td>
        <td>${article.id}</td>
        <td>${article.title[c.lang]}</td>
        <td>${', '.join([t.name[lang] for t in article.tags])}</td>
        <td>${', '.join(article.language_ids)}</td>
        <td>
            <div class="status ${article.published and _('published') or _('draft')}">
                ${article.published and _('published') or _('draft')}
            </div>
        </td>
        <td>
            <a class="icon edit" title="${_('edit')}" href="${tg.url('/article/%s/edit' % article.id)}"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/article/%s/delete' % article.id)}" rel="#overlay"></a>
            % if article.published:
                <a class="icon unpublish" title="${_('unpublish')}" href="${tg.url('/article/%s/unpublish' % article.id)}" rel="#overlay"></a>
            % else:
                <a class="icon publish" title="${_('publish')}" href="${tg.url('/article/%s/publish' % article.id)}" rel="#overlay"></a>
            % endif
        </td>
    </tr>
    % endfor
</table>
