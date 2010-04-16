<%inherit file="local:templates.admin"/>

<%def name="title()">
  tagger - ${_('Tags')}
</%def>

<div class="content_title">
    <h1>${_('Tags')}</h1>
    <a class="button overlay" href="${tg.url('/tag/new')}" rel="#overlay">${_('add new')}</a>
</div>

<table>
    <tr>
        <th>${_('ID')}</th>
        <th>${_('Name')}</th>
        <th>${_('Languages')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for tag in tags:
    <tr>
        <td>${tag.id}</td>
        <td>${tag.name[c.lang]}</td>
        <td>${', '.join(tag.language_ids)}</td>
        <td>
            <a class="icon edit overlay" title="${_('edit')}" href="${tg.url('/tag/%s/edit' % tag.id)}" rel="#overlay"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/tag/%s/delete' % tag.id)}" rel="#overlay"></a>
        </td>
    </tr>
    % endfor
</table>
