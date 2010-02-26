<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
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

<%def name="title()"></%def>

<%def name="header()">
  <div id="header">
  </div>
</%def>

<%def name="footer()">
  <div id="footer">
  </div>
</%def>

</html>
