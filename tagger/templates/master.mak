<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<%!
    show_side = True
%>

<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/themes/%s/css/style.css' % c.theme)}" />
    <script type="text/javascript" src="${tg.url('/js/jquery.js')}"></script>
    <script type="text/javascript" src="${tg.url('/js/jquery.tools.js')}"></script>
    <script type="text/javascript" src="${tg.url('/js/tagger.js')}"></script>

    <script type="text/javascript">
    $(function() {
        % if page:
            % if page[0]:
                $("#header .menu_bottom .${page[0]}").addClass('active');
            % endif
            % if page[1]:
                $("#side .${page[1]}").addClass('active');
            % endif
        % endif
    });
    </script>
</head>
<body>
    <div id="overlay">
        <div class="wrap"></div>
    </div>

    ${self.header()}
    % if self.attr.show_side:
        <div id="side">
            ${self.side()}
        </div>
    % endif
    ${self.content_wrapper()}
    ${self.footer()}
</body>

<%def name="content_wrapper()">
    % if self.attr.show_side:
        <div id="content_with_side">
            ${self.body()}
        </div>
    % else:
        <div id="content_without_side">
            ${self.body()}
        </div>
    % endif
</%def>

<%def name="meta()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="title()">
    ${c.title}
</%def>

<%def name="header()">
    <div id="header">
        <a href="${tg.url('/')}" class="logo"></a>
        <div class="menu_top">
            <div class="authbox">
                % if request.identity is None:
                    <a class="login button" href="${tg.url('/login')}">login</a>
                % else:
                    <a class="logout button" href="${tg.url('/logout_handler')}">logout ${c.user.user_name}</a>
                % endif
            </div>
        </div>
        <div class="banner"></div>
        <div class="menu_bottom">
            <ul>
                % for cat in c.categories:
                <li class="${cat.name}"><a href="${tg.url('/article/%s' % cat.name)}">${cat.name}</a></li>
                % endfor
                <li class="media"><a href="${tg.url('/media')}">media</a></li>
                <li class="links"><a href="${tg.url('/link')}">links</a></li>
                % if tg.predicates.has_permission('manage'):
                <li class="admin"><a href="${tg.url('/admin')}">admin</a></li>
                % endif
            </ul>
        </div>
        ${self.flash_wrapper()}
    </div>
</%def>

<%def name="flash_wrapper()">
    <%
    flash = tg.flash_obj.render('flash', use_js=False)
    %>
    % if flash:
        ${flash | n}
    % endif
</%def>

<%def name="side()">
</%def>

<%def name="footer()">
    <div id="footer">
        <div class="copyright">${c.copyright}</div>
    </div>
</%def>

</html>
