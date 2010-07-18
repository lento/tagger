<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tagger.lib.render.rst import render_summary
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Articles')
%>

<ul>
    % for article in articles:
        <li class="object summary">
            ${c.w_object_title(obj=article, tg=tg, lang=c.lang, add_link=True) | n}
            <%
                text, has_more = render_summary(article.text[lang], lang)
            %>
            <div>
                ${text | n}
            </div>
            <div>
                % if has_more:
                    <a href="${tg.url('/%s/%s' % (article.category.id, article.id))}">
                        [...${_('read more')}]
                    </a>
                % endif
            </div>
        </li>
    % endfor
</ul>

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

