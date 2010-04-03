<%inherit file="local:templates.admin"/>

<%def name="title()">
  tagger - ${_('Articles')}
</%def>

<div class="content_title">
    <h1>${_('Articles')}</h1>
    <a class="button overlay" href="${tg.url('/article/new')}" rel="#overlay">${_('add new')}</a>
</div>

<table>
    <tr>
        <th>${_('ID')}</th>
        <th>${_('Title')}</th>
        <th>${_('category')}</th>
        <th>${_('languages')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for article in articles:
    <tr>
        <td>${article.id}</td>
        <td>${article.title['']}</td>
        <td>${article.category.name}</td>
        <td>${', '.join(article.languages)}</td>
        <td>
            <a class="icon edit" title="${_('edit')}" href="${tg.url('/article/%s/edit' % article.id)}"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/article/%s/delete' % article.id)}" rel="#overlay"></a>
        </td>
    </tr>
    % endfor
</table>
