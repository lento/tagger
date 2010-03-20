<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Article Categories')}
</%def>

<table>
    <th>
        <td>${_('ID')}</td>
        <td>${_('Name')}</td>
        <td>${_('Description')}</td>
        <td>${_('Actions')}</td>
    </th>
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
