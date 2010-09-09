<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<%!
    show_side = True
    subtitle = ''
%>

<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" href="${tg.url('/themes/%s/css/style.css' % c.theme)}" />

    ##${c.j_startup()}
    <script type="text/javascript">
    $(function() {
        % if path:
            % if path[0]:
                $("#header .menu_bottom .${path[0]}").addClass('active');
            % endif
            % if path[1]:
                $("#side .${path[1]}").addClass('active');
            % endif
        % endif
    });
    </script>
</head>

<body>
    <div id="overlay">
        <div class="wrap"></div>
        <iframe src="about:blank"></iframe>
    </div>

    ${self.header()}

    <div id="main">
        % if self.attr.show_side:
            <div id="side">
                ${self.side()}
            </div>
        % endif
        ${self.content_wrapper()}
    </div>
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
    ${c.title and self.attr.subtitle and ' - '}
    ${self.attr.subtitle}
</%def>

<%def name="header()">
    <script type="text/javascript">
        $(function() {
            $(".menu_top .languages").addClass("hidden");
            $(".menu_top .language_chooser").click(
                function(event){$(".menu_top .languages").toggle("fast");}
            ).hover(
                function(event){},
                function(event){$(".menu_top .languages").hide("fast");}
            );
        });
    </script>
    <div id="header">
        <div class="logo">
            % if c.logo_mediaurl:
                <script type="text/javascript">
                    $(function() {
                        $(".logo").css("background-image", "url('${c.logo_mediaurl}')");
                    });
                </script>
            % endif
        </div>
        <div class="menu_top">
            <ul>
                <li class="language_chooser">
                    <div class="current_language">${c.lang and '%s: %s' % (_('preferred language'), c.lang) or _('choose a language')}</div>
                    <div class="languages">
                        % for language in [l for l in c.languages if l.id != c.lang]:
                            <div class="language"><a href="${tg.url('/set_language/%s?came_from=%s' % (language.id, c.current_url))}">${language.name}</a></div>
                        % endfor
                        % if c.lang:
                            <div class="language"><a href="${tg.url('/unset_language/?came_from=%s' % c.current_url)}">${_('(none)')}</a></div>
                        % endif
                    </div>
                </li>
                <li class="authbox">
                    % if request.identity is None:
                        <a class="login" href="${tg.url('/login')}">login</a>
                    % else:
                        <a class="logout" href="${tg.url('/logout_handler')}">logout ${c.user.user_name}</a>
                    % endif
                </li>
            </ul>
        </div>
        <div class="banner">
            % if c.banner_linkid:
                ${c.w_link(linkid=c.banner_linkid, label=' ', lang=c.lang) | n}
            % endif
            % if c.banner_mediaurl:
                <script type="text/javascript">
                    $(function() {
                        $(".banner").css("background-image", "url('${c.banner_mediaurl}')");
                    });
                </script>
            % endif
        </div>
        ${self.flash_wrapper()}
        <div class="menu_bottom">
            <ul>
                <li class="home"><a href="${tg.url('/')}">${_('home')}</a></li>
                % for cat in c.categories:
                <li class="${cat.id}"><a href="${tg.url('/%s/' % cat.id)}">${cat.name[c.lang]}</a></li>
                % endfor
                <li class="media"><a href="${tg.url('/media')}">${_('media')}</a></li>
                <li class="links"><a href="${tg.url('/link')}">${_('links')}</a></li>
                % if tg.predicates.has_permission('manage'):
                <li class="admin"><a href="${tg.url('/admin')}">${_('admin')}</a></li>
                % endif
            </ul>
        </div>
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
        % if c.cc == 'cc by':
            <div class="cc">
                <a rel="license" href="http://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0 Unported License</a>.
            </div>
        % elif c.cc == 'cc by-sa':
            <div class="cc">
                <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br />The contents and style of this site are licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.
            </div>
        % elif c.cc == 'cc by-nd':
            <div class="cc">
                <a rel="license" href="http://creativecommons.org/licenses/by-nd/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nd/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nd/3.0/">Creative Commons Attribution-NoDerivs 3.0 Unported License</a>.
            </div>
        % elif c.cc == 'cc by-nc':
            <div class="cc">
                <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/">Creative Commons Attribution-NonCommercial 3.0 Unported License</a>.
            </div>
        % elif c.cc == 'cc by-nc-sa':
            <div class="cc">
                <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>.
            </div>
        % elif c.cc == 'cc by-nc-nd':
            <div class="cc">
                <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-nd/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/">Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License</a>.
            </div>
        % endif
    </div>
</%def>

</html>
