<%inherit file="local:templates.admin.index"/>

<%def name="title()">
  tagger - ${_('Articles')}
</%def>

${c.f_edit(args, child_args=child_args) | n}

<div class="content_title">
    <h1>${_('Pages')}</h1>
    <a class="button overlay" href="${tg.url('/page/%s/new' % article.id)}" rel="#overlay">${_('add new')}</a>
</div>

<table>
    <tr class="table_header">
        <th>${_('Date')}</th>
        <th>${_('ID')}</th>
        <th>${_('String ID')}</th>
        <th>${_('Name')}</th>
        <th>${_('Languages')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for page in article.pages:
    <tr class="${page.id}">
        <td>${page.created}</td>
        <td>${page.id}</td>
        <td>${page.string_id}</td>
        <td>${page.name[c.lang]}</td>
        <td>${', '.join(page.language_ids)}</td>
        <td>
            <a class="icon edit" title="${_('edit')}" href="${tg.url('/page/%s/%s/edit' % (article.id, page.string_id))}" rel="#overlay"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/page/%s/%s/delete' % (article.id, page.string_id))}" rel="#overlay"></a>
        </td>
    </tr>
    % endfor
</table>

