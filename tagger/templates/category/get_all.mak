<%inherit file="local:templates.admin"/>

<%def name="title()">
  tagger - ${_('Article Categories')}
</%def>

<h1>${_('Article Categories')}</h1>

<table>
    <tr>
        <th>${_('ID')}</th>
        <th>${_('Name')}</th>
        <th>${_('Description')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for cat in categories:
    <tr>
        <td>${cat.id}</td>
        <td>${cat.name}</td>
        <td>${cat.description}</td>
        <td>
        </td>
    </tr>
    % endfor
</table>
