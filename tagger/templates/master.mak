<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/themes/%s/css/style.css' % c.theme)}" />
</head>
<body>
    ${self.header()}
    ${self.content_wrapper()}
    ${self.footer()}
</body>

<%def name="content_wrapper()">
    <div id="content">
        ${self.body()}
    </div>
</%def>

<%def name="meta()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="title()">
    ${c.title}
</%def>

<%def name="header()">
    <div id="header">
        <div class="logo"></div>
        <div class="menu_top">
            <div class="authbox">
                <div class="login"><a href="">login</a></div>
                <div class="logout"><a href="">logout</a></div>
                <div class="username">lorenzo</div>
            </div>
        </div>
        <div class="banner"></div>
        <div class="menu_bottom">
            <ul>
                % for cat in c.categories:
                <li><a href="${tg.url('/article/%s' % cat.name)}">${cat.name}</a></li>
                % endfor
                <li><a href="${tg.url('/media')}">media</a></li>
                <li><a href="${tg.url('/link')}">links</a></li>
            </ul>
        </div>
    </div>
</%def>

<%def name="footer()">
    <div id="footer">
    </div>
</%def>

</html>
