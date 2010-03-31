<%inherit file="local:templates.master"/>

<%def name="title()">
  tagger - ${_('Languages')}
</%def>

<table>
    <tr>
        <th>${_('ID')}</th>
        <th>${_('Name')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for language in languages:
    <tr>
        <td>${language.id}</td>
        <td>${language.name}</td>
        <td>
        </td>
    </tr>
    % endfor
</table>
