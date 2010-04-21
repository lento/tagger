<%inherit file="local:templates.admin.index"/>

<%def name="title()">
  tagger - ${_('Links')}
</%def>

<div class="content_title">
    <h1>${_('Links')}</h1>
    <a class="button overlay" href="${tg.url('/link/new')}" rel="#overlay">${_('add new')}</a>
</div>

<table>
    <tr class="table_header">
        <th>${_('ID')}</th>
        <th>${_('Name')}</th>
        <th>${_('URI')}</th>
        <th>${_('Tags')}</th>
        <th>${_('Languages')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for link in links:
    <tr>
        <td>${link.id}</td>
        <td>${link.name[c.lang]}</td>
        <td>${link.uri}</td>
        <td>${', '.join([t.name[lang] for t in link.tags])}</td>
        <td>${', '.join(link.language_ids)}</td>
        <td>
            <a class="icon edit overlay" title="${_('edit')}" href="${tg.url('/link/%s/edit' % link.id)}" rel="#overlay"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/link/%s/delete' % link.id)}" rel="#overlay"></a>
        </td>
    </tr>
    % endfor
</table>