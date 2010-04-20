<%inherit file="local:templates.admin.index"/>

<%def name="title()">
  tagger - ${_('Comments')}
</%def>

<div class="content_title">
    <h1>${_('Comments')}</h1>
</div>

<table>
    <tr class="table_header">
        <th>${_('Date')}</th>
        <th>${_('ID')}</th>
        <th>${_('To')}</th>
        <th>${_('By')}</th>
        <th>${_('E-Mail')}</th>
        <th>${_('Text')}</th>
        <th>${_('Status')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for comment in comments:
    <tr>
        <td>${comment.created}</td>
        <td>${comment.id}</td>
        <td>${comment.to}</td>
        <td>${comment.name}</td>
        <td>${comment.email}</td>
        <td>${comment.summary}</td>
        <td><div class="status ${comment.status}">${comment.status}</div></td>
        <td>
            <a class="icon edit overlay" title="${_('edit')}" href="${tg.url('/comment/%s/edit' % comment.id)}" rel="#overlay"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/comment/%s/delete' % comment.id)}" rel="#overlay"></a>
            % if comment.status == 'waiting':
                <a class="icon approve" title="${_('approve')}" href="${tg.url('/comment/%s/approve' % comment.id)}"></a>
                <a class="icon spam" title="${_('mark as spam')}" href="${tg.url('/comment/%s/spam' % comment.id)}"></a>
            % elif comment.status == 'approved':
                <a class="icon revoke" title="${_('revoke approval')}" href="${tg.url('/comment/%s/revoke' % comment.id)}"></a>
            % elif comment.status == 'spam':
                <a class="icon unspam" title="${_('not spam')}" href="${tg.url('/comment/%s/unspam' % comment.id)}"></a>
            % endif
        </td>
    </tr>
    % endfor
</table>
