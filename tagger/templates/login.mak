<%inherit file="local:templates.master"/>

<%!
    show_side = False
%>

<div id="loginform">
<h2><span>Login</span></h2>

${c.f_login(fargs) |n}

</div>

