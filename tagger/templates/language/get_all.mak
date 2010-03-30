<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Languages')}
</%def>

<table>
    <th>
        <td>${_('ID')}</td>
        <td>${_('Name')}</td>
        <td>${_('Actions')}</td>
    </th>
    % for language in languages:
    <tr>
        <td>${language.id}</td>
        <td>${language.name}</td>
        <td>
        </td>
    </tr>
    % endfor
</table>
