<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Articles')}
</%def>

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
        </td>
    </tr>
    % endfor
</table>
