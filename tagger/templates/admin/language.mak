<%inherit file="local:templates.admin.index"/>

<%def name="title()">
  tagger - ${_('Languages')}
</%def>

<div class="content_title">
    <h1>${_('Languages')}</h1>
    <a class="button overlay" href="${tg.url('/language/new')}" rel="#overlay">${_('add new')}</a>
</div>

<table>
    <tr class="table_header">
        <th>${_('ID')}</th>
        <th>${_('Name')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for language in languages:
    <tr class="${language.id}">
        <td>${language.id}</td>
        <td>${language.name}</td>
        <td>
            <a class="icon edit overlay" title="${_('edit')}" href="${tg.url('/language/%s/edit' % language.id)}" rel="#overlay"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/language/%s/delete' % language.id)}" rel="#overlay"></a>
        </td>
    </tr>
    % endfor
</table>
