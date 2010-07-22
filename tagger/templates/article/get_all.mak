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
                text, has_more = render_summary(article.text[c.lang], c.lang)
            %>
            <div class="object_body">
                ${text | n}
            % if has_more:
                <div class="more">
                    <a href="${tg.url('/%s/%s' % (article.category.id, article.id))}">
                        [...${_('read more')}]
                    </a>
                </div>
            % endif
            </div>
        </li>
    % endfor
</ul>

% if more_results:
    <div class="more_results">
        ${'%s %s' % (more_results, _('more articles in this category'))}
        <a href="${tg.url('/%s?max_results=0' % article.category.id)}">
            ${_('view all')}
        </a>
    </div>
% endif

<%def name="side()">
    ${sidebars.side_recent()}
</%def>

