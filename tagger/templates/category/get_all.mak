<%inherit file="local:templates.admin"/>

<%def name="title()">
  tagger - ${_('Article Categories')}
</%def>

<div class="content_title">
    <h1>${_('Article Categories')}</h1>
    <a class="button overlay" href="${tg.url('/category/new')}" rel="#overlay">${_('add new')}</a>
</div>

<table>
    <tr class="table_header">
        <th>${_('ID')}</th>
        <th>${_('Name')}</th>
        <th>${_('Description')}</th>
        <th>${_('Languages')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for cat in categories:
    <tr class="${cat.id}">
        <td>${cat.id}</td>
        <td>${cat.name[c.lang]}</td>
        <td>${cat.description[c.lang]}</td>
        <td>${', '.join(cat.language_ids)}</td>
        <td>
            <a class="icon edit overlay" title="${_('edit')}" href="${tg.url('/category/%s/edit' % cat.id)}" rel="#overlay"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/category/%s/delete' % cat.id)}" rel="#overlay"></a>
        </td>
    </tr>
    % endfor
</table>
