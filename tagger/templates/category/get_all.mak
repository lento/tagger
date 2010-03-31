<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Article Categories')}
</%def>

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
