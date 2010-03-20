<%inherit file="local:templates.standalone"/>

<%def name="style()">
    ##<link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/themes/%s/css/form.css' % c.theme)}" />
</%def>

<div class="result ${result}"></div>
<div class="msg">${msg}</div>

