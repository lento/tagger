# -*- coding: utf-8 -*-
"""
Functional test suite for the root controller.

This is an example of how functional tests can be written for controllers.

As opposed to a unit-test, which test a small unit of functionality,
functional tests exercise the whole application and its WSGI stack.

Please read http://pythonpaste.org/webtest/ for more information.

"""
from nose.tools import assert_true, eq_

from tagger.tests import TestController
from tagger.model import DBSession, User, Category, Article
import transaction


class TestRootController(TestController):
    """Tests for the method in the root controller."""

    def test_index(self):
        """The front page is working properly"""
        response = self.app.get('/')
        msg = 'index'
        # You can look for specific strings:
        assert_true(msg in response)

    def test_default(self):
        """articles can be retrived with url: /category/string_id"""
        cat = DBSession.query(Category).get(1)
        user = DBSession.query(User).get(1)
        article = Article(u'A Test Article!', cat, u'en', user, u'random text')
        DBSession.add(article)
        transaction.commit()

        response = self.app.get('/blog/a_test_article')

        expected = ('<div id="content_with_side">\n'
                    '<div>1</div>\n'
                    '<div>A Test Article!</div>\n'
                    '<div>blog</div>\n'
                    '<div>en</div>\n'
                    '</div>'
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)


