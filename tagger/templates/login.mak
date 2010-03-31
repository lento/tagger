<%inherit file="local:templates.master"/>

<%!
    show_side = False
%>

<div id="loginform">
<form action="${tg.url('/login_handler')}" method="POST" class="loginfields">
    <h2><span>Login</span></h2>
    <input type="hidden" id="came_from" name="came_from" value="${came_from.encode('utf-8')}"></input>
    <input type="hidden" id="logins" name="__logins" value="${login_counter.encode('utf-8')}"></input>
    <label for="login">Username:</label><input type="text" id="login" name="login" class="text"></input>
    <label for="password">Password:</label><input type="password" id="password" name="password" class="text"></input>
    <input type="submit" id="submit" value="Login" />
</form>
</div>

